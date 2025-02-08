import os
import subprocess

# Настройки Git
REPO_PATH = "D:/AI_Coordinator_Project"  # Путь к твоему проекту
COMMIT_MESSAGE = "Автоматическое обновление кода"

def run_git_command(command):
    """Функция для выполнения Git-команд"""
    result = subprocess.run(command, shell=True, capture_output=True, text=True, cwd=REPO_PATH)
    print(result.stdout)
    if result.stderr:
        print("Ошибка:", result.stderr)

def auto_commit():
    """Автоматически добавляет, коммитит и отправляет изменения в GitHub"""
    print("Добавляем файлы в Git...")
    run_git_command("git add .")

    print("Создаём коммит...")
    run_git_command(f'git commit -m "{COMMIT_MESSAGE}"')

    print("Отправляем в удалённый репозиторий...")
    run_git_command("git push origin main")  # Или другая ветка

if __name__ == "__main__":
    auto_commit()
