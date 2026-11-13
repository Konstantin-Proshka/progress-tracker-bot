from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from bot.database.requests import get_user_metrics, add_record
from bot.keyboards import get_metrics_kb, get_main_kb

records_router = Router()

class RecordState(StatesGroup):
    waiting_for_value = State()

@records_router.message(F.text == "📝 Внести запись")
async def cmd_add_record(message: Message):
    # Достаем список метрик пользователя из БД
    metrics = await get_user_metrics(message.from_user.id)
    
    if not metrics:
        await message.answer("У тебя пока нет ни одной метрики. Сначала нажми «➕ Новая метрика».")
        return
    
    await message.answer(
        "Выбери метрику, для которой хочешь добавить запись:",
        reply_markup=get_metrics_kb(metrics, action="record")
    )

@records_router.callback_query(F.data.startswith("record_"))
async def process_metric_selection(callback: CallbackQuery, state: FSMContext):
    # Извлекаем ID метрики из callback_data (например, из "metric_1" берем "1")
    metric_id = int(callback.data.split("_")[1])
    await state.update_data(metric_id=metric_id)
    
    await callback.message.edit_text(
        "Отлично. Теперь отправь числовое значение (например, `75` или `10.5`):",
        parse_mode="Markdown"
    )
    await state.set_state(RecordState.waiting_for_value)

@records_router.message(RecordState.waiting_for_value)
async def process_record_value(message: Message, state: FSMContext):
    try:
        # Меняем запятую на точку, если пользователь ввел дробное число с телефона
        value = float(message.text.strip().replace(',', '.'))
    except ValueError:
        await message.answer("Пожалуйста, отправь просто число (например, 75 или 12.5).")
        return

    user_data = await state.get_data()
    metric_id = user_data['metric_id']
    
    await add_record(metric_id, value)
    await state.clear()
    
    await message.answer(
        f"✅ Запись `{value}` успешно добавлена!",
        parse_mode="Markdown",
        reply_markup=get_main_kb()
    )