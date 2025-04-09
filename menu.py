import customtkinter as ctk
from utils import resize_image
import mysql.connector
from dbconnection import DB_CONFIG
from headerNav import NavigationHeader
from ordertracking import OrderTrackingPage
from order import OrderPage

class MenuPage(ctk.CTkFrame):
    def __init__(self, parent, app, user=None):
        super().__init__(parent)
        self.configure(width=600, height=700, fg_color="transparent")
        self.app = app
        self.user = user
        self.cart = {}
        self.cart_button = None
        self.image_refs = []
        self.category_var = ctk.StringVar(value="All")

        self.create_header()
        self.create_menu_body()


    def create_header(self):
        NavigationHeader(self, app=self.app).pack(side="top", fill="x")


    def create_menu_body(self):
        
        self.body_frame = ctk.CTkFrame(self, fg_color="#EDEDED")
        self.body_frame.pack(fill="both", expand=True)

        try:
            self.bg_image = resize_image((900, 900), "images/loginbackground.png")
            bg_label = ctk.CTkLabel(self.body_frame, image=self.bg_image, text="")
            bg_label.place(relx=0, rely=0, relwidth=1, relheight=1)
        except Exception as e:
            print("[Background Error]", e)

        self.searchbar_frame = ctk.CTkFrame(self.body_frame, fg_color="#F9F0E5")
        self.searchbar_frame.pack(fill="x")

        self.content_frame = ctk.CTkFrame(self.body_frame, fg_color="#F9F0E5")
        self.content_frame.pack(fill="both", expand=True)

        
        self.create_search_bar()
        self.create_category_filters()
        self.create_product_display()


    def create_search_bar(self):
        self.search_frame = ctk.CTkFrame(self.searchbar_frame, fg_color="transparent")
        self.search_frame.pack(pady=10)

        self.search_bar = ctk.CTkEntry(self.search_frame, 
                                       placeholder_text="Search food...", 
                                       width=250,
                                       fg_color="white", 
                                       text_color="black", 
                                       corner_radius=5)
        self.search_bar.pack(side="left", padx=10)

        search_button = ctk.CTkButton(self.search_frame, 
                                    text="Search", 
                                    fg_color="#F1D94B", 
                                    text_color="black",
                                    command=self.create_product_display)
        search_button.pack(side="left")

        self.cart_button = ctk.CTkButton(self.search_frame, 
                                         text="Cart (0)", 
                                         fg_color="#F1D94B", 
                                         text_color="black",
                                         command=self.view_cart)
        self.cart_button.pack(side="left", padx=10)


    def update_cart_button(self):
        total_items = sum(item["quantity"] for item in self.cart.values())
        self.cart_button.configure(text=f"Cart ({total_items})")


    def create_category_filters(self):
        filter_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        filter_frame.pack(pady=(0, 5))

        ctk.CTkLabel(filter_frame, text="Category:", text_color="black").pack(side="left", padx=5)
        self.category_var = ctk.StringVar(value="All")

        categories = ["All", "Biryani", "Pizza", "Burger", "Desserts", "Bevarages"]
        for cat in categories:
            ctk.CTkRadioButton(filter_frame, 
                               text=cat, value=cat, 
                               variable=self.category_var,
                               text_color="black", 
                               fg_color="#F1D94B", 
                               command=self.create_product_display).pack(side="left", padx=5)


    def create_product_display(self):

        search_query = self.search_bar.get().strip().lower()
        
        if search_query:
            self.show_search_results(search_query)
        
        else:
            self.multiple_scroll_sections()
            
    def multiple_scroll_sections(self):
        
        # --- MOST POPULAR SECTION ---
        most_popular_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        most_popular_frame.pack(fill="x", pady=(10, 0))

        self.create_scroll(
            title="Most Popular",
            query="SELECT MenuID, name, description, price, imagePath FROM Menu ORDER BY RAND() LIMIT 10",
            parent=most_popular_frame
        )

        # --- POPULAR LUNCH SECTION ---
        lunch_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        lunch_frame.pack(fill="x", pady=(5, 0))

        self.create_scroll(
            title="Popular Lunch",
            query="SELECT MenuID, name, description, price, imagePath FROM Menu WHERE category = 'Biryani'",
            parent=lunch_frame
        )


    def scroll_left(self, target_frame):
        target_frame._parent_canvas.xview_scroll(-50, "units")


    def scroll_right(self, target_frame):
        target_frame._parent_canvas.xview_scroll(50, "units")

        
    def create_scroll(self, query, title, parent):
        scroll_frame = ctk.CTkFrame(parent, fg_color="transparent")
        scroll_frame.pack(pady=(10, 0), fill="x")

        self.lefticon = resize_image((30, 50), "images/arrow-left.PNG")
        self.righticon = resize_image((30, 50), "images/arrow-right.PNG")

        # Title Label
        title_label = ctk.CTkLabel(scroll_frame, text=title,
            font=("Poppins", 16, "bold"), text_color="black",
            anchor="w", justify="left")
        title_label.pack(side="top", anchor="w", padx=20, pady=(10, 0))

        # Frame to hold arrows and scrollable product list
        row_frame = ctk.CTkFrame(scroll_frame, fg_color="transparent")
        row_frame.pack(fill="x", pady=(0, 0), padx=5)

        # LEFT BUTTON (Use 'place' and lift to overlay)
        left_btn = ctk.CTkButton(
            row_frame, text="", image=self.lefticon, width=5,
            corner_radius=5, fg_color="transparent",
            command=lambda: self.scroll_left(product_frame)
        )
        left_btn.place(relx=0, rely=0.5, anchor="w", x=5)
        left_btn.lift()

        # PRODUCT SCROLLABLE FRAME
        product_frame = ctk.CTkScrollableFrame(row_frame, fg_color="white", orientation="horizontal")
        product_frame.pack(side="left", fill="both", expand=True, padx=10)
        product_frame._parent_canvas.configure(xscrollcommand=lambda *args: None)
        product_frame._scrollbar.grid_forget()

        # RIGHT BUTTON (place over edge)
        right_btn = ctk.CTkButton(
            row_frame, text="", image=self.righticon, width=5,
            corner_radius=5, fg_color="transparent",
            command=lambda: self.scroll_right(product_frame)
        )
        right_btn.place(relx=1.0, rely=0.5, anchor="e", x=-5)
        right_btn.lift()

        # Load items into the scrollable frame
        self.load_menu_items(query, parent_frame=product_frame)


    def load_menu_items(self, query,parent_frame=None):
        for widget in parent_frame.winfo_children():
            widget.destroy()

        menu_items = self.get_menu_items(query)
        
        if not menu_items:
            ctk.CTkLabel(
                    self.content_frame,
                    text="Couldn't find the item you're looking for.",
                    font=("poppins", 14, "italic"),
                    text_color="red").pack(pady=20)
            return

        for item in menu_items:
            self.create_food_card(item, parent_frame= parent_frame)


    def get_menu_items(self, query):
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor(dictionary=True)
            filters = []
            params = []

            if self.category_var.get() != "All":
                filters.append("category = %s")
                params.append(self.category_var.get())

            search = self.search_bar.get().strip().lower()
            if search:
                filters.append("LOWER(name) LIKE %s")
                params.append(f"%{search}%")

            if filters:
                query += " WHERE " + " AND ".join(filters)

            cursor.execute(query, params)
            items = cursor.fetchall()
            conn.close()
            return items
        except Exception as e:
            print("DB Error:", e)
            return []


    def create_food_card(self, item, parent_frame=None):
        

        card = ctk.CTkFrame(
                parent_frame,
                fg_color="transparent",
                border_width=2,
                border_color="#F1D94B",
                width=400,
                height=200,
                corner_radius=10
            )
        card.pack(side="left", padx=10, pady=5)
        card.pack_propagate(False) 

        cardimage_frame = ctk.CTkFrame(card, fg_color="white")
        cardimage_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        cardimage_frame.pack_propagate(False) 

        try:
            # print("Trying image:", item["image"])
            
            menu_img = resize_image((200,200),item["imagePath"])
            self.image_refs.append(menu_img)
            ctk.CTkLabel(cardimage_frame, image=menu_img, text="").pack(side="left",padx=10, pady=10)
        except Exception as e:
            print("Image Error:", e)
            menu_img = None
            ctk.CTkLabel(cardimage_frame, text="Image not found", font=("poppins", 10, "italic")).pack(padx=10)

        carddetail_frame = ctk.CTkFrame(card, fg_color="white")
        carddetail_frame.pack(side="left", fill="both", expand=True, padx=2, pady=10)
        carddetail_frame.pack_propagate(False) 
        
        
        # Name
        ctk.CTkLabel(
                carddetail_frame, text=item["name"],
                font=("Inter", 16, "bold"), text_color="black", wraplength=120,anchor="w", justify="left"
            ).pack(anchor="w", fill="x")

        # Description
        ctk.CTkLabel(
                carddetail_frame, text=item["description"][:80] + "...",
                font=("Inter", 10), text_color="gray",
                wraplength=200, anchor="w", justify="left"
            ).pack(anchor="w", fill="x", pady=(2, 5))

        # Price
        ctk.CTkLabel(
                carddetail_frame, text=f"$ {item['price']}",
                font=("Inter", 16), text_color="black",anchor="w", justify="left"
            ).pack(anchor="w",  fill="x",pady=(0, 15))

        # Add to Cart Button
        ctk.CTkButton(
                carddetail_frame, text="Add to Cart",
                fg_color="#F1D94B", text_color="black",width=150,
                command=lambda: self.update_cart(item, 1, None)
            ).pack(anchor="w", pady=(10, 5))


    def show_search_results(self, search_query):

        search_query = self.search_bar.get().strip().lower()

        if not search_query:
            self.create_product_display()
            return

        for widget in self.content_frame.winfo_children():
            widget.destroy()

        
        searchresults_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        searchresults_frame.pack(fill="both", expand=True, padx=10, pady=10)

        query = "SELECT MenuID, name, description, price, imagePath FROM Menu"
        items = self.get_menu_items(query, parent_frame=searchresults_frame)
        matched_items = [item for item in items if search_query in item["name"].lower()]

        if not matched_items:
            ctk.CTkLabel(searchresults_frame, text="No items match your search.",
                        font=("Poppins", 14, "italic"), text_color="red").pack(pady=20)
            return

        for item in matched_items:
            self.create_vertical_foodcards(item, parent_frame=searchresults_frame)



    def create_vertical_foodcards(self,item,parent_frame):
        
        frame = ctk.CTkFrame(parent_frame, fg_color="transparent", 
                             width=500, height=200, corner_radius=10,border_width=2, border_color="#F1D94B")
        frame.pack(pady=10, padx=5, fill="x")
        

        try:
            searchmenu_img = resize_image((250,250),item["imagePath"])
            self.image_refs.append(searchmenu_img)
        except Exception as e:
                print(f"Error loading image: {e}")
                searchmenu_img = None

        if searchmenu_img:
            img_label = ctk.CTkLabel(frame, image=searchmenu_img, text="")
            img_label.image = searchmenu_img
            img_label.place(x=10, y=10)

            carddetails_frame = ctk.CTkFrame(frame, fg_color="white", width=220, height=150)
            carddetails_frame.place(x=270, y=15)
            carddetails_frame.pack_propagate(False) 

            ctk.CTkLabel(carddetails_frame, text=item["name"], font=("poppins", 14, "bold"), text_color="black").pack(anchor="w")
            ctk.CTkLabel(carddetails_frame, text=item["description"], font=("poppins", 10), text_color="gray").pack(anchor="w")
            ctk.CTkLabel(carddetails_frame, text=f"${item['price']}", font=("poppins", 12), text_color="#E53935").pack(anchor="w")

            add_button = ctk.CTkButton(carddetails_frame, text="Add to Cart", fg_color="#F1D94B", text_color="black",
                                    command=lambda item=item: self.update_cart(item, 1, add_button))
            add_button.pack()

    def create_order_tracking_button(self):
            tracking_btn = ctk.CTkButton(
                self.content_frame,
                text="order Tracking",
                fg_color="#F1D94B",
                text_color="black",
                command=lambda: OrderTrackingPage(self.user)
            )
            tracking_btn.pack(pady=15)
        

    def update_cart(self, item, change, button=None):
        menu_id = item.get("MenuID")
        if not menu_id:
            # print("Missing MenuID for item:", item)
            return

        if menu_id not in self.cart:
            self.cart[menu_id] = {
                "name": item["name"],
                "price": item["price"],
                "quantity": 0
            }

        #to update the quantity
        self.cart[menu_id]["quantity"] += change

        # Remove if quantity is zero or less
        if self.cart[menu_id]["quantity"] <= 0:
            del self.cart[menu_id]
            if button and hasattr(button, "configure"):
                button.configure(text="Add to Cart", command=lambda: self.update_cart(item, 1, button))
        else:
            qty = self.cart[menu_id]["quantity"]
            if button and hasattr(button, "configure"):
                button.configure(text=f"- {qty} +", command=lambda: self.update_cart(item, 1, button))

        self.update_cart_button()


    def view_cart(self):
        
        print(f"Opening cart for user: {self.user.get('id', 'N/A') if self.user else 'Unknown'}")
        if not self.cart:
            print("Cart is empty!")
            return

        print(f"Opening cart for user: {self.user.get('id', 'N/A') if self.user else 'Unknown'}")
        self.app.clear_main_frame()

        self.app.show_order_page(user=self.user, cart=self.cart)
