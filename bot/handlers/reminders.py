# Файл: bot/handlers/reminders.py
from aiogram import Router, F
from aiogram.types import Message
from bot.database.requests import toggle_reminder

reminders_router = Router()

@reminders_router.message(F.text == "⏰ Напоминания")
async def cmd_toggle_reminder(message: Message):
    await toggle_reminder(message.from_user.id)
    await message.answer(
        "Статус напоминаний изменен!\n"
        "Если они включены, бот будет писать тебе каждый вечер в 21:00 (по твоему местному времени).",
        parse_mode="Markdown"
    )