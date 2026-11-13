# Файл: main.py
import asyncio
import logging
from aiogram import Bot, Dispatcher
from bot.config import BOT_TOKEN
from bot.database.db import init_db
from bot.services.scheduler import reminder_scheduler

from bot.handlers.start import start_router
from bot.handlers.metrics import metrics_router
from bot.handlers.records import records_router
from bot.handlers.analytics import analytics_router
from bot.handlers.reminders import reminders_router

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

async def main():
    await init_db()
    
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    
    # Подключаем роутеры
    dp.include_router(start_router)
    dp.include_router(metrics_router)
    dp.include_router(records_router)
    dp.include_router(analytics_router)
    dp.include_router(reminders_router)
    
    # Запускаем фоновую задачу для напоминаний
    asyncio.create_task(reminder_scheduler(bot))
    
    logging.info("Бот успешно запущен!")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Остановлено.")