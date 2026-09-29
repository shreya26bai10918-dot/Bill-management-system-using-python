import sqlite3


def create_database():
    connection = sqlite3.connect("bills.db")
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bills (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer TEXT,
            phone TEXT,
            subtotal REAL,
            gst REAL,
            total REAL,
            date_time TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bill_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            bill_id INTEGER,
            product TEXT,
            quantity INTEGER,
            price REAL,
            total REAL
        )
    """)

    connection.commit()
    connection.close()


def save_bill(customer, phone, items, subtotal, gst, total, date_time):
    connection = sqlite3.connect("bills.db")
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO bills
        (customer, phone, subtotal, gst, total, date_time)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (customer, phone, subtotal, gst, total, date_time))

    bill_id = cursor.lastrowid

    for item in items:
        cursor.execute("""
            INSERT INTO bill_items
            (bill_id, product, quantity, price, total)
            VALUES (?, ?, ?, ?, ?)
        """, (
            bill_id,
            item["product"],
            item["quantity"],
            item["price"],
            item["total"]
        ))

    connection.commit()
    connection.close()