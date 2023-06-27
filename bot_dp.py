import random
import sqlite3


def sql_create():
    global conn, cursor
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    if conn:
        print("База данных подключена!")

    conn.execute("CREATE TABLE IF NOT EXISTS anketa "
               "(id INTEGER PRIMARY KEY AUTOINCREMENT,"
               "name VARCHAR (100) NOT NULL,"
               "age INTEGER NOT NULL,"
               "groups VARCHAR (10),"
               "direction VARCHAR (144) NOT NULL)")
    conn.commit()
async def sql_command_insert(state):
    async with state.proxy() as data:
        cursor.execute(
            "INSERT INTO anketa "
            "(name,age,groups,direction) "
            "VALUES (?, ?, ?, ?)",
            tuple(data.values())
        )
        conn.commit()


async def sql_command_random():
    mentors = cursor.execute("SELECT * FROM anketa").fetchall()
    random_mentors = random.choice(mentors)
    return random_mentors


async def sql_command_all():
    return cursor.execute("SELECT * FROM anketa").fetchall()


async def sql_command_all_ids():
    return cursor.execute("SELECT id FROM anketa").fetchall()


async def sql_command_delete(user_id):
    cursor.execute("DELETE FROM anketa WHERE id = ?", (user_id,))
    conn.commit()
