# Файл: bot/keyboards.py
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

def get_main_kb() -> ReplyKeyboardMarkup:
    """Главное меню (Reply-кнопки)."""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="➕ Новая метрика"), KeyboardButton(text="📝 Внести запись")],
            [KeyboardButton(text="📈 Мой прогресс"), KeyboardButton(text="⏰ Напоминания")]
        ],
        resize_keyboard=True
    )

def get_timezone_kb() -> InlineKeyboardMarkup:
    """Inline-кнопки для выбора часового пояса."""
    builder = InlineKeyboardBuilder()
    builder.button(text="UTC+3 (Москва)", callback_data="tz_3")
    builder.button(text="UTC+5 (Екатеринбург)", callback_data="tz_5")
    builder.button(text="UTC+7 (Красноярск)", callback_data="tz_7")
    builder.button(text="Ввести вручную", callback_data="tz_manual")
    builder.adjust(1)
    return builder.as_markup()

def get_metrics_kb(metrics: list, action: str) -> InlineKeyboardMarkup:
    """Динамическая Inline-клавиатура со списком метрик пользователя."""
    builder = InlineKeyboardBuilder()
    for metric in metrics:
        # action будет "record" или "stat"
        builder.button(text=f"{metric['name']} ({metric['unit']})", callback_data=f"{action}_{metric['id']}")
    builder.adjust(1)
    return builder.as_markup()