import sqlite3

__connection = None


def ensure_connection(func):
    def inner(*args, **kwargs):
        with sqlite3.connect('schedule.db') as conn:
            res = func(*args, conn=conn, **kwargs)
        return res

    return inner


@ensure_connection
def init_db(conn):
    c = conn.cursor()

    c.execute('''
        CREATE TABLE IF NOT EXISTS schedule (
            group_          TEXT,
            day_            TEXT,
            lessons_        TEXT
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS reminder (
            tg_id_          TEXT,
            group_          TEXT,
            time_           TEXT
        )
    ''')

    conn.commit()


@ensure_connection
def get_lessons(conn, group, day):
    c = conn.cursor()

    c.execute(
        'SELECT lessons_ FROM schedule WHERE group_ = ? and day_ = ? LIMIT 1',
        (group, day)
    )
    cost = c.fetchone()
    if cost is None:
        return "Ошибка"
    else:
        (res,) = cost
        return res


@ensure_connection
def add_reminder(conn, tg_id, group, time):
    c = conn.cursor()

    c.execute('INSERT into reminder (tg_id_, group_, time_) VALUES (?, ?, ?)', (tg_id, group, time))
    conn.commit()


@ensure_connection
def get_all_reminders(conn):
    c = conn.cursor()

    c.execute('SELECT tg_id_, group_, time_ FROM reminder')
    return c.fetchall()
