# `configs/`

#TODO: добавить сюда env и env.example

Содержит модули конфигурации, которые обеспечивают обеспечивают структурированное и валидируемое управление настройками приложения. Они основаны на библиотеке `Pydantic` и загружают параметры из переменных окружения и файла `.env`.

```{attention}
Sphinx **некорректно обрабатывает** модули конфигурации на основе `Pydantic`, поскольку при автодокументировании (`automodule`) происходит повторная инициализация моделей и чтение переменных окружения, что **зацикливает сборку**.

Есть два способа обойти это:

* **Моки (`MagicMock`)** — отключают реальные импорты, но теряют структуру классов и не отражают реальное содержимое.
* **`literalinclude`** — просто включает исходный код как текст, без выполнения модуля.

В этом проекте выбран **второй вариант**, так как конфигурация не требует автогенерации API-документации, а `literalinclude` обеспечивает стабильную и безопасную сборку.

Подробнее см.:

* [Pydantic BaseSettings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/)
* [Sphinx autodoc — Mocking Imports](https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html#mocking-imports)
```

## Основной файл настроек

```{eval-rst} 
.. literalinclude:: ../../configs/settings.py
   :language: python
   :caption: settings.py
```

## `schemas/`

### `base.py`

```{eval-rst} 
.. literalinclude:: ../../configs/schemas/base.py
   :language: python
   :caption: base.py
```

### `ai.py`

```{eval-rst} 
.. literalinclude:: ../../configs/schemas/ai.py
   :language: python
   :caption: ai.py
```

### `telegram.py`

```{eval-rst} 
.. literalinclude:: ../../configs/schemas/telegram.py
   :language: python
   :caption: telegram.py
```

### `storage.py`

```{eval-rst} 
.. literalinclude:: ../../configs/schemas/storage.py
   :language: python
   :caption: storage.py
```

### `database.py`

```{eval-rst} 
.. literalinclude:: ../../configs/schemas/database.py
   :language: python
   :caption: database.py
```

### `file_processing.py`

```{eval-rst} 
.. literalinclude:: ../../configs/schemas/file_processing.py
   :language: python
   :caption: file_processing
```