import customtkinter as ctk
from admin_nav import AdminNav
from dbconnection import DB_CONFIG
import mysql.connector
from PIL import Image
from datetime import datetime, timedelta
import os
import tkinter.messagebox as messagebox
from admin_stats import AdminStatsPage

class AdminOrdersPage(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.configure(fg_color="#F1E8DD")
        self.pack(fill="both", expand=True)
        
        # Create main container
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.pack(fill="both", expand=True)
        
        # Create layout
        self.create_header()
        self.create_orders_body()
        
    def create_header(self):
        # Nav on left
        AdminNav(self.main_container, app=self.app).pack(side="left", fill="y")
        
    def create_orders_body(self):
        # Body frame on right
        self.body_frame = ctk.CTkFrame(self.main_container, fg_color="#F1E8DD")
        self.body_frame.pack(side="right", fill="both", expand=True)

        # Stats Frame at top
        self.stats_frame = ctk.CTkFrame(self.body_frame, fg_color="transparent", height=200)
        self.stats_frame.pack(fill="x")
        self.stats_frame.pack_propagate(False)
        
        # Create AdminStatsPage instance for stats
        AdminStatsPage(self.stats_frame, self.app)
        
        # Bottom border line
        border_line = ctk.CTkFrame(self.body_frame, fg_color="#E0E0E0", height=2)
        border_line.pack(fill="x", padx=10)

        # Orders content frame
        self.orders_content = ctk.CTkFrame(self.body_frame, fg_color="transparent")
        self.orders_content.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Orders header
        header_frame = ctk.CTkFrame(self.orders_content, fg_color="transparent", height=50)
        header_frame.pack(fill="x", pady=(0, 10))
        header_frame.pack_propagate(False)
        
        ctk.CTkLabel(
            header_frame,
            text="Orders",
            font=("Poppins", 24, "bold"),
            text_color="#2B2B2B"
        ).pack(side="left")
        
        # Filter dropdown
        self.filter_var = ctk.StringVar(value="Pending")
        filter_menu = ctk.CTkOptionMenu(
            header_frame,
            values=["All Orders", "Pending", "Completed", "Cancelled"],
            variable=self.filter_var,
            font=("Poppins", 12),
            fg_color="white",
            text_color="black",
            button_color="#F1D94B",
            button_hover_color="#E5CE45",
            dropdown_fg_color="white",
            dropdown_text_color="black",
            width=120,
            height=32,
            command=self.filter_orders
        )
        filter_menu.pack(side="right")
        
        # Create scrollable frame for orders
        self.orders_frame = ctk.CTkScrollableFrame(
            self.orders_content,
            fg_color="transparent",
            height=400
        )
        self.orders_frame.pack(fill="both", expand=True)
        
        # Load orders
        self.load_orders()

    def create_orders_table(self):
        # Headers
        headers = ["OrderId", "Name", "Payment", "Type", "Status", "Total", "Action"]
        header_frame = ctk.CTkFrame(self.orders_content, fg_color="#F1D94B", height=35)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)
        
        # Configure columns
        for i in range(7):
            header_frame.grid_columnconfigure(i, weight=1)
            ctk.CTkLabel(
                header_frame,
                text=headers[i],
                font=("Poppins", 12, "bold"),
                text_color="black"
            ).grid(row=0, column=i, padx=10, pady=5, sticky="w")
        
        # Orders frame
        self.orders_frame = ctk.CTkScrollableFrame(
            self.orders_content,
            fg_color="transparent",
            height=400
        )
        self.orders_frame.pack(fill="both", expand=True)
        
        # Load orders
        self.load_orders()
        
    def load_orders(self):
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor(dictionary=True)
            
            query = """
                SELECT OrderID, UserName, payment_method, order_type, 
                       orderStatus, Total_price, Item_list
                FROM `Order`
                ORDER BY OrderID DESC
            """
            
            cursor.execute(query)
            orders = cursor.fetchall()
            conn.close()
            
            # Clear existing orders
            for widget in self.orders_frame.winfo_children():
                widget.destroy()
            
            # Create order rows
            for order in orders:
                self.create_order_row(order)
                
        except mysql.connector.Error as err:
            print(f"Database Error: {err}")
            
    def create_order_row(self, order):
        # Container for order and items
        container = ctk.CTkFrame(self.orders_frame, fg_color="transparent")
        container.pack(fill="x", pady=(0, 5))
        
        # Order card
        card = ctk.CTkFrame(
            container,
            fg_color="white",
            corner_radius=10,
            border_width=1,
            border_color="#E0E0E0"
        )
        card.pack(fill="x")
        
        # Top section with order details
        top_section = ctk.CTkFrame(card, fg_color="transparent")
        top_section.pack(fill="x", padx=15, pady=10)
        
        # Left side with order info
        left_info = ctk.CTkFrame(top_section, fg_color="transparent")
        left_info.pack(side="left", fill="both", expand=True)
        
        # Order ID and customer name
        id_name_frame = ctk.CTkFrame(left_info, fg_color="transparent")
        id_name_frame.pack(fill="x")
        
        ctk.CTkLabel(
            id_name_frame,
            text=f"#{order['OrderID']:08d}",
            font=("Poppins", 16, "bold"),
            text_color="#2B2B2B"
        ).pack(side="left", padx=(0, 10))
        
        ctk.CTkLabel(
            id_name_frame,
            text=order['UserName'],
            font=("Poppins", 14),
            text_color="#2B2B2B"
        ).pack(side="left")
        
        # Payment and Type
        payment_type_frame = ctk.CTkFrame(left_info, fg_color="transparent")
        payment_type_frame.pack(fill="x", pady=(5, 0))
        
        # Payment Method Dropdown
        payment_var = ctk.StringVar(value=order.get('payment_method', 'Cash'))
        payment_dropdown = ctk.CTkOptionMenu(
            payment_type_frame,
            values=["Cash", "Card"],
            variable=payment_var,
            font=("Poppins", 12),
            fg_color="transparent",
            text_color="black",
            button_color="transparent",
            button_hover_color="#F0F0F0",
            dropdown_fg_color="white",
            dropdown_hover_color="#F0F0F0",
            width=100,
            command=lambda x: self.update_payment_method(order['OrderID'], x)
        )
        payment_dropdown.pack(side="left", padx=(0, 15))
        payment_dropdown.configure(cursor="hand2")
        
        # Order Type Dropdown
        type_var = ctk.StringVar(value=order.get('order_type', 'Online'))
        type_dropdown = ctk.CTkOptionMenu(
            payment_type_frame,
            values=["Online", "Restaurant", "Mobile"],
            variable=type_var,
            font=("Poppins", 12),
            fg_color="transparent",
            text_color="black",
            button_color="transparent",
            button_hover_color="#F0F0F0",
            dropdown_fg_color="white",
            dropdown_hover_color="#F0F0F0",
            width=120,
            command=lambda x: self.update_order_type(order['OrderID'], x)
        )
        type_dropdown.pack(side="left")
        type_dropdown.configure(cursor="hand2")
        
        # Right side with status and actions
        right_info = ctk.CTkFrame(top_section, fg_color="transparent")
        right_info.pack(side="right")
        
        # Status and Total in one row
        status_total_frame = ctk.CTkFrame(right_info, fg_color="transparent")
        status_total_frame.pack(fill="x")
        
        # Status Dropdown
        status_var = ctk.StringVar(value=order.get('orderStatus', 'Pending').title())
        status_dropdown = ctk.CTkOptionMenu(
            status_total_frame,
            values=["Pending", "Preparing", "Ready", "Delivered", "Cancelled"],
            variable=status_var,
            font=("Poppins", 12),
            fg_color="#FFF3E0",
            text_color="#FFA000",
            button_color="#FFF3E0",
            button_hover_color="#FFE0B2",
            dropdown_fg_color="white",
            dropdown_hover_color="#FFF3E0",
            width=120,
            command=lambda x: self.update_order_status_direct(order['OrderID'], x)
        )
        status_dropdown.pack(side="left", padx=(0, 15))
        
        # Total amount
        try:
            total = float(order['Total_price'])
            total_text = f"${total:.2f}"
        except:
            total_text = "$0.00"
            
        ctk.CTkLabel(
            status_total_frame,
            text=total_text,
            font=("Poppins", 16, "bold"),
            text_color="#2B2B2B"
        ).pack(side="right")
        
        # Cancel button
        ctk.CTkButton(
            right_info,
            text="Cancel Order",
            font=("Poppins", 12),
            fg_color="#FF6B6B",
            hover_color="#FF5252",
            text_color="white",
            width=120,
            height=28,
            command=lambda: self.cancel_order(order['OrderID'])
        ).pack(pady=(5, 0))
        
        # Items list (initially hidden)
        self.items_frame = None
        
        def toggle_items(event=None):
            if self.items_frame is None:
                # Create items frame
                self.items_frame = ctk.CTkFrame(card, fg_color="white")
                self.items_frame.pack(fill="x", padx=15, pady=(0, 10))
                
                # Add separator line
                separator = ctk.CTkFrame(self.items_frame, fg_color="#E0E0E0", height=1)
                separator.pack(fill="x", pady=(0, 10))
                
                try:
                    import json
                    items = json.loads(order['Item_list'])
                    for item in items:
                        item_frame = ctk.CTkFrame(self.items_frame, fg_color="transparent")
                        item_frame.pack(fill="x", pady=2)
                        
                        ctk.CTkLabel(
                            item_frame,
                            text=f"{item['name']}",
                            font=("Poppins", 12),
                            text_color="#2B2B2B"
                        ).pack(side="left")
                        
                        ctk.CTkLabel(
                            item_frame,
                            text=f"x{item.get('quantity', 1)}",
                            font=("Poppins", 12),
                            text_color="gray"
                        ).pack(side="right")
                except:
                    ctk.CTkLabel(
                        self.items_frame,
                        text="No items to display",
                        font=("Poppins", 12),
                        text_color="gray"
                    ).pack(anchor="w", pady=5)
            else:
                self.items_frame.destroy()
                self.items_frame = None
        
        # Bind click event to the entire card
        card.bind("<Button-1>", toggle_items)
        for widget in card.winfo_children():
            widget.bind("<Button-1>", toggle_items)
        
    def cancel_order(self, order_id):
        if messagebox.askyesno("Confirm Cancellation", "Are you sure you want to cancel this order?"):
            try:
                conn = mysql.connector.connect(**DB_CONFIG)
                cursor = conn.cursor()
                
                cursor.execute("""
                    UPDATE `Order` 
                    SET orderStatus = 'cancelled',
                        statusUpdateAt = CURRENT_TIMESTAMP
                    WHERE OrderID = %s
                """, (order_id,))
                
                conn.commit()
                conn.close()
                
                messagebox.showinfo("Success", "Order cancelled successfully")
                self.load_orders()
                
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Failed to cancel order: {err}")
                
    def filter_orders(self, value=None):
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor(dictionary=True)
            
            query = """
                SELECT OrderID, UserName, payment_method, order_type, 
                       orderStatus, Total_price, Item_list
                FROM `Order`
            """
            
            if value and value != "All Orders":
                query += " WHERE orderStatus = %s"
                cursor.execute(query, (value.lower(),))
            else:
                cursor.execute(query)
                
            orders = cursor.fetchall()
            conn.close()
            
            # Clear existing orders
            for widget in self.orders_frame.winfo_children():
                widget.destroy()
            
            # Create order rows
            for order in orders:
                self.create_order_row(order)
                
        except mysql.connector.Error as err:
            print(f"Database Error: {err}")

    def update_payment_method(self, order_id, payment_method):
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor()
            
            cursor.execute("""
                UPDATE `Order` 
                SET payment_method = %s
                WHERE OrderID = %s
            """, (payment_method, order_id))
            
            conn.commit()
            conn.close()
            
        except mysql.connector.Error as err:
            print(f"Database Error: {err}")

    def update_order_type(self, order_id, order_type):
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor()
            
            cursor.execute("""
                UPDATE `Order` 
                SET order_type = %s
                WHERE OrderID = %s
            """, (order_type, order_id))
            
            conn.commit()
            conn.close()
            
        except mysql.connector.Error as err:
            print(f"Database Error: {err}")

    def update_order_status_direct(self, order_id, new_status):
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor()
            
            cursor.execute("""
                UPDATE `Order` 
                SET orderStatus = %s,
                    statusUpdateAt = CURRENT_TIMESTAMP
                WHERE OrderID = %s
            """, (new_status.lower(), order_id))
            
            conn.commit()
            conn.close()
            
            # Refresh orders display
            self.load_orders()
            
        except mysql.connector.Error as err:
            print(f"Database Error: {err}")

    def cancel_product(self, order_id):
        # Implement product cancellation
        pass

    def send_message(self, order_id):
        # Implement message sending
        pass 