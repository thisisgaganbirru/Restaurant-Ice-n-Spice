import customtkinter as ctk
from admin_stats import AdminStatsPage
from dbconnection import DB_CONFIG
import mysql.connector
from PIL import Image, ImageTk
from datetime import datetime, timedelta
import os
import tkinter.messagebox as messagebox
from tkinter import StringVar
import json
import threading
from adminreport_download import OrdersOnlyExporter  # Import the missing function
from typing import List, Dict, Any, Optional, Callable

class AdminOrdersPage(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.configure(fg_color="#F1E8DD")
        self.pack(fill="both", expand=True)
        
        # Stats Frame at top
        self.stats_frame = ctk.CTkFrame(self, fg_color="transparent", height=200)
        self.stats_frame.pack(fill="x")
        self.stats_frame.pack_propagate(False)
        
        # Create AdminStatsPage instance for stats
        AdminStatsPage(self.stats_frame, self.app)
        
        # Bottom border line
        border_line = ctk.CTkFrame(self, fg_color="grey", height=2)
        border_line.pack(fill="x", padx=2)
        
        # Orders Container
        self.orders_container = ctk.CTkFrame(self, fg_color="transparent")
        self.orders_container.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Initialize variables
        self.expanded_order_id = None
        self.items_container = None
        self.filter_var = StringVar(value="pending")
        
        # Create Orders UI Structure
        self._create_orders_header()
        self._create_filter_bar()
        self._create_orders_list()
        self._create_footer()
        
        # Load initial data
        self.after(100, self.load_orders)
        
    def _create_orders_header(self):
                
        header_frame = ctk.CTkFrame(self.orders_container, fg_color="#F1D94B", height=50)
        header_frame.pack(fill="x",  padx=5, pady=10)
        header_frame.pack_propagate(False)
        
        # Orders title
        ctk.CTkLabel(
            header_frame,
            text="Admin Orders Dashboard",
            font=("Poppins", 24, "bold"),
            text_color="black"
        ).pack(side="left", padx=10)
        # Orders count
        self.orders_count = ctk.CTkLabel(
            header_frame,
            text="",
            font=("Poppins", 12),
            text_color="#757575"
        )
        self.orders_count.pack(side="left", padx=(10, 0))
        
    def _create_filter_bar(self):
        filter_frame = ctk.CTkFrame(self.orders_container, fg_color="transparent")
        filter_frame.pack(fill="x", pady=(10, 10))
        
        # Left side - Filters
        filter_left = ctk.CTkFrame(filter_frame, fg_color="transparent")
        filter_left.pack(side="left")
        
        # Status filter
        ctk.CTkLabel(
            filter_left,
            text="Status:",
            font=("Poppins", 12),
            text_color="#2B2B2B"
        ).pack(side="left", padx=(0, 5))
        
        status_menu = ctk.CTkOptionMenu(
            filter_left,
            values=["All Orders", "pending", "ready for pickup", "delivered", "cancelled"],
            variable=self.filter_var,
            font=("Poppins", 12),
            fg_color="white",
            text_color="#2B2B2B",
            button_color="#F1D94B",
            button_hover_color="#E5CE45",
            dropdown_fg_color="white",
            width=160,
            height=32,
            command=self.filter_orders
        )
        status_menu.pack(side="left", padx=5)
        
        # Right side - Search
        search_frame = ctk.CTkFrame(filter_frame, fg_color="transparent")
        search_frame.pack(side="right")
        
        self.search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="Search orders...",
            font=("Poppins", 12),
            width=200,
            height=32
        )
        self.search_entry.pack(side="left", padx=5)
        
        search_button = ctk.CTkButton(
            search_frame,
            text="Search",
            font=("Poppins", 12),
            fg_color="#F1D94B",
            hover_color="#E5CE45",
            text_color="#2B2B2B",
            width=100,
            height=32,
            command=self.search_orders
        )
        search_button.pack(side="left", padx=5)
        
    def _create_orders_list(self):
        # Header
        self.list_header = ctk.CTkFrame(self.orders_container, fg_color="#F1D94B", height=50)
        self.list_header.pack(fill="x")
        self.list_header.pack_propagate(False)
        
        # Configure grid for header
        self.list_header.grid_columnconfigure((0, 1, 2, 3, 4, 5, 6), weight=1, uniform="equal")
        self.list_header.grid_rowconfigure(0, weight=1)
        
        # Header columns
        headers = ["Order ID", "Customer", "Payment", "Type", "Status", "Total", "Actions"]
        for i, header in enumerate(headers):
            ctk.CTkLabel(
                self.list_header,
                text=header,
                font=("Poppins", 12, "bold"), height=40,
                text_color="#2B2B2B"
            ).grid(row=0, column=i, padx=8, sticky="ew")
        
        # Scrollable orders frame
        self.orders_frame = ctk.CTkScrollableFrame(
            self.orders_container,
            fg_color="transparent",
            corner_radius=0
        )
        self.orders_frame.pack(fill="both", expand=True)
        
    def _create_footer(self):
        self.footer = ctk.CTkFrame(self.orders_container, fg_color="transparent", height=50)
        self.footer.pack(fill="x", pady=(10, 0))
        self.footer.pack_propagate(False)
        
        # Refresh button
        refresh_btn = ctk.CTkButton(
            self.footer,
            text="Refresh",
            font=("Poppins", 12),
            fg_color="#2196F3",
            hover_color="#1976D2",
            width=100,
            height=32,
            command=self.load_orders
        )
        refresh_btn.pack(side="left", padx=5)
        
        # Export button
        export_btn = ctk.CTkButton(
            self.footer,
            text="Export",
            font=("Poppins", 12),
            fg_color="#4CAF50",
            hover_color="#388E3C",
            width=100,
            height=32,
            command=self.export_orders
        )
        export_btn.pack(side="right", padx=5)

    def search_orders(self):
        search_term = self.search_entry.get().strip()
        if search_term:
            self.load_orders(search_term)
            
    def export_orders(self):
        """Export orders using the OrdersOnlyExporter."""
        try:
            # Create dictionaries to store UI data
            payment_info = {}  # OrderID -> payment method
            order_type_info = {}  # OrderID -> order type
            
            # Collect data from UI
            # Example code (modify according to your UI implementation):
            # for order in self.orders_list:
            #     payment_info[order.id] = order.payment_method
            #     order_type_info[order.id] = order.order_type
            
            # Create an instance of OrdersOnlyExporter
            exporter = OrdersOnlyExporter()
            
            # Call the export_orders method with the collected UI data
            exporter.export_orders(
                time_filter="All Time",
                payment_info=payment_info, 
                order_type_info=order_type_info
            )
            
            # Show a success message to the user
            messagebox.showinfo("Export Successful", "Orders have been exported successfully!")
        except Exception as e:
            # Handle any errors that occur during the export process
            error_message = f"Failed to export orders: {str(e)}"
            print(error_message)  # Log the error for debugging
            messagebox.showerror("Export Failed", error_message)

    def _create_order_card(self, parent, order_data):
        card = ctk.CTkFrame(parent, fg_color="white", corner_radius=10, width=800, height=80)
        card.pack(fill="x", padx=(0,5), pady=5)
        
        # Extract order data
        order_id = order_data.get('OrderID', 0)
        user_name = order_data.get('UserName', 'Unknown')
        payment_method = order_data.get('Status', 'Cash')
        order_type = order_data.get('Type', 'Online')
        order_status = order_data.get('orderStatus', 'pending')
        total = float(order_data.get('Total_price', 0))
        
        # Create items frame with consistent dimensions
        items_frame = ctk.CTkFrame(
            parent,
            fg_color="#F8F5EF",
            corner_radius=10,
            border_width=1,
            border_color="#E0E0E0",
            width=800,  # Set a fixed width
            height=80  # Set a fixed height
        )
        items_frame.pack_propagate(False)  # Prevent resizing based on content
        parent.items_frame = items_frame
        
        # Parse items data
        items_str = order_data.get('Item_list', '[]')
        try:
            if isinstance(items_str, str):
                items = json.loads(items_str)
                print(f"Successfully parsed items for OrderID {order_id}: {items}")
            else:
                print(f"Item_list is not a string for OrderID {order_id}")
                items = []
            items_frame.items = items
        except Exception as e:
            print(f"Error parsing Item_list for OrderID {order_id}: {e}")
            print(f"Raw Item_list: {items_str}")
            items_frame.items = []
        
        # Main card setup
        card.grid_columnconfigure((0, 1, 2, 3, 4, 5, 6), weight=1, uniform="equal")
        card.grid_rowconfigure(0, weight=1)
        
        # Save order_id to card for reference
        card.order_id = order_id
        
        # Build card sections
        self._create_order_id_section(card, order_id)
        self._create_name_section(card, user_name)
        self._create_payment_section(card, payment_method, order_id)
        self._create_type_section(card, order_type, order_id)
        self._create_status_section(card, order_status, order_id)
        self._create_price_section(card, total)
        self._create_action_section(card, order_id)
        
        return card

    def _create_order_id_section(self, parent, order_id):
        id_frame = ctk.CTkFrame(parent, fg_color="transparent")
        id_frame.grid(row=0, column=0, padx=5, pady=8, sticky="ew")
        
        id_label = ctk.CTkLabel(
            id_frame,
            text=f"#{order_id:08d}",
            font=("Poppins", 12),
            text_color="#2B2B2B",
            cursor="hand2"
        )
        id_label.pack(anchor="center", padx=5)
        
        # Make the label clickable to expand/collapse items
        id_label.bind("<Button-1>", lambda e: self.toggle_order_items(order_id))

    def _create_name_section(self, parent, user_name):
        name_frame = ctk.CTkFrame(parent, fg_color="transparent")
        name_frame.grid(row=0, column=1, padx=5, pady=8, sticky="ew")
        
        ctk.CTkLabel(
            name_frame,
            text=user_name,
            font=("Poppins", 12),
            text_color="#2B2B2B"
        ).pack(anchor="center", padx=5)

    def _create_payment_section(self, parent, payment_method, order_id):
        payment_frame = ctk.CTkFrame(parent, fg_color="transparent")
        payment_frame.grid(row=0, column=2, padx=5, pady=8, sticky="ew")
        
        payment_var = StringVar(value=payment_method)
        payment_dropdown = ctk.CTkOptionMenu(
            payment_frame,
            values=["Cash", "Card"],
            variable=payment_var,
            font=("Poppins", 12),
            fg_color="white",
            text_color="#2B2B2B",
            button_color="white",
            button_hover_color="#F5F5F5",
            dropdown_fg_color="white",
            width=120,
            height=32,
            command=lambda v: self.update_order_field(order_id, "payment", v)
        )
        payment_dropdown.pack(anchor="center", padx=5)

    def _create_type_section(self, parent, order_type, order_id):
        type_frame = ctk.CTkFrame(parent, fg_color="transparent")
        type_frame.grid(row=0, column=3, padx=5, pady=8, sticky="ew")
        
        type_var = StringVar(value=order_type)
        type_dropdown = ctk.CTkOptionMenu(
            type_frame,
            values=["Online", "Restaurant"],
            variable=type_var,
            font=("Poppins", 12),
            fg_color="white",
            text_color="#2B2B2B",
            button_color="white",
            button_hover_color="#F5F5F5",
            dropdown_fg_color="white",
            width=120,
            height=32,
            command=lambda v: self.update_order_field(order_id, "type", v)
        )
        type_dropdown.pack(anchor="center", padx=5)

    def _create_status_section(self, parent, order_status, order_id):
        status_frame = ctk.CTkFrame(parent, fg_color="transparent")
        status_frame.grid(row=0, column=4, padx=5, pady=8, sticky="ew")
        
        # Create a horizontal container for the status indicator and dropdown
        status_container = ctk.CTkFrame(status_frame, fg_color="transparent")
        status_container.pack(anchor="w", fill="x")
        
        # Status indicator - vertical bar
        status_indicator = ctk.CTkFrame(
            status_container, 
            width=4,
            height=32,
            corner_radius=2
        )
        status_indicator.pack(side="left", padx=(5, 10))
        
        # Status dropdown
        status_var = StringVar(value=order_status)
        status_dropdown = ctk.CTkOptionMenu(
            status_container,
            values=["pending", "ready for pickup", "delivered", "cancelled"],
            variable=status_var,
            font=("Poppins", 12),
            fg_color="white",
            text_color="#2B2B2B",
            button_color="#F1D94B",
            button_hover_color="#E5CE45",
            dropdown_fg_color="white",
            width=140,
            height=32,
            command=lambda v: self.update_order_field(order_id, "status", v)
        )
        status_dropdown.pack(side="left")
        
        # Initialize status color
        self._update_status_indicator(status_indicator, order_status)

    def _create_price_section(self, parent, total):
        price_frame = ctk.CTkFrame(parent, fg_color="transparent")
        price_frame.grid(row=0, column=5, padx=5, pady=8, sticky="ew")
        
        ctk.CTkLabel(
            price_frame,
            text=f"${total:.2f}",
            font=("Poppins", 12, "bold"),
            text_color="#2B2B2B"
        ).pack(anchor="center", padx=5)

    def _create_action_section(self, parent, order_id):
        actions_frame = ctk.CTkFrame(parent, fg_color="transparent")
        actions_frame.grid(row=0, column=6, padx=5, pady=8, sticky="ew")
        
        # Action dropdown
        action_var = StringVar(value="Actions")
        action_dropdown = ctk.CTkOptionMenu(
            actions_frame,
            values=["Cancel Order", "Mark as Done"],
            variable=action_var,
            font=("Poppins", 12),
            fg_color="white",
            text_color="#2B2B2B",
            button_color="#F44336",
            button_hover_color="#D32F2F",
            dropdown_fg_color="white",
            width=100,
            height=32,
            command=lambda v: self._handle_action(v, order_id)
        )
        action_dropdown.pack(anchor="center", padx=5)

    def _update_status_indicator(self, indicator, status):
        if status == "pending":
            color = "#FF5722"
        elif status == "ready for pickup":
            color = "#2196F3"
        elif status == "delivered":
            color = "#4CAF50"
        else:
            color = "#F44336"
        indicator.configure(fg_color=color)

    def _handle_action(self, value, order_id):
        if value == "Cancel Order":
            if messagebox.askyesno("Confirm Cancellation", "Are you sure you want to cancel this order?"):
                self.update_order_field(order_id, "status", "cancelled")
        elif value == "Mark as Done":
            self.update_order_field(order_id, "status", "delivered")

    def show_items(self, parent_frame, items):
        """Display order items in the parent frame"""
        # Clear the parent frame
        for widget in parent_frame.winfo_children():
            widget.destroy()
        
        # Debug information
        print(f"Items to display: {items}")
        print(f"Items type: {type(items)}")
        
        # Create items list
        if not items:
            ctk.CTkLabel(
                parent_frame,
                text="No items to display",
                font=("Poppins", 12),
                text_color="#757575"
            ).pack(anchor="w", padx=15, pady=10)
        else:
            # Create a frame for items
            # Items rows
            for i, item in enumerate(items):
                item_frame = ctk.CTkFrame(parent_frame, fg_color="grey", corner_radius=10)
                item_frame.pack(fill="x", padx=15, pady=(0, 5))
                
                # Alternate background color for rows
                bg_color = "#F5F5F5" if i % 2 == 0 else "#FFFFFF"
                item_frame.configure(fg_color=bg_color)
                
                # Print item for debugging
                print(f"Item {i}: {item}")
                
                # Get item details
                # For debugging, print all keys in the item
                if isinstance(item, dict):
                    print(f"Item keys: {list(item.keys())}")
                
                # Get item details with more robust handling
                name = None
                quantity = None
                
                if isinstance(item, dict):
                    # Try to get name
                    if 'name' in item:
                        name = item['name']
                    elif 'itemName' in item:
                        name = item['itemName']
                    elif 'item_name' in item:
                        name = item['item_name']
                    
                    # Try to get quantity
                    if 'quantity' in item:
                        quantity = item['quantity']
                    elif 'Quantity' in item:
                        quantity = item['Quantity']
                    elif 'qty' in item:
                        quantity = item['qty']
                    
                
                # Set defaults if not found
                if name is None:
                    name = "Unknown Item"
                if quantity is None:
                    quantity = 1
                
                # Item name with left alignment
                ctk.CTkLabel(
                    item_frame,
                    text=name,
                    font=("Poppins", 12),
                    text_color="#2B2B2B"
                ).pack(side="left")
                
                # Item quantity with left alignment
                ctk.CTkLabel(
                    item_frame,
                    text=f"x{quantity}",
                    font=("Poppins", 12),
                    text_color="#757575"
                ).pack(side="left")

    def toggle_order_items(self, order_id):
        """Toggle the visibility of order items"""
        # Find the container frame for this order
        container = None
        for widget in self.orders_frame.winfo_children():
            if hasattr(widget, 'order_id') and widget.order_id == order_id:
                container = widget
                break
        
        if not container:
            print(f"Container not found for OrderID {order_id}")
            return
            
        # Check if we're clicking the already expanded order
        if self.expanded_order_id == order_id:
            # Collapse the current order
            if hasattr(container, 'items_frame'):
                container.items_frame.pack_forget()
            self.expanded_order_id = None
        else:
            # Collapse any previously expanded order
            if self.expanded_order_id is not None:
                for widget in self.orders_frame.winfo_children():
                    if hasattr(widget, 'order_id') and widget.order_id == self.expanded_order_id:
                        if hasattr(widget, 'items_frame'):
                            widget.items_frame.pack_forget()
                        break
            
            # Expand the new order
            self._populate_items_frame(container, order_id)
            if hasattr(container, 'items_frame'):
                container.items_frame.pack(fill="x", pady=(0, 5))
            self.expanded_order_id = order_id
    
    def _populate_items_frame(self, container, order_id):
        """Populate the items frame with order items"""
        # Get items directly from the container's items_frame
        if hasattr(container, 'items_frame') and hasattr(container.items_frame, 'items'):
            items = container.items_frame.items
            
            # If items is a string (JSON), parse it
            if isinstance(items, str):
                try:
                    items = json.loads(items)
                    print(f"Parsed items from JSON: {items}")
                except Exception as e:
                    print(f"Error parsing items JSON: {e}")
                    items = []
            
            # Display the items
            self.show_items(container.items_frame, items)
        else:
            print(f"Items frame not found for OrderID {order_id}")

    def update_order_field(self, order_id, field, value):
        """Update an order field in the database"""
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor()
            
            # Map field to database column
            field_map = {
                "payment": "Status",  # Payment field maps to Status column
                "type": "Type",      # Type field maps to Type column
                "status": "orderStatus"  # Status field maps to orderStatus column
            }
            
            if field in field_map:
                column = field_map[field]
                # Update timestamp for status changes
                if field == "status":
                    cursor.execute(f"""
                        UPDATE `Order` 
                        SET {column} = %s,
                            statusUpdateAt = CURRENT_TIMESTAMP
                        WHERE OrderID = %s
                    """, (value, order_id))
                else:
                    cursor.execute(f"""
                        UPDATE `Order` 
                        SET {column} = %s
                        WHERE OrderID = %s
                    """, (value, order_id))
                
                conn.commit()
                conn.close()
                
                # Refresh orders with less visual disruption
                # Only refresh if the current filter allows this order to be visible
                current_filter = self.filter_var.get()
                if current_filter == "All Orders" or current_filter == value or (field != "status"):
                    # No need to reload everything, just update the UI element
                    pass
                else:
                    # If status changed and doesn't match filter, refresh the list
                    self.load_orders()
                    
        except mysql.connector.Error as err:
            print(f"Database Error: {err}")
            messagebox.showerror("Error", f"Failed to update order: {err}")
    
    def filter_orders(self, value=None):
        """Filter orders by status"""
        self.load_orders()

    def load_orders(self, search_term=None):
        """Load orders from database with threading to avoid UI freezing"""
        # Show loading indicator
        self._show_loading()
        
        # Start a thread to fetch data
        threading.Thread(target=self._fetch_orders_data, args=(search_term,), daemon=True).start()
    
    def _show_loading(self):
        """Show loading indicator in orders frame"""
        # Clear existing orders
        for widget in self.orders_frame.winfo_children():
            widget.destroy()
        
        # Show loading label
        loading_frame = ctk.CTkFrame(self.orders_frame, fg_color="transparent")
        loading_frame.pack(fill="x", pady=20)
        
        ctk.CTkLabel(
            loading_frame,
            text="Loading orders...",
            font=("Poppins", 12),
            text_color="#757575"
        ).pack()
    
    def _fetch_orders_data(self, search_term):
        """Fetch orders data from database in a separate thread"""
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor(dictionary=True)
            
            # Get orders based on filter
            status_filter = self.filter_var.get()
            if status_filter == "All Orders":
                query = """
                    SELECT OrderID, UserID, UserName, Item_list, 
                           Total_price, Status, CreatedAT, orderStatus, statusUpdateAt
                    FROM `Order`
                    ORDER BY OrderID DESC
                """
                cursor.execute(query)
            else:
                query = """
                    SELECT OrderID, UserID, UserName, Item_list, 
                           Total_price, Status, CreatedAT, orderStatus, statusUpdateAt
                    FROM `Order`
                    WHERE orderStatus = %s
                    ORDER BY OrderID DESC
                """
                cursor.execute(query, (status_filter,))
            
            orders = cursor.fetchall()
            conn.close()
            
            # Update UI in main thread
            self.after(0, lambda: self._update_orders_ui(orders))
            
        except mysql.connector.Error as err:
            print(f"Database Error: {err}")
            # Update UI in main thread to show error
            self.after(0, lambda: self._show_error(str(err)))
    
    def _update_orders_ui(self, orders):
        """Update the UI with fetched orders data"""
        # Clear existing orders
        for widget in self.orders_frame.winfo_children():
            widget.destroy()
        
        # Reset expanded items tracking
        self.expanded_order_id = None
        
        # Update order count
        self.orders_count.configure(text=f"({len(orders)})")
        
        # No orders message if empty
        if not orders:
            empty_frame = ctk.CTkFrame(self.orders_frame, fg_color="transparent")
            empty_frame.pack(fill="x", pady=20)
            
            ctk.CTkLabel(
                empty_frame,
                text="No orders found",
                font=("Poppins", 12),
                text_color="#757575"
            ).pack()
            return
        
        # Create order cards
        for order in orders:
            # Container for the order card and its expandable items
            container_frame = ctk.CTkFrame(self.orders_frame, fg_color="transparent")
            container_frame.pack(fill="x", pady=5)
            
            # Store the order ID in the container for reference
            container_frame.order_id = order.get('OrderID', 0)
            
            # Order card
            order_card = self._create_order_card(container_frame, order)
            order_card.pack(fill="x")

    def _show_error(self, error_message):
        """Show error message in orders frame"""
        # Clear existing content
        for widget in self.orders_frame.winfo_children():
            widget.destroy()
        
        # Show error message
        error_frame = ctk.CTkFrame(self.orders_frame, fg_color="transparent")
        error_frame.pack(fill="x", pady=20)
        
        ctk.CTkLabel(
            error_frame,
            text="Error loading orders",
            font=("Poppins", 12, "bold"),
            text_color="#F44336"
        ).pack(pady=(0, 5))
        
        ctk.CTkLabel(
            error_frame,
            text=error_message,
            font=("Poppins", 12),
            text_color="#757575"
        ).pack()
        
        # Retry button
        retry_btn = ctk.CTkButton(
            error_frame,
            text="Retry",
            font=("Poppins", 12),
            fg_color="#F1D94B",
            hover_color="#E5CE45",
            text_color="#2B2B2B",
            width=100,
            height=32,
            corner_radius=15,
            command=self.load_orders
        )
        retry_btn.pack(pady=10)