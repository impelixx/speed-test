import json
import matplotlib.pyplot as plt
import pandas as pd
import os
import glob  # Добавлен glob

# Пути определяются относительно директории, в которой находится скрипт.
script_dir = os.path.dirname(os.path.abspath(__file__))

# Имя файла для нового графика
chart_file_path = os.path.join(script_dir, 'performance_over_limits_chart.png')
# Путь к README.md в корневой директории проекта
readme_file_path = os.path.join(script_dir, '..', 'README.md')

# Убедимся, что директория для выходных файлов существует
os.makedirs(script_dir, exist_ok=True)

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

    # --- Обновление README.md ---
    try:
        with open(readme_file_path, 'r', encoding='utf-8') as f:
            readme_content = f.readlines()
    except FileNotFoundError:
        print(f"Ошибка: Файл {readme_file_path} не найден. График не будет вставлен в README.")
        return

    new_readme_content = []
    section_found = False
    in_old_plot_section = False

    # Новое имя файла для графика в README
    new_chart_filename_in_readme = os.path.basename(chart_file_path)

    for line in readme_content:
        if line.strip() == "## Сравнение производительности (Решето Эратосфена)":
            new_readme_content.append(line)
            new_readme_content.append("\nНиже приведен график зависимости времени выполнения от предела N для разных языков:\n")
            new_readme_content.append(f"![Сравнение производительности по пределам N]({new_chart_filename_in_readme})\n\n")
            section_found = True
            in_old_plot_section = True  # Начинаем пропускать старый контент (график и таблицу)
            continue
        elif in_old_plot_section:
            # Пропускаем старую ссылку на диаграмму и старую таблицу
            if line.strip().startswith("![") or line.strip().startswith("|"):
                continue
            else:
                # Если строка не является частью старого графика или таблицы,
                # заканчиваем пропуск и добавляем эту строку.
                in_old_plot_section = False
                new_readme_content.append(line)
        else:
            new_readme_content.append(line)

    # Если заголовок для секции не был найден, добавляем его и график в конец файла
    if not section_found:
        new_readme_content.append("\n## Сравнение производительности (Решето Эратосфена)\n")
        new_readme_content.append("\nНиже приведен график зависимости времени выполнения от предела N для разных языков:\n")
        new_readme_content.append(f"![Сравнение производительности по пределам N]({new_chart_filename_in_readme})\n\n")

    try:
        with open(readme_file_path, 'w', encoding='utf-8') as f:
            f.writelines(new_readme_content)
        print(f"README.md обновлен новым графиком: {new_chart_filename_in_readme}")
    except Exception as e:
        print(f"Ошибка при обновлении README.md: {e}")

if __name__ == '__main__':
    generate_report()
