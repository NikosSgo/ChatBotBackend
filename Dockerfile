# Используем официальный образ Python
FROM python:3.13-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y \
  gcc \
  curl \
  && rm -rf /var/lib/apt/lists/*

# Устанавливаем uv
RUN pip install --no-cache-dir uv

# Копируем файлы зависимостей
COPY pyproject.toml uv.lock ./

# Синхронизируем зависимости через uv (включая dev-зависимости)
RUN uv sync --frozen

# Копируем исходный код
COPY app/ ./app/
COPY main.py ./
COPY alembic.ini ./
COPY run.sh ./
COPY .env ./
COPY alembic/ ./alembic/

# Создаем пользователя для безопасности
RUN useradd --create-home --shell /bin/bash appuser && \
  chown -R appuser:appuser /app
RUN chmod +x run.sh
USER appuser

# Указываем команду для запуска
EXPOSE 8000
ENTRYPOINT [ "./run.sh" ]
