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
        
        # Initialize tracking button
        self.tracking_btn = None
        
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
        self.create_floating_tracking_button()



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
        if total_items > 0:
            self.tracking_btn.pack(side="bottom", anchor="e", padx=20, pady=20)
        else:
            self.tracking_btn.pack_forget()


    def create_category_filters(self):
        filter_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        filter_frame.pack(pady=(0, 0))

        ctk.CTkLabel(filter_frame, text="Category:", text_color="black").pack(side="left", padx=5)
        self.category_var = ctk.StringVar(value="All")

        categories = ["All", "Biryani", "Pizza", "Burger", "Desserts", "Beverages"]
        for cat in categories:
            ctk.CTkRadioButton(
                filter_frame, 
                text=cat,
                value=cat, 
                variable=self.category_var,
                text_color="black", 
                fg_color="#F1D94B",
                hover_color="#E5C63D",
                command=self.create_product_display
            ).pack(side="left", padx=5)


    def create_product_display(self):
        search_query = self.search_bar.get().strip().lower()
        selected_category = self.category_var.get()
        
        # Clear existing content
        for widget in self.content_frame.winfo_children():
            if isinstance(widget, ctk.CTkFrame) and widget != self.searchbar_frame:
                widget.destroy()

        if search_query:
            # Create scrollable frame for search results
            results_frame = ctk.CTkScrollableFrame(
                self.content_frame, 
                fg_color="transparent",
                width=550,
                height=500
            )
            results_frame.pack(fill="both", expand=True, padx=10, pady=10)
            
            query = "SELECT MenuID, name, description, price, imagePath FROM Menu"
            menu_items = self.get_menu_items(query)
            
            if not menu_items:
                ctk.CTkLabel(
                    self.content_frame,
                    text="No items match your search.",
                    font=("Poppins", 14, "italic"),
                    text_color="red"
                ).pack(pady=20)
                return
            
            for item in menu_items:
                self.create_vertical_foodcards(item, parent_frame=results_frame)
        else:
            self.multiple_scroll_sections()


    def multiple_scroll_sections(self):
        
        # --- MOST POPULAR SECTION ---
        most_popular_frame = ctk.CTkFrame(self.content_frame, fg_color="#F9F0E5")
        most_popular_frame.pack(fill="x", pady=(0, 5))

        self.create_scroll(
            title="Most Popular",
            query="SELECT MenuID, name, description, price, imagePath FROM Menu ORDER BY RAND() LIMIT 10",
            parent=most_popular_frame
        )

        # --- POPULAR LUNCH SECTION ---
        lunch_frame = ctk.CTkFrame(self.content_frame, fg_color="#F9F0E5")
        lunch_frame.pack(fill="x", pady=(0, 5))

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
        scroll_frame = ctk.CTkFrame(parent, fg_color="#F9F0E5", width=600, height=250)
        scroll_frame.pack(pady=(0, 10), fill="x")
        scroll_frame.pack_propagate(False)

        self.lefticon = resize_image((30, 50), "images/expand-button_left.PNG")
        self.righticon = resize_image((30, 50), "images/expand-button_right.PNG")

        # Title Label
        title_label = ctk.CTkLabel(scroll_frame, text=title,
            font=("Poppins", 16, "bold"), text_color="black",
            anchor="w", justify="left")
        title_label.pack(side="top", anchor="w", padx=20, pady=(5, 3))

        # Main container for navigation and products
        container_frame = ctk.CTkFrame(scroll_frame, fg_color="#F9F0E5", width=600, height=200)
        container_frame.pack(fill="x", pady=(5, 2), padx=(5, 5))
        container_frame.pack_propagate(False)

        # LEFT BUTTON with border
        left_btn_frame = ctk.CTkFrame(
            container_frame, 
            fg_color="white",
            border_width=1,
            border_color="#F1D94B",
            width=32,
            height=200,
            corner_radius=0
        )
        left_btn_frame.place(x=0, rely=0.5, anchor="w")
        
        left_btn = ctk.CTkButton(
            left_btn_frame, 
            text="", 
            image=self.lefticon,
            width=30,
            height=200,
            corner_radius=0,
            fg_color="white",
            hover_color="#E5DCD0",
            command=lambda: self.scroll_left(product_frame)
        )
        left_btn.place(relx=0.5, rely=0.5, anchor="center")

        # CENTER FRAME for products
        center_frame = ctk.CTkFrame(container_frame, fg_color="#F9F0E5", width=540, height=200)
        center_frame.place(relx=0.5, rely=0.5, anchor="center")

        # PRODUCT SCROLLABLE FRAME
        product_frame = ctk.CTkScrollableFrame(
            center_frame, 
            fg_color="#F9F0E5",
            orientation="horizontal",
            width=520,
            height=200
        )
        product_frame.pack(fill="both", anchor="center", expand=True)
        product_frame._parent_canvas.configure(xscrollcommand=lambda *args: None)
        product_frame._scrollbar.grid_forget()

        # RIGHT BUTTON with border
        right_btn_frame = ctk.CTkFrame(
            container_frame,
            fg_color="white",
            border_width=1,
            border_color="#F1D94B",
            width=32,
            height=200,
            corner_radius=0
        )
        right_btn_frame.place(x=600, rely=0.5, anchor="e")
        
        right_btn = ctk.CTkButton(
            right_btn_frame,
            text="",
            image=self.righticon,
            width=30,
            height=200,
            corner_radius=0,
            fg_color="white",
            hover_color="#E5DCD0",
            command=lambda: self.scroll_right(product_frame)
        )
        right_btn.place(relx=0.5, rely=0.5, anchor="center")

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

            # Always check category first (unless it's "All")
            if self.category_var.get() != "All":
                filters.append("category = %s")
                params.append(self.category_var.get())

            # Then check search term
            search = self.search_bar.get().strip().lower()
            if search:
                filters.append("LOWER(name) LIKE %s")
                params.append(f"%{search}%")

            if filters:
                query += " WHERE " + " AND ".join(filters)

            cursor.execute(query, params)
            items = cursor.fetchall()
            cursor.close()
            conn.close()
            return items
        except Exception as e:
            print("DB Error:", e)
            return []


    def create_food_card(self, item, parent_frame=None):
        # Create a single frame to hold the card
        card = ctk.CTkFrame(
            parent_frame,
            fg_color="white",
            width=350,
            height=200,
            corner_radius=10,
            border_width=2,
            border_color="#F1D94B"
        )
        card.pack(side="left", padx=10, pady=5, anchor="center")
        card.pack_propagate(False)

        # Image Frame using place
        image_frame = ctk.CTkFrame(card, fg_color="white", width=140, height=180)
        image_frame.place(x=15, y=20)

        try:
            menu_img = resize_image((180, 180), item["imagePath"])
            self.image_refs.append(menu_img)
            ctk.CTkLabel(image_frame, image=menu_img, text="").pack(expand=True)
        except Exception as e:
            print("Image Error:", e)
            ctk.CTkLabel(image_frame, text="Image not found", font=("poppins", 10, "italic")).pack(padx=10)

        # Details Frame using place
        details_frame = ctk.CTkFrame(card, fg_color="white", width=180, height=120)
        details_frame.place(x=160, y=20)
        details_frame.pack_propagate(False)

        # Name label (truncated if > 15 words)
        name_text = item["name"]
        words = name_text.split()
        if len(words) > 15:
            name_text = " ".join(words[:15]) + "..."

        name_label = ctk.CTkLabel(
            details_frame, 
            text=name_text,
            font=("Inter", 16, "bold"), 
            text_color="black", 
            wraplength=180, 
            anchor="w", 
            justify="left"
        )
        name_label.pack(anchor="w", fill="x", padx=10)

        # Description (truncated)
        description_text = item["description"]
        if len(description_text) > 50:
            description_text = description_text[:47] + "..."

        description_label = ctk.CTkLabel(
            details_frame, 
            text=description_text,
            font=("Inter", 11), 
            text_color="gray",
            wraplength=160, 
            anchor="w", 
            justify="left"
        )
        description_label.pack(anchor="w", fill="x", padx=10, pady=(5, 10))

        # Price (always visible)
        price_label = ctk.CTkLabel(
            details_frame, 
            text=f"$ {item['price']}",
            font=("Inter", 16, "bold"), 
            text_color="black", 
            anchor="w", 
            justify="left"
        )
        price_label.pack(anchor="w", fill="x", padx=10)

        # Button Frame using place
        button_frame = ctk.CTkFrame(card, fg_color="white", width=180, height=50)
        button_frame.place(x=160, y=120)
        button_frame.pack_propagate(False)

        # Add to Cart Button
        add_button = ctk.CTkButton(
            button_frame, 
            text="Add to Cart",
            fg_color="#F1D94B", 
            text_color="black", 
            width=150,
            height=30,
            corner_radius=0,
            command=lambda: self.update_cart(item, 1, add_button)
        )
        add_button.pack(pady=10, padx=15)


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



    def create_vertical_foodcards(self, item, parent_frame):
        Verticalcard = ctk.CTkFrame(
            parent_frame,
            fg_color="white",
            width=550,
            height=200,
            corner_radius=10,
            border_width=2,
            border_color="#F1D94B"
        )
        Verticalcard.pack(pady=10, padx=10)
        Verticalcard.pack_propagate(False)

        # Image Frame (50% width)
        image_frame = ctk.CTkFrame(Verticalcard, fg_color="white", width=275, height=180)
        image_frame.place(relx=0, rely=0.5, anchor="w", x=10)
        image_frame.pack_propagate(False)

        try:
            menu_img = resize_image((180, 180), item["imagePath"])
            self.image_refs.append(menu_img)
            ctk.CTkLabel(image_frame, image=menu_img, text="").pack(expand=True)
        except Exception as e:
            print("Image Error:", e)
            ctk.CTkLabel(image_frame, text="Image not found", font=("poppins", 10, "italic")).pack(padx=10)

        # Details Frame (50% width)
        details_frame = ctk.CTkFrame(Verticalcard, fg_color="white", width=275, height=180)
        details_frame.place(relx=1, rely=0.5, anchor="e", x=-10)
        details_frame.pack_propagate(False)

        # Details section (70% height)
        details_section = ctk.CTkFrame(details_frame, fg_color="white", height=126)
        details_section.pack(fill="x", expand=True)
        
        ctk.CTkLabel(
            details_section,
            text=item["name"],
            font=("Inter", 16, "bold"),
            text_color="black",
            wraplength=250,
            anchor="w"
        ).pack(fill="x", padx=10, pady=(10,5))

        ctk.CTkLabel(
            details_section,
            text=item["description"],
            font=("Inter", 12),
            text_color="gray",
            wraplength=250,
            anchor="w"
        ).pack(fill="x", padx=10)

        ctk.CTkLabel(
            details_section,
            text=f"$ {item['price']}",
            font=("Inter", 16, "bold"),
            text_color="black",
            anchor="w"
        ).pack(fill="x", padx=10, pady=5)

        # Button section (30% height)
        button_frame = ctk.CTkFrame(details_frame, fg_color="white", height=54)
        button_frame.pack(fill="x")
        
        add_button = ctk.CTkButton(
            button_frame,
            text="Add to Cart",
            fg_color="#F1D94B",
            text_color="black",
            width=150,
            height=30,
            corner_radius=5,
            command=lambda: self.update_cart(item, 1, button_frame)
        )
        add_button.pack(pady=10)

    def create_floating_tracking_button(self):
        """Creates a floating tracking button at bottom right"""
        if self.has_pending_orders():
            # Create a frame for the floating button
            floating_frame = ctk.CTkFrame(
                self.content_frame,  # Changed from body_frame to content_frame
                fg_color="transparent",
                width=120,
                height=40
            )
            floating_frame.place(relx=0.95, rely=0.95, anchor="se")
            
            # Shadow effect
            shadow_frame = ctk.CTkFrame(
                self.content_frame,  # Changed from body_frame to content_frame
                fg_color="#d0cccc",
                corner_radius=20,
                width=120,
                height=40
            )
            shadow_frame.place(relx=0.952, rely=0.955, anchor="se")
            
            # Tracking button
            tracking_btn = ctk.CTkButton(
                floating_frame,
                text="Track Order",
                font=("Poppins", 12, "bold"),
                fg_color="#F1D94B",
                text_color="black",
                hover_color="#E5C63D",
                width=120,
                height=40,
                corner_radius=20,
                command=self.app.show_ordertracking_page
            )
            tracking_btn.pack(side="right")
            
            # Store reference to the button
            self.tracking_btn = tracking_btn
            
            # Bring button to front
            floating_frame.lift()

    def update_cart(self, item, change, button_container):
        menu_id = item["MenuID"]
        
        if menu_id not in self.cart:
            self.cart[menu_id] = {
                "name": item["name"],
                "price": item["price"],
                "quantity": 0
            }

        # Update quantity
        self.cart[menu_id]["quantity"] += change

        if self.cart[menu_id]["quantity"] <= 0:
            del self.cart[menu_id]

        # Update cart display
        self.update_cart_button()

        # Clear previous buttons inside the container
        for widget in button_container.winfo_children():
            widget.destroy()

        # If item is in cart, show quantity UI
        if menu_id in self.cart:
            qty = self.cart[menu_id]["quantity"]

            ctk.CTkButton(button_container, text="-", width=50, fg_color="#F1D94B", text_color="black",
                        command=lambda: self.update_cart(item, -1, button_container)).pack(side="left")
            
            ctk.CTkLabel(button_container, text=str(qty), width=40, text_color="black",
                        font=("Inter", 14, "bold")).pack(side="left", padx=5)
            
            ctk.CTkButton(button_container, text="+", width=50, fg_color="#F1D94B", text_color="black",
                        command=lambda: self.update_cart(item, 1, button_container)).pack(side="left")

        else:
            # Back to Add to Cart button
            ctk.CTkButton(
                button_container, text="Add to Cart",
                fg_color="#F1D94B", text_color="black", width=150,
                command=lambda: self.update_cart(item, 1, button_container)
            ).pack()



    def view_cart(self):
        print(f"Opening cart for user: {self.user}")  # Debug print
        self.app.clear_main_frame()
        try:
            OrderPage(
                self.app.main_frame, 
                app=self.app, 
                user=self.user or {"username": "User"}, 
                cart=self.cart
            ).pack(fill="both", expand=True)
        except Exception as e:
            print(f"Error creating OrderPage: {e}")

    def has_pending_orders(self):
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor()
            
            sql = """
            SELECT COUNT(*) FROM `Order` 
            WHERE UserID = %s 
            AND Status IN ('pending', 'preparing', 'ready for pickup')
            """
            cursor.execute(sql, (self.user.get('userID'),))
            count = cursor.fetchone()[0]
            
            return count > 0
            
        except mysql.connector.Error as err:
            print(f"Database Error: {err}")
            return False
            
        finally:
            if 'conn' in locals():
                conn.close()
