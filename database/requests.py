from aiosqlite import connect

async def add_user(user_id, gender, age, weight, height):
    async with connect('database/database.db') as db:
        await db.execute("""INSERT INTO users (user_id, gender, age, weight, height) VALUES(?, ?, ?, ?, ?) 
                         ON CONFLICT (user_id) DO UPDATE SET
                         gender = excluded.gender,
                         age = excluded.age,
                         weight = excluded.weight,
                         height = excluded.height;""", 
                         (user_id, gender, age, weight, height))
        await db.commit()

async def get_userprofile(user_id):
    async with connect('database/database.db') as db:
        async with db.execute('SELECT * FROM users WHERE user_id == ?', (user_id, )) as cursor:
            return await cursor.fetchone()