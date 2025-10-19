"""
Графическое приложение для выбора файлов проекта, объединения их содержимого
и копирования в буфер обмена. Использует библиотеку Tkinter для построения
дерева каталогов и взаимодействия с пользователем.

Основные возможности:
---------------------
- Просмотр файлов и папок в указанной директории проекта.
- Игнорирование служебных директорий и файлов (например, __pycache__, .pyc).
- Выбор отдельных файлов с помощью клика.
- Сбор и объединение содержимого выбранных файлов.
- Копирование объединённого текста в системный буфер обмена.
- Отображение уведомлений о результате действия.
- Возможность копирования дерева структуры проекта.
- Возможность копирования дерева + содержимого выбранных файлов.
- Возможность выбора промпта из папки notes (если есть).
- Возможность включения/исключения дерева в копирование.
- Кнопка "Сбросить все галочки" для очистки выбора файлов.
- Кнопка "Обновить дерево" для пересборки дерева при изменении файлов.

Использование
1. Откройте консоль Git Bash в виртуальном окружении вашего проекта в VS Code
2. Запустите приложение командой `python tools/collect_code.py &`
3. Выберите нужные файлы для объединения и нажмите кнопку "Скопировать в буфер обмена"
"""

# TODO: сделать кнопки красивее и удобнее расположить

import os
import tkinter as tk
from tkinter import ttk

# Папки, которые нужно игнорировать
IGNORE_FOLDERS = {
    ".git",
    "__pycache__",
    ".venv",
    "venv",
    "_build",  # папка сборки Sphinx
    # "_static",  # Стили Sphinx
    # "_templates",  # Шаблоны Sphinx
    ".ruff_cache",
    "docs/_build",
}

# Файлы и расширения, которые нужно игнорировать
IGNORE_FILES = {
    ".DS_Store",
    ".pyc",  # Скомпилированные Python-файлы
    ".pyo",
    ".pyd",
    ".mo",
    ".log",
    ".tmp",
    "~",  # Временные файлы редакторов
}


def should_ignore(name, is_dir):
    """Определяет, нужно ли игнорировать файл или директорию при выводе.

    Args:
        name (str): Имя файла или директории.
        is_dir (bool): Флаг, указывающий является ли элемент директорией.

    Returns:
        bool: True если элемент нужно игнорировать, False если нужно включить в вывод.
    """
    if is_dir:
        return name in IGNORE_FOLDERS
    else:
        # Игнорируем по имени или по расширению
        if name in IGNORE_FILES:
            return True
        _, ext = os.path.splitext(name)
        return ext in IGNORE_FILES or name.startswith(".")


def get_tree_structure(start_path, prefix=""):
    """Рекурсивно возвращает структуру каталогов в виде строки ASCII-дерева.

    Args:
        start_path (str): Путь к корневой директории для вывода.
        prefix (str): Префикс для отступов (используется при рекурсивных вызовах).

    Returns:
        str: Строковое представление дерева структуры.
    """
    try:
        entries = sorted(os.listdir(start_path))
    except PermissionError:
        return f"{prefix}└── [Нет доступа]\n"

    output_lines = []
    filtered_entries = []
    for entry in entries:
        full_path = os.path.join(start_path, entry)
        is_dir = os.path.isdir(full_path)
        if not should_ignore(entry, is_dir):
            filtered_entries.append((entry, is_dir))

    for i, (entry, is_dir) in enumerate(filtered_entries):
        path = os.path.join(start_path, entry)
        is_last = i == len(filtered_entries) - 1

        connector = "└── " if is_last else "├── "
        line = f"{prefix}{connector}{entry}" + ("/" if is_dir else "")
        output_lines.append(line)

        if is_dir:
            new_prefix = "    " if is_last else "│   "
            subdir_output = get_tree_structure(path, prefix + new_prefix)
            # Удаляем лишние пустые строки из подкаталогов
            output_lines.append(subdir_output.rstrip())

    return "\n".join(output_lines) + "\n"


# === Основной класс приложения ===


class CodeCollectorApp:
    """
    GUI-приложение для выбора файлов, объединения их содержимого
    и копирования в буфер обмена.
    Использует Tkinter для отображения дерева файлов.
    """

    def __init__(self, root, project_path="."):
        """
        Инициализация главного окна приложения.

        :param root: корневой объект Tkinter
        :param project_path: путь к проекту (по умолчанию — текущая директория)
        """
        self.root = root
        self.project_path = project_path
        self.selected_files = set()  # множество выбранных файлов
        self.tree_items = {}  # словарь: item_id -> {'path', 'type'}
        self.prompts = {}  # словарь: имя_файла -> путь
        self.setup_prompts()  # ищем промпты
        self.setup_ui()

    def setup_prompts(self):
        """
        Сканирует папку notes и собирает все файлы *_prompt.md в словарь.
        """
        notes_path = os.path.join(self.project_path, "notes")
        if os.path.isdir(notes_path):
            for file_name in os.listdir(notes_path):
                if file_name.endswith("_prompt.md"):
                    file_path = os.path.join(notes_path, file_name)
                    self.prompts[file_name] = file_path

    def setup_ui(self):
        """
        Настройка интерфейса: дерево файлов, кнопки копирования, метка уведомления.
        """
        self.root.title("Сбор кода для отправки")
        self.root.geometry("800x650")  # Увеличили высоту и ширину

        # Основной фрейм
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Дерево файлов
        self.tree = ttk.Treeview(main_frame)
        self.tree.heading("#0", text="Файлы и папки", anchor=tk.W)
        self.tree.column("#0", width=600)

        # Прокрутка
        scrollbar = ttk.Scrollbar(
            main_frame, orient=tk.VERTICAL, command=self.tree.yview
        )
        self.tree.configure(yscroll=scrollbar.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Нижняя панель
        bottom_frame = ttk.Frame(self.root)
        bottom_frame.pack(fill=tk.X, padx=10, pady=5)

        # Слева: выпадающий список промптов
        left_frame = ttk.Frame(bottom_frame)
        left_frame.pack(side=tk.LEFT, padx=(0, 20))

        ttk.Label(left_frame, text="📝 Промпт:").pack(anchor=tk.W)
        self.prompt_var = tk.StringVar()

        # Создаём список значений: "Без промпта" + имена промптов
        prompt_options = ["Без промпта"] + list(self.prompts.keys())
        self.prompt_combo = ttk.Combobox(
            left_frame,
            textvariable=self.prompt_var,
            values=prompt_options,
            state="readonly",
            width=25,
        )
        # Устанавливаем "Без промпта" как значение по умолчанию
        self.prompt_combo.set("Без промпта")

        # Если промптов нет, всё равно показываем "Без промпта"
        if not self.prompts:
            self.prompt_combo.config(state="disabled")
        self.prompt_combo.pack(pady=2)

        # Центр: чекбокс "Дерево" и кнопка "Обновить"
        center_frame = ttk.Frame(bottom_frame)
        center_frame.pack(side=tk.LEFT, padx=20)

        self.tree_var = tk.BooleanVar()
        self.tree_checkbox = ttk.Checkbutton(
            center_frame, text="Дерево", variable=self.tree_var
        )
        self.tree_checkbox.pack(pady=2)

        self.refresh_btn = ttk.Button(
            center_frame, text="🔄 Обновить дерево", command=self.refresh_tree
        )
        self.refresh_btn.pack(pady=5)

        # Справа: кнопки "Сбросить" и "Скопировать"
        right_frame = ttk.Frame(bottom_frame)
        right_frame.pack(side=tk.RIGHT, padx=(20, 0))

        self.clear_btn = ttk.Button(
            right_frame, text="🧹 Сбросить чекбоксы", command=self.clear_all_selections
        )
        self.clear_btn.pack(pady=3)

        self.copy_btn = ttk.Button(
            right_frame,
            text="📋 Скопировать в буфер обмена",
            command=self.copy_selected_to_clipboard,
        )
        self.copy_btn.pack(pady=3)

        # Метка для уведомления (изначально скрыта)
        self.status_label = tk.Label(self.root, text="", fg="green", font=("Arial", 10))
        self.status_label.pack(pady=5)

        # Заполняем дерево
        self.populate_tree()

        # Привязываем одинарный клик к переключению выбора файла
        self.tree.bind("<ButtonRelease-1>", self.on_item_click)
        # Привязываем двойной клик для копирования дерева папки в буфер обмена
        self.tree.bind("<Double-Button-1>", self.on_item_double_click)

        # Привязываем горячие клавиши В КОНЦЕ, чтобы не перекрывались другими событиями
        # Привязываем горячую клавишу Ctrl+C к функции копирования
        self.root.bind_all(
            "<Control-c>", lambda event: self.copy_selected_to_clipboard()
        )
        # Также ловим Ctrl + физическая клавиша C/С (keycode 67 в русской раскладке)
        self.root.bind_all("<Control-Key>", self.on_ctrl_key_press)
        # Привязываем клавишу T (или Е, на той же физической клавише) для переключения чекбокса "Дерево"
        self.root.bind_all("<Key>", self.on_key_press)

    def on_ctrl_key_press(self, event):
        # Проверяем английскую раскладку
        if event.keysym == "c":
            self.copy_selected_to_clipboard()
        # Проверяем русскую раскладку (если keycode == 67 — это физическая клавиша C/С)
        elif event.keycode == 67:
            self.copy_selected_to_clipboard()

    def on_key_press(self, event):
        """
        Обработчик нажатия клавиш.
        Переключает чекбокс "Дерево", если нажата T/t или Е/е.
        """
        char = event.char.lower()
        if char == "t" or char == "е":
            # Переключаем состояние чекбокса
            current_value = self.tree_var.get()
            self.tree_var.set(not current_value)

    def populate_tree(self):
        """
        Заполняет дерево файлами и папками из проекта.
        """
        root_node = self.tree.insert(
            "", "end", text=f"{os.path.basename(self.project_path)}", open=True
        )
        self.tree_items[root_node] = {"path": self.project_path, "type": "dir"}
        self._add_directory_contents(root_node, self.project_path)

    def refresh_tree(self):
        """Обновляет дерево файлов, сохраняя выбранные файлы, если они остались."""
        # Сохраняем пути выбранных файлов
        selected_paths = {
            self.tree_items[item_id]["path"] for item_id in self.selected_files
        }

        # Очищаем дерево
        self.tree.delete(*self.tree.get_children())
        self.tree_items.clear()
        self.selected_files.clear()

        # Пересобираем дерево
        self.populate_tree()

        # Повторно выделяем файлы, которые остались
        for item_id, data in self.tree_items.items():
            if data["type"] == "file" and data["path"] in selected_paths:
                self.selected_files.add(item_id)
                self.tree.item(item_id, text=f"{self.tree.item(item_id, 'text')} [✓]")

        self.show_status("Дерево обновлено.", "green")

    def copy_single_dir_tree(self, dir_path):
        """
        Копирует дерево структуры указанной директории в буфер обмена.
        """
        dir_name = os.path.basename(dir_path) + "/"
        tree_output = f"{dir_name}\n{get_tree_structure(dir_path).rstrip()}\n"
        self.root.clipboard_clear()
        self.root.clipboard_append(tree_output)
        self.root.update()
        self.show_status(f"Дерево папки '{dir_name}' скопировано в буфер.", "green")

    def _add_directory_contents(self, parent, path):
        """
        Рекурсивно добавляет содержимое директории в дерево.

        :param parent: родительский элемент в дереве
        :param path: путь к директории
        """
        try:
            for entry in os.listdir(path):
                entry_path = os.path.join(path, entry)

                # Проверяем, нужно ли игнорировать файл/папку
                if should_ignore(entry, os.path.isdir(entry_path)):
                    continue

                if os.path.isdir(entry_path):
                    node = self.tree.insert(
                        parent, "end", text=f"[DIR] {entry}", open=False
                    )
                    self.tree_items[node] = {"path": entry_path, "type": "dir"}
                    # Рекурсивно добавляем содержимое
                    self._add_directory_contents(node, entry_path)
                else:
                    node = self.tree.insert(parent, "end", text=f"[FILE] {entry}")
                    self.tree_items[node] = {"path": entry_path, "type": "file"}

        except PermissionError:
            pass  # Игнорируем папки, к которым нет доступа

    def on_item_click(self, event):
        """
        Обработчик одинарного клика по элементу дерева.
        Если клик по файлу — переключает выбор.
        Если клик по папке — просто раскрывает/сворачивает.
        """
        item_id = self.tree.identify_row(event.y)
        if item_id not in self.tree_items:
            return

        item = self.tree_items[item_id]

        if item["type"] == "file":
            # Логика для файлов (переключение галочки)
            if item_id in self.selected_files:
                self.selected_files.remove(item_id)
                self.tree.item(
                    item_id, text=self.tree.item(item_id, "text").replace(" [✓]", "")
                )
            else:
                self.selected_files.add(item_id)
                self.tree.item(item_id, text=f"{self.tree.item(item_id, 'text')} [✓]")

    def on_item_double_click(self, event):
        """
        Обработчик двойного клика по элементу дерева.
        Если клик по папке — копирует дерево этой папки в буфер обмена.
        """
        item_id = self.tree.identify_row(event.y)
        if item_id not in self.tree_items:
            return

        item = self.tree_items[item_id]

        if item["type"] == "dir":
            # Копируем дерево папки
            self.copy_single_dir_tree(item["path"])

    def clear_all_selections(self):
        """
        Снимает выбор со всех файлов.
        """
        for item_id in self.selected_files.copy():
            # Убираем галочку с файла в дереве
            self.tree.item(
                item_id, text=self.tree.item(item_id, "text").replace(" [✓]", "")
            )
        self.selected_files.clear()
        self.show_status("Все галочки сняты.", "green")

    def copy_selected_to_clipboard(self):
        """
        Собирает: промпт (если выбран), дерево (если чекбокс включен), файлы (если выбраны).
        Копирует всё в буфер обмена.
        """
        output_parts = []

        # Добавляем промпт, если выбран и не равен "Без промпта"
        prompt_name = self.prompt_var.get()
        if prompt_name and prompt_name != "Без промпта":
            prompt_path = self.prompts.get(prompt_name)
            if prompt_path:
                try:
                    with open(prompt_path, encoding="utf-8") as f:
                        prompt_content = f.read()
                    output_parts.append(
                        f"=== Промпт: {prompt_name} ===\n{prompt_content}\n"
                    )
                except Exception as e:
                    print(f"Ошибка при чтении промпта {prompt_path}: {e}")

        # Добавляем дерево, если чекбокс включен
        if self.tree_var.get():
            root_name = os.path.basename(self.project_path) + "/"
            tree_output = f"=== Дерево проекта ===\n{root_name}\n{get_tree_structure(self.project_path).rstrip()}\n"
            output_parts.append(tree_output)

        # Добавляем содержимое файлов, если есть выбранные
        if self.selected_files:
            files_content = []
            for item_id in self.selected_files:
                data = self.tree_items[item_id]
                try:
                    with open(data["path"], encoding="utf-8") as f:
                        content = f.read()
                    files_content.append(f"=== {data['path']} ===\n{content}\n")
                except Exception as e:
                    print(f"Ошибка при чтении {data['path']}: {e}")
            output_parts.append("\n".join(files_content))

        if not output_parts:
            self.show_status("Нечего копировать.", "red")
            return

        full_output = "\n".join(output_parts)

        # Копируем в буфер обмена
        self.root.clipboard_clear()
        self.root.clipboard_append(full_output)
        self.root.update()

        # Формируем сообщение
        parts_info = []
        if prompt_name and prompt_name != "Без промпта":
            parts_info.append("промпт")
        if self.tree_var.get():
            parts_info.append("дерево")
        if self.selected_files:
            parts_info.append(f"{len(self.selected_files)} файл(ов)")

        if parts_info:
            self.show_status(f"Скопировано: {', '.join(parts_info)}.", "green")

    def show_status(self, message, color):
        """
        Показывает уведомление на 3 секунды.
        """
        self.status_label.config(text=message, fg=color)
        self.root.after(3000, self.clear_status)  # Через 3 секунды очистить

    def clear_status(self):
        """
        Очищает текст уведомления.
        """
        self.status_label.config(text="")


if __name__ == "__main__":
    root = tk.Tk()
    app = CodeCollectorApp(root)
    root.mainloop()
