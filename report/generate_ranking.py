import json
import os
from typing import List, Dict

def load_test_results(limit: int = 1000) -> List[Dict]:
    """Load test results for a specific limit."""
    filename = f"test_results-{limit}.json"
    if not os.path.exists(filename):
        return []
    
    with open(filename, 'r') as f:
        return json.load(f)

def generate_ranking(results: List[Dict]) -> str:
    """Generate a markdown table with rankings."""
    # Filter out failed tests and sort by time
    valid_results = [r for r in results if 'time_seconds' in r and not r.get('error')]
    sorted_results = sorted(valid_results, key=lambda x: float(x['time_seconds']))
    
    # Generate markdown table
    table = "| Ранг | Язык | Время (с) |\n"
    table += "|------|------|-----------|\n"
    
    for i, result in enumerate(sorted_results, 1):
        language = result['language']
        time = result['time_seconds']
        table += f"| {i} | {language} | {time} |\n"
    
    return table

def update_readme(ranking_table: str):
    """Update the README.md with the new ranking table."""
    readme_path = "../README.md"
    
    with open(readme_path, 'r') as f:
        content = f.read()
    
    # Find the table section
    table_start = content.find("| Ранг | Язык | Время (с) |")
    if table_start == -1:
        # If table doesn't exist, add it after the last image
        image_end = content.rfind("![Сравнение производительности")
        if image_end != -1:
            next_line = content.find("\n", image_end)
            if next_line != -1:
                content = content[:next_line+1] + "\n" + ranking_table + content[next_line+1:]
    else:
        # Replace existing table
        table_end = content.find("\n\n", table_start)
        if table_end != -1:
            content = content[:table_start] + ranking_table + content[table_end:]
    
    with open(readme_path, 'w') as f:
        f.write(content)

def main():
    # Load results for limit 1000
    results = load_test_results(1000)
    if not results:
        print("No test results found!")
        return
    
    # Generate ranking table
    ranking_table = generate_ranking(results)
    
    # Update README
    update_readme(ranking_table)
    print("README.md has been updated with the new ranking table!")

if __name__ == "__main__":
    main() 