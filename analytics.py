import sqlite3


def get_analytics():
    connection = sqlite3.connect("bills.db")
    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM bills")
    bill_count = cursor.fetchone()[0]

    cursor.execute("SELECT SUM(total) FROM bills")
    sales = cursor.fetchone()[0]

    if sales is None:
        sales = 0

    cursor.execute("""
        SELECT product, SUM(quantity)
        FROM bill_items
        GROUP BY product
        ORDER BY SUM(quantity) DESC
        LIMIT 1
    """)

    result = cursor.fetchone()

    if result:
        top_product = result[0]
        top_quantity = result[1]
    else:
        top_product = "No product"
        top_quantity = 0

    connection.close()

    return bill_count, sales, top_product, top_quantity