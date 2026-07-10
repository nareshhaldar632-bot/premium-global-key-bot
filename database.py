import sqlite3

DB_NAME = "store.db"


def connect():
    conn = sqlite3.connect(
        DB_NAME,
        timeout=30,
        check_same_thread=False
    )
    return conn


def create_tables():

    conn = connect()
    conn.execute("PRAGMA journal_mode=WAL")
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users(
        user_id INTEGER PRIMARY KEY,
        username TEXT,
        first_name TEXT
    )
    """)


    cur.execute("""
    CREATE TABLE IF NOT EXISTS orders(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id TEXT,
        user_id INTEGER,
        product TEXT,
        duration TEXT,
        amount INTEGER,
        utr TEXT UNIQUE,
        status TEXT
    )
    """)


    conn.commit()
    conn.close()



def add_user(user_id, username, first_name):

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT OR IGNORE INTO users
        (user_id, username, first_name)
        VALUES (?, ?, ?)
        """,
        (
            user_id,
            username,
            first_name
        )
    )

    conn.commit()
    conn.close()



def check_utr(utr):

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "SELECT id FROM orders WHERE utr=?",
        (utr,)
    )

    data = cur.fetchone()

    conn.close()

    return data is not None



def add_order(
    order_id,
    user_id,
    product,
    duration,
    amount,
    utr
):

    conn = connect()
    cur = conn.cursor()


    cur.execute("""
INSERT INTO orders
(order_id, user_id, product, duration, amount, utr, status)
VALUES (?, ?, ?, ?, ?, ?, ?)
""",
(
    order_id,
    user_id,
    product,
    duration,
    amount,
    None if utr == "" else utr,
    "PENDING"
))


    conn.commit()
    conn.close()



def update_order_status(order_id, status):

    conn = connect()
    cur = conn.cursor()


    cur.execute(
        """
        UPDATE orders
        SET status=?
        WHERE order_id=?
        """,
        (
            status,
            order_id
        )
    )


    conn.commit()
    conn.close()



def get_order(order_id):

    conn = connect()
    cur = conn.cursor()


    cur.execute(
        """
        SELECT *
        FROM orders
        WHERE order_id=?
        """,
        (order_id,)
    )


    data = cur.fetchone()

    conn.close()

    return data
