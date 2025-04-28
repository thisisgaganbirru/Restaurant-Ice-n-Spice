import customtkinter as ctk
from utils import resize_image
from customer_nav import NavigationHeader
from decimal import Decimal
import mysql.connector
from dbconnection import DB_CONFIG
from customer_ordertracking import OrderTrackingPage
import os
import json

class OrderPage(ctk.CTkFrame):
    def __init__(self, parent, app, user, cart):
        super().__init__(parent)
        self.app = app
        self.user = user
        self.cart = cart
        self.image_refs = []  # Initialize image_refs list
        self.configure(width=600, height=700, fg_color="transparent")
        
        
        self.create_header()
        self.create_order_body()

    def create_header(self):
        NavigationHeader(self, app=self.app, user=self.user).pack(side="top", fill="x")

    def create_order_body(self):
        self.body_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.body_frame.pack(fill="both", expand=True)

        # Background
        self.bg_image = resize_image((800, 800), "images/backg.jpg")
        bg_label = ctk.CTkLabel(self.body_frame, image=self.bg_image, text="")
        bg_label.pack(fill="both", expand=True)

        # Main content frame
        self.main_frame = ctk.CTkFrame(self.body_frame, fg_color="#F9F0E5",width=500, height=600)
        self.main_frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.9, relheight=0.9)

        # Create header
        self.create_header_section()
        
        # Create content area
        self.create_content_area()

    def create_header_section(self):
        header_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent", height=50)
        header_frame.pack(fill="x", padx=20, pady=(20,10))
        header_frame.pack_propagate(False)

        # Back arrow with square background
        arrow_frame = ctk.CTkFrame(header_frame, width=40, height=40, fg_color="transparent")
        arrow_frame.pack(side="left")
        arrow_frame.pack_propagate(False)

        try:
            arrow_img = resize_image((30, 30), "images/arrow.png")
            arrow_btn = ctk.CTkButton(
                arrow_frame,
                image=arrow_img,
                text="",
                width=40,
                height=40,
                corner_radius=0,
                fg_color="transparent",
                hover_color="#D5CCC0",
                command=lambda: self.app.show_customer_dashboard(self.user) if hasattr(self.app, 'show_customer_dashboard') else print("Customer dashboard navigation not implemented")
            )
            self.image_refs.append(arrow_img)  # Keep reference to prevent garbage collection
            arrow_btn.place(relx=0.5, rely=0.5, anchor="center")
        except Exception as e:
            print("Arrow Image Error:", e)
            # Fallback to text button if image fails to load
            arrow_btn = ctk.CTkButton(
                arrow_frame,
                text="←",
                width=40,
                height=40,
                corner_radius=0,
                fg_color="#E5DCD0",
                hover_color="#D5CCC0",
                command=lambda: self.app.show_customer_dashboard(self.user) if hasattr(self.app, 'show_customer_dashboard') else print("Customer dashboard navigation not implemented")
            )
            arrow_btn.place(relx=0.5, rely=0.5, anchor="center")

        # Title
        name = self.user.get("first_name", "User")
        title_text = f"{name}'s Cart"
        ctk.CTkLabel(
            header_frame,
            text=title_text,
            font=("Poppins", 18, "bold"),
            text_color="black"
        ).pack(pady=5, expand=True, anchor="center")

    def create_content_area(self):
        self.content_area = ctk.CTkFrame(
            self.main_frame, 
            fg_color="white", 
            border_width=1, 
            corner_radius=0,
            border_color="#ADD8E6"
        )
        self.content_area.pack(fill="both", expand=True, padx=20, pady=(0, 10))

        if not self.cart:
            self.show_empty_cart()
        else:
            self.show_cart_contents()

    def show_empty_cart(self):
        empty_frame = ctk.CTkFrame(self.content_area, fg_color="white", corner_radius=0)
        empty_frame.pack(expand=True)
        
        message_frame = ctk.CTkFrame(empty_frame, fg_color="white", corner_radius=0)
        message_frame.pack(expand=True)
        
        ctk.CTkLabel(
            message_frame,
            text="Your cart is empty",
            font=("Poppins", 18, "bold"),
            text_color="gray"
        ).pack(expand=True)

    def show_cart_contents(self):
        # Main container
        container = ctk.CTkFrame(self.content_area, fg_color="white", corner_radius=0)
        container.pack(fill="both", expand=True, padx=10, pady=10)

        # Cards section
        self.cards_section = ctk.CTkFrame(container, fg_color="white", height=250, corner_radius=0)  
        self.cards_section.pack(fill="x", pady=(0,5))
        self.cards_section.pack_propagate(False)

        # Scrollable frame
        self.cart_frame = ctk.CTkScrollableFrame(
            self.cards_section,
            fg_color="white",
            height=280,
            width=480,
            corner_radius=0
        )
        self.cart_frame.pack(fill="both", expand=True, padx=5)

        # Load items
        self.load_cart_items()

        # Summary section
        self.summary_frame = ctk.CTkFrame(container, fg_color="white", height=150, corner_radius=0)  
        self.summary_frame.pack(fill="x", pady=(5,0))
        self.summary_frame.pack_propagate(False)
        
        self.update_summary()

    def update_summary(self):
        for widget in self.summary_frame.winfo_children():
            widget.destroy()

        subtotal = sum(Decimal(str(item["price"])) * item["quantity"] for item in self.cart.values())
        tax = subtotal * Decimal("0.06")
        total = subtotal + tax

        # Main summary frame
        summary_content = ctk.CTkFrame(self.summary_frame, fg_color="white", corner_radius=0)
        summary_content.pack(fill="both", expand=True, padx=10)

        # Price rows with proper alignment
        # Subtotal row
        subtotal_frame = ctk.CTkFrame(summary_content, fg_color="white", corner_radius=0)
        subtotal_frame.pack(fill="x")
        ctk.CTkLabel(subtotal_frame, text="Sub Total", font=("Poppins", 14), text_color="black").pack(side="left")
        ctk.CTkLabel(subtotal_frame, text=f"${subtotal:.2f}", font=("Poppins", 14)).pack(side="right")

        # Tax row
        tax_frame = ctk.CTkFrame(summary_content, fg_color="white", corner_radius=0)
        tax_frame.pack(fill="x", pady=2)
        ctk.CTkLabel(tax_frame, text="Estimated Taxes (6%)", font=("Poppins", 14), text_color="gray").pack(side="left")
        ctk.CTkLabel(tax_frame, text=f"${tax:.2f}", font=("Poppins", 14), text_color="gray").pack(side="right")

        # Divider
        divider = ctk.CTkFrame(summary_content, height=2, fg_color="#EEEEEE", corner_radius=0)
        divider.pack(fill="x", pady=5)
        
        # Total row
        total_frame = ctk.CTkFrame(summary_content, fg_color="white", corner_radius=0)
        total_frame.pack(fill="x", pady=(2,5))
        ctk.CTkLabel(total_frame, text="Total", font=("Poppins", 16, "bold")).pack(side="left")
        ctk.CTkLabel(total_frame, text=f"${total:.2f}", font=("Poppins", 16, "bold")).pack(side="right")

        # Order button
        ctk.CTkButton(
            summary_content,
            text="Order",
            fg_color="#F1D94B",
            text_color="black",
            width=140,
            height=40,
            corner_radius=0,
            command=self.place_order
        ).pack(pady=5)

    def load_cart_items(self):
        # Clear existing items
        for widget in self.cart_frame.winfo_children():
            widget.destroy()

        if not self.cart:
            self.show_empty_cart()
            return

        # Create food cards
        for item_id, details in self.cart.items():
            self.create_food_card(item_id, details)

    def create_food_card(self, item_id, details):
        # Card container
        card = ctk.CTkFrame(
            self.cart_frame,
            fg_color="white",
            height=80,
            corner_radius=0,
            border_width=1,
            border_color="#F1D94B"
        )
        card.pack(fill="x", pady=(0, 5), padx=5)
        card.pack_propagate(False) 

        # Item name
        name_label = ctk.CTkLabel(
            card,
            text=details["name"],
            font=("Poppins", 15, "bold"),
            text_color="black"
        )
        name_label.place(x=20, y=15)

        # Quantity controls
        quantity = details["quantity"]

        # Minus button
        minus_btn = ctk.CTkButton(
            card,
            text="-",
            width=25,
            height=25,
            corner_radius=0,
            fg_color="#F1D94B",
            text_color="black",
            hover_color="#E0E0E0",
            command=lambda: self.decrease_quantity(item_id)
        )
        minus_btn.place(x=20, y=45)
        
        # Quantity display
        qty_frame = ctk.CTkFrame(
            card,
            width=40,
            height=25,
            corner_radius=0,
            fg_color="transparent"
        )
        qty_frame.place(x=50, y=45)
        qty_frame.pack_propagate(False)
        
        ctk.CTkLabel(
            qty_frame,
            text=str(quantity),
            font=("Poppins", 14, "bold"),
            text_color="black"
        ).pack(expand=True)
        
        # Plus button
        plus_btn = ctk.CTkButton(
            card,
            text="+",
            width=25,
            height=25,
            corner_radius=0,
            fg_color="#F1D94B",
            text_color="black",
            hover_color="#E1C93B",
            command=lambda: self.increase_quantity(item_id)
        )
        plus_btn.place(x=85, y=45)

        # Price display
        item_price = Decimal(str(details["price"])) * details["quantity"]
        ctk.CTkLabel(
            card,
            text=f"${item_price:.2f}",
            font=("Poppins", 15, "bold"),
            text_color="#E53935"
        ).place(x=260, y=40, anchor="e")

    def decrease_quantity(self, item_id):
        if self.cart[item_id]["quantity"] > 1:
            self.cart[item_id]["quantity"] -= 1
            self.load_cart_items()
            self.update_summary()
        else:
            self.remove_item(item_id)

    def increase_quantity(self, item_id):
        self.cart[item_id]["quantity"] += 1
        self.load_cart_items()
        self.update_summary()

    def remove_item(self, item_id):
        try:
            del self.cart[item_id]
            
            # Reload the cart display
            self.load_cart_items()
            # Update the summary
            self.update_summary()
            
            if not self.cart:  # If cart becomes empty
                
                self.show_empty_cart()
                app_ref = self.app,
                self.after(3000, lambda: [
                    # Navigate back to menu page
                    app_ref.show_customer_dashboard() if hasattr(self.app, 'show_menu_page') else print("Menu page navigation not implemented")
        ])
        except KeyError:
            print(f"Error: Item {item_id} not found in cart")

    def place_order(self):
        try:
            print("Connecting to database...")
            conn = mysql.connector.connect(**DB_CONFIG)
            print("Database connection successful")
            cursor = conn.cursor()

            # Get menu details including category for each item in cart
            menu_ids = list(self.cart.keys())
            
            # If there are items in the cart
            if menu_ids:
                # Fetch category information from Menu table
                placeholders = ", ".join(["%s"] * len(menu_ids))
                fetch_sql = f"""
                SELECT MenuID, Category FROM Menu 
                WHERE MenuID IN ({placeholders})
                """
                cursor.execute(fetch_sql, menu_ids)
                menu_data = {row[0]: row[1] for row in cursor.fetchall()}
                
                # Create items list with proper category information
                items_list = [{
                    'MenuID': int(item_id),
                    'name': item['name'],
                    'price': str(item['price']),
                    'quantity': item['quantity'],
                    'category': menu_data.get(int(item_id), '')  # Get category from Menu table
                } for item_id, item in self.cart.items()]
                
                items_json = json.dumps(items_list)
                
                total_price = sum(Decimal(str(item["price"])) * item["quantity"] for item in self.cart.values())
                
                # 1. Compute next per-user order number
                cursor.execute(
                    "SELECT COALESCE(MAX(orderIDByUser), 0) + 1 "
                    "FROM `Order` WHERE UserID = %s",
                    (self.user.get('userID'),)
                )
                next_seq = cursor.fetchone()[0]
                
                # 2. Insert everything at once
                sql = """
                INSERT INTO `Order`
                  (UserID, orderIDByUser, UserName, Item_list, Total_price, Status)
                VALUES (%s, %s, %s, %s, %s, %s)
                """
                vals = (
                    self.user.get('userID'),
                    next_seq,
                    self.user.get('username'),
                    items_json,
                    float(total_price),
                    'pending'
                )
                
                cursor.execute(sql, vals)
                conn.commit()
                print("Order placed successfully")
                
                # Show success popup
                self.show_success_popup()
            else:
                print("Error: Cart is empty")
                error_label = ctk.CTkLabel(
                    self,
                    text="Cannot place order: Cart is empty",
                    font=("Poppins", 14),
                    text_color="red"
                )
                error_label.place(relx=0.5, rely=0.5, anchor="center")
                self.after(3000, error_label.destroy)
        
        except mysql.connector.Error as err:
            print(f"Database Error: {err}")
            # Show error message
            error_label = ctk.CTkLabel(
                self,
                text=f"Error placing order. Please try again.",
                font=("Poppins", 14),
                text_color="red"
            )
            error_label.place(relx=0.5, rely=0.5, anchor="center")
            self.after(3000, error_label.destroy)
            
        finally:
            # Close connection if it exists
            if 'conn' in locals() and conn.is_connected():
                conn.close()

    def show_success_popup(self):
        # Create blur effect
        blur_frame = ctk.CTkFrame(
            self.main_frame,
            fg_color="#FFFFFF",  # Use a valid color without alpha transparency
            corner_radius=0
        )
        blur_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

        # Success popup
        popup_frame = ctk.CTkFrame(
            blur_frame,
            fg_color="#FFFFFF",
            corner_radius=0,
            border_width=2,
            border_color="#F1D94B",
            width=300,
            height=200
        )
        popup_frame.place(relx=0.5, rely=0.5, anchor="center")
        popup_frame.pack_propagate(False)

        # Success icon
        try:
            success_icon = resize_image((50, 50), "images/success_icon.png")
            ctk.CTkLabel(popup_frame, image=success_icon, text="").pack(pady=(20, 10))
            # Keep a reference to prevent garbage collection
            self.image_refs.append(success_icon)
        except Exception as e:
            print(f"Success icon error: {e}")
            # Fallback if image fails to load
            success_frame = ctk.CTkFrame(popup_frame, width=60, height=60, fg_color="#4CAF50", corner_radius=0)
            success_frame.pack(pady=(20, 10))
            success_frame.pack_propagate(False)
            ctk.CTkLabel(
                success_frame,
                text="✓",
                font=("Arial", 30, "bold"),
                text_color="white"
            ).pack(expand=True)

        # Success message
        ctk.CTkLabel(
            popup_frame,
            text="Order Placed Successfully!",
            font=("Poppins", 16, "bold"),
            text_color="#333333"
        ).pack(pady=10)
        
        ctk.CTkLabel(
            popup_frame,
            text="Returning to menu...",
            font=("Poppins", 14),
            text_color="gray"
        ).pack(pady=5)
        
        app_ref = self.app

        # Schedule return to menu
        self.after(5000, lambda: [
            blur_frame.destroy(),
            app_ref.show_customer_dashboard() if hasattr(self.app, 'show_menu_page') else print("Menu page navigation not implemented")
        ])