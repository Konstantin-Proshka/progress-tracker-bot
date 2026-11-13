from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from bot.database.requests import add_user, update_utc_offset
from bot.keyboards import get_main_kb, get_timezone_kb

start_router = Router()

class TimezoneState(StatesGroup):
    waiting_for_offset = State()

@start_router.message(CommandStart())
async def cmd_start(message: Message):
    await add_user(message.from_user.id)
    await message.answer(
        "Привет! Я трекер твоего прогресса 📈\n\n"
        "Для начала давай настроим твой часовой пояс (это нужно для точных графиков и своевременных напоминаний).",
        reply_markup=get_timezone_kb()
    )

@start_router.callback_query(F.data.startswith("tz_"))
async def process_timezone_callback(callback: CallbackQuery, state: FSMContext):
    action = callback.data.split("_")[1]
    
    if action == "manual":
        await callback.message.edit_text(
            "Введи свой сдвиг от UTC числом (например, `3` для UTC+3 или `-5` для UTC-5):",
            parse_mode="Markdown"
        )
        await state.set_state(TimezoneState.waiting_for_offset)
        return

    # Если выбрана готовая кнопка
    offset = int(action)
    await update_utc_offset(callback.from_user.id, offset)
    await callback.message.delete()
    await callback.message.answer(
        f"✅ Часовой пояс установлен на UTC{'+' if offset >= 0 else ''}{offset}.\n"
        "Выбери действие в меню ниже:",
        reply_markup=get_main_kb()
    )

@start_router.message(TimezoneState.waiting_for_offset)
async def process_manual_timezone(message: Message, state: FSMContext):
    try:
        offset = int(message.text.strip().replace('+', ''))
        if not -12 <= offset <= 14:
            raise ValueError
    except ValueError:
        await message.answer("Пожалуйста, введи целое число от -12 до 14.")
        return

    await update_utc_offset(message.from_user.id, offset)
    await state.clear()
    await message.answer(
        f"✅ Часовой пояс установлен на UTC{'+' if offset >= 0 else ''}{offset}.\n"
        "Выбери действие в меню ниже:",
        reply_markup=get_main_kb()
    )