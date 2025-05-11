import json
import matplotlib.pyplot as plt
import pandas as pd
import os
import glob  # Добавлен glob
import numpy as np
from typing import Dict, List
import generate_ranking

# Пути определяются относительно директории, в которой находится скрипт.
script_dir = os.path.dirname(os.path.abspath(__file__))

# Имя файла для нового графика
chart_file_path = os.path.join(script_dir, 'performance_over_limits_chart.png')
# Путь к README.md в корневой директории проекта
readme_file_path = os.path.join(script_dir, '..', 'README.md')

# Убедимся, что директория для выходных файлов существует
os.makedirs(script_dir, exist_ok=True)

def load_test_results(limit: int) -> List[Dict]:
    """Load test results for a specific limit."""
    filename = f"test_results-{limit}.json"
    if not os.path.exists(filename):
        return []
    
    with open(filename, 'r') as f:
        return json.load(f)

def generate_performance_chart(results: List[Dict], limit: int):
    """Generate performance comparison chart."""
    # Filter out failed tests
    valid_results = [r for r in results if 'time_seconds' in r and not r.get('error')]
    
    # Sort by time
    sorted_results = sorted(valid_results, key=lambda x: float(x['time_seconds']))
    
    # Prepare data for plotting
    languages = [r['language'] for r in sorted_results]
    times = [float(r['time_seconds']) for r in sorted_results]
    
    # Create the plot
    plt.figure(figsize=(12, 6))
    bars = plt.bar(languages, times)
    
    # Customize the plot
    plt.title(f'Сравнение производительности (предел N = {limit})')
    plt.xlabel('Язык программирования')
    plt.ylabel('Время выполнения (с)')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    
    # Add value labels on top of bars
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.9f}',
                ha='center', va='bottom')
    
    # Save the plot
    plt.savefig('performance_over_limits_chart.png')
    plt.close()

def generate_report():
    """
    Собирает данные из всех файлов test_results-*.json,
    генерирует линейный график сравнения производительности по пределам N
    и обновляет README.md.
    """
    all_data = []
    result_files = glob.glob(os.path.join(script_dir, 'test_results-*.json'))

    if not result_files:
        print("Не найдены файлы результатов test_results-*.json.")
        return

    for file_path in result_files:
        try:
            sieve_limit_str = os.path.basename(file_path).replace('test_results-', '').replace('.json', '')
            sieve_limit = int(sieve_limit_str)
        except ValueError:
            print(f"Не удалось извлечь предел из имени файла: {file_path}. Пропуск файла.")
            continue

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data_from_file = json.load(f)
        except FileNotFoundError:
            print(f"Ошибка: Файл {file_path} не найден во время чтения.")  # Маловероятно, т.к. glob его нашел
            continue
        except json.JSONDecodeError:
            print(f"Ошибка: Не удалось декодировать JSON из файла {file_path}.")
            continue

        for entry in data_from_file:
            if 'error' not in entry and all(k in entry for k in ['language', 'time_seconds']):
                entry['limit'] = sieve_limit  # Добавляем предел N к каждой записи
                all_data.append(entry)
            else:
                # Если в записи есть 'limit' из run_all_tests.sh, он будет перезаписан, что нормально
                print(f"Пропуск записи с ошибкой или отсутствующими ключами в файле {file_path}: {entry.get('language', 'N/A')} для предела {entry.get('limit', sieve_limit)}")

    if not all_data:
        print("Нет валидных данных для генерации отчета.")
        return

    df = pd.DataFrame(all_data)

    # Преобразование типов на случай, если что-то пошло не так
    df['time_seconds'] = pd.to_numeric(df['time_seconds'], errors='coerce')
    df['limit'] = pd.to_numeric(df['limit'], errors='coerce')
    df.dropna(subset=['time_seconds', 'limit', 'language'], inplace=True)

    # --- Генерация линейного графика ---
    plt.figure(figsize=(12, 8))
    
    languages = df['language'].unique()
    for lang in sorted(languages):  # Сортируем языки для консистентного порядка в легенде
        lang_df = df[df['language'] == lang].sort_values(by='limit')
        if not lang_df.empty:
            plt.plot(lang_df['limit'], lang_df['time_seconds'], marker='o', linestyle='-', label=lang)

    plt.xlabel('Предел N для Решета Эратосфена (логарифмическая шкала)')
    plt.ylabel('Время выполнения (секунды, логарифмическая шкала)')
    plt.title('Сравнение производительности: Время выполнения vs. Предел N')
    plt.xscale('log')
    plt.yscale('log')
    plt.legend(title='Язык программирования')
    plt.grid(True, which="both", ls="-", alpha=0.5)  # Добавлена сетка для лучшей читаемости
    plt.tight_layout()

    try:
        plt.savefig(chart_file_path)
        print(f"График сохранен в {chart_file_path}")
    except Exception as e:
        print(f"Ошибка при сохранении графика: {e}")
        return
    try:
        with open(readme_file_path, 'r', encoding='utf-8') as f:
            readme_content = f.readlines()
    except FileNotFoundError:
        print(f"Ошибка: Файл {readme_file_path} не найден. График не будет вставлен в README.")
        return

    new_readme_content = []
    section_found = False
    in_old_plot_section = False

    # Определяем корректный относительный путь к графику из корневого README.md
    report_dir_name = os.path.basename(script_dir) # Должно быть "report"
    actual_chart_filename = os.path.basename(chart_file_path) # Имя файла графика
    chart_path_for_readme = os.path.join(report_dir_name, actual_chart_filename)
    # Гарантируем использование forward slashes для веб-совместимости
    chart_path_for_readme = chart_path_for_readme.replace(os.sep, '/')

    for line in readme_content:
        if line.strip() == "## Сравнение производительности (Решето Эратосфена)":
            new_readme_content.append(line)
            new_readme_content.append("\nНиже приведен график зависимости времени выполнения от предела N для разных языков:\n")
            new_readme_content.append(f"![Сравнение производительности по пределам N]({chart_path_for_readme})\n\n")
            section_found = True
            in_old_plot_section = True
            continue
        elif in_old_plot_section:
            if line.strip().startswith("![") or line.strip().startswith("|"):
                continue
            else:
                in_old_plot_section = False
                new_readme_content.append(line)
        else:
            new_readme_content.append(line)

    if not section_found:
        new_readme_content.append("\n## Сравнение производительности (Решето Эратосфена)\n")
        new_readme_content.append("\nНиже приведен график зависимости времени выполнения от предела N для разных языков:\n")
        new_readme_content.append(f"![Сравнение производительности по пределам N]({chart_path_for_readme})\n\n")

    try:
        with open(readme_file_path, 'w', encoding='utf-8') as f:
            f.writelines(new_readme_content)
        print(f"README.md обновлен новым графиком: {chart_path_for_readme}")
    except Exception as e:
        print(f"Ошибка при обновлении README.md: {e}")

    # Process results for limit 1000
    limit = 1000
    results = load_test_results(limit)
    
    if not results:
        print(f"No test results found for limit {limit}!")
        return
    
    # Generate performance chart
    generate_performance_chart(results, limit)
    
    # Generate and update ranking table
    generate_ranking.main()
    
    # Clean up JSON files
    for file in os.listdir('.'):
        if file.startswith('test_results-') and file.endswith('.json'):
            os.remove(file)
    
    print("Report generation completed!")

if __name__ == '__main__':
    generate_report()
    def remove_test_files():

        result_files = glob.glob(os.path.join(script_dir, 'test_results-*.json'))
        
        if not result_files:
            print("No test result files found to remove.")
            return
        
        file_count = 0
        for file_path in result_files:
            try:
                os.remove(file_path)
                file_count += 1
                print(f"Removed: {file_path}")
            except Exception as e:
                print(f"Error removing file {file_path}: {e}")
        
        print(f"Successfully removed {file_count} test result files.")
    remove_test_files()