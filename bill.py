gst_rate = 0.05


def calculate_bill(items):
    subtotal = 0

    for item in items:
        subtotal = subtotal + item["total"]

    gst = subtotal * gst_rate
    total = subtotal + gst

    return subtotal, gst, total


def create_bill_text(customer, phone, items, subtotal, gst, total, date_time):
    text = ""
    text = text + "          BILL MANAGEMENT SYSTEM\n"
    text = text + "------------------------------------------\n"
    text = text + "Customer: " + customer + "\n"
    text = text + "Phone: " + phone + "\n"
    text = text + "Date: " + date_time + "\n"
    text = text + "------------------------------------------\n"

    text = text + "Product       Qty       Price       Total\n"
    text = text + "------------------------------------------\n"

    for item in items:
        text = text + item["product"] + "       "
        text = text + str(item["quantity"]) + "       "
        text = text + str(item["price"]) + "       "
        text = text + str(item["total"]) + "\n"

    text = text + "------------------------------------------\n"
    text = text + "Subtotal: " + str(round(subtotal, 2)) + "\n"
    text = text + "GST 5%: " + str(round(gst, 2)) + "\n"
    text = text + "Total: " + str(round(total, 2)) + "\n"
    text = text + "------------------------------------------\n"
    text = text + "        Thank You!\n"

    return text