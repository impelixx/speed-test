#!/bin/bash

# Store the initial directory where the script is run (should be .../report)
INITIAL_DIR=$(pwd)

# Массив с директориями языков и именами скриптов
languages_scripts=(
    "python:sieve"
    "javascript:javascript_sieve"
    "java:JavaSieve"
    "cpp:cpp_sieve"
    "go:go_sieve"
    "rust:app"
)

# Определение предела для решета Эратосфена
sieve_limit=$1
if [ -z "$sieve_limit" ]; then
  echo "Предел для Решета Эратосфена не указан. Используется значение по умолчанию: 2000000"
  sieve_limit=2000000
elif ! [[ "$sieve_limit" =~ ^[0-9]+$ ]]; then
  echo "Ошибка: Предел должен быть положительным целым числом."
  exit 1
fi

echo "Запуск тестов для Решета Эратосфена до N = $sieve_limit..."
all_results_json="[]"

for item in "${languages_scripts[@]}"
do
  IFS=':' read -r lang script_name <<< "$item"
  echo "Тестирование $lang..."

  # Ensure we are in INITIAL_DIR before trying to cd to a relative path
  cd "$INITIAL_DIR" || { echo "Критическая ошибка: не удалось вернуться в $INITIAL_DIR"; exit 1; }

  if [ ! -d "../$lang" ]; then
    echo "Ошибка: Директория ../$lang не найдена (относительно $INITIAL_DIR)."
    error_json=$(jq -n --arg lang "$lang" --arg limit "$sieve_limit" --arg msg "Directory ../$lang not found" \
                   '{language: $lang, limit: ($limit | tonumber), error: $msg, raw_output: ""}')
    all_results_json=$(echo "$all_results_json" | jq --argjson err "$error_json" '. + [$err]')
    continue
  fi

  cd "../$lang" || { echo "Ошибка: Не удалось перейти в директорию ../$lang."; continue; } # Now CWD is, e.g., spidtest/python

  image_name="${lang}-sieve-test"
  docker build -t "$image_name" . > /dev/null 2>&1
  if [ $? -ne 0 ]; then
    echo "Ошибка сборки Docker-образа для $lang."
    error_json=$(jq -n --arg lang "$lang" --arg limit "$sieve_limit" --arg msg "Docker build failed" \
                   '{language: $lang, limit: ($limit | tonumber), error: $msg, raw_output: ""}')
    all_results_json=$(echo "$all_results_json" | jq --argjson err "$error_json" '. + [$err]')
    docker rmi "$image_name" > /dev/null 2>&1
    cd "$INITIAL_DIR"
    continue
  fi

  container_output=$(docker run --rm "$image_name" "$sieve_limit")
  if echo "$container_output" | jq -e . > /dev/null 2>&1; then
    all_results_json=$(echo "$all_results_json" | jq --argjson res "$container_output" '. + [$res]')
  else
    echo "Ошибка: Невалидный JSON от $lang: $container_output"
    error_json=$(jq -n --arg lang "$lang" --arg limit "$sieve_limit" --arg output "$container_output" \
                   '{language: $lang, limit: ($limit | tonumber), error: "Invalid JSON output", raw_output: $output}')
    all_results_json=$(echo "$all_results_json" | jq --argjson err "$error_json" '. + [$err]')
  fi
  cd "$INITIAL_DIR" # Return to INITIAL_DIR (report/)
done

results_file="test_results-$sieve_limit.json"
echo "$all_results_json" | jq '.' > "$INITIAL_DIR/$results_file"
if [ $? -eq 0 ]; then
  echo "Результаты сохранены в $INITIAL_DIR/$results_file"
else
  echo "Ошибка записи результатов в $INITIAL_DIR/$results_file. Код ошибки: $?. Убедитесь, что есть права на запись."
fi
