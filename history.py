import sqlite3


def get_history():
    connection = sqlite3.connect("bills.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, customer, phone, total, date_time
        FROM bills
        ORDER BY id DESC
    """)

    records = cursor.fetchall()

    connection.close()

    return records