products = {
    "Rice": 60,
    "Wheat": 50,
    "Milk": 30,
    "Bread": 40,
    "Biscuits": 20,
    "Juice": 50
}


def get_price(product):
    return products.get(product, 0)


def get_products():
    return list(products.keys())