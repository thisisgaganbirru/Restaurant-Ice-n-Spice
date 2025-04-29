import customtkinter as ctk
from utils import resize_image
import mysql.connector
from dbconnection import DB_CONFIG
from admin_stats import AdminStatsPage
from PIL import Image, UnidentifiedImageError
import os

class AdminDashboard(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.configure(fg_color="#F1E8DD")
        
        # Initialize variables
        self.page_size = 6
        self.current_page = 0
        self.total_items = 0
        self.current_category = "All"
        self.category_dropdown = None
        self.show_unavailable = False

        # Create main layout
        self.create_stats_section()
        self.create_menu_dashboard()

    def create_stats_section(self):
        # Stats Frame at top
        self.stats_frame = ctk.CTkFrame(self, fg_color="transparent", height=200)
        self.stats_frame.pack(fill="x")
        self.stats_frame.pack_propagate(False)

        # Create AdminStatsPage instance
        AdminStatsPage(self.stats_frame, self.app)

        # Bottom border line
        border_line = ctk.CTkFrame(self, fg_color="grey", height=2)
        border_line.pack(fill="x", padx=20)

    def create_menu_dashboard(self):
        # Menu Dashboard Frame
        self.menu_dashboard_frame = ctk.CTkFrame(self, fg_color="#F1E8DD")
        self.menu_dashboard_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Create header and search section
        self.create_header_section()
        
        # Create actions section
        self.create_actions_section()
        
        # Create items display section
        self.create_items_section()

    def create_header_section(self):
        # Header frame
        header_frame = ctk.CTkFrame(self.menu_dashboard_frame, 
            fg_color="#F1D94B", 
            height=50)
        header_frame.pack(fill="x", padx=5, pady=10)
        header_frame.pack_propagate(False)

        # Title
        ctk.CTkLabel(
            header_frame,
            text=" Admin Menu Dashboard",
            font=("Poppins", 24, "bold"),
            text_color="Black"
        ).pack(side="left", padx=10)

        # Sub-frame for search and buttons
        sub_frame = ctk.CTkFrame(self.menu_dashboard_frame, fg_color="transparent", height=50)
        sub_frame.pack(fill="x", padx=20, pady=5)
        sub_frame.pack_propagate(False)

        # Left side - Search section
        search_frame = ctk.CTkFrame(sub_frame, fg_color="transparent")
        search_frame.pack(side="left")

        self.search_var = ctk.StringVar()
        search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="Search menu items...",
            width=200,
            height=35
        )
        search_entry.pack(side="left", padx=(0, 10))

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
            command=lambda: self.filter_items(self.search_var.get())
        ).pack(side="left")

        # Right side - Filter and Add Item buttons
        buttons_frame = ctk.CTkFrame(sub_frame, fg_color="transparent")
        buttons_frame.pack(side="right")

        # Filter button
        self.filter_btn = ctk.CTkButton(
            buttons_frame,
            text="Filter Menu",
            font=("Poppins", 12),
            fg_color="#2B2B2B",
            text_color="white",
            hover_color="#3B3B3B",
            width=100,
            height=35,
            command=self.show_category_dropdown
        )
        self.filter_btn.pack(side="left", padx=10)

        # Add Item button
        ctk.CTkButton(
            buttons_frame,
            text="+ Add Item",
            font=("Poppins", 12),
            fg_color="#F1D94B",
            text_color="black",
            hover_color="#E5CE45",
            width=120,
            height=35,
            command=self.show_add_item
        ).pack(side="left")

    def create_actions_section(self):
        # Actions frame for item count
        actions_frame = ctk.CTkFrame(self.menu_dashboard_frame, fg_color="transparent", height=20)
        actions_frame.pack(fill="x", padx=20)
        actions_frame.pack_propagate(False)

        # Items count label
        self.items_count_label = ctk.CTkLabel(
            actions_frame,
            text="0 items found",
            font=("Poppins", 14),
            text_color="gray"
        )
        self.items_count_label.pack(anchor="w", padx=20, pady=(5, 5))

    def create_items_section(self):
        # Scrollable frame for menu items
        self.items_frame = ctk.CTkScrollableFrame(
            self.menu_dashboard_frame,
            fg_color="transparent",
            height=400
        )
        self.items_frame.pack(fill="both", expand=True, padx=20)

        # Load more button frame
        self.load_more_frame = ctk.CTkFrame(self.menu_dashboard_frame, fg_color="transparent")
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

        # Load initial items
        self.load_menu_items()

    def filter_items(self, search_term=""):
        """Filter menu items based on search term and category"""
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor(dictionary=True)

            # Base query
            if hasattr(self, 'show_unavailable') and self.show_unavailable:
                query = "SELECT COUNT(*) as count FROM Menu WHERE Available = FALSE"
            else:
                query = "SELECT COUNT(*) as count FROM Menu WHERE Available = TRUE"
            
            params = []

            # Add search condition if there's a search term
            if search_term:
                query += " AND (LOWER(Name) LIKE %s OR LOWER(Description) LIKE %s)"
                search_param = f"%{search_term.lower()}%"
                params.extend([search_param, search_param])

            # Add category filter if not "All" and not showing unavailable
            if self.current_category != "All" and not (hasattr(self, 'show_unavailable') and self.show_unavailable):
                query += " AND Category = %s"
                params.append(self.current_category)

            # Get total count
            cursor.execute(query, params)
            self.total_items = cursor.fetchone()["count"]

            # Update query for items
            query = query.replace("COUNT(*) as count", "*")
            query += " ORDER BY Name LIMIT %s OFFSET %s"
            params.extend([self.page_size, self.current_page * self.page_size])

            cursor.execute(query, params)
            items = cursor.fetchall()

            # Update items count label
            self.items_count_label.configure(text=f"{self.total_items} items found")

            # Clear existing items
            for widget in self.items_frame.winfo_children():
                widget.destroy()

            # Create grid of items
            row = 0
            col = 0
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

    def show_category_dropdown(self):
        """Show dropdown menu for category filtering"""
        if self.category_dropdown and self.category_dropdown.winfo_exists():
            self.category_dropdown.destroy()
            self.category_dropdown = None
            return

        # Get button position
        button_x = self.filter_btn.winfo_rootx()
        button_y = self.filter_btn.winfo_rooty()
        button_height = self.filter_btn.winfo_height()

        # Create main dropdown window
        self.category_dropdown = ctk.CTkToplevel(self)
        self.category_dropdown.withdraw()  # Hide initially
        self.category_dropdown.overrideredirect(True)  # Remove window decorations
        
        # Create main frame with yellow theme
        dropdown_frame = ctk.CTkFrame(
            self.category_dropdown,
            fg_color="#FFF9E5",  # Light yellow background
            corner_radius=8,
            border_width=1,
            border_color="#F1D94B"  # Yellow border
        )
        dropdown_frame.pack(fill="both", expand=True, padx=2, pady=2)

        # Categories Section
        category_section = ctk.CTkFrame(dropdown_frame, fg_color="transparent")
        category_section.pack(fill="x", padx=2, pady=2)

        ctk.CTkLabel(
            category_section,
            text="Categories",
            font=("Poppins", 12, "bold"),
            text_color="#2B2B2B",
            fg_color="#F1D94B"  # Yellow background
        ).pack(fill="x", padx=4, pady=(4, 2))

        # Add "All" option
        self.create_dropdown_item("All", category_section)

        # Add active categories
        categories = self.get_categories()
        for category in categories:
            self.create_dropdown_item(category, category_section)

        # Separator with padding
        separator = ctk.CTkFrame(
            dropdown_frame,
            height=2,
            fg_color="#F1D94B"  # Yellow separator
        )
        separator.pack(fill="x", padx=10, pady=8)

        # Unavailable Items Section
        unavailable_section = ctk.CTkFrame(dropdown_frame, fg_color="transparent")
        unavailable_section.pack(fill="x", padx=2, pady=2)

        ctk.CTkLabel(
            unavailable_section,
            text="Unavailable Items",
            font=("Poppins", 12, "bold"),
            text_color="#2B2B2B",
            fg_color="#F1D94B"  # Yellow background
        ).pack(fill="x", padx=4, pady=(4, 2))

        # Get unavailable items count
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM Menu WHERE Available = FALSE")
            unavailable_count = cursor.fetchone()[0]
            conn.close()

            # Show unavailable items option with count
            self.create_dropdown_item(
                f"Show Unavailable ({unavailable_count})", 
                unavailable_section, 
                is_unavailable=True
            )
        except mysql.connector.Error:
            self.create_dropdown_item("Show Unavailable", unavailable_section, is_unavailable=True)

        # Update dropdown size and position
        self.category_dropdown.update_idletasks()
        dropdown_width = max(200, self.filter_btn.winfo_width())
        dropdown_height = dropdown_frame.winfo_reqheight() + 4  # Add padding
        self.category_dropdown.geometry(f"{dropdown_width}x{dropdown_height}+{button_x}+{button_y + button_height + 2}")
        
        # Show dropdown
        self.category_dropdown.deiconify()

        # Bind click outside to close dropdown
        def on_click_outside(event):
            if self.category_dropdown and self.category_dropdown.winfo_exists():
                x, y = event.x_root, event.y_root
                if not (button_x <= x <= button_x + dropdown_width and
                       button_y <= y <= button_y + button_height + dropdown_height):
                    self.category_dropdown.destroy()
                    self.category_dropdown = None

        self.category_dropdown.bind("<FocusOut>", on_click_outside)
        self.bind("<Button-1>", on_click_outside)

    def create_dropdown_item(self, category, parent, is_unavailable=False):
        """Create individual dropdown items"""
        item = ctk.CTkButton(
            parent,
            text=category,
            font=("Poppins", 12),
            fg_color="transparent",
            text_color="#FF6B6B" if is_unavailable else "#2B2B2B",
            hover_color="#F1D94B",  # Yellow hover
            anchor="w",
            height=35,
            command=lambda: self.select_category(category, is_unavailable)
        )
        item.pack(fill="x", padx=2, pady=1)

    def select_category(self, category, is_unavailable=False):
        """Handle category selection"""
        self.current_category = category
        self.show_unavailable = is_unavailable
        
        if self.category_dropdown:
            self.category_dropdown.destroy()
            self.category_dropdown = None

        button_text = "Show Unavailable" if is_unavailable else f"Filter: {category}"
        self.filter_btn.configure(text=button_text)
        
        self.current_page = 0
        self.filter_items()

    def get_categories(self):
        """Fetch distinct categories from database"""
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

    def load_more_items(self):
        """Load next page of items"""
        self.current_page += 1
        self.filter_items()

    def show_add_item(self):
        """Show dialog to add new menu item"""
        dialog = ctk.CTkToplevel(self)
        dialog.title("Add Menu Item")
        dialog.geometry("400x600")
        dialog.resizable(False, False)
        dialog.configure(fg_color="#F1D94B")  # Match main window color

        # Make dialog modal
        dialog.grab_set()
        dialog.focus_set()

        # Center dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() - 400) // 2
        y = (dialog.winfo_screenheight() - 600) // 2
        dialog.geometry(f"400x600+{x}+{y}")

        # Title
        ctk.CTkLabel(
            dialog,
            text="Add New Menu Item",
            font=("Poppins", 20, "bold"),
            text_color="#2B2B2B"
        ).pack(pady=20)

        # Form container with background color
        form_container = ctk.CTkFrame(dialog, fg_color="#F1D94B")
        form_container.pack(fill="both", expand=True, padx=20)

        # Form fields
        fields = [
            ("Item Name", "name"),
            ("Description", "description"),
            ("Price", "price"),
            ("Category", "category"),
            ("Image Path", "image_path")
        ]

        self.add_item_entries = {}
        
        for label_text, key in fields:
            container = ctk.CTkFrame(form_container, fg_color="transparent")
            container.pack(fill="x", pady=5)

            ctk.CTkLabel(
                container,
                text=label_text,
                font=("Poppins", 12),
                text_color="#2B2B2B"
            ).pack(anchor="w")

            entry = ctk.CTkEntry(
                container, 
                height=35,
                fg_color="white",
                border_color="#E0E0E0",
                text_color="#2B2B2B"
            )
            entry.pack(fill="x", pady=(0, 5))
            self.add_item_entries[key] = entry

        # Buttons frame
        buttons_frame = ctk.CTkFrame(form_container, fg_color="transparent")
        buttons_frame.pack(fill="x", pady=20)

        ctk.CTkButton(
            buttons_frame,
            text="Cancel",
            font=("Poppins", 12),
            fg_color="white",
            border_width=1,
            border_color="#E0E0E0",
            text_color="black",
            hover_color="#F5F5F5",
            command=dialog.destroy
        ).pack(side="left", expand=True, padx=5)

        ctk.CTkButton(
            buttons_frame,
            text="Add Item",
            font=("Poppins", 12),
            fg_color="black",
            text_color="white",
            hover_color="#F1D94B",
            command=lambda: self.add_menu_item(dialog)
        ).pack(side="left", expand=True, padx=5)

    def create_menu_item_card(self, item, row, col):
        """Create a menu item card"""
        # Create card frame
        card = ctk.CTkFrame(
            self.items_frame,
            fg_color="white",
            corner_radius=15,
            border_width=2,
            border_color="#F1D94B",
            width=200,
            height=250
        )
        card.grid(row=row, column=col, padx=15, pady=15, sticky="nsew")
        card.grid_propagate(False)

        # Image frame
        image_frame = ctk.CTkFrame(
            card,
            fg_color="#F9F9F9",
            height=120,
            corner_radius=12
        )
        image_frame.pack(fill="x", padx=10, pady=10)
        image_frame.pack_propagate(False)

        try:
            # Use the utils.resize_image function
            photo = resize_image((100, 100), item['ImagePath'])
            if photo:
                # Convert PIL image to CTkImage
                ctk_image = ctk.CTkImage(
                    light_image=Image.open(item['ImagePath']),
                    dark_image=Image.open(item['ImagePath']),
                    size=(100, 100)
                )
                image_label = ctk.CTkLabel(
                    image_frame,
                    image=ctk_image,
                    text=""
                )
                image_label.place(relx=0.5, rely=0.5, anchor="center")
            else:
                raise FileNotFoundError("Image could not be loaded")

        except Exception as e:
            print(f"Image error for {item['Name']}: {str(e)}")
            self.create_placeholder_image(image_frame)

        # Info frame with top and bottom sections
        info_frame = ctk.CTkFrame(
            card,
            fg_color="transparent",
            height=120
        )
        info_frame.pack(fill="x", padx=10, pady=(0, 10))
        info_frame.pack_propagate(False)

        # Name section at top
        name_label = ctk.CTkLabel(
            info_frame,
            text=item['Name'][:22] + ('...' if len(item['Name']) > 22 else ''),
            font=("Poppins", 14, "bold"),
            text_color="#2B2B2B",
            anchor="w"
        )
        name_label.pack(anchor="w", pady=(0, 5))

        # Bottom section with category, price and edit button
        bottom_frame = ctk.CTkFrame(info_frame, fg_color="transparent")
        bottom_frame.pack(fill="x")

        # Left side info (category and price)
        left_info = ctk.CTkFrame(bottom_frame, fg_color="transparent")
        left_info.pack(side="left", fill="both", expand=True)

        ctk.CTkLabel(
            left_info,
            text=item['Category'],
            font=("Poppins", 12),
            text_color="gray",
            anchor="w"
        ).pack(anchor="w")

        ctk.CTkLabel(
            left_info,
            text=f"${float(item['Price']):.2f}",
            font=("Poppins", 14, "bold"),
            text_color="#2B2B2B",
            anchor="w"
        ).pack(anchor="w")

        # Button on right - different based on availability
        if hasattr(self, 'show_unavailable') and self.show_unavailable:
            # Add Back button for unavailable items
            ctk.CTkButton(
                bottom_frame,
                text="Add Back",
                font=("Poppins", 12),
                fg_color="#2ECC71",  # Green color
                text_color="white",
                hover_color="#27AE60",
                width=80,
                height=32,
                corner_radius=8,
                command=lambda: self.restore_menu_item(item['MenuID'])
            ).pack(side="right", pady=5)
        else:
            # Edit button for available items
            ctk.CTkButton(
                bottom_frame,
                text="Edit",
                font=("Poppins", 12),
                fg_color="#F1D94B",
                text_color="black",
                hover_color="#E5CE45",
                width=60,
                height=32,
                corner_radius=8,
                command=lambda: self.edit_item(item)
            ).pack(side="right", pady=5)

    def load_menu_items(self, clear=True):
        """Load initial menu items"""
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor(dictionary=True)

            # Get total count
            cursor.execute("SELECT COUNT(*) as count FROM Menu WHERE Available = TRUE")
            self.total_items = cursor.fetchone()["count"]

            # Get paginated items - only show available items
            cursor.execute("""
                SELECT MenuID, Name, Description, Price, Category, ImagePath
                FROM Menu 
                WHERE Available = TRUE
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

            # Create grid of items
            row = 0
            col = 0
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

    def add_menu_item(self, dialog):
        """Add new menu item to database"""
        try:
            # Get values from entry fields
            data = {
                'name': self.add_item_entries["name"].get().strip(),
                'description': self.add_item_entries["description"].get().strip(),
                'price': self.add_item_entries["price"].get().strip(),
                'category': self.add_item_entries["category"].get().strip(),
                'image_path': self.add_item_entries["image_path"].get().strip()
            }

            # Validate input
            if not self.validate_menu_item(dialog, data):
                return

            # Add to database
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO Menu (Name, Description, Price, Category, ImagePath)
                VALUES (%s, %s, %s, %s, %s)
            """, (data['name'], data['description'], float(data['price']), 
                  data['category'], data['image_path']))

            conn.commit()
            conn.close()

            # Show success message
            self.show_success(dialog, "Menu item added successfully!")

            # Close dialog after 2 seconds and refresh items
            dialog.after(2000, lambda: [dialog.destroy(), 
                                      self.set_current_page(0),
                                      self.load_menu_items()])

        except mysql.connector.Error as err:
            self.show_error(dialog, f"Database Error: {err}")

    def edit_item(self, item):
        """Show dialog to edit menu item"""
        dialog = ctk.CTkToplevel(self)
        dialog.title("Edit Menu Item")
        dialog.geometry("400x600")
        dialog.resizable(False, False)
        dialog.configure(fg_color="#F1D94B")  # Match main window color

        # Make dialog modal
        dialog.grab_set()  # This makes the dialog modal
        dialog.focus_set()  # This gives focus to the dialog

        # Center dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() - 400) // 2
        y = (dialog.winfo_screenheight() - 600) // 2
        dialog.geometry(f"400x600+{x}+{y}")

        # Title
        ctk.CTkLabel(
            dialog,
            text="Edit Menu Item",
            font=("Poppins", 20, "bold"),
            text_color="#2B2B2B"
        ).pack(pady=20)

        # Form container with background color
        form_container = ctk.CTkFrame(dialog, fg_color="#F1D94B")
        form_container.pack(fill="both", expand=True, padx=20)

        # Form fields
        fields = [
            ("Item Name", "name", item['Name']),
            ("Description", "description", item['Description']),
            ("Price", "price", str(item['Price'])),
            ("Category", "category", item['Category']),
            ("Image Path", "image_path", item['ImagePath'])
        ]

        self.edit_entries = {}

        for label_text, key, value in fields:
            container = ctk.CTkFrame(form_container, fg_color="transparent")
            container.pack(fill="x", pady=5)

            ctk.CTkLabel(
                container,
                text=label_text,
                font=("Poppins", 12),
                text_color="#2B2B2B"
            ).pack(anchor="w")

            entry = ctk.CTkEntry(
                container, 
                height=35,
                fg_color="white",
                border_color="#E0E0E0",
                text_color="#2B2B2B"
            )
            entry.insert(0, value)
            entry.pack(fill="x", pady=(0, 5))
            self.edit_entries[key] = entry

        # Add a separator before remove button
        separator = ctk.CTkFrame(
            form_container,
            height=2,
            fg_color="grey"
        )
        separator.pack(fill="x", pady=20)

        # Add Remove Item button
        remove_button = ctk.CTkButton(
            form_container,
            text="Remove Item",
            font=("Poppins", 12),
            fg_color="#FF6B6B",  # Red color for warning
            text_color="white",
            hover_color="#FF5252",
            command=lambda: self.remove_menu_item(dialog, item['MenuID'])
        )
        remove_button.pack(pady=(0, 5))

        # Buttons frame
        buttons_frame = ctk.CTkFrame(form_container, fg_color="transparent")
        buttons_frame.pack(fill="x", pady=20)

        ctk.CTkButton(
            buttons_frame,
            text="Cancel",
            font=("Poppins", 12),
            fg_color="white",
            border_width=1,
            border_color="#E0E0E0",
            text_color="black",
            hover_color="#F5F5F5",
            command=dialog.destroy
        ).pack(side="left", expand=True, padx=5)

        ctk.CTkButton(
            buttons_frame,
            text="Save Changes",
            font=("Poppins", 12),
            fg_color="black",
            text_color="white",
            hover_color="#F1D94B",
            command=lambda: self.update_menu_item(dialog, item['MenuID'])
        ).pack(side="left", expand=True, padx=5)

    def update_menu_item(self, dialog, menu_id):
        """Update existing menu item in database"""
        try:
            # Get values from entry fields
            name = self.edit_entries["name"].get().strip()
            description = self.edit_entries["description"].get().strip()
            price = self.edit_entries["price"].get().strip()
            category = self.edit_entries["category"].get().strip()
            image_path = self.edit_entries["image_path"].get().strip()

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

            # Update database
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
            self.show_success(dialog, "Menu item updated successfully!")  # Show success message

        except mysql.connector.Error as err:
            self.show_error(dialog, f"Database Error: {err}")

    def remove_menu_item(self, dialog, menu_id):
        """Mark menu item as unavailable"""
        try:
            # Show confirmation dialog
            if not self.show_confirmation(dialog, "Are you sure you want to remove this item?"):
                return

            # Update database to mark item as unavailable
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor()

            cursor.execute("""
                UPDATE Menu
                SET Available = FALSE
                WHERE MenuID = %s
            """, (menu_id,))

            conn.commit()
            conn.close()

            # Show success message
            self.show_success(dialog, "Item removed successfully!")

            # Close dialog and refresh items after 2 seconds
            dialog.after(2000, lambda: [
                dialog.destroy(),
                self.load_menu_items()
            ])

        except mysql.connector.Error as err:
            self.show_error(dialog, f"Database Error: {err}")

    def restore_menu_item(self, menu_id):
        """Restore unavailable menu item back to available"""
        try:
            # Show confirmation dialog
            if not self.show_confirmation(self, "Are you sure you want to add this item back to the menu?"):
                return

            # Update database to mark item as available
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor()

            cursor.execute("""
                UPDATE Menu
                SET Available = TRUE
                WHERE MenuID = %s
            """, (menu_id,))

            conn.commit()
            conn.close()

            # Show success message in a small popup
            success_dialog = ctk.CTkToplevel(self)
            success_dialog.title("Success")
            success_dialog.geometry("300x100")
            success_dialog.resizable(False, False)
            success_dialog.configure(fg_color="#F1E8DD")
            success_dialog.grab_set()

            ctk.CTkLabel(
                success_dialog,
                text="Item restored successfully!",
                font=("Poppins", 12),
                text_color="#2ECC71"
            ).pack(pady=20)

            # Auto close success dialog and refresh items
            success_dialog.after(2000, lambda: [
                success_dialog.destroy(),
                self.filter_items()  # Refresh the current view
            ])

        except mysql.connector.Error as err:
            print(f"Database Error: {err}")
            self.show_error(self, "Failed to restore item")

    def show_confirmation(self, parent, message):
        """Show confirmation dialog"""
        confirm_dialog = ctk.CTkToplevel(parent)
        confirm_dialog.title("Confirm Action")
        confirm_dialog.geometry("300x150")
        confirm_dialog.resizable(False, False)
        confirm_dialog.configure(fg_color="#F1D94B")
        
        # Make dialog modal
        confirm_dialog.grab_set()
        confirm_dialog.focus_set()
        
        # Center dialog
        confirm_dialog.update_idletasks()
        x = (confirm_dialog.winfo_screenwidth() - 300) // 2
        y = (confirm_dialog.winfo_screenheight() - 150) // 2
        confirm_dialog.geometry(f"300x150+{x}+{y}")
        
        # Message
        ctk.CTkLabel(
            confirm_dialog,
            text=message,
            font=("Poppins", 12),
            text_color="#2B2B2B"
        ).pack(pady=20)
        
        # Result list (using list instead of dict to store result)
        result = [False]
        
        # Buttons
        buttons_frame = ctk.CTkFrame(confirm_dialog, fg_color="transparent")
        buttons_frame.pack(fill="x", padx=20, pady=10)
        
        def on_cancel():
            result[0] = False
            confirm_dialog.destroy()
            
        def on_confirm():
            result[0] = True
            confirm_dialog.destroy()
        
        ctk.CTkButton(
            buttons_frame,
            text="Cancel",
            font=("Poppins", 12),
            fg_color="transparent",
            border_width=1,
            border_color="#E0E0E0",
            text_color="black",
            hover_color="#F5F5F5",
            command=on_cancel
        ).pack(side="left", expand=True, padx=5)
        
        ctk.CTkButton(
            buttons_frame,
            text="Confirm",
            font=("Poppins", 12),
            fg_color="#FF6B6B",
            text_color="white",
            hover_color="#FF5252",
            command=on_confirm
        ).pack(side="left", expand=True, padx=5)
        
        # Wait for dialog to close
        parent.wait_window(confirm_dialog)
        return result[0]

    def show_error(self, parent, message):
        """Display error message in dialog"""
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

    def show_success(self, parent, message):
        """Display success message in dialog"""
        success_frame = ctk.CTkFrame(
            parent,
            fg_color="#E8F5E9",
            corner_radius=6,
            border_width=1,
            border_color="#A5D6A7"
        )
        success_frame.pack(fill="x", padx=20, pady=(0, 10))

        ctk.CTkLabel(
            success_frame,
            text=message,
            text_color="#2E7D32",
            font=("Poppins", 12)
        ).pack(pady=10)

        # Auto-hide after 3 seconds
        parent.after(3000, success_frame.destroy)

    def validate_menu_item(self, dialog, data):
        """Validate menu item data"""
        errors = []
        
        # Check required fields
        if not all([data['name'], data['description'], data['price'], 
                    data['category'], data['image_path']]):
            errors.append("All fields are required")
            
        # Validate price
        try:
            price = float(data['price'])
            if price <= 0:
                errors.append("Price must be greater than 0")
        except ValueError:
            errors.append("Price must be a valid number")
            
        # Validate name length
        if len(data['name']) > 50:
            errors.append("Name must be less than 50 characters")
            
        # Validate image using utils.resize_image
        if not resize_image((100, 100), data['image_path']):
            errors.append("Invalid image file or format")
            
        # Show errors if any
        if errors:
            self.show_error(dialog, "\n".join(errors))
            return False
            
        return True

    def create_placeholder_image(self, parent):
        """Create placeholder for missing/invalid images"""
        no_image_frame = ctk.CTkFrame(
            parent,
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
