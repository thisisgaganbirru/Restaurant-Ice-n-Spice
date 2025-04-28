import customtkinter as ctk
import mysql.connector
from dbconnection import DB_CONFIG
from utils import resize_image
from customer_nav import NavigationHeader
import json  # Importing json to parse JSON data

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
        NavigationHeader(self, app=self.app, user=self.user).pack(side="top", fill="x")

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
        content_frame = ctk.CTkFrame(self.body_frame, fg_color="#F9F0E5", width=550, height=550)
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Header with icon
        header_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        header_frame.pack(fill="x", pady=20)
        
        ctk.CTkLabel(
            header_frame,
            text="Your Orders",
            font=("Poppins", 24, "bold"),
            text_color="black"
        ).pack(anchor="center")

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
        # Order card - made taller to accommodate items
        card = ctk.CTkFrame(
            parent,
            fg_color="white",
            border_width=1,
            border_color="#FFD700",
            height=120  # Increased height
        )
        card.pack(fill="x", pady=5, padx=10)
        card.pack_propagate(False)
        
        # Create a container for the two-panel layout
        content_container = ctk.CTkFrame(card, fg_color="white")
        content_container.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Left frame (50%) - Items list
        left_frame = ctk.CTkFrame(content_container, fg_color="white")
        left_frame.pack(side="left", fill="both", expand=True)
        left_frame.pack_propagate(False)
        
        # left top frame - Total
        left_top = ctk.CTkFrame(left_frame, fg_color="white")
        left_top.pack(side="top", fill="both", expand=True)
        
        
        total_frame = ctk.CTkFrame(left_top, fg_color="white")
        total_frame.pack(anchor="w")
        
        ctk.CTkLabel(
            total_frame,
            text="Total:",
            font=("Poppins", 12, "bold"),
            text_color="black"
        ).pack(side="left")
        
        try:
            ctk.CTkLabel(
                total_frame,
                text=f"${order['total_price']:.2f}",
                font=("Poppins", 12, "bold"),
                text_color="black"
            ).pack(side="left", padx=5)
        except (KeyError, TypeError) as e:
            print(f"Error displaying price: {e}")
            ctk.CTkLabel(
                total_frame,
                text="$0.00",
                font=("Poppins", 12, "bold"),
                text_color="gray"
            ).pack(side="left", padx=5)
        
               # Right bottom frame - Status
        left_bottom = ctk.CTkFrame(left_frame, fg_color="white")
        left_bottom.pack(side="bottom", fill="both", expand=True)
           
        # Items header
        ctk.CTkLabel(
            left_bottom,
            text="Items:",
            font=("Poppins", 14, "bold"),
            text_color="black"
        ).pack(anchor="w", pady=(5, 0))
        
        # Parse items and display them
        try:
            # Assuming items_list is a JSON string or structured data
            items_list = json.loads(order['items_list'])  # Parse JSON string into a Python list
            items_frame = ctk.CTkFrame(left_bottom, fg_color="white")
            items_frame.pack(fill="x", anchor="w")
            
            for item in items_list:
                # Ensure the item has 'name' and 'quantity' keys
                if 'name' in item and 'quantity' in item:
                    ctk.CTkLabel(
                        items_frame,
                        text=f"• {item['name']} (x{item['quantity']})",
                        font=("Poppins", 12),
                        text_color="black"
                    ).pack(anchor="w")
        except (KeyError, AttributeError, json.JSONDecodeError) as e:
            print(f"Error parsing items: {e}")
            ctk.CTkLabel(
                left_frame,
                text="• Items data unavailable",
                font=("Poppins", 12),
                text_color="gray"
            ).pack(anchor="w")
        
        # Right frame (50%)
        right_frame = ctk.CTkFrame(content_container, fg_color="white")
        right_frame.pack(side="right", fill="both", expand=True)
        
        # Status with different colors and icons
        status_info = {
            'pending': {'color': '#FFA500', 'icon': '⏳', 'bg_color': '#FFE8C2'},
            'preparing': {'color': '#4169E1', 'icon': '👨‍🍳', 'bg_color': '#D1E5F9'},
            'ready for pickup': {'color': '#32CD32', 'icon': '✅', 'bg_color': '#D1F0C2'},
            'pending payment': {'color': '#FF4500', 'icon': '💰', 'bg_color': '#FFD1C2'},
            'delivered': {'color': '#228B22', 'icon': '🚚', 'bg_color': '#C2F0D1'},
            'cancelled': {'color': '#DC143C', 'icon': '❌', 'bg_color': '#FFCCCB'}
        }
        
        try:
            status = order.get('status', '').lower()
            status_data = status_info.get(status, {'color': '#000000', 'icon': '❓', 'bg_color': '#EEEEEE'})
            
            # Create a rounded rectangle status indicator
            status_indicator = ctk.CTkFrame(
                right_frame,
                fg_color=status_data['bg_color'],
                corner_radius=15
            )
            status_indicator.pack(side="left", padx=10, pady=(0, 10))
            
            # Status icon and text
            ctk.CTkLabel(
                status_indicator,
                text=f"{status_data['icon']} {status.capitalize()}",
                font=("Poppins", 12, "bold"),
                text_color=status_data['color'],
                fg_color="transparent"
            ).pack(padx=10, pady=5)
        except Exception as e:
            print(f"Error displaying status: {e}")
            ctk.CTkLabel(
                right_frame,
                text="Status unavailable",
                font=("Poppins", 12),
                text_color="gray"
            ).pack(side="left", padx=10, pady=(0, 10))

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