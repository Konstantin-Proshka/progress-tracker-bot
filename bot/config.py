import os
from dotenv import load_dotenv

# Загружаем переменные окружения из файла .env
load_dotenv()

# Получаем токен бота
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Защита от запуска без токена
if not BOT_TOKEN:
    raise ValueError("Переменная BOT_TOKEN не найдена! Проверьте файл .env.")