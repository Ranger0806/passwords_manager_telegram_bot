import sqlite3 as sq
from user_passwords_db import user_db_conect


async def db_conect(user_id) -> None:
    global cur
    global db

    db = sq.connect("passwordstg.db")
    cur = db.cursor()

    cur.execute(
        "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, name TEXT, status TEXT, botPassword TEXT)")
    db.commit()
    await user_db_conect(user_id=user_id)


async def cheker_user(user_id) -> bool:
    cur.execute("SELECT COUNT(*) FROM users WHERE user_id = ?", (user_id,))
    if cur.fetchone()[0] == 0:
        return False
    else:
        return True


async def get_new_user(user_id, name, status, botPassword) -> None:
    cur.execute("INSERT INTO 'users' ('user_id', 'name', 'status', 'botPassword') VALUES (?, ?, ?, ?)",
                (user_id, name, status, botPassword,))
    db.commit()


async def get_status(user_id) -> str:
    cur.execute("SELECT status FROM users WHERE user_id = ?", (user_id,))
    return cur.fetchone()[0]


async def set_status(status, user_id) -> None:
    cur.execute("UPDATE users SET status = ? WHERE user_id = ?", (status, user_id,))
    db.commit()


async def get_botPassword(user_id) -> str:
    cur.execute("SELECT botPassword FROM users WHERE user_id = ?", (user_id,))
    return cur.fetchone()[0]


async def set_botPassword(botPassword, user_id) -> None:
    cur.execute("UPDATE users SET botPassword = ? WHERE user_id = ?", (botPassword, user_id,))
    db.commit()


async def reset_password(user_id, new_password):
    cur.execute("UPDATE users SET botPassword = ? WHERE user_id = ?", (new_password, user_id,))
    db.commit()


async def close():
    db.close()
