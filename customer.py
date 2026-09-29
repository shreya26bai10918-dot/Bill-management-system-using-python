def validate_customer(name, phone):
    name = name.strip()
    phone = phone.strip()

    if name == "":
        return False, "Please enter customer name."

    if phone == "":
        return False, "Please enter phone number."

    if not phone.isdigit():
        return False, "Phone number should contain only numbers."

    if len(phone) != 10:
        return False, "Phone number should be 10 digits."

    return True, ""