import os
from datetime import datetime

ROOT_DIR = "."
README_PATH = "README.md"
DIFFICULTY_FOLDERS = ["Easy", "Medium", "Hard"]
PROGRESS_START = "## 🧾 Progress Log"

def extract_problem_name(file_name):
    name = file_name.replace(".java", "")
    return ' '.join([word.capitalize() for word in name.replace('_', ' ').split()])

def collect_problems():
    entries = []
    for difficulty in DIFFICULTY_FOLDERS:
        folder_path = os.path.join(ROOT_DIR, difficulty)
        if not os.path.isdir(folder_path):
            continue
        for file in sorted(os.listdir(folder_path)):
            if file.endswith(".java"):
                problem_name = extract_problem_name(file)
                date = datetime.today().strftime("%Y-%m-%d")  # or use file modified time
                entries.append((problem_name, difficulty, date))
    return entries

def generate_table(entries):
    table = [
        "| Day | Date       | Problem Name            | Level  | Status     |",
        "|-----|------------|--------------------------|--------|------------|"
    ]
    for i, (name, level, date) in enumerate(entries, 1):
        table.append(f"| {i}   | {date} | {name:<24} | {level:<6} | ✅ Done |")
    return '\n'.join(table)

def update_readme(table_md):
    with open(README_PATH, "r", encoding="utf-8") as f:
        lines = f.readlines()

    new_lines = []
    in_progress_section = False
    for line in lines:
        if line.strip().startswith(PROGRESS_START):
            new_lines.append(line)
            new_lines.append("\n" + table_md + "\n\n")
            new_lines.append("_(Updated automatically)_\n")
            break
        new_lines.append(line)

    with open(README_PATH, "w", encoding="utf-8") as f:
        f.writelines(new_lines)

    print("✅ Progress Log updated in README.md")

if __name__ == "__main__":
    problems = collect_problems()
    table_md = generate_table(problems)
    update_readme(table_md)
