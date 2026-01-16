# Используем официальный Python образ как родительский
FROM python:3.11-slim

# Устанавливаем переменные окружения
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# Устанавливаем системные зависимости (если нужны для сборки пакетов)
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        gcc \
        libpq-dev \
        postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Создаем и переходим в рабочую директорию
WORKDIR /app

# Копируем файл зависимостей
COPY requirements.txt .

# Устанавливаем Python-зависимости
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Копируем весь проект
COPY . .

# Собираем статику (если нужно, можно сделать позже)
# RUN python manage.py collectstatic --noinput

# Открываем порт
EXPOSE 8000

# Команда для запуска
# Для разработки:
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
# Для продакшена замените на:
# CMD ["gunicorn", "--bind", "0.0.0.0:8000", "ваш_проект.wsgi:application"]