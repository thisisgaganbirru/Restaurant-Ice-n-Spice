import customtkinter as ctk
import mysql.connector
from dbconnection import DB_CONFIG
from utils import resize_image
from headerNav import NavigationHeader

class OrderTrackingPage(ctk.CTkFrame):
    def __init__(self, parent, app=None, user=None):
        super().__init__(parent)
        self.app = app
        self.user = user
        self.configure(width=600, height=700, fg_color="transparent")
        
        self.create_tracking_page()

    def create_tracking_page(self):
        # Main container with navigation header
        
        # Add navigation header
        NavigationHeader(self, app=self.app).pack(side="top", fill="x")

        # Main body frame
        self.body_frame = ctk.CTkFrame(self, fg_color="#EDEDED")
        self.body_frame.pack(fill="both", expand=True)

        try:
            self.bg_image = resize_image((900, 900), "images/loginbackground.png")
            bg_label = ctk.CTkLabel(self.body_frame, image=self.bg_image, text="")
            bg_label.place(relx=0, rely=0, relwidth=1, relheight=1)
        except Exception as e:
            print("[Background Error]", e)

        # Content frame
        content_frame = ctk.CTkFrame(self.body_frame, fg_color="#F9F0E5")
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Header with icon
        header_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        header_frame.pack(fill="x", pady=20)

        # Box icon and title
        try:
            box_icon = resize_image((30, 30), "images/box_icon.png")
            ctk.CTkLabel(header_frame, image=box_icon, text="").pack(side="left", padx=10)
        except:
            pass
        
        ctk.CTkLabel(
            header_frame,
            text="Your Orders",
            font=("Poppins", 24, "bold"),
            text_color="black"
        ).pack(side="left", padx=10)

        # Orders container
        orders_frame = ctk.CTkScrollableFrame(
            content_frame,
            fg_color="white",
            height=400
        )
        orders_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Get and display orders
        orders = self.get_orders()
        if orders:
            for order in orders:
                self.create_order_card(orders_frame, order)
        else:
            ctk.CTkLabel(
                orders_frame,
                text="No orders yet",
                font=("Poppins", 16, "italic"),
                text_color="gray"
            ).pack(pady=20)

    def create_order_card(self, parent, order):
        # Order card
        card = ctk.CTkFrame(
            parent,
            fg_color="white",
            border_width=1,
            border_color="#FFD700",
            height=100
        )
        card.pack(fill="x", pady=5, padx=10)
        card.pack_propagate(False)

        # Items list
        items_frame = ctk.CTkFrame(card, fg_color="white")
        items_frame.pack(fill="x", padx=10, pady=5)

        ctk.CTkLabel(
            items_frame,
            text="📝 Items:",
            font=("Poppins", 12, "bold"),
            text_color="black"
        ).pack(side="left")

        ctk.CTkLabel(
            items_frame,
            text=order['items_list'],
            font=("Poppins", 12),
            text_color="black"
        ).pack(side="left", padx=5)

        # Total and status
        info_frame = ctk.CTkFrame(card, fg_color="white")
        info_frame.pack(fill="x", padx=10)

        ctk.CTkLabel(
            info_frame,
            text=f"Total: ${order['total_price']:.2f}",
            font=("Poppins", 14, "bold"),
            text_color="black"
        ).pack(side="left")

        # Status with different colors and icons
        status_info = {
            'pending': {'color': '#FFA500', 'icon': '⏳'},
            'preparing': {'color': '#4169E1', 'icon': '👨‍🍳'},
            'ready for pickup': {'color': '#32CD32', 'icon': '✅'},
            'pending payment': {'color': '#FF4500', 'icon': '💰'},
            'delivered': {'color': '#228B22', 'icon': '🚚'}
        }

        status = order['status'].lower()
        status_data = status_info.get(status, {'color': '#000000', 'icon': '❓'})

        status_frame = ctk.CTkFrame(info_frame, fg_color="white")
        status_frame.pack(side="right")

        # Status icon and text
        ctk.CTkLabel(
            status_frame,
            text=f"{status_data['icon']} {status.capitalize()}",
            font=("Poppins", 12, "bold"),
            text_color=status_data['color']
        ).pack(side="right")

    def get_orders(self):
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor(dictionary=True)
            
            cursor.execute("""
                SELECT OrderID as id, Item_list as items_list, Total_price as total_price, 
                       Status as status, CreatedAT as created_at
                FROM `Order` 
                WHERE UserID = %s 
                ORDER BY CreatedAT DESC
            """, (self.user.get('userID'),))
            
            return cursor.fetchall()
        except Exception as e:
            print(f"Database Error: {e}")
            return []
        finally:
            if 'conn' in locals():
                conn.close()

# Utility launcher

def open_order_tracking(parent, app=None, user=None):
    for widget in parent.winfo_children():
        widget.destroy()
    OrderTrackingPage(parent, app=app, user=user).pack(fill="both", expand=True)
