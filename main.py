"""
TodoList - консольное приложение для управления списком задач.

Функциональность:
- Добавление задачи
- Отображение всех задач (с сортировкой по статусу)
- Отметка задачи как выполненной
- Удаление задачи по номеру
- Сохранение задач в файл JSON
- Загрузка задач из файла при старте
"""

import json
import os

DATA_FILE = "tasks.json"


def load_tasks():
    """Загружает задачи из JSON-файла при старте программы."""
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            print("Не удалось прочитать файл с задачами. Начинаем с пустого списка.")
            return []
    return []


def save_tasks(tasks):
    """Сохраняет текущий список задач в JSON-файл."""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)


def add_task(tasks):
    """Добавляет новую задачу в список."""
    title = input("Введите текст задачи: ").strip()
    if not title:
        print("Задача не может быть пустой.")
        return
    tasks.append({"title": title, "done": False})
    save_tasks(tasks)
    print(f'Задача "{title}" добавлена.')


def show_tasks(tasks, sort_by_status=False):
    """Показывает список всех задач. При sort_by_status=True сначала невыполненные."""
    if not tasks:
        print("Список задач пуст.")
        return

    items = list(enumerate(tasks, start=1))
    if sort_by_status:
        items.sort(key=lambda pair: pair[1]["done"])

    print("\n--- Список задач ---")
    for number, task in items:
        status = "✓" if task["done"] else "Х"
        print(f'{number}. [{status}] {task["title"]}')
    print("--------------------\n")


def complete_task(tasks):
    """Отмечает задачу как выполненную по номеру."""
    show_tasks(tasks)
    if not tasks:
        return
    try:
        number = int(input("Введите номер задачи для отметки выполненной: "))
        index = number - 1
        if 0 <= index < len(tasks):
            tasks[index]["done"] = True
            save_tasks(tasks)
            print(f'Задача "{tasks[index]["title"]}" отмечена как выполненная.')
        else:
            print("Задачи с таким номером нет.")
    except ValueError:
        print("Нужно ввести число.")


def delete_task(tasks):
    """Удаляет задачу по номеру."""
    show_tasks(tasks)
    if not tasks:
        return
    try:
        number = int(input("Введите номер задачи для удаления: "))
        index = number - 1
        if 0 <= index < len(tasks):
            removed = tasks.pop(index)
            save_tasks(tasks)
            print(f'Задача "{removed["title"]}" удалена.')
        else:
            print("Задачи с таким номером нет.")
    except ValueError:
        print("Нужно ввести число.")


def print_menu():
    print("=== TodoList ===")
    print("1 — добавить задачу")
    print("2 — показать все задачи")
    print("3 — показать задачи (сортировка по статусу)")
    print("4 — отметить задачу выполненной")
    print("5 — удалить задачу")
    print("0 — выход")


def main():
    tasks = load_tasks()

    while True:
        print_menu()
        choice = input("Выберите пункт меню: ").strip()

        if choice == "1":
            add_task(tasks)
        elif choice == "2":
            show_tasks(tasks)
        elif choice == "3":
            show_tasks(tasks, sort_by_status=True)
        elif choice == "4":
            complete_task(tasks)
        elif choice == "5":
            delete_task(tasks)
        elif choice == "0":
            print("Список задач сохранён. До свидания!")
            break
        else:
            print("Неверный пункт меню, попробуйте снова.")


if __name__ == "__main__":
    main()
