# Используем базовый образ Python 3.10.7
FROM python:3.10.7

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файл зависимостей
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем все остальные файлы проекта
COPY . .

# Указываем команду для запуска приложения
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5050"]
