# import customtkinter as ctk
# from PIL import Image, ImageTk
# from utils import resize_image
# import mysql.connector
# from dbconnection import DB_CONFIG
# from headerNav import NavigationHeader

# class MenuPage(ctk.CTkFrame):
#     def __init__(self, parent, app, user=None):
#         super().__init__(parent)
#         self.app = app
#         self.user = user
#         self.cart = {}
#         self.cart_button = None
#         self.image_refs = []
#         self.category_var = ctk.StringVar(value="All")

#         self.configure(fg_color="white")

#         self.create_header()
#         self.create_menu_body()


#     def create_header(self):
#         NavigationHeader(self, app=self.app).pack(side="top", fill="x")

#     def create_menu_body(self):

#         # frame to hold the background image and content
#         self.body_frame = ctk.CTkFrame(self, fg_color="transparent")
#         self.body_frame.pack(fill="both", expand=True)

#         # Background image
#         self.bg_image = resize_image((800, 800), "images/loginbackground.png")
#         bg_label = ctk.CTkLabel(self.body_frame, image=self.bg_image, text="")
#         bg_label.pack(fill="both", expand=True)

#         # Overlay content frame on top of the background
#         self.content_frame = ctk.CTkFrame(self.body_frame, fg_color="transparent")
#         self.content_frame.place(relx=0, rely=0, relwidth=1, relheight=1)
        
        
#         self.create_search_bar()
#         self.create_category_filters()
#         self.create_product_display()



#     def create_search_bar(self):
#         self.search_frame = ctk.CTkFrame(self.content_frame, fg_color="white")
#         self.search_frame.pack(pady=10)

#         self.search_bar = ctk.CTkEntry(self.search_frame, placeholder_text="Search food...", width=250,
#                                        fg_color="white", text_color="black", corner_radius=10)
#         self.search_bar.pack(side="left", padx=10)

#         search_button = ctk.CTkButton(self.search_frame, text="Search", fg_color="#F1D94B", text_color="black",
#                                       command=self.load_menu_items)
#         search_button.pack(side="left")

#         self.cart_button = ctk.CTkButton(self.search_frame, text="Cart (0)", fg_color="#F1D94B", text_color="black",
#                                          command=self.view_cart)
#         self.cart_button.pack(side="left", padx=10)

#     def update_cart_button(self):
#         total_items = sum(item["quantity"] for item in self.cart.values())
#         self.cart_button.configure(text=f"Cart ({total_items})")

#     def create_category_filters(self):
#         filter_frame = ctk.CTkFrame(self.content_frame, fg_color="white")
#         filter_frame.pack()

#         ctk.CTkLabel(filter_frame, text="Category:", text_color="black").pack(side="left", padx=5)
#         categories = ["All", "Biryani", "Pizza"]
#         for cat in categories:
#             ctk.CTkRadioButton(filter_frame, text=cat, value=cat, variable=self.category_var,
#                                text_color="black", fg_color="#F1D94B", command=self.load_menu_items).pack(side="left", padx=5)

#     def create_product_display(self):
#         self.product_frame = ctk.CTkScrollableFrame(self.content_frame, fg_color="white")
#         self.product_frame.pack(expand=True, fill="both", padx=10, pady=10)
#         self.load_menu_items()

#     def load_menu_items(self):
#         for widget in self.product_frame.winfo_children():
#             widget.destroy()

#         menu_items = self.get_menu_items()
#         if not menu_items:
#             ctk.CTkLabel(self.product_frame, text="No items found", text_color="black").pack(pady=20)
#             return

#         for item in menu_items:
#             self.create_food_card(item)

#     def get_menu_items(self):
#         try:
#             conn = mysql.connector.connect(**DB_CONFIG)
#             cursor = conn.cursor(dictionary=True)

#             query = "SELECT MenuID, name, description, price, imagePath FROM Menu"
#             filters = []
#             params = []

#             if self.category_var.get() != "All":
#                 filters.append("category = %s")
#                 params.append(self.category_var.get())

#             search = self.search_bar.get().strip().lower()
#             if search:
#                 filters.append("LOWER(name) LIKE %s")
#                 params.append(f"%{search}%")

#             if filters:
#                 query += " WHERE " + " AND ".join(filters)

#             cursor.execute(query, params)
#             items = cursor.fetchall()
#             conn.close()
#             return items
#         except Exception as e:
#             print("DB Error:", e)
#             return []


#     def create_food_card(self, item):
#         card = ctk.CTkFrame(self.product_frame, fg_color="white", border_width=1, border_color="#F1D94B")
#         card.pack(padx=5, pady=5, fill="x")

#         try:
#             img = Image.open(item["image"]).resize((200, 120))
#             img = ImageTk.PhotoImage(img)
#             self.image_refs.append(img)
#         except:
#             img = None

#         ctk.CTkLabel(card, image=img, text="").pack(side="left", padx=10)

#         detail = ctk.CTkFrame(card, fg_color="white")
#         detail.pack(side="left", padx=10)

#         ctk.CTkLabel(detail, text=item["name"], font=("Arial", 14, "bold"), text_color="black").pack(anchor="w")
#         ctk.CTkLabel(detail, text=item["description"], text_color="gray").pack(anchor="w")
#         ctk.CTkLabel(detail, text=f"${item['price']}", text_color="#E53935").pack(anchor="w")

#         add_btn = ctk.CTkButton(detail, text="Add to Cart", fg_color="#F1D94B", text_color="black",
#                                 command=lambda: self.update_cart(item, 1, add_btn))
#         add_btn.pack()

#     def update_cart(self, item, change, button):
#         if item["id"] not in self.cart:
#             self.cart[item["id"]] = {"name": item["name"], "price": item["price"], "quantity": 0}

#         self.cart[item["id"]]["quantity"] += change

#         if self.cart[item["id"]]["quantity"] <= 0:
#             del self.cart[item["id"]]
#             button.configure(text="Add to Cart", command=lambda: self.update_cart(item, 1, button))
#         else:
#             qty = self.cart[item["id"]]["quantity"]
#             button.configure(text=f"- {qty} +", command=lambda: self.update_cart(item, 1, button))

#         self.update_cart_button()

#     def view_cart(self):
#         print(f"Opening cart for user: {self.user.get('id', 'N/A') if self.user else 'Unknown'}")
#         # You can implement or connect your cart window here




#------------------------------orders page---------------------------------

# import mysql.connector
# from dbconnection import DB_CONFIG
# import os
# import time
# import customtkinter as ctk


# class OrderPage(ctk.CTkFrame):
#     def __init__(self, parent, app):
#         super().__init__(parent)
#         self.app = app
#         self.configure(width=600, height=700, fg_color="transparent")
        
#         self.create_header()
#         self.create_orders_body()

#     def create_header(self):
#         NavigationHeader(self, app=self.app).pack(side="top", fill="x")

#     def create_orders_body(self):

#         # frame to hold the background image and content
#         body_frame = ctk.CTkFrame(self, fg_color="transparent")
#         body_frame.pack(fill="both", expand=True)

#         # Background image
#         self.bg_image = resize_image((800, 800), "images/loginbackground.png")
#         bg_label = ctk.CTkLabel(body_frame, image=self.bg_image, text="")
#         bg_label.pack(fill="both", expand=True)

#         # Overlay content frame on top of the background
#         content_frame = ctk.CTkFrame(body_frame, fg_color="transparent")
#         content_frame.place(relx=0.5, rely=0.5, anchor="center")  # Center the content


#     def place_order(user_id, cart, app, current_window):

#         if not cart:
#             print("Error: Cart is empty! Cannot place order.")
#             return

#         try:
#             conn = mysql.connector.connect(**DB_CONFIG)
#             cursor = conn.cursor(dictionary=True)

#             cursor.execute("SELECT id, username FROM users WHERE id = %s", (user_id,))
#             user = cursor.fetchone()

#             if not user:
#                 print(f"Error: No user found for user_id = {user_id}")
#                 return

#             username = user["username"]
#             print(f"Placing Order -> User ID: {user_id}, Username: {username}")

#             items_list = ", ".join([f"{details['name']} (x{details['quantity']})" for details in cart.values()])
#             total_price = sum(details["price"] * details["quantity"] for details in cart.values())

#             cursor.execute("""
#                 INSERT INTO orders (UserID, UserName, Item_list, Total_price, Status)
#                 VALUES (%s, %s, %s, %s, 'pending')
#             """, (user_id, username, items_list, total_price))

#             conn.commit()
#             conn.close()

#             print(f"Order placed successfully! 🛒 {username} ordered: {items_list} (Total: ${total_price:.2f})")

#             current_window.destroy()

#             # Navigate to Home Page
#             app.show_frame("CustomerHomePage", user_id=user_id)

#         except mysql.connector.Error as err:
#             print(f"Database Error: {err}")
