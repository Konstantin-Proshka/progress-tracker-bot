# Файл: bot/services/charts.py
import matplotlib
matplotlib.use('Agg')  # Включаем headless-режим для работы на сервере без интерфейса
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import io
from datetime import datetime

def generate_progress_chart(dates: list[datetime], values: list[float], metric_name: str, unit: str) -> io.BytesIO:
    """Генерирует PNG-график прогресса в оперативной памяти."""
    plt.figure(figsize=(9, 5))
    
    # Рисуем линию с точками
    plt.plot(dates, values, marker='o', linestyle='-', color='#2c3e50', linewidth=2, markersize=6)
    
    # Настройка осей и заголовка
    plt.title(f'Прогресс: {metric_name}', fontsize=14, pad=15)
    plt.ylabel(f'Значение ({unit})', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.6)
    
    # Форматирование дат на оси X
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d.%m %H:%M'))
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Сохраняем в буфер
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=150)
    plt.close()
    buf.seek(0)
    
    return buf