# Файл: bot/services/scheduler.py
import asyncio
from datetime import datetime, timezone
from aiogram import Bot
from bot.database.requests import get_users_for_reminder
from bot.keyboards import get_main_kb

async def reminder_scheduler(bot: Bot):
    """Фоновый планировщик для отправки ежедневных напоминаний."""
    while True:
        now = datetime.now(timezone.utc)
        
        # Запускаем рассылку только ровно в 00 минут каждого часа
        if now.minute == 0:
            users_to_notify = await get_users_for_reminder(now.hour)
            for row in users_to_notify:
                try:
                    await bot.send_message(
                        row['user_id'],
                        "⏰ Время внести сегодняшние показатели прогресса!\nНе прерывай свой стрик.",
                        reply_markup=get_main_kb()
                    )
                except Exception as e:
                    pass # Пользователь мог заблокировать бота
            
            # Спим 60 минут до следующего часа
            await asyncio.sleep(3600)
        else:
            # Если бот запущен не ровно в 00 минут, спим до следующей минуты
            await asyncio.sleep(60)