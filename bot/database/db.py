import aiosqlite
import logging

DB_PATH = "progress_tracker.db"

async def init_db():
    """Асинхронная инициализация базы данных и создание таблиц."""
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("PRAGMA foreign_keys = ON;")
        
        # Таблица пользователей
        await db.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                utc_offset INTEGER DEFAULT 3,
                reminder_enabled INTEGER DEFAULT 0,
                reminder_hour INTEGER DEFAULT 21
            )
        ''')
        
        # Таблица метрик
        await db.execute('''
            CREATE TABLE IF NOT EXISTS metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                unit TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE
            )
        ''')
        
        # Таблица записей
        await db.execute('''
            CREATE TABLE IF NOT EXISTS records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                metric_id INTEGER NOT NULL,
                value REAL NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (metric_id) REFERENCES metrics (id) ON DELETE CASCADE
            )
        ''')
        
        await db.commit()
        logging.info("База данных успешно пересоздана и инициализирована.")