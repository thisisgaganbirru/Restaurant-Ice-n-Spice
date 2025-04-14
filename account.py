import customtkinter as ctk
from utils import resize_image
from headerNav import NavigationHeader
import mysql.connector
from dbconnection import DB_CONFIG
from orderhistory import OrderHistory
import json
from decimal import Decimal

class CustomerAccountPage(ctk.CTkFrame):
    def __init__(self, parent, app=None):
        super().__init__(parent)
        self.app = app
        self.configure(width=600, height=700)

        self.edit_icon = resize_image((20, 20), "images/edit_entry.png")
        self.check_icon = resize_image((20, 20), "images/checkmark.png")

        self.create_header()
        self.create_account_body()

    def create_header(self):
        NavigationHeader(self, app=self.app).pack(side="top", fill="x")

    def create_account_body(self):
        body_frame = ctk.CTkFrame(self, fg_color="transparent")
        body_frame.pack(fill="both", expand=True)
        body_frame.pack_propagate(False)

        try:
            self.bg_image = resize_image((800, 800), "images/backg.jpg")
            bg_label = ctk.CTkLabel(body_frame, image=self.bg_image, text="")
            bg_label.pack(fill="both", expand=True)
        except:
            pass

        self.content_frame = ctk.CTkFrame(body_frame, fg_color="#F9F0E5", width=500, height=500, corner_radius=5)
        self.content_frame.place(relx=0.5, rely=0.05, anchor="n")
        self.content_frame.pack_propagate(False)

        self.create_tabs()

        self.views = {
            "profile": self.create_profile_view(),
            "orders": self.create_orders_view()
        }

        self.profile_tab.border_frame.bind("<Button-1>", lambda e: self.show_view("profile"))
        self.profile_tab.label.bind("<Button-1>", lambda e: self.show_view("profile"))
        self.orders_tab.border_frame.bind("<Button-1>", lambda e: self.show_view("orders"))
        self.orders_tab.label.bind("<Button-1>", lambda e: self.show_view("orders"))

        self.show_view("profile")

        self.logout_button = ctk.CTkButton(
            body_frame,
            text="Logout ⮕",
            text_color="black",
            fg_color="#F1D94B",
            hover_color="#f7e565",
            font=("Poppins", 14, "bold"),
            width=140,
            height=40,
            anchor="center",
            command=self.logout
        )
        self.logout_button.place(relx=0.5, rely=0.92, anchor="center")

    def create_tabs(self):
        self.header_frame = ctk.CTkFrame(self.content_frame, height=50, fg_color="#F5F5F5", corner_radius=0)
        self.header_frame.pack(fill="x")
        self.header_frame.pack_propagate(False)

        self.tab_container = ctk.CTkFrame(self.header_frame, fg_color="transparent")
        self.tab_container.pack(fill="x", expand=True)
        self.tab_container.pack_propagate(False)

        left_half = ctk.CTkFrame(self.tab_container, fg_color="transparent")
        left_half.pack(side="left", fill="both", expand=True)

        right_half = ctk.CTkFrame(self.tab_container, fg_color="transparent")
        right_half.pack(side="left", fill="both", expand=True)

        self.profile_tab = TabFrame(left_half, "Profile")
        self.profile_tab.pack(fill="both", expand=True)

        self.orders_tab = TabFrame(right_half, "Orders")
        self.orders_tab.pack(fill="both", expand=True)

        self.content_frame_inner = ctk.CTkFrame(self.content_frame, fg_color="#F9F0E5", corner_radius=0)
        self.content_frame_inner.pack(fill="both", expand=True)

    def show_view(self, view_name):
        if view_name == "profile":
            self.profile_tab.activate()
            self.orders_tab.deactivate()
        else:
            self.profile_tab.deactivate()
            self.orders_tab.activate()

        for view in self.views.values():
            view.pack_forget()

        self.views[view_name].pack(fill="both", expand=True)

    def create_profile_view(self):
        frame = ctk.CTkFrame(self.content_frame_inner, fg_color="transparent")

        welcome_frame = ctk.CTkFrame(frame, fg_color="transparent")
        welcome_frame.pack(fill="x", padx=20, pady=(5, 5))

        name = self.app.logged_in_user.get("first_name", "User")

        ctk.CTkLabel(welcome_frame, text=f"Welcome {name}", font=("Arial", 24, "bold"), text_color="#660033").pack(anchor="w")
        ctk.CTkLabel(welcome_frame, text="Manage your profile information", font=("Arial", 14), text_color="gray").pack(anchor="w", pady=(5, 0))

        ctk.CTkFrame(frame, height=2, fg_color="#E5E5E5").pack(fill="x", padx=20, pady=(0, 0))

        user_id = self.app.logged_in_user.get("userID", 0)
        user_data = self.fetch_user_data(user_id)

        if user_data:
            name, username, mobile, email, password = user_data
        else:
            name, username, mobile, email, password = ("N/A",)*5

        fields = ["Name", "Username", "Mobile", "Email", "Password"]
        values = [name, username, mobile, email, password]

        for i, (label_text, value) in enumerate(zip(fields, values)):
            self.create_entry_row(frame, label_text, value)

        return frame

    def create_orders_view(self):
        frame = ctk.CTkFrame(self.content_frame_inner, fg_color="transparent")

        welcome_frame = ctk.CTkFrame(frame, fg_color="transparent")
        welcome_frame.pack(fill="x", padx=20, pady=(5, 5))

        name = self.app.logged_in_user.get("first_name", "User")
        ctk.CTkLabel(welcome_frame, text=f"Welcome {name}", font=("Arial", 24, "bold"), text_color="#660033").pack(anchor="w")
        ctk.CTkLabel(welcome_frame, text="View your order history", font=("Arial", 14), text_color="gray").pack(anchor="w", pady=(5, 0))

        # Orders container with automatic scrolling
        orders_container = ctk.CTkFrame(frame, fg_color="transparent")
        orders_container.pack(fill="both", expand=True, padx=20, pady=(20,0))

        # Orders frame that will scroll if content exceeds height
        self.orders_frame = ctk.CTkScrollableFrame(
            orders_container,
            fg_color="transparent",
            height=350,  # Fixed height
            width=460    # Fixed width
        )
        self.orders_frame.pack(fill="both", expand=True)

        orders = self.fetch_orders(self.app.logged_in_user["userID"])
        if orders:
            for order in orders:
                self.create_ordercard(self.orders_frame, order)
        else:
            ctk.CTkLabel(
                self.orders_frame,
                text="No orders yet",
                font=("Poppins", 16, "italic"),
                text_color="gray"
            ).pack(pady=20)

        return frame

    def create_ordercard(self, parent, order):
        # Main card frame
        card = ctk.CTkFrame(
            parent,
            fg_color="white",
            corner_radius=10,
            border_width=1,
            border_color="#F1D94B",
            height=150  # Fixed height for the card
        )
        card.pack(fill="x", pady=5)
        card.pack_propagate(False)

        # Header frame
        header_frame = ctk.CTkFrame(card, fg_color="transparent", height=40)
        header_frame.pack(fill="x", padx=15, pady=(10,5))
        header_frame.pack_propagate(False)

        # Order ID and Date
        formatted_id = f"Order Id: #{order['OrderID']:07d}"
        ctk.CTkLabel(
            header_frame,
            text=formatted_id,
            font=("Poppins", 14, "bold"),
            text_color="black"
        ).pack(side="left")

        date_str = f"Ordered on {order['CreatedAT'].strftime('%a, %b %d, %Y, %I:%M %p')}"
        ctk.CTkLabel(
            header_frame,
            text=date_str,
            font=("Poppins", 12),
            text_color="gray"
        ).pack(side="right")

        # Separator line
        separator = ctk.CTkFrame(card, height=1, fg_color="#E5E5E5")
        separator.pack(fill="x", padx=15, pady=5)

        # Items list
        items = json.loads(order['Item_list'])
        items_frame = ctk.CTkFrame(card, fg_color="transparent")
        items_frame.pack(fill="x", padx=15)

        for item in items:
            item_text = f"{item['name']} x {item['quantity']}"
            ctk.CTkLabel(
                items_frame,
                text=item_text,
                font=("Poppins", 12),
                text_color="black",
                anchor="w",
                justify="left"
            ).pack(fill="x")

        # Total amount
        total_frame = ctk.CTkFrame(card, fg_color="transparent")
        total_frame.pack(fill="x", padx=15, pady=5)

        ctk.CTkLabel(
            total_frame,
            text=f"Total Paid: $ {float(order['Total_price']):.2f}",
            font=("Poppins", 12, "bold"),
            text_color="black"
        ).pack(side="right")

        # Reorder button
        reorder_btn = ctk.CTkButton(
            card,
            text="Reorder",
            font=("Poppins", 12),
            fg_color="#F1D94B",
            text_color="black",
            width=100,
            height=30,
            command=lambda: self.reorder(order)
        )
        reorder_btn.place(relx=0.92, rely=0.85, anchor="e")

    def reorder(self, order):
        try:
            # Parse the stored items from Item_list
            items = json.loads(order['Item_list'])
            
            # Create a new cart with the items
            cart = {}
            for item in items:
                cart[item['id']] = {
                    'name': item['name'],
                    'price': Decimal(item['price']),
                    'quantity': item['quantity'],
                    'image_path': item.get('image_path', '')
                }
            
            # Redirect to order page with the recreated cart
            self.app.show_order_page(cart=cart)

        except Exception as e:
            print(f"Error reordering items: {e}")

    # Sample usage to test rendering one card
    def fetch_orders(self, user_id):
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM `Order` WHERE UserID = %s ORDER BY CreatedAT DESC", (user_id,))
        orders = cursor.fetchall()
        conn.close()
        return orders

    def create_entry_row(self, parent, label, value):
        row = ctk.CTkFrame(parent, fg_color="transparent")
        row.pack(padx=20, pady=(10, 0), anchor="w")

        ctk.CTkLabel(row, text=label, font=("Poppins", 14), text_color="black").pack(anchor="w")

        entry_frame = ctk.CTkFrame(row, fg_color="#F9F0E5", corner_radius=6)
        entry_frame.pack(fill="x", pady=(2, 5))

        entry = ctk.CTkEntry(entry_frame, width=300, height=35)
        entry.insert(0, value)
        entry.configure(state="disabled")
        entry.pack(side="left", padx=5)

        edit_button = ctk.CTkButton(
            entry_frame,
            text="",
            image=self.edit_icon,
            width=35,
            height=35,
            fg_color="transparent",
            hover_color="#E0E0E0",
            command=lambda: self.toggle_edit(entry, edit_button, label.lower())
        )
        edit_button.pack(side="left", padx=5)

    def toggle_edit(self, entry, edit_button, field):
        if entry.cget("state") == "disabled":
            entry.configure(state="normal")
            edit_button.configure(image=self.check_icon)
        else:
            new_value = entry.get()
            user_id = self.app.logged_in_user.get("userID", 0)
            if self.update_user_data(user_id, field, new_value):
                entry.configure(state="disabled")
                edit_button.configure(image=self.edit_icon)
            else:
                entry.delete(0, 'end')
                entry.insert(0, self.fetch_user_data(user_id)[["name", "username", "mobile", "email", "password"].index(field)])

    def fetch_user_data(self, user_id):
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor()
            query = """
                SELECT CONCAT(first_name, ' ', last_name) as name, 
                       username, phone_number, email, password 
                FROM users 
                WHERE userID = %s
            """
            cursor.execute(query, (user_id,))
            user_data = cursor.fetchone()
            conn.close()
            return user_data if user_data else ("N/A",)*5
        except Exception as e:
            print("Database Error:", e)
            return ("N/A",)*5

    def update_user_data(self, user_id, field, value):
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor()

            field_mapping = {
                "name": ("first_name", "last_name"),
                "username": "username",
                "mobile": "phone_number",
                "email": "email",
                "password": "password"
            }

            if field == "name":
                names = value.split(" ", 1)
                first_name = names[0]
                last_name = names[1] if len(names) > 1 else ""
                query = "UPDATE users SET first_name = %s, last_name = %s WHERE userID = %s"
                cursor.execute(query, (first_name, last_name, user_id))
            else:
                db_field = field_mapping.get(field)
                if db_field:
                    query = f"UPDATE users SET {db_field} = %s WHERE userID = %s"
                    cursor.execute(query, (value, user_id))

            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print("Update Error:", e)
            return False

    def logout(self):
        self.app.show_login_page()

    def show_order_history(self):
        # Clear current content
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # Show order history
        OrderHistory(self.content_frame, self.app, self.user).pack(fill="both", expand=True)

class TabFrame(ctk.CTkFrame):
    def __init__(self, parent, text):
        super().__init__(parent)
        self.border_frame = ctk.CTkFrame(self, fg_color="#F9F0E5", border_width=1, border_color="#E0E0E0", corner_radius=0)
        self.border_frame.pack(fill="both", expand=True)
        self.label = ctk.CTkLabel(self.border_frame, text=text, font=("Arial", 16), text_color="gray")
        self.label.pack(pady=10)

    def activate(self):
        self.border_frame.configure(border_color="#660033", fg_color="#FFFFFF")
        self.label.configure(font=("Arial", 16, "bold"), text_color="black")

    def deactivate(self):
        self.border_frame.configure(border_color="#E0E0E0", fg_color="#F5F5F5")
        self.label.configure(font=("Arial", 16), text_color="gray")
