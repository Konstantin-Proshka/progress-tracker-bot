from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from bot.database.requests import add_metric
from bot.keyboards import get_main_kb

metrics_router = Router()

class MetricState(StatesGroup):
    waiting_for_name = State()
    waiting_for_unit = State()

@metrics_router.message(F.text == "➕ Новая метрика")
async def cmd_new_metric(message: Message, state: FSMContext):
    await message.answer(
        "Введи название для новой метрики.\n\n"
        "Например: `Жим лежа`, `Олимпиадная математика`, `Подтягивания`",
        parse_mode="Markdown"
    )
    await state.set_state(MetricState.waiting_for_name)

@metrics_router.message(MetricState.waiting_for_name)
async def process_metric_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text.strip())
    await message.answer(
        "Теперь введи единицу измерения.\n\n"
        "Например: `кг`, `задач`, `раз`",
        parse_mode="Markdown"
    )
    await state.set_state(MetricState.waiting_for_unit)

@metrics_router.message(MetricState.waiting_for_unit)
async def process_metric_unit(message: Message, state: FSMContext):
    user_data = await state.get_data()
    metric_name = user_data['name']
    metric_unit = message.text.strip()
    
    await add_metric(message.from_user.id, metric_name, metric_unit)
    await state.clear()
    
    await message.answer(
        f"✅ Метрика *{metric_name} ({metric_unit})* успешно создана!\n"
        "Теперь ты можешь вносить по ней записи.",
        parse_mode="Markdown",
        reply_markup=get_main_kb()
    )