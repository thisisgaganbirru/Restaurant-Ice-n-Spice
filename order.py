import customtkinter as ctk
from utils import resize_image
from headerNav import NavigationHeader
from decimal import Decimal
import mysql.connector
from dbconnection import DB_CONFIG
from ordertracking import OrderTrackingPage
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
        NavigationHeader(self, app=self.app).pack(side="top", fill="x")

    def create_order_body(self):
        self.body_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.body_frame.pack(fill="both", expand=True)

        # Background
        self.bg_image = resize_image((800, 800), "images/backg.jpg")
        bg_label = ctk.CTkLabel(self.body_frame, image=self.bg_image, text="")
        bg_label.pack(fill="both", expand=True)

        # Main content frame
        self.main_frame = ctk.CTkFrame(self.body_frame, fg_color="#F9F0E5")
        self.main_frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.8, relheight=0.8)

        # Create header
        self.create_header_section()
        
        # Create content area
        self.create_content_area()

    def create_header_section(self):
        header_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent", height=50)
        header_frame.pack(fill="x", padx=20, pady=(20,10))
        header_frame.pack_propagate(False)

        # Back arrow with circle background
        arrow_frame = ctk.CTkFrame(header_frame, width=60, height=60, fg_color="transparent")
        arrow_frame.pack(side="left")
        arrow_frame.pack_propagate(False)

        try:
            arrow_img = resize_image((50, 50), "images/arrow.png")
            arrow_btn = ctk.CTkButton(
                arrow_frame,
                image=arrow_img,
                text="",
                width=60,
                height=60,
                fg_color="transparent",
                hover_color="#E5DCD0",
                command=lambda: self.app.show_menu_page()
            )
            self.image_refs.append(arrow_img)  # Keep reference to prevent garbage collection
            arrow_btn.place(relx=0.5, rely=0.5, anchor="center")
        except Exception as e:
            print("Arrow Image Error:", e)
            # Fallback to text button if image fails to load
            arrow_btn = ctk.CTkButton(
                arrow_frame,
                text="←",
                width=30,
                fg_color="transparent",
                hover_color="#E5DCD0",
                command=lambda: self.app.show_menu_page()
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
            border_color="#ADD8E6"
        )
        self.content_area.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        if not self.cart:
            self.show_empty_cart()
        else:
            self.show_cart_contents()

    def show_empty_cart(self):
        empty_frame = ctk.CTkFrame(self.content_area, fg_color="white")
        empty_frame.pack(expand=True)
        
        message_frame = ctk.CTkFrame(empty_frame, fg_color="white")
        message_frame.pack(expand=True)
        
        ctk.CTkLabel(
            message_frame,
            text="Your cart is empty",
            font=("Poppins", 18, "bold"),
            text_color="gray"
        ).pack(expand=True)

    def show_cart_contents(self):
        # Main container
        container = ctk.CTkFrame(self.content_area, fg_color="white")
        container.pack(fill="both", expand=True, padx=10, pady=10)

        # Cards section (reduced height)
        self.cards_section = ctk.CTkFrame(container, fg_color="white", height=220)  # Reduced more
        self.cards_section.pack(fill="x", pady=(0,5))
        self.cards_section.pack_propagate(False)

        # Scrollable frame
        self.cart_frame = ctk.CTkScrollableFrame(
            self.cards_section,
            fg_color="white",
            height=200,
            width=480
        )
        self.cart_frame.pack(fill="both", expand=True, padx=5)

        # Load items
        self.load_cart_items()

        # Summary section (increased height)
        self.summary_frame = ctk.CTkFrame(container, fg_color="white", height=230)  # Increased height
        self.summary_frame.pack(fill="x", pady=(5,0))
        self.summary_frame.pack_propagate(False)  # Force fixed height
        
        self.update_summary()

    def update_summary(self):
        for widget in self.summary_frame.winfo_children():
            widget.destroy()

        subtotal = sum(Decimal(str(item["price"])) * item["quantity"] for item in self.cart.values())
        tax = subtotal * Decimal("0.06")
        total = subtotal + tax

        # Main summary frame
        summary_content = ctk.CTkFrame(self.summary_frame, fg_color="white")
        summary_content.pack(fill="both", expand=True, padx=10)

        # Price rows with proper alignment
        # Subtotal row
        subtotal_frame = ctk.CTkFrame(summary_content, fg_color="white")
        subtotal_frame.pack(fill="x")
        ctk.CTkLabel(subtotal_frame, text="Sub Total", font=("Poppins", 12), text_color="black").pack(side="left")
        ctk.CTkLabel(subtotal_frame, text=f"${subtotal:.2f}", font=("Poppins", 12)).pack(side="right")

        # Tax row
        tax_frame = ctk.CTkFrame(summary_content, fg_color="white")
        tax_frame.pack(fill="x", pady=2)
        ctk.CTkLabel(tax_frame, text="Estimated Taxes", font=("Poppins", 12), text_color="gray").pack(side="left")
        ctk.CTkLabel(tax_frame, text=f"${tax:.2f}", font=("Poppins", 12), text_color="gray").pack(side="right")

        # Total row
        total_frame = ctk.CTkFrame(summary_content, fg_color="white")
        total_frame.pack(fill="x", pady=(2,5))
        ctk.CTkLabel(total_frame, text="Total", font=("Poppins", 14, "bold")).pack(side="left")
        ctk.CTkLabel(total_frame, text=f"${total:.2f}", font=("Poppins", 14, "bold")).pack(side="right")

        # Order button
        ctk.CTkButton(
            summary_content,
            text="Order",
            fg_color="#F1D94B",
            text_color="black",
            width=150,
            height=30,
            corner_radius=3,
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
            border_width=1,
            border_color="#F1D94B"
        )
        card.pack(fill="x", pady=(0, 5), padx=5)
        card.pack_propagate(False) 

        # Left side frame for letter/image
        letter_frame = ctk.CTkFrame(card, fg_color="white", width=60, height=60)
        letter_frame.pack(side="left", padx=(10,5), pady=10)
        letter_frame.pack_propagate(False)

        # Display first letter of item name
        ctk.CTkLabel(
            letter_frame,
            text=details["name"][:1].upper(),
            font=("Poppins", 24, "bold"),
            text_color="gray"
        ).pack(expand=True)

        # Details frame
        details_frame = ctk.CTkFrame(card, fg_color="white")
        details_frame.pack(side="left", fill="both", expand=True, pady=5, padx=5)

        # Item name and price in one row
        info_frame = ctk.CTkFrame(details_frame, fg_color="white")
        info_frame.pack(fill="x", expand=True)

        ctk.CTkLabel(
            info_frame,
            text=details["name"],
            font=("Poppins", 14),
            text_color="black"
        ).pack(side="left")

        ctk.CTkLabel(
            info_frame,
            text=f"${details['price']} × {details['quantity']}",
            font=("Poppins", 12),
            text_color="#E53935"
        ).pack(side="right", padx=10)

        # Remove button
        remove_btn = ctk.CTkButton(
            details_frame,
            text="Remove",
            fg_color="#D9534F",
            text_color="white",
            width=70,
            height=25,
            corner_radius=3,
            command=lambda: self.remove_item(item_id)
        )
        remove_btn.pack(side="right", padx=5)

    def remove_item(self, item_id):
        try:
            if self.cart[item_id]["quantity"] > 1:
                self.cart[item_id]["quantity"] -= 1
                self.cart[item_id]["total"] = self.cart[item_id]["quantity"] * self.cart[item_id]["price"]
                self.update_cart_display()
            else:
                del self.cart[item_id]
                self.update_cart_display()
                
                if not self.cart:  # If cart becomes empty
                    self.show_empty_cart()
                    self.after(3000, self.return_to_menu)  # Return to menu after 3 seconds
        except KeyError:
            print(f"Error: Item {item_id} not found in cart")

    def place_order(self):
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor()

            # Get order details
            items_list = json.dumps([{
                'id': item_id,
                'name': item['name'],
                'price': str(item['price']),
                'quantity': item['quantity']
            } for item_id, item in self.cart.items()])
            
            total_price = sum(Decimal(str(item["price"])) * item["quantity"] for item in self.cart.values())

            sql = """
            INSERT INTO `Order` (UserID, UserName, Item_list, Total_price, Status)
            VALUES (%s, %s, %s, %s, %s)
            """
            values = (
                self.user.get('userID'),
                self.user.get('username'),
                items_list,
                float(total_price),
                'pending'
            )

            cursor.execute(sql, values)
            conn.commit()

            # Create blur effect
            blur_frame = ctk.CTkFrame(
                self,
                fg_color=("#FFFFFF80", "#00000080"),  # Semi-transparent
            )
            blur_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

            # Success popup
            popup_frame = ctk.CTkFrame(
                blur_frame,
                fg_color="#FFFFFF",
                corner_radius=10,
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
                ctk.CTkLabel(popup_frame, image=success_icon, text="").pack(pady=(20,10))
            except:
                pass

            # Success message
            ctk.CTkLabel(
                popup_frame,
                text="Order Placed Successfully!",
                font=("Poppins", 16, "bold"),
                text_color="green"
            ).pack(pady=10)

            # Schedule return to menu
            self.after(5000, lambda: [
                blur_frame.destroy(),
            self.app.show_menu_page()
            ])

        except mysql.connector.Error as err:
            print(f"Database Error: {err}")
            # Show error message
            error_label = ctk.CTkLabel(
                self,
                text="Error placing order. Please try again.",
                font=("Poppins", 14),
                text_color="red"
            )
            error_label.place(relx=0.5, rely=0.5, anchor="center")
            self.after(2000, error_label.destroy)

        finally:
            if 'conn' in locals():
                conn.close()
