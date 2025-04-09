import customtkinter as ctk
import mysql.connector
from dbconnection import DB_CONFIG
from utils import resize_image

class OrderTrackingPage(ctk.CTkFrame):
    def __init__(self, parent, app=None, user=None):
        super().__init__(parent)
        self.app = app
        self.configure(width=600, height=700, fg_color="transparent")

        self.user = user or {}
        self.user_id = self.user.get("id")
        self.username = self.user.get("username")

        self.image_refs = []

        self.configure(fg_color="transparent")

        self.create_header()
        self.create_order_section()

    def create_header(self):
        title = ctk.CTkLabel(
            self, text=f"Your Orders, {self.username}",
            font=("Poppins", 22, "bold"), text_color="black"
        )
        title.pack(pady=(20, 10))

    def create_order_section(self):
        self.orders_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.orders_frame.pack(fill="both", expand=True, padx=20, pady=10)

        self.load_orders()

    def get_orders(self):
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor(dictionary=True)

            cursor.execute("""
                SELECT items_list, total_price, status 
                FROM orders WHERE user_id = %s ORDER BY id DESC
            """, (self.user_id,))
            return cursor.fetchall()
        except mysql.connector.Error as err:
            print(f"DB Error: {err}")
            return []

    def load_orders(self):
        for widget in self.orders_frame.winfo_children():
            widget.destroy()

        orders = self.get_orders()
        if not orders:
            ctk.CTkLabel(self.orders_frame, text="No orders yet.",
                         font=("Arial", 14), text_color="gray").pack(pady=20)
            return

        for order in orders:
            self.create_order_card(order)

    def create_order_card(self, order):
        card = ctk.CTkFrame(
            self.orders_frame,
            fg_color="white",
            border_width=2,
            border_color="#F1D94B",
            width=430,
            height=160,
            corner_radius=10
        )
        card.pack(pady=10, padx=10, fill="x")
        card.pack_propagate(False)

        # --- Image Frame ---
        image_frame = ctk.CTkFrame(card, width=160, height=160, fg_color="white")
        image_frame.pack(side="left", fill="y")
        image_frame.pack_propagate(False)

        try:
            placeholder_img = resize_image((130, 130), "images/food_order_icon.png")
            self.image_refs.append(placeholder_img)
            ctk.CTkLabel(image_frame, image=placeholder_img, text="").pack(padx=10, pady=10)
        except Exception as e:
            print("Image Load Error:", e)
            ctk.CTkLabel(image_frame, text="🛒 Order", font=("Arial", 16)).pack(pady=20)

        # --- Details Frame ---
        details_frame = ctk.CTkFrame(card, fg_color="white")
        details_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        details_frame.pack_propagate(False)

        ctk.CTkLabel(details_frame, text=f"📝 {order['items_list']}",
                     font=("Arial", 12), text_color="black", wraplength=220,
                     justify="left").pack(anchor="w", pady=(0, 5))

        ctk.CTkLabel(details_frame, text=f"💲 Total: ${order['total_price']:.2f}",
                     font=("Arial", 12, "bold"), text_color="#E53935").pack(anchor="w")

        ctk.CTkLabel(details_frame, text=f"📦 Status: {order['status'].capitalize()}",
                     font=("Arial", 12), text_color="blue").pack(anchor="w", pady=(5, 0))

# Utility launcher

def open_order_tracking(parent, app=None, user=None):
    for widget in parent.winfo_children():
        widget.destroy()
    OrderTrackingPage(parent, app=app, user=user).pack(fill="both", expand=True)
