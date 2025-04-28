import customtkinter as ctk
from utils import resize_image
import os
from dbconnection import DB_CONFIG
import mysql.connector
from PIL import Image, ImageTk
from admin_stats import AdminStatsPage

class AdminDashboard(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.configure(fg_color="#F1E8DD")
        self.pack(fill="both", expand=True)

        # Stats Frame at top
        self.stats_frame = ctk.CTkFrame(self, fg_color="transparent", height=200)
        self.stats_frame.pack(fill="x", padx=20, pady=10)
        self.stats_frame.pack_propagate(False)

        # Create AdminStatsPage instance for stats
        AdminStatsPage(self.stats_frame, self.app)

        # Bottom border line
        border_line = ctk.CTkFrame(self, fg_color="grey", height=2)
        border_line.pack(fill="x", padx=20)

        # Menu Dashboard Frame
        menu_dashboard_frame = ctk.CTkFrame(self, fg_color="#F1E8DD")
        menu_dashboard_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Header with title and search
        self.create_header_and_subframe(menu_dashboard_frame)

        # Items count and Add Item button
        actions_frame = ctk.CTkFrame(menu_dashboard_frame, fg_color="transparent", height=40)
        actions_frame.pack(fill="x", padx=20, pady=10)
        actions_frame.pack_propagate(False)

        self.items_count_label = ctk.CTkLabel(
            actions_frame,
            text="0 items found",
            font=("Poppins", 14),
            text_color="gray"
        )
        self.items_count_label.pack(anchor="w", padx=15, pady=(15, 5))

        # Filter by category button and dropdown
        self.category_frame = ctk.CTkFrame(actions_frame, fg_color="transparent")
        self.category_frame.pack(side="right", padx=10)

        self.filter_btn = ctk.CTkButton(
            self.category_frame,
            text="Filter Menu",
            font=("Poppins", 12),
            fg_color="#2B2B2B",
            text_color="white",
            hover_color="#3B3B3B",
            width=150,
            height=35,
            command=self.show_category_dropdown
        )
        self.filter_btn.pack(side="right")

        # Create scrollable frame for menu items
        self.items_frame = ctk.CTkScrollableFrame(
            menu_dashboard_frame,
            fg_color="transparent",
            height=400
        )
        self.items_frame.pack(fill="both", expand=True, padx=20)

        # Load more button frame
        self.load_more_frame = ctk.CTkFrame(menu_dashboard_frame, fg_color="transparent")
        self.load_more_frame.pack(fill="x", pady=10)

        self.load_more_button = ctk.CTkButton(
            self.load_more_frame,
            text="Load More",
            font=("Poppins", 12),
            fg_color="#F1D94B",
            text_color="black",
            hover_color="#E5CE45",
            width=120,
            height=35,
            command=self.load_more_items
        )
        self.load_more_button.pack()

        # Initialize pagination
        self.page_size = 6
        self.current_page = 0
        self.total_items = 0

        # Load initial items
        self.load_menu_items()

        self.current_category = "All"  # Default category

        self.category_dropdown = None  # Initialize category dropdown

    def create_header_and_subframe(self, parent):
        # Main frame
        main_frame = ctk.CTkFrame(parent, fg_color="transparent", height=100)
        main_frame.pack(fill="x", padx=20, pady=10)
        main_frame.pack_propagate(False)

        # Header frame
        header_frame = ctk.CTkFrame(main_frame, fg_color="transparent", height=50)
        header_frame.pack(fill="x", padx=10, pady=(0, 10))
        header_frame.pack_propagate(False)

        # Title
        ctk.CTkLabel(
            header_frame,
            text="Menu Dashboard",
            font=("Poppins", 24, "bold"),
            text_color="#2B2B2B"
        ).pack(side="left", padx=10)

        # Subframe for search, filter, and add item
        subframe = ctk.CTkFrame(main_frame, fg_color="transparent", height=50)
        subframe.pack(fill="x", padx=10, pady=(0, 10))
        subframe.pack_propagate(False)

        # Search bar
        search_var = ctk.StringVar()
        search_entry = ctk.CTkEntry(
            subframe,
            placeholder_text="Search menu items...",
            textvariable=search_var,
            width=200,
            height=35
        )
        search_entry.pack(side="left", padx=(0, 10))

        # Search button
        search_button = ctk.CTkButton(
            subframe,
            text="Search",
            font=("Poppins", 12),
            fg_color="#F1D94B",
            text_color="black",
            hover_color="#E5CE45",
            width=100,
            height=35,
            command=lambda: self.filter_items(search_var.get())
        )
        search_button.pack(side="left", padx=(0, 10))

        # Filter button
        filter_button = ctk.CTkButton(
            subframe,
            text="Filter",
            font=("Poppins", 12),
            fg_color="#2B2B2B",
            text_color="white",
            hover_color="#3B3B3B",
            width=100,
            height=35,
            command=self.show_category_dropdown
        )
        filter_button.pack(side="right", padx=(10, 0))

        # Add Item button
        add_item_button = ctk.CTkButton(
            subframe,
            text="+ Add Item",
            font=("Poppins", 12),
            fg_color="#F1D94B",
            text_color="black",
            hover_color="#E5CE45",
            width=120,
            height=35,
            command=self.show_add_item
        )
        add_item_button.pack(side="right", padx=(10, 0))

    def create_menu_item_card(self, item, row, col):
        # Create card frame
        card = ctk.CTkFrame(
            self.items_frame,
            fg_color="white",
            corner_radius=15,
            border_width=2,
            border_color="#F1D94B",
            width=250,  # Adjusted width
            height=250  # Adjusted height
        )
        card.grid(row=row, column=col, padx=15, pady=15, sticky="nsew")
        card.grid_propagate(False)

        # Image frame
        image_frame = ctk.CTkFrame(
            card,
            fg_color="#F9F9F9",  # Light gray background
            height=120,          # Adjusted height
            corner_radius=12
        )
        image_frame.pack(fill="x", padx=10, pady=10)
        image_frame.pack_propagate(False)

        try:
            # Load and display item image
            image = Image.open(item['ImagePath'])
            photo = ctk.CTkImage(
                light_image=image,
                dark_image=image,
                corner_radius=10,
                size=(100, 100)  # Adjusted image size
            )
            image_label = ctk.CTkLabel(
                image_frame,
                image=photo,
                text=""
            )
            image_label.place(relx=0.5, rely=0.5, anchor="center")
        except Exception as e:
            # Show placeholder if image fails to load
            no_image_frame = ctk.CTkFrame(
                image_frame,
                fg_color="#EAEAEA",
                corner_radius=10,
                width=100,
                height=100
            )
            no_image_frame.place(relx=0.5, rely=0.5, anchor="center")

            ctk.CTkLabel(
                no_image_frame,
                text="No Image",
                font=("Poppins", 14, "bold"),
                text_color="gray"
            ).place(relx=0.5, rely=0.5, anchor="center")

        # Info frame
        info_frame = ctk.CTkFrame(
            card,
            fg_color="transparent",
            height=120  # Adjusted height
        )
        info_frame.pack(fill="x", padx=10, pady=(0, 5))
        info_frame.pack_propagate(False)

        # Top frame for item name
        top_frame = ctk.CTkFrame(
            info_frame,
            fg_color="transparent",
            height=40
        )
        top_frame.pack(fill="x", pady=(0, 5))
        top_frame.pack_propagate(False)

        # Item name with ellipsis if too long
        name_label = ctk.CTkLabel(
            top_frame,
            text=item['Name'][:22] + ('...' if len(item['Name']) > 22 else ''),  # Adjusted length
            font=("Poppins", 14, "bold"),  # Adjusted font size
            text_color="#2B2B2B",
            anchor="w"
        )
        name_label.pack(anchor="w")

        # Bottom frame for details and button
        bottom_frame = ctk.CTkFrame(
            info_frame,
            fg_color="transparent",
            height=80
        )
        bottom_frame.pack(fill="x")
        bottom_frame.pack_propagate(False)

        # Left frame for category and price
        left_frame = ctk.CTkFrame(
            bottom_frame,
            fg_color="transparent",
            width=100
        )
        left_frame.pack(side="left", fill="y", padx=(0, 5))
        left_frame.pack_propagate(False)

        # Category label
        category_label = ctk.CTkLabel(
            left_frame,
            text=item['Category'],
            font=("Poppins", 12),
            text_color="gray",
            anchor="w"
        )
        category_label.pack(anchor="w", pady=(2, 4))

        # Price label
        price_label = ctk.CTkLabel(
            left_frame,
            text=f"${float(item['Price']):.2f}",
            font=("Poppins", 14, "bold"),  # Adjusted font size
            text_color="#2B2B2B",
            anchor="w"
        )
        price_label.pack(anchor="w")

        # Right frame for edit button
        right_frame = ctk.CTkFrame(
            bottom_frame,
            fg_color="transparent",
            width=100
        )
        right_frame.pack(side="right", fill="y")
        right_frame.pack_propagate(False)

        # Edit button
        edit_button = ctk.CTkButton(
            right_frame,
            text="Edit",
            font=("Poppins", 12),
            fg_color="#F1D94B",
            text_color="black",
            hover_color="#E5CE45",
            width=60,
            height=32,
            corner_radius=8,
            command=lambda: self.edit_item(item)
        )
        edit_button.pack(anchor="center", pady=5)

        # Configure grid weights for proper spacing
        self.items_frame.grid_columnconfigure(col, weight=1)
        self.items_frame.grid_rowconfigure(row, weight=1)

    def load_menu_items(self, clear=True):
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor(dictionary=True)

            # Get total count
            cursor.execute("SELECT COUNT(*) as count FROM Menu")
            self.total_items = cursor.fetchone()["count"]

            # Get paginated items
            cursor.execute("""
                SELECT MenuID, Name, Description, Price, Category, ImagePath
                FROM Menu 
                ORDER BY Name 
                LIMIT %s OFFSET %s
            """, (self.page_size, self.current_page * self.page_size))

            items = cursor.fetchall()

            # Update items count label
            self.items_count_label.configure(text=f"{self.total_items} items found")

            # Clear existing items if needed
            if clear:
                for widget in self.items_frame.winfo_children():
                    widget.destroy()

            # Update grid configuration for 2 columns instead of 3
            self.items_frame.grid_columnconfigure(0, weight=1)
            self.items_frame.grid_columnconfigure(1, weight=1)

            # Create grid of items
            row = len(self.items_frame.winfo_children()) // 3     # Changed from 3 to 2
            col = len(self.items_frame.winfo_children()) % 3  # Changed from 3 to 2

            for item in items:
                self.create_menu_item_card(item, row, col)
                col += 1
                if col == 3:
                    col = 0
                    row += 1

            # Update load more button
            remaining_items = self.total_items - ((self.current_page + 1) * self.page_size)
            if remaining_items > 0:
                self.load_more_button.configure(text=f"Load More ({remaining_items} items)")
                self.load_more_button.pack()
            else:
                self.load_more_button.pack_forget()

            conn.close()

        except mysql.connector.Error as err:
            print(f"Database Error: {err}")

    def load_more_items(self):
        self.current_page += 1
        self.load_menu_items(clear=False)

    def filter_items(self, search_term=""):
        search_term = search_term.strip().lower()

        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor(dictionary=True)

            # Reset pagination
            self.current_page = 0

            # Base query
            query = "SELECT COUNT(*) as count FROM Menu WHERE 1=1"
            params = []

            # Add search condition if there's a search term
            if search_term:
                query += " AND (LOWER(Name) LIKE %s OR LOWER(Description) LIKE %s)"
                search_param = f"%{search_term}%"
                params.extend([search_param, search_param])

            # Add category condition if a specific category is selected
            if self.current_category != "All":
                query += " AND Category = %s"
                params.append(self.current_category)

            # Get total count
            cursor.execute(query, params)
            self.total_items = cursor.fetchone()["count"]

            # Modify query for item selection
            query = query.replace("COUNT(*) as count", "MenuID, Name, Description, Price, Category, ImagePath")
            query += " ORDER BY Name LIMIT %s OFFSET %s"
            params.extend([self.page_size, self.current_page * self.page_size])

            cursor.execute(query, params)
            items = cursor.fetchall()

            # Update items count
            self.items_count_label.configure(text=f"{self.total_items} items found")

            # Clear existing items
            for widget in self.items_frame.winfo_children():
                widget.destroy()

            # Update grid configuration for 2 columns instead of 3
            self.items_frame.grid_columnconfigure(0, weight=1)
            self.items_frame.grid_columnconfigure(1, weight=1)

            # Create grid of filtered items
            row = 0
            col = 0
            for item in items:
                self.create_menu_item_card(item, row, col)
                col += 1
                if col == 2:  # Changed from 3 to 2
                    col = 0
                    row += 1

            # Update load more button
            remaining_items = self.total_items - self.page_size
            if remaining_items > 0:
                self.load_more_button.configure(text=f"Load More ({remaining_items} items)")
                self.load_more_button.pack()
            else:
                self.load_more_button.pack_forget()

            conn.close()

        except mysql.connector.Error as err:
            print(f"Database Error: {err}")

    def show_add_item(self):
        # Create popup dialog
        dialog = ctk.CTkToplevel(self)
        dialog.title("Add New Item")
        dialog.geometry("400x500")
        dialog.resizable(False, False)

        # Make dialog modal
        dialog.grab_set()

        # Center dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() - 400) // 2
        y = (dialog.winfo_screenheight() - 500) // 2
        dialog.geometry(f"400x500+{x}+{y}")

        # Configure dialog appearance
        dialog.configure(fg_color="#F1D94B")

        # Title
        ctk.CTkLabel(
            dialog,
            text="+ Add New Menu Item",
            font=("Poppins", 20, "bold"),
            text_color="black"
        ).pack(pady=(20, 30))

        # Form fields
        fields = [
            ("Item Name", "name", "Enter item name"),
            ("Description", "description", "Enter description"),
            ("Price", "price", "Enter price"),
            ("Category", "category", "Enter category"),
            ("Image Path", "ImagePath", "Enter image path")
        ]

        # Dictionary to store entry widgets
        self.entries = {}

        # Create entry fields
        for label_text, key, placeholder in fields:
            container = ctk.CTkFrame(dialog, fg_color="transparent")
            container.pack(fill="x", padx=20, pady=5)

            entry = ctk.CTkEntry(
                container,
                placeholder_text=placeholder,
                height=35,
                fg_color="white",
                border_color="#E0E0E0",
                corner_radius=5
            )
            entry.pack(fill="x")

            self.entries[key] = entry

        # Buttons frame
        buttons_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        buttons_frame.pack(fill="x", padx=20, pady=(20, 0))

        # Cancel button
        ctk.CTkButton(
            buttons_frame,
            text="Cancel",
            font=("Poppins", 13),
            fg_color="white",
            text_color="black",
            hover_color="#E5E5E5",
            height=35,
            command=dialog.destroy
        ).pack(side="left", padx=(0, 10), expand=True)

        # Add Item button
        ctk.CTkButton(
            buttons_frame,
            text="+ Add Item",
            font=("Poppins", 13),
            fg_color="black",
            text_color="white",
            hover_color="#2B2B2B",
            height=35,
            command=lambda: self.add_menu_item(dialog)
        ).pack(side="left", expand=True)

    def add_menu_item(self, dialog):
        try:
            # Get values from entries
            name = self.entries["name"].get().strip()
            description = self.entries["description"].get().strip()
            price = self.entries["price"].get().strip()
            category = self.entries["category"].get().strip()
            imagePath = self.entries["ImagePath"].get().strip()

            # Validate required fields
            if not all([name, description, price, category, imagePath]):
                self.show_error(dialog, "Please fill in all fields")
                return

            # Validate price format
            try:
                price = float(price)
            except ValueError:
                self.show_error(dialog, "Price must be a valid number")
                return

            # Insert into database
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO Menu (Name, Description, Price, ImagePath, Category)
                VALUES (%s, %s, %s, %s, %s)
            """, (name, description, price, imagePath, category))

            conn.commit()
            conn.close()

            # Close dialog and refresh
            dialog.destroy()
            self.load_menu_items()

        except mysql.connector.Error as err:
            self.show_error(dialog, f"Database Error: {err}")

    def show_error(self, parent, message):
        if not hasattr(self, 'error_label'):
            self.error_label = ctk.CTkLabel(
                parent,
                text=message,
                text_color="red",
                font=("Poppins", 12)
            )
            self.error_label.pack(pady=(0, 10))
        else:
            self.error_label.configure(text=message)
            self.error_label.pack(pady=(0, 10))

    def edit_item(self, item):
        # Create popup dialog
        dialog = ctk.CTkToplevel(self)
        dialog.title("Edit Menu Item")
        dialog.geometry("400x500")
        dialog.resizable(False, False)

        # Make dialog modal
        dialog.grab_set()

        # Center dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() - 400) // 2
        y = (dialog.winfo_screenheight() - 500) // 2
        dialog.geometry(f"400x500+{x}+{y}")

        # Configure dialog appearance
        dialog.configure(fg_color="#F1D94B")

        # Title
        ctk.CTkLabel(
            dialog,
            text="Edit Menu Item",
            font=("Poppins", 20, "bold"),
            text_color="black"
        ).pack(pady=(20, 30))

        # Form fields
        fields = [
            ("Item Name", "name", item['Name']),
            ("Description", "description", item['Description']),
            ("Price", "price", str(item['Price'])),
            ("Category", "category", item['Category']),
            ("Image Path", "ImagePath", item['ImagePath'])
        ]

        # Dictionary to store entry widgets
        self.edit_entries = {}

        # Create entry fields
        for label_text, key, value in fields:
            container = ctk.CTkFrame(dialog, fg_color="transparent")
            container.pack(fill="x", padx=20, pady=5)

            ctk.CTkLabel(
                container,
                text=label_text,
                font=("Poppins", 12),
                text_color="black"
            ).pack(anchor="w")

            entry = ctk.CTkEntry(
                container,
                height=35,
                fg_color="white",
                border_color="#E0E0E0",
                corner_radius=5
            )
            entry.insert(0, value)  # Pre-fill with the current value
            entry.pack(fill="x")

            self.edit_entries[key] = entry

        # Buttons frame
        buttons_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        buttons_frame.pack(fill="x", padx=20, pady=(20, 0))

        # Cancel button
        ctk.CTkButton(
            buttons_frame,
            text="Cancel",
            font=("Poppins", 13),
            fg_color="white",
            text_color="black",
            hover_color="#E5E5E5",
            height=35,
            command=dialog.destroy
        ).pack(side="left", padx=(0, 10), expand=True)

        # Save Changes button
        ctk.CTkButton(
            buttons_frame,
            text="Save Changes",
            font=("Poppins", 13),
            fg_color="black",
            text_color="white",
            hover_color="#2B2B2B",
            height=35,
            command=lambda: self.update_menu_item(dialog, item['MenuID'])
        ).pack(side="left", expand=True)

    def update_menu_item(self, dialog, menu_id):
        try:
            # Get updated values from entries
            name = self.edit_entries["name"].get().strip()
            description = self.edit_entries["description"].get().strip()
            price = self.edit_entries["price"].get().strip()
            category = self.edit_entries["category"].get().strip()
            image_path = self.edit_entries["ImagePath"].get().strip()

            # Validate required fields
            if not all([name, description, price, category, image_path]):
                self.show_error(dialog, "Please fill in all fields")
                return

            # Validate price format
            try:
                price = float(price)
            except ValueError:
                self.show_error(dialog, "Price must be a valid number")
                return

            # Update the database
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor()

            cursor.execute("""
                UPDATE Menu
                SET Name = %s, Description = %s, Price = %s, Category = %s, ImagePath = %s
                WHERE MenuID = %s
            """, (name, description, price, category, image_path, menu_id))

            conn.commit()
            conn.close()

            # Close dialog and refresh items
            dialog.destroy()
            self.load_menu_items()

        except mysql.connector.Error as err:
            self.show_error(dialog, f"Database Error: {err}")

    def load_filter_icon(self):
        try:
            icon_path = "images/icons/filter.png"  # Make sure to have this icon
            icon_img = Image.open(icon_path)
            return ctk.CTkImage(light_image=icon_img, dark_image=icon_img, size=(20, 20))
        except:
            return None

    def show_category_dropdown(self):
        # Destroy existing dropdown if it exists
        if self.category_dropdown and self.category_dropdown.winfo_exists():
            self.category_dropdown.destroy()
            self.category_dropdown = None
            return

        # Get categories from the database
        categories = self.get_categories()

        # Create dropdown frame
        self.category_dropdown = ctk.CTkFrame(
            self.category_frame,
            fg_color="white",
            corner_radius=8,
            border_width=1,
            border_color="#E0E0E0",
            width=150,
            height=len(categories) * 35 + 35  # Adjust height based on number of categories
        )
        self.category_dropdown.place(relx=1, rely=1, anchor="ne")  # Position below the filter button

        # Add "All" option
        self.create_dropdown_item("All", self.category_dropdown)

        # Add category options
        for category in categories:
            self.create_dropdown_item(category, self.category_dropdown)

    def create_dropdown_item(self, category, parent):
        item = ctk.CTkButton(
            parent,
            text=category,
            font=("Poppins", 12),
            fg_color="transparent",
            text_color="black",
            hover_color="#F1D94B",
            anchor="w",
            height=35,
            width=146,  # Slightly less than parent width
            command=lambda: self.select_category(category)
        )
        item.pack(fill="x", padx=2, pady=1)

    # Add this method to handle clicking outside the dropdown
    def bind_click_outside(self):
        def on_click_outside(event):
            if self.category_dropdown and self.category_dropdown.winfo_exists():
                if not (hasattr(event, 'widget') and 
                    (event.widget == self.category_dropdown or 
                     event.widget in self.category_dropdown.winfo_children())):
                    self.category_dropdown.destroy()

        self.bind('<Button-1>', on_click_outside)
        for child in self.winfo_children():
            child.bind('<Button-1>', on_click_outside)

    def select_category(self, category):
        self.current_category = category
        if self.category_dropdown:
            self.category_dropdown.destroy()
            self.category_dropdown = None

        # Update filter button text to show selected category
        self.filter_btn.configure(text=f"Filter: {category}")

        # Reset pagination
        self.current_page = 0

        # Refresh items with category filter
        self.filter_items()

    def get_categories(self):
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor()

            cursor.execute("SELECT DISTINCT Category FROM Menu ORDER BY Category")
            categories = [category[0] for category in cursor.fetchall()]

            conn.close()
            return categories
        except mysql.connector.Error as err:
            print(f"Database Error: {err}")
            return []  # Return an empty list if there's an error
