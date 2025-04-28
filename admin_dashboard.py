from admin_base import AdminBasePage
import customtkinter as ctk
from utils import resize_image 
import os
<<<<<<< Updated upstream
=======
from dbconnection import DB_CONFIG
import mysql.connector
from PIL import Image, ImageTk
from admin_stats import AdminStatsPage
>>>>>>> Stashed changes

class AdminHomePage(AdminBasePage):
    def __init__(self, parent, app):
<<<<<<< Updated upstream
        super().__init__(parent, app, "Dashboard")
        self.create_dashboard()

    def create_dashboard(self):
        # Stats container
        stats_frame = ctk.CTkFrame(self.main_content, fg_color="transparent")
        stats_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Create stat cards
        self.create_stat_card(stats_frame, "Total Orders", "156", "#4CAF50")
        self.create_stat_card(stats_frame, "Pending Orders", "23", "#FFA000")
        self.create_stat_card(stats_frame, "Total Revenue", "$2,345", "#2196F3")
        self.create_stat_card(stats_frame, "Total Items", "45", "#9C27B0")

        # Recent orders section
        orders_card = self.create_content_card("Recent Orders", height=300)
        orders_card.pack(fill="x", padx=20, pady=20)

        # Create scrollable frame for orders
        orders_list = ctk.CTkScrollableFrame(
            orders_card,
            fg_color="transparent",
            height=250
        )
        orders_list.pack(fill="both", expand=True, padx=15, pady=(0,10))

        # Sample orders (replace with actual data)
        for i in range(5):
            self.create_order_row(orders_list, f"#00000{i+1}", "Pending", f"${20+i}.99")

    def create_stat_card(self, parent, title, value, color):
        card = ctk.CTkFrame(
            parent,
            fg_color="#2b2b2b",
            corner_radius=10,
            width=200,
            height=100
        )
        card.pack(side="left", padx=10, pady=10)
        card.pack_propagate(False)

        ctk.CTkLabel(
            card,
            text=title,
=======
        super().__init__(parent)
        self.app = app
        self.configure(fg_color="#F1E8DD")
  
        # Create dashboard content
        self._create_dashboard_ui()

    def _create_dashboard_ui(self):
        # Stats Frame at top
        self.stats_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.stats_frame.pack(fill="x")
        self.stats_frame.pack_propagate(False)
        
        # Create AdminStatsPage instance for stats
        AdminStatsPage(self.stats_frame, self.app)
        
        # Bottom border line
        border_line = ctk.CTkFrame(self, fg_color="grey", height=2)
        border_line.pack(fill="x", padx=2)

        # Menu Dashboard Frame  
        menu_dashboard_frame = ctk.CTkFrame(self, fg_color="#F1E8DD")
        menu_dashboard_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Header with title and search
        header_frame = ctk.CTkFrame(menu_dashboard_frame, fg_color="transparent", height=50)
        header_frame.pack(fill="x", padx=20, pady=10)
        header_frame.pack_propagate(False)
        
        # Title
        ctk.CTkLabel(
            header_frame,
            text="Menu Dashboard",
            font=("Poppins", 24, "bold"),
            text_color="#2B2B2B"
        ).pack(side="left")
        
        # Search frame
        search_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        search_frame.pack(side="right")
        
        # Search entry
        self.search_var = ctk.StringVar()
        self.search_var.trace("w", lambda *args: self.filter_items())
        self.search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="Search menu items...",
            width=200,
            height=35
        )
        self.search_entry.pack(side="left", padx=(0, 10))
        
        # Search button
        ctk.CTkButton(
            search_frame,
            text="Search",
            font=("Poppins", 12),
            fg_color="#F1D94B",
            text_color="black",
            hover_color="#E5CE45",
            width=100,
            height=35,
            command=self.filter_items
        ).pack(side="left")
        
        
        
        # Items count and Add Item button
        actions_frame = ctk.CTkFrame(menu_dashboard_frame, fg_color="transparent", height=40)
        actions_frame.pack(fill="x", padx=20, pady=10)
        actions_frame.pack_propagate(False)
        
        self.items_count_label = ctk.CTkLabel(
            actions_frame,
            text="0 items found",
>>>>>>> Stashed changes
            font=("Poppins", 14),
            text_color="gray"
        ).pack(anchor="w", padx=15, pady=(15,5))

        ctk.CTkLabel(
            card,
            text=value,
            font=("Poppins", 24, "bold"),
            text_color=color
        ).pack(anchor="w", padx=15)

    def create_order_row(self, parent, order_id, status, amount):
        row = ctk.CTkFrame(parent, fg_color="#333333", height=50)
        row.pack(fill="x", pady=2)
        row.pack_propagate(False)

        ctk.CTkLabel(
            row,
            text=order_id,
            font=("Poppins", 12),
<<<<<<< Updated upstream
            text_color="white"
        ).pack(side="left", padx=15)

        status_color = "#4CAF50" if status == "Completed" else "#FFA000"
        ctk.CTkLabel(
            row,
            text=status,
            font=("Poppins", 12),
            text_color=status_color
        ).pack(side="left", padx=15)

        ctk.CTkLabel(
            row,
            text=amount,
            font=("Poppins", 12),
            text_color="white"
        ).pack(side="right", padx=15)
=======
            fg_color="#F1D94B",
            text_color="black",
            hover_color="#E5CE45",
            width=100,
            height=35,
            command=self.show_add_item
        ).pack(side="right")

        # Filter by category button and dropdown
        self.category_frame = ctk.CTkFrame(actions_frame, fg_color="transparent")
        self.category_frame.pack(side="right", padx=10)
        
        # Create filter button with icon
        self.filter_btn = ctk.CTkButton(
            self.category_frame,
            text="Filter Menu",
            font=("Poppins", 12),
            fg_color="#2B2B2B",
            text_color="white",
            hover_color="#3B3B3B",
            width=150,
            height=35,
            image=self.load_filter_icon(),
            compound="right",
            command=self.show_category_dropdown
        )
        self.filter_btn.pack(side="right")
        
        # Bind click outside event
        self.bind_click_outside()
        
        # Create dropdown (initially hidden)
        self.category_dropdown = None
        self.current_category = "All"
        
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
        self.page_size = 6  # Changed from 9 to 6
        self.current_page = 0
        self.total_items = 0
        
        # Load initial items
        self.load_menu_items()

    def create_menu_item_card(self, item, row, col):
        # Create card frame
        card = ctk.CTkFrame(
            self.items_frame,
            fg_color="white",
            corner_radius=15,
            border_width=2,
            border_color="#F1D94B",
            width=225,  # Increased width
            height=225  # Increased height
        )
        card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
        card.grid_propagate(False)
        
        # Image frame
        image_frame = ctk.CTkFrame(
            card,
            fg_color="#F9F9F9",  # Light gray background
            height=120,          # Increased height
            corner_radius=12
        )
        image_frame.pack(fill="x", padx=8, pady=8)
        image_frame.pack_propagate(False)
        
        try:
            # Load and display item image
            image = Image.open(item['ImagePath'])
            photo = ctk.CTkImage(
                light_image=image,
                dark_image=image,
                corner_radius=10,
                size=(120, 120)  # Larger image size
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
                width=120,
                height=120
            )
            no_image_frame.place(relx=0.5, rely=0.5, anchor="center")
            
            ctk.CTkLabel(
                no_image_frame,
                text="No Image",
                font=("Poppins", 14),
                text_color="gray"
            ).place(relx=0.5, rely=0.5, anchor="center")
            
        # Content frame
        content_frame = ctk.CTkFrame(
            card,
            fg_color="transparent",
            height=80
        )
        content_frame.pack(fill="x", padx=12, pady=(0, 8))
        content_frame.pack_propagate(False)
        
        # Left side info
        info_frame = ctk.CTkFrame(
            content_frame,
            fg_color="transparent",
            width=180  # Fixed width for text
        )
        info_frame.pack(side="left", fill="y", padx=10)
        info_frame.pack_propagate(False)
        
        # Item name with ellipsis if too long
        name_label = ctk.CTkLabel(
            info_frame,
            text=item['Name'][:25] + ('...' if len(item['Name']) > 25 else ''),
            font=("Poppins", 16, "bold"),
            text_color="#2B2B2B",
            anchor="w"
        )
        name_label.pack(anchor="w")
        
        # Category label
        category_label = ctk.CTkLabel(
            info_frame,
            text=item['Category'],
            font=("Poppins", 12),
            text_color="gray",
            anchor="w"
        )
        category_label.pack(anchor="w", pady=(2, 4))
        
        # Price
        price_label = ctk.CTkLabel(
            info_frame,
            text=f"${float(item['Price']):.2f}",
            font=("Poppins", 15, "bold"),
            text_color="#2B2B2B",
            anchor="w"
        )
        price_label.pack(anchor="w")
        
        # Edit button frame
        button_frame = ctk.CTkFrame(
            content_frame,
            fg_color="transparent"
        )
        button_frame.pack(side="right", fill="y", padx=(0, 5))
        
        # Edit button
        edit_button = ctk.CTkButton(
            button_frame,
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
        edit_button.pack(side="right", pady=5)

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

    def filter_items(self, *args):
        search_term = self.search_entry.get().strip().lower()
        
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
            imagePath = self.entries["imagePath"].get().strip()
            
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
        # Implementation for editing items
        pass

    def load_filter_icon(self):
        try:
            icon_path = "images/icons/filter.png"  # Make sure to have this icon
            icon_img = Image.open(icon_path)
            return ctk.CTkImage(light_image=icon_img, dark_image=icon_img, size=(20, 20))
        except:
            return None

    def show_category_dropdown(self):
        if self.category_dropdown and self.category_dropdown.winfo_exists():
            self.category_dropdown.destroy()
            return

        # Get categories from database
        categories = self.get_categories()
        
        # Create dropdown frame with width and height in constructor
        self.category_dropdown = ctk.CTkFrame(
            self.category_frame,
                fg_color="white",
            corner_radius=8,
            border_width=1,
                border_color="#E0E0E0",
            width=150,  # Set width in constructor
            height=len(categories) * 35 + 35  # Height based on number of items
        )
        
        # Position the dropdown below the filter button
        button_x = self.category_frame.winfo_x()
        button_y = self.category_frame.winfo_y()
        self.category_dropdown.place(
            relx=1,
            rely=1,
            anchor="ne"
        )

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
            return []
>>>>>>> Stashed changes
