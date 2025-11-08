import aiosqlite
import asyncio
db_name = "laravel"
async def async_fetch_users():
    async with aiosqlite.connect(db_name) as db:
        async with db.execute('SELECT * FROM users') as cursor:
            return await cursor.fetchall()
async def async_fetch_older_users():
    async with aiosqlite.connect(db_name) as db:
        async with db.execute('SELECT * FROM users WHERE age > ?',(40,)) as cursor:
            return await cursor.fetchall()

async def fetch_concurrently():
    users,older_users = await asyncio.gather(
        async_fetch_users(),async_fetch_older_users()
    )
    print("All users:")
    for u in users:
        print(u)
    print("\nUsers older than 40:")
    for u in older_users:
        print(u)

if __name__ == "__main__":
    asyncio.run(fetch_concurrently())
