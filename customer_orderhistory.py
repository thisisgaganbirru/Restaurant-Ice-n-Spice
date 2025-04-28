import customtkinter as ctk
from utils import resize_image
from customer_nav import NavigationHeader
import mysql.connector
from dbconnection import DB_CONFIG
import json
from decimal import Decimal

class OrderHistory(ctk.CTkFrame):
    def __init__(self, parent, app, user):
        super().__init__(parent)
        self.app = app
        self.user = user
        self.configure(fg_color="transparent")
        self.create_order_history_page()

    def create_order_history_page(self):
        # Main container
        main_frame = ctk.CTkFrame(self, fg_color="#F9F0E5")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Header
        NavigationHeader(main_frame, app=self.app).pack(fill="x")

        # Content frame
        self.content_frame = ctk.CTkFrame(main_frame, fg_color="#FFFFFF", corner_radius=15)
        self.content_frame.pack(fill="both", expand=True, padx=40, pady=40)

        # Title
        ctk.CTkLabel(
            self.content_frame,
            text="Order History",
            font=("Poppins", 24, "bold"),
            text_color="black"
        ).pack(pady=20)

        # Orders container
        self.orders_frame = ctk.CTkScrollableFrame(
            self.content_frame,
            fg_color="transparent",
            height=400
        )
        self.orders_frame.pack(fill="both", expand=True, padx=20)

        self.load_orders()

    def load_orders(self):
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor(dictionary=True)

            sql = """
            SELECT * FROM `Order`
            WHERE UserID = %s
            ORDER BY CreatedAT DESC
            """
            cursor.execute(sql, (self.user.get('userID'),))
            orders = cursor.fetchall()

            if not orders:
                self.show_no_orders_message()
            else:
                for order in orders:
                    self.create_order_card(order)

        except mysql.connector.Error as err:
            print(f"Database Error: {err}")
        finally:
            if 'conn' in locals():
                conn.close()

    def create_order_card(self, order):
        # Card container
        card = ctk.CTkFrame(
            self.orders_frame,
            fg_color="white",
            border_width=1,
            border_color="#F1D94B",
            height=120
        )
        card.pack(fill="x", pady=5, padx=10)
        card.pack_propagate(False)

        # Order details
        details_frame = ctk.CTkFrame(card, fg_color="transparent")
        details_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # Order ID and Date
        header_frame = ctk.CTkFrame(details_frame, fg_color="transparent")
        header_frame.pack(fill="x")
        
        # Update Order ID format
        formatted_id = f"#{order['OrderID']:07d}"
        ctk.CTkLabel(
            header_frame,
            text=f"Order {formatted_id}",
            font=("Poppins", 14, "bold")
        ).pack(side="left")

        ctk.CTkLabel(
            header_frame,
            text=order['CreatedAT'].strftime("%Y-%m-%d %H:%M"),
            font=("Poppins", 12),
            text_color="gray"
        ).pack(side="right")

        # Items list
        items = json.loads(order['Item_list'])
        items_text = ", ".join([f"{item['name']} (x{item['quantity']})" for item in items])
        
        ctk.CTkLabel(
            details_frame,
            text=items_text,
            font=("Poppins", 12),
            wraplength=400,
            justify="left"
        ).pack(fill="x", pady=5)

        # Bottom frame for status and reorder button
        bottom_frame = ctk.CTkFrame(details_frame, fg_color="transparent")
        bottom_frame.pack(fill="x")

        # Status label
        status_color = {
            'pending': '#FFA500',
            'preparing': '#4169E1',
            'ready for pickup': '#32CD32',
            'delivered': '#808080'
        }
        
        ctk.CTkLabel(
            bottom_frame,
            text=order['Status'],
            font=("Poppins", 12),
            text_color=status_color.get(order['Status'].lower(), 'black')
        ).pack(side="left")

        # Reorder button
        ctk.CTkButton(
            bottom_frame,
            text="Reorder",
            fg_color="#F1D94B",
            text_color="black",
            width=100,
            command=lambda o=order: self.reorder_items(o)
        ).pack(side="right")

    def reorder_items(self, order):
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

    def show_no_orders_message(self):
        ctk.CTkLabel(
            self.orders_frame,
            text="No orders found",
            font=("Poppins", 14),
            text_color="gray"
        ).pack(pady=20) 