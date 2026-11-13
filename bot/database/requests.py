import aiosqlite
from bot.database.db import DB_PATH

async def add_user(user_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("INSERT OR IGNORE INTO users (user_id) VALUES (?)", (user_id,))
        await db.commit()

async def update_utc_offset(user_id: int, offset: int):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("UPDATE users SET utc_offset = ? WHERE user_id = ?", (offset, user_id))
        await db.commit()

async def add_metric(user_id: int, name: str, unit: str):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("INSERT INTO metrics (user_id, name, unit) VALUES (?, ?, ?)", (user_id, name, unit))
        await db.commit()

async def get_user_metrics(user_id: int) -> list:
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT id, name, unit FROM metrics WHERE user_id = ?", (user_id,)) as cursor:
            return await cursor.fetchall()

async def add_record(metric_id: int, value: float):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("INSERT INTO records (metric_id, value) VALUES (?, ?)", (metric_id, value))
        await db.commit()

async def get_metric_records(metric_id: int) -> list:
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        # Сортируем по дате создания для корректного графика
        async with db.execute("SELECT value, created_at FROM records WHERE metric_id = ? ORDER BY created_at ASC", (metric_id,)) as cursor:
            return await cursor.fetchall()

async def toggle_reminder(user_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("UPDATE users SET reminder_enabled = 1 - reminder_enabled WHERE user_id = ?", (user_id,))
        await db.commit()

async def get_users_for_reminder(current_utc_hour: int) -> list:
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        # Отбираем тех, у кого включены уведомления и локальное время совпадает с reminder_hour
        query = "SELECT user_id FROM users WHERE reminder_enabled = 1 AND (? + utc_offset + 24) % 24 = reminder_hour"
        async with db.execute(query, (current_utc_hour,)) as cursor:
            return await cursor.fetchall()