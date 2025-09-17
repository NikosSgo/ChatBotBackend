# Используем официальный образ Python
FROM python:3.13-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Устанавливаем uv
RUN pip install --no-cache-dir uv

# Копируем файлы зависимостей
COPY pyproject.toml uv.lock ./

# Синхронизируем зависимости через uv
RUN uv sync --frozen --no-dev

# Копируем исходный код
COPY src/ ./src/
COPY .env ./

# Создаем пользователя для безопасности
RUN useradd --create-home --shell /bin/bash appuser && \
  chown -R appuser:appuser /app

USER appuser

# Указываем команду для запуска (замените на вашу)
EXPOSE 8000

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
