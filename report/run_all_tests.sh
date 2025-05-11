#!/bin/bash

INITIAL_DIR=$(pwd)

# Массив с языками и компиляторами (формат: язык:скрипт:компилятор:dockerfile)
languages_compilers=(
    "python:sieve:python:Dockerfile"
    "python:sieve:pypy:Dockerfile.pypy"
    "python:sieve:cpython:Dockerfile.cpython"
    "javascript:javascript_sieve:node:Dockerfile"
    "javascript:javascript_sieve:bun:Dockerfile.bun"
    "javascript:javascript_sieve:deno:Dockerfile.deno"
    "java:JavaSieve:openjdk:Dockerfile"
    "cpp:cpp_sieve:gcc:Dockerfile"
    "cpp:cpp_sieve:clang:Dockerfile.clang"
    "go:go_sieve:go:Dockerfile"
    "rust:app:rust:Dockerfile"
    "dart:dart_sieve:dart:Dockerfile"
    "ruby:ruby_sieve:ruby:Dockerfile"
)

sieve_limit=$1
if [ -z "$sieve_limit" ]; then
  echo "Предел для Решета Эратосфена не указан. Используется значение по умолчанию: 2000000"
  sieve_limit=2000000
elif ! [[ "$sieve_limit" =~ ^[0-9]+$ ]]; then
  echo "Ошибка: Предел должен быть положительным целым числом."
  exit 1
fi

echo "Запуск тестов для Решета Эратосфена до N = $sieve_limit..."


declare -A lang_results
for item in "${languages_compilers[@]}"
do
  IFS=':' read -r lang script_name compiler dockerfile <<< "$item"
  if [ -z "${lang_results[$lang]}" ]; then
    lang_results[$lang]="[]"
  fi
done

for item in "${languages_compilers[@]}"
do
  IFS=':' read -r lang script_name compiler dockerfile <<< "$item"
  echo "Тестирование $lang ($compiler)..."

  cd "$INITIAL_DIR" || { echo "Критическая ошибка: не удалось вернуться в $INITIAL_DIR"; exit 1; }

  if [ ! -d "../$lang" ]; then
    echo "Ошибка: Директория ../$lang не найдена (относительно $INITIAL_DIR)."
    error_json=$(jq -n --arg lang "$lang" --arg compiler "$compiler" --arg limit "$sieve_limit" --arg msg "Directory ../$lang not found" \
                   '{language: $lang, compiler: $compiler, limit: ($limit | tonumber), error: $msg, raw_output: ""}')
    lang_results[$lang]=$(echo "${lang_results[$lang]}" | jq --argjson err "$error_json" '. + [$err]')
    continue
  fi

  cd "../$lang" || { echo "Ошибка: Не удалось перейти в директорию ../$lang."; continue; }

  image_name="${lang}-${compiler}-sieve-test"
  docker build -t "$image_name" -f "$dockerfile" . > /dev/null 2>&1
  if [ $? -ne 0 ]; then
    echo "Ошибка сборки Docker-образа для $lang ($compiler)."
    error_json=$(jq -n --arg lang "$lang" --arg compiler "$compiler" --arg limit "$sieve_limit" --arg msg "Docker build failed" \
                   '{language: $lang, compiler: $compiler, limit: ($limit | tonumber), error: $msg, raw_output: ""}')
    lang_results[$lang]=$(echo "${lang_results[$lang]}" | jq --argjson err "$error_json" '. + [$err]')
    docker rmi "$image_name" > /dev/null 2>&1
    cd "$INITIAL_DIR"
    continue
  fi

  extra_env=""
  if [ "$lang" = "javascript" ]; then
    if [ "$compiler" = "bun" ]; then
      extra_env="--env JS_RUNTIME_NAME=JavaScript-Bun"
    elif [ "$compiler" = "deno" ]; then
      extra_env="--env JS_RUNTIME_NAME=JavaScript-Deno"
    else
      extra_env="--env JS_RUNTIME_NAME=JavaScript-Node"
    fi
  elif [ "$lang" = "python" ]; then
    if [ "$compiler" = "pypy" ]; then
      extra_env="--env PYTHON_INTERPRETER_NAME=PyPy"
    else
      extra_env="--env PYTHON_INTERPRETER_NAME=CPython"
    fi
  fi

  container_output=$(docker run --rm $extra_env "$image_name" "$sieve_limit")
  if echo "$container_output" | jq -e . > /dev/null 2>&1; then
    lang_results[$lang]=$(echo "${lang_results[$lang]}" | jq --argjson res "$container_output" '. + [$res]')
  else
    echo "Ошибка: Невалидный JSON от $lang ($compiler): $container_output"
    error_json=$(jq -n --arg lang "$lang" --arg compiler "$compiler" --arg limit "$sieve_limit" --arg output "$container_output" \
                   '{language: $lang, compiler: $compiler, limit: ($limit | tonumber), error: "Invalid JSON output", raw_output: $output}')
    lang_results[$lang]=$(echo "${lang_results[$lang]}" | jq --argjson err "$error_json" '. + [$err]')
  fi
  cd "$INITIAL_DIR"
done

# Сохраняем результаты для каждого языка в отдельный файл
# for lang in "${!lang_results[@]}"
# do
#   results_file="$INITIAL_DIR/test_results-${lang}-${sieve_limit}.json"
#   echo "${lang_results[$lang]}" | jq '.' > "$results_file"
#   if [ $? -eq 0 ]; then
#     echo "Результаты для $lang сохранены в $results_file"
#   else
#     echo "Ошибка записи результатов для $lang в $results_file. Код ошибки: $?. Убедитесь, что есть права на запись."
#   fi
# done

# Создаем общий файл со всеми результатами
all_results_json="[]"
for lang in "${!lang_results[@]}"
do
  all_results_json=$(echo "$all_results_json" | jq --argjson res "${lang_results[$lang]}" '. + $res')
done

results_file="test_results-$sieve_limit.json"
echo "$all_results_json" | jq '.' > "$INITIAL_DIR/$results_file"
if [ $? -eq 0 ]; then
  echo "Все результаты сохранены в $INITIAL_DIR/$results_file"
else
  echo "Ошибка записи всех результатов в $INITIAL_DIR/$results_file. Код ошибки: $?. Убедитесь, что есть права на запись."
fi
