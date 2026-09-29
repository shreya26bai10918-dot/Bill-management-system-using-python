import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

from customer import validate_customer
from products import get_products, get_price
from bill import calculate_bill, create_bill_text
from database import save_bill
from history import get_history
from analytics import get_analytics


class BillApp(tk.Tk):

    def __init__(self):
        super().__init__()

        self.title("Bill Management System")
        self.geometry("900x650")

        self.items = []

        self.create_widgets()

    def create_widgets(self):

        title = tk.Label(
            self,
            text="Bill Management System",
            font=("Arial", 22, "bold")
        )
        title.pack(pady=10)

        customer_frame = tk.Frame(self)
        customer_frame.pack(pady=5)

        tk.Label(
            customer_frame,
            text="Customer Name:"
        ).grid(row=0, column=0, padx=5, pady=5)

        self.customer_entry = tk.Entry(customer_frame, width=25)
        self.customer_entry.grid(row=0, column=1, padx=5)

        tk.Label(
            customer_frame,
            text="Phone:"
        ).grid(row=0, column=2, padx=5)

        self.phone_entry = tk.Entry(customer_frame, width=20)
        self.phone_entry.grid(row=0, column=3, padx=5)

        product_frame = tk.Frame(self)
        product_frame.pack(pady=10)

        tk.Label(
            product_frame,
            text="Product:"
        ).grid(row=0, column=0, padx=5)

        self.product_box = ttk.Combobox(
            product_frame,
            values=get_products(),
            state="readonly",
            width=18
        )
        self.product_box.grid(row=0, column=1, padx=5)

        tk.Label(
            product_frame,
            text="Quantity:"
        ).grid(row=0, column=2, padx=5)

        self.quantity_entry = tk.Entry(
            product_frame,
            width=10
        )
        self.quantity_entry.grid(row=0, column=3, padx=5)

        add_button = tk.Button(
            product_frame,
            text="Add Product",
            command=self.add_product
        )
        add_button.grid(row=0, column=4, padx=10)

        self.item_list = tk.Listbox(
            self,
            width=80,
            height=8
        )
        self.item_list.pack(pady=10)

        button_frame = tk.Frame(self)
        button_frame.pack(pady=5)

        generate_button = tk.Button(
            button_frame,
            text="Generate Bill",
            command=self.generate_bill,
            width=15
        )
        generate_button.grid(row=0, column=0, padx=5)

        clear_button = tk.Button(
            button_frame,
            text="Clear",
            command=self.clear_all,
            width=15
        )
        clear_button.grid(row=0, column=1, padx=5)

        history_button = tk.Button(
            button_frame,
            text="Bill History",
            command=self.show_history,
            width=15
        )
        history_button.grid(row=0, column=2, padx=5)

        analytics_button = tk.Button(
            button_frame,
            text="Analytics",
            command=self.show_analytics,
            width=15
        )
        analytics_button.grid(row=0, column=3, padx=5)

        self.bill_text = tk.Text(
            self,
            width=80,
            height=15
        )
        self.bill_text.pack(pady=10)

    def add_product(self):

        product = self.product_box.get()
        quantity = self.quantity_entry.get()

        if product == "":
            messagebox.showerror(
                "Error",
                "Please select a product."
            )
            return

        if not quantity.isdigit():
            messagebox.showerror(
                "Error",
                "Please enter a valid quantity."
            )
            return

        quantity = int(quantity)

        if quantity <= 0:
            messagebox.showerror(
                "Error",
                "Quantity must be greater than zero."
            )
            return

        price = get_price(product)
        total = price * quantity

        item = {
            "product": product,
            "quantity": quantity,
            "price": price,
            "total": total
        }

        self.items.append(item)

        self.item_list.insert(
            tk.END,
            product + " | Quantity: " +
            str(quantity) + " | Price: " +
            str(price) + " | Total: " +
            str(total)
        )

        self.product_box.set("")
        self.quantity_entry.delete(0, tk.END)

    def generate_bill(self):

        customer = self.customer_entry.get()
        phone = self.phone_entry.get()

        valid, message = validate_customer(
            customer,
            phone
        )

        if not valid:
            messagebox.showerror(
                "Error",
                message
            )
            return

        if len(self.items) == 0:
            messagebox.showerror(
                "Error",
                "Please add at least one product."
            )
            return

        subtotal, gst, total = calculate_bill(
            self.items
        )

        date_time = datetime.now().strftime(
            "%d-%m-%Y %H:%M:%S"
        )

        bill = create_bill_text(
            customer,
            phone,
            self.items,
            subtotal,
            gst,
            total,
            date_time
        )

        self.bill_text.delete(
            "1.0",
            tk.END
        )

        self.bill_text.insert(
            tk.END,
            bill
        )

        save_bill(
            customer,
            phone,
            self.items,
            subtotal,
            gst,
            total,
            date_time
        )

        messagebox.showinfo(
            "Success",
            "Bill generated successfully."
        )

    def clear_all(self):

        self.customer_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
        self.product_box.set("")
        self.quantity_entry.delete(0, tk.END)

        self.item_list.delete(
            0,
            tk.END
        )

        self.bill_text.delete(
            "1.0",
            tk.END
        )

        self.items = []

    def show_history(self):

        records = get_history()

        window = tk.Toplevel(self)
        window.title("Bill History")
        window.geometry("700x400")

        text = tk.Text(
            window,
            width=80,
            height=20
        )
        text.pack(padx=10, pady=10)

        if len(records) == 0:
            text.insert(
                tk.END,
                "No bills found."
            )
            return

        for record in records:

            text.insert(
                tk.END,
                "Bill ID: " + str(record[0]) + "\n"
            )

            text.insert(
                tk.END,
                "Customer: " + str(record[1]) + "\n"
            )

            text.insert(
                tk.END,
                "Phone: " + str(record[2]) + "\n"
            )

            text.insert(
                tk.END,
                "Total: ₹" + str(record[3]) + "\n"
            )

            text.insert(
                tk.END,
                "Date: " + str(record[4]) + "\n"
            )

            text.insert(
                tk.END,
                "--------------------------------\n"
            )

    def show_analytics(self):

        bill_count, sales, product, quantity = get_analytics()

        message = (
            "Total Bills: " + str(bill_count) + "\n"
            "Total Sales: ₹" + str(round(sales, 2)) + "\n"
            "Most Purchased Product: " + product + "\n"
            "Quantity Sold: " + str(quantity)
        )

        messagebox.showinfo(
            "Sales Analytics",
            message
        )