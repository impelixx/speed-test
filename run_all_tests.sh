#!/bin/bash

# Массив с директориями языков и именами скриптов
# Формат: "директория:имя_скрипта_без_расширения"
languages_scripts=(
    "python:sieve"
    "javascript:javascript_sieve"
    "java:JavaSieve"
    "cpp:cpp_sieve"
    "go:go_sieve"
    "rust:app" # Имя исполняемого файла Rust (из Cargo.toml и Dockerfile)
)

# Переменная для хранения общего вывода
output_summary=""

# Определение предела для решета Эратосфена
sieve_limit=$1
if [ -z "$sieve_limit" ]; then
  echo "Аргумент для предела решета не передан. Используется значение по умолчанию: 2000000"
  sieve_limit=2000000
fi

echo "Запуск тестов производительности для Решета Эратосфена до N = $sieve_limit..."
echo "======================================================================"

# Перебор пар язык/скрипт
for item in "${languages_scripts[@]}"
do
  # Разделение строки на директорию и имя скрипта
  IFS=':' read -r lang script_name <<< "$item"
  
  echo ""
  echo "Тестирование $lang (скрипт: $script_name)..."
  
  # Переход в директорию языка
  cd "$lang" || { echo "Ошибка: Директория $lang не найдена."; cd ..; continue; }
  
  # Имя образа Docker
  image_name="${lang}-sieve-test"
  
  echo "Сборка Docker-образа $image_name..."
  # Подавляем вывод docker build для чистоты
  docker build -t "$image_name" . > /dev/null 2>&1
  if [ $? -ne 0 ]; then
    echo "Ошибка: Не удалось собрать Docker-образ для $lang."
    cd ..
    continue
  fi
  
  echo "Запуск контейнера $image_name с аргументом $sieve_limit..."
  # Запуск контейнера и захват вывода
  container_output=$(docker run --rm "$image_name" "$sieve_limit")
  
  if [ $? -ne 0 ]; then
    echo "Ошибка: Не удалось запустить Docker-контейнер для $lang."
    echo "Вывод контейнера: $container_output"
    cd ..
    continue
  fi
  
  # Извлечение времени выполнения
  # Ожидаем строку вида "Time taken: X.XXXXXX seconds"
  time_taken=$(echo "$container_output" | grep "Time taken:" | awk '{print $3, $4}')
  # Извлечение количества найденных простых чисел
  primes_count=$(echo "$container_output" | grep "primes" | awk '{print $4}') 

  if [ -z "$time_taken" ]; then
    echo "Не удалось извлечь время выполнения для $lang."
    echo "Полный вывод контейнера:"
    echo "$container_output"
    time_taken="N/A"
    primes_count_display="N/A"
  else
    echo "$lang - Количество простых: $primes_count, Время выполнения: $time_taken"
    primes_count_display=$primes_count
  fi
  
  output_summary+="$lang (N=$sieve_limit): $primes_count_display primes, $time_taken\n"
  
  # Возврат в корневую директорию проекта
  cd ..
done

echo ""
echo "======================================================================"
echo "Сводка результатов для Решета Эратосфена до N = $sieve_limit:"
echo -e "$output_summary"
echo "Все тесты завершены."

# Сделать скрипт исполняемым: chmod +x run_all_tests.sh
# Запустить скрипт: ./run_all_tests.sh [предел_решета]
