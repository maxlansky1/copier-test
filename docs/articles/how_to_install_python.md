# Установка и настройка Python

#TODO: переписать вступление

Python — один из самых популярных языков программирования, который используется в веб-разработке, анализе данных, машинном обучении и других областях. Это руководство поможет вам установить Python и настроить виртуальное окружение на различных операционных системах.

## Шаг 1: Проверьте наличие Python

*   **Windows (PowerShell или командная строка):**
    ```powershell
    python --version
    # или
    py --version
    ```
*   **Linux/macOS (терминал):**
    ```bash
    python3 --version
    # или
    python --version
    ```

Если команда возвращает номер версии (например, `Python 3.12.2`), Python уже установлен. Убедитесь, что это Python 3, а не Python 2.

## Шаг 2: Скачайте и установите Python

Выберите инструкции в зависимости от вашей операционной системы.

### Windows

1.  Перейдите на [официальный сайт Python](https://www.python.org/downloads/windows/).
2.  Скачайте последнюю версию Python 3.x.x для Windows (рекомендуется 64-битная версия, `Windows installer (64-bit)`).
3.  Запустите скачанный `.exe` файл.
4.  В первом окне установщика **обязательно поставьте галочку "Add Python to PATH"**. Это позволит использовать команду `python` из любой директории в командной строке.
5.  Выберите "Install Now" для стандартной установки или "Customize installation", если хотите изменить путь установки (рекомендуется выбрать путь без пробелов и кириллицы, например, `C:\Python312\`) или настроить дополнительные параметры.
6.  Дождитесь завершения установки.

#### Linux (Ubuntu/Debian)

1.  Откройте терминал.
2.  Обновите список пакетов:
    ```bash
    sudo apt update
    ```
3.  Установите Python 3 и `pip` (менеджер пакетов):
    ```bash
    sudo apt install python3 python3-pip
    ```

Другие дистрибутивы:
*   **Fedora:** `sudo dnf install python3 python3-pip`
*   **Arch Linux:** `sudo pacman -S python python-pip`

#### macOS

Существует несколько способов установки Python на macOS.

**Способ 1: Официальный установщик**

1.  Посетите [официальный сайт Python](https://www.python.org/downloads/macos/).
2.  Скачайте последнюю версию (например, `python-3.x.x-macos11.pkg`).
3.  Запустите скачанный `.pkg` файл и следуйте инструкциям установщика.

**Способ 2: Homebrew**

Если у вас установлен [Homebrew](https://brew.sh/):

1.  Откройте терминал.
2.  Выполните команду:
    ```bash
    brew install python
    ```

## Шаг 3: Создайте виртуальное окружение (рекомендуется)

Рекомендуется использовать виртуальные окружения для изоляции зависимостей проектов. Это предотвращает конфликты между библиотеками, используемыми разными проектами.

1.  Откройте терминал или командную строку.
2.  Перейдите в директорию вашего проекта (или создайте новую для тестирования).
3.  Создайте виртуальное окружение:
    *   **Windows:**
        ```powershell
        python -m venv venv
        ```
    *   **Linux/macOS:**
        ```bash
        python3 -m venv myenv
        ```
4.  Активируйте виртуальное окружение:
    *   **Windows (PowerShell):**
        ```powershell
        venv\Scripts\Activate.ps1
        ```
        *(Возможно, потребуется [настройка политики выполнения](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.security/set-executionpolicy) для первого запуска скриптов: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser` в PowerShell)*
    *   **Windows (cmd):**
        ```cmd
        venv\Scripts\activate
        ```
    *   **Linux/macOS:**
        ```bash
        source venv/bin/activate
        ```
5.  Вы должны увидеть `(venv)` в начале строки командной строки, что означает активацию окружения.
6.  Установите зависимости вашего проекта (например, из `requirements.txt`) с помощью `pip`:
    ```bash
    pip install -r requirements.txt
    ```
7.  Для деактивации окружения введите в командной строке:
    ```bash
    deactivate
    ```