import sqlite3 as sq


async def user_db_conect(user_id) -> None:
    global cur
    global db

    db = sq.connect("passwordstg.db")
    cur = db.cursor()

    cur.execute(
        f"CREATE TABLE IF NOT EXISTS '{user_id}' (site TEXT, login TEXT, password TEXT)")
    db.commit()


async def set_new_info(user_id, site, login, password):
    cur.execute(f"INSERT INTO '{user_id}' (site, login, password) VALUES (?, ?, ?)", (site, login, password,))
    db.commit()


async def get_data(user_id) -> str:
    stroka = str()
    cur.execute(f"SELECT site, login, password FROM '{user_id}'")
    for i in cur.fetchall():
        stroka += f"Name: `{i[0]}` \nLogin: `{i[1]}` \nPasswod: `{i[2]}`\n\n"
    stroka += "Вы можете скопировать нужные данные нажав на них."
    return stroka

async def update_data(user_id, site_old, site ,login, password):
    cur.execute(f"UPDATE '{user_id}' SET site = ?, login = ?, password = ? WHERE site = ?", (site, login, password, site_old))
    db.commit()

async def delete_data(user_id, site):
    cur.execute(f"DELETE FROM '{user_id}' WHERE site = ?", (site, ))
    db.commit()

async def check_data(user_id, site):
    cur.execute(f"SELECT COUNT(*) FROM '{user_id}' WHERE site = ?", (site, ))
    if cur.fetchone()[0] == 0:
        return False
    else:
        return True

async def close_users():
    db.close()
