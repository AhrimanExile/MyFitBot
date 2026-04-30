from aiosqlite import connect

async def init_db():
    async with connect('database/database.db') as db:
        await db.execute("""
                             CREATE TABLE IF NOT EXISTS users (
                             user_id INTEGER PRIMARY KEY,
                             gender TEXT,
                             age INTEGER,
                             weight REAL,
                             height REAL
                             )
                        """)
        await db.commit()