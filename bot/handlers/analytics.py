# Файл: bot/handlers/analytics.py
from datetime import datetime
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, BufferedInputFile

from bot.database.requests import get_user_metrics, get_metric_records
from bot.keyboards import get_metrics_kb
from bot.services.charts import generate_progress_chart

analytics_router = Router()

@analytics_router.message(F.text == "📈 Мой прогресс")
async def cmd_progress(message: Message):
    metrics = await get_user_metrics(message.from_user.id)
    if not metrics:
        await message.answer("Сначала создай метрику и добавь записи!")
        return
    await message.answer("График какой метрики ты хочешь посмотреть?", reply_markup=get_metrics_kb(metrics, action="stat"))

@analytics_router.callback_query(F.data.startswith("stat_"))
async def process_stat_selection(callback: CallbackQuery):
    metric_id = int(callback.data.split("_")[1])
    
    # Достаем метрику для названия и единиц измерения
    metrics = await get_user_metrics(callback.from_user.id)
    current_metric = next((m for m in metrics if m['id'] == metric_id), None)
    
    records = await get_metric_records(metric_id)
    if not records:
        await callback.message.edit_text("По этой метрике пока нет записей.")
        return
        
    await callback.message.edit_text("Генерирую график, подожди секунду... ⏳")
    
    # Парсим даты и значения
    dates = [datetime.strptime(r['created_at'], "%Y-%m-%d %H:%M:%S") for r in records]
    values = [r['value'] for r in records]
    
    # Считаем статистику
    min_val, max_val = min(values), max(values)
    growth = values[-1] - values[0]
    growth_sign = "+" if growth > 0 else ""
    
    # Рисуем график
    chart_buf = generate_progress_chart(dates, values, current_metric['name'], current_metric['unit'])
    photo = BufferedInputFile(chart_buf.read(), filename="chart.png")
    
    text = (
        f"📊 **Аналитика: {current_metric['name']}**\n\n"
        f"Текущий результат: `{values[-1]} {current_metric['unit']}`\n"
        f"Минимум: `{min_val}` | Максимум: `{max_val}`\n"
        f"Общий прирост: `{growth_sign}{round(growth, 2)}`"
    )
    
    await callback.message.delete()
    await callback.message.answer_photo(photo=photo, caption=text, parse_mode="Markdown")