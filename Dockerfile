FROM python:3.12-slim

# Устанавливаем локали (без вывода предупреждений)
RUN apt-get update && \
    apt-get install -y locales && \
    echo "en_US.UTF-8 UTF-8" > /etc/locale.gen && \
    locale-gen en_US.UTF-8 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Устанавливаем переменные окружения для локалей
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8

# Устанавливаем PYTHONPATH и PATH
ENV PYTHONPATH /app
ENV PATH /home/deployer/.local/bin:$PATH

# Устанавливаем рабочую директорию
WORKDIR /app

# Создаём пользователя ДО установки зависимостей и даем ему права на чтение и запись
ARG UID=1001
ARG GID=1001
RUN groupadd -g ${GID} deployer && \
    useradd -m -u ${UID} -g deployer deployer

# Копируем requirements
COPY requirements.txt .

# Устанавливаем зависимости от root
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Копируем исходный код
COPY . .

# Даём права пользователю на всё содержимое
RUN chown -R deployer:deployer /app && \
    chmod +x /app/src/main.py

# Переключаемся на пользователя
USER deployer

# Проверка состояния контейнера
HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

# Запуск приложения
CMD ["python", "-m", "src.main"]