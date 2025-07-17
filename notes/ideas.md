# TODO
- [ ] Автоматизировать Dockerfile - чтобы в зависимости от содержимого requirements.txt скрипт определял,
какие зависимости нужны и добавлял их к python 3.11 slim

- [ ] Улучшить diagram_auto_update - он должен автоматически определять корень текущего проекта

- [ ] EditorConfig - настройки для текстовых редакторов. Пока необязательно, в будущем может быть полезно

- [ ] Улучшить pre-commit
- [ ] доделать CI/CD
- [ ] доделать линтеры Make, Docker, GitHub
- [ ] Hadolint (docker)

- [ ] Доделать Sphinx
    - [ ] внедрить plantuml?
    - [ ] сделать красивое оформление Make и Docker в документации
    - [ ] посмотреть примеры топ компаний

- [ ] Сделать тесты и покрытие 

- [ ] Настроить деплой на GitHub Pages
    - [ ] отредактировать размер диаграммы

- [ ] Сделать нормальный TODO

# MUST HAVE
Полезная статья на будущее 

https://habr.com/ru/companies/otus/articles/713992/

1. Тестирование
- unittest
- pytest
- тесты на покрытие

2. CI 
- Github Actions

3. Форматирование
Editor Config - единый стиль для всех IDE
Pre-commit - проверка коммитов перед отправкой
- Стиль кода и форматирование
black
- Линтинг
ruff (быстрый линтер)
Bandit (линтер безопасности)

4. Документация
- Добавить CHANGELOG.md? https://keepachangelog.com/en/1.1.0/
- Sphinx + autodoc для рендера
    - добавить тему sphinx book theme?
    - работать вместе с  Material for MkDocs?
- Github Pages/Read the docs для хостинга

5. Визуализация репозитория (прикрутить к репо?)
https://githubnext.com/projects/repo-visualization

6. Расширения к VS Code
- шпаргалки по VS Code

7. Логирование
- loguru?
- structlog?

8. Управление шаблоном проекта
- настроено через copier

9. Управление зависимостями
- uv? pip? poetry?
- pyproject.toml


9. Трекер задач + статистика выполнения задач


# Полезные ссылки
Шаблоны проектирования
https://python-patterns.guide/

Сравнение библиотек
https://www.libhunt.com/

Пример управления проектом
https://blog.dusktreader.dev/2025/04/06/bootstrapping-python-projects-with-copier/#to-github