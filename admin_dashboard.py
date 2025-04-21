import customtkinter as ctk
from utils import resize_image 
import os
from admin_nav import AdminNav
from dbconnection import DB_CONFIG
import mysql.connector
from PIL import Image
from admin_stats import AdminStatsPage

class AdminDashboard(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.configure(fg_color="white")
        self.pack(fill="both", expand=True)
        
        # Create main container
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.pack(fill="both", expand=True)
        
        # Create layout
        self.create_header()
        self.create_dashboard_body()
        
    def create_header(self):
        # Nav on left
        AdminNav(self.main_container, app=self.app).pack(side="left", fill="y")
        
    def create_dashboard_body(self):
        self.body_frame = ctk.CTkFrame(self.main_container, fg_color="#F1E8DD")
        self.body_frame.pack(side="right", fill="both", expand=True)

        # Stats Frame
        self.stats_frame = ctk.CTkFrame(self.body_frame, fg_color="transparent")
        self.stats_frame.pack(fill="x")
        
        # Create AdminStatsPage instance for stats
        AdminStatsPage(self.stats_frame, self.app)
        
        # Bottom border line
        border_line = ctk.CTkFrame(self.body_frame, fg_color="#E0E0E0", height=2)
        border_line.pack(fill="x", padx=10)
        
        # Header with title and search
        header_frame = ctk.CTkFrame(self.body_frame, fg_color="transparent", height=50)
        header_frame.pack(fill="x", padx=10, pady=10)
        header_frame.pack_propagate(False)
        
        # Title
        ctk.CTkLabel(
            header_frame,
            text="Admin Dashboard",
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
            placeholder_text="search....",
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
        
        # Content Frame
        self.content_frame = ctk.CTkFrame(self.body_frame, fg_color="transparent")
        self.content_frame.pack(fill="both", expand=True, padx=20)
        
        # Items count and Add Item button
        actions_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent", height=40)
        actions_frame.pack(fill="x", pady=10)
        actions_frame.pack_propagate(False)
        
        self.items_count_label = ctk.CTkLabel(
            actions_frame,
            text="0 items found...",
            font=("Poppins", 14),
            text_color="gray"
        )
        self.items_count_label.pack(side="left")
        
        ctk.CTkButton(
            actions_frame,
            text="+ Add Item",
            font=("Poppins", 12),
            fg_color="#F1D94B",
            text_color="black",
            hover_color="#E5CE45",
            width=100,
            height=35,
            command=self.show_add_item
        ).pack(side="right")
        
        # Create scrollable frame for menu items
        self.items_frame = ctk.CTkScrollableFrame(
            self.content_frame,
            fg_color="transparent",
            height=400
        )
        self.items_frame.pack(fill="both", expand=True)
        
        # Load more button frame
        self.load_more_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
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
        self.page_size = 9  # 3x3 grid
        self.current_page = 0
        self.total_items = 0
        
        # Load initial items
        self.load_menu_items()

    def create_menu_item_card(self, item, row, col):
        try:
            print("Creating card for item:", item)  # Debug print
            
            card = ctk.CTkFrame(
                self.items_frame,
                fg_color="white",
                corner_radius=10,
                border_width=2,
                border_color="#F1D94B",
                width=200,
                height=200
            )
            card.grid(row=row, column=col, padx=10, pady=5, sticky="nsew")
            card.grid_propagate(False)
            
            image_frame = ctk.CTkFrame(
                card,
                fg_color="transparent",
                height=130,
                corner_radius=10
            )
            image_frame.pack(fill="x", padx=5, pady=5)
            image_frame.pack_propagate(False)
            
            try:
                # Load and display item image
                image = Image.open(item['Image_path'])
                photo = ctk.CTkImage(
                    light_image=image,
                    dark_image=image,
                    corner_radius=10,
                    size=(120, 120)
                )
                image_label = ctk.CTkLabel(
                    image_frame,
                    image=photo,
                    text=""
                )
                image_label.place(relx=0.5, rely=0.5, anchor="center")
            except Exception as e:
                print(f"Error loading image for {item['Name']}: {e}")
                # Show placeholder if image fails to load
                ctk.CTkLabel(
                    image_frame,
                    text="No Image",
                    font=("Poppins", 14),
                    text_color="gray"
                ).place(relx=0.5, rely=0.5, anchor="center")
            
            # Bottom frame
            bottom_frame = ctk.CTkFrame(
                card,
                fg_color="transparent",
                height=60
            )
            bottom_frame.pack(fill="x", padx=5)
            bottom_frame.pack_propagate(False)
            
            # Text frame
            text_frame = ctk.CTkFrame(
                bottom_frame,
                fg_color="transparent",
                width=150
            )
            text_frame.pack(side="left", fill="y")
            text_frame.pack_propagate(False)
            
            # Item name with ellipsis if too long
            name_label = ctk.CTkLabel(
                text_frame,
                text=item['Name'][:20] + ('...' if len(item['Name']) > 20 else ''),
                font=("Poppins", 16, "bold"),
                text_color="#2B2B2B"
            )
            name_label.pack(anchor="w")
            
            # Price
            price_label = ctk.CTkLabel(
                text_frame,
                text=f"${float(item['Price']):.2f}",
                font=("Poppins", 14),
                text_color="#2B2B2B"
            )
            price_label.pack(anchor="w", pady=(2, 0))
            
            # Edit button frame
            edit_frame = ctk.CTkFrame(
                bottom_frame,
                fg_color="transparent",
                width=50
            )
            edit_frame.pack(side="right", fill="y")
            edit_frame.pack_propagate(False)
            
            # Edit button
            edit_button = ctk.CTkButton(
                edit_frame,
                text="Edit",
                font=("Poppins", 12),
                fg_color="#F1D94B",
                text_color="black",
                hover_color="#E5CE45",
                width=45,
                height=28,
                corner_radius=8,
                command=lambda: self.edit_item(item)
            )
            edit_button.place(relx=0.5, rely=0.5, anchor="center")
            
        except Exception as e:
            print(f"Error creating card: {e}")

    def load_menu_items(self, clear=True):
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor(dictionary=True)
            
            # Get total count of items in the Menu table
            cursor.execute("""
                SELECT COUNT(*) AS count 
                FROM Menu
            """)
            self.total_items = cursor.fetchone()["count"]
            
            # Get paginated results from the Menu table
            cursor.execute("""
                SELECT 
                    MenuID,
                    Name,
                    Description,
                    Price,
                    Category,
                    ImagePath
                FROM Menu 
                ORDER BY Name 
                LIMIT %s OFFSET %s
            """, (self.page_size, self.current_page * self.page_size))
            
            items = cursor.fetchall()
            print("Fetched items:", items)  # Debug print
            
            conn.close()
            
            # Update items count
            self.items_count_label.configure(text=f"{self.total_items} items found")
            
            # Clear existing items if needed
            if clear:
                for widget in self.items_frame.winfo_children():
                    widget.destroy()
            
            # Create grid of items
            row = len(self.items_frame.winfo_children()) // 3
            col = len(self.items_frame.winfo_children()) % 3
            
            for item in items:
                self.create_menu_item_card(item, row, col)
                col += 1
                if col == 3:
                    col = 0
                    row += 1
            
            # Configure grid columns to be equal width
            self.items_frame.grid_columnconfigure(0, weight=1)
            self.items_frame.grid_columnconfigure(1, weight=1)
            self.items_frame.grid_columnconfigure(2, weight=1)
            
            # Update load more button visibility
            remaining_items = self.total_items - ((self.current_page + 1) * self.page_size)
            if remaining_items > 0:
                self.load_more_button.configure(text=f"Load More ({remaining_items} items)")
                self.load_more_button.pack()
            else:
                self.load_more_button.pack_forget()
                    
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
            
            if search_term:
                # Get filtered count
                cursor.execute("""
                    SELECT COUNT(*) AS count 
                    FROM Menu 
                    WHERE LOWER(Name) LIKE %s OR LOWER(Description) LIKE %s
                """, (f"%{search_term}%", f"%{search_term}%"))
                
                self.total_items = cursor.fetchone()["count"]
                
                # Get filtered items
                cursor.execute("""
                    SELECT 
                        MenuID,
                        Name,
                        Description,
                        Price,
                        Category,
                        ImagePath
                    FROM Menu 
                    WHERE LOWER(Name) LIKE %s OR LOWER(Description) LIKE %s
                    ORDER BY Name 
                    LIMIT %s
                """, (f"%{search_term}%", f"%{search_term}%", self.page_size))
            else:
                # Get total count
                cursor.execute("""
                    SELECT COUNT(*) AS count 
                    FROM Menu
                """)
                self.total_items = cursor.fetchone()["count"]
                
                # Get first page
                cursor.execute("""
                    SELECT 
                        MenuID,
                        Name,
                        Description,
                        Price,
                        Category,
                        ImagePath
                    FROM Menu 
                    ORDER BY Name 
                    LIMIT %s
                """, (self.page_size,))
                
            items = cursor.fetchall()
            conn.close()
            
            # Update items count
            self.items_count_label.configure(text=f"{self.total_items} items found")
            
            # Clear existing items
            for widget in self.items_frame.winfo_children():
                widget.destroy()
            
            # Create grid of filtered items
            row = 0
            col = 0
            for item in items:
                self.create_menu_item_card(item, row, col)
                col += 1
                if col == 3:
                    col = 0
                    row += 1
            
            # Update load more button visibility
            remaining_items = self.total_items - self.page_size
            if remaining_items > 0:
                self.load_more_button.configure(text=f"Load More ({remaining_items} items)")
                self.load_more_button.pack()
            else:
                self.load_more_button.pack_forget()
                    
        except mysql.connector.Error as err:
            print(f"Database Error: {err}")

    def show_add_item(self):
        # Create popup dialog
        dialog = ctk.CTkToplevel(self)
        dialog.title("")
        dialog.geometry("400x500")
        dialog.resizable(False, False)
        
        # Make dialog modal (disable main window while popup is open)
        dialog.grab_set()
        
        # Center the dialog on screen
        dialog.update_idletasks()
        screen_width = dialog.winfo_screenwidth()
        screen_height = dialog.winfo_screenheight()
        x = (screen_width - 400) // 2
        y = (screen_height - 500) // 2
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
        
        # Create form fields
        fields = [
            ("Item Name", "name", "Enter item name"),
            ("Description", "description", "Enter description"),
            ("Price", "price", "Enter price"),
            ("Category", "category", "Enter category"),
            ("Image Path", "imagePath", "Enter image path")
        ]
        
        # Dictionary to store entry widgets
        self.entries = {}
        
        # Create entry fields
        for label_text, key, placeholder in fields:
            # Entry container
            container = ctk.CTkFrame(dialog, fg_color="transparent")
            container.pack(fill="x", padx=20, pady=5)
            
            # Entry widget
            entry = ctk.CTkEntry(
                container,
                placeholder_text=placeholder,
                height=35,
                fg_color="white",
                border_color="#E0E0E0",
                corner_radius=5
            )
            entry.pack(fill="x")
            
            # Store entry widget reference
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
            
            # Connect to database
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor()
            
            # Insert new menu item
            query = """
                INSERT INTO Menu (Name, Description, Price, ImagePath, Category)
                VALUES (%s, %s, %s, %s, %s)
            """
            values = (name, description, price, imagePath, category)
            
            cursor.execute(query, values)
            conn.commit()
            conn.close()
            
            # Close dialog
            dialog.destroy()
            
            # Refresh menu items
            self.load_menu_items()
            
        except mysql.connector.Error as err:
            self.show_error(dialog, f"Database Error: {err}")
    
    def show_error(self, parent, message):
        # Create error label if it doesn't exist
        if not hasattr(self, 'error_label'):
            self.error_label = ctk.CTkLabel(
                parent,
                text=message,
                text_color="red",
                font=("Poppins", 12)
            )
            self.error_label.pack(pady=(0, 10))
        else:
            # Update existing error label
            self.error_label.configure(text=message)
            self.error_label.pack(pady=(0, 10))
        
    def edit_item(self, item):
        # Create popup dialog
        dialog = ctk.CTkToplevel(self)
        dialog.title("")
        dialog.geometry("400x550")
        dialog.resizable(False, False)
        
        # Make dialog modal
        dialog.grab_set()
        
        # Center the dialog
        dialog.update_idletasks()
        screen_width = dialog.winfo_screenwidth()
        screen_height = dialog.winfo_screenheight()
        x = (screen_width - 400) // 2
        y = (screen_height - 550) // 2
        dialog.geometry(f"400x550+{x}+{y}")
        
        # Configure dialog appearance
        dialog.configure(fg_color="#F1D94B")
        
        # Title
        ctk.CTkLabel(
            dialog,
            text="+ Update Menu Item",
            font=("Poppins", 20, "bold"),
            text_color="black"
        ).pack(pady=(20, 30))
        
        # Create form fields
        fields = [
            ("Item ID (Required)", "menuID", str(item['MenuID']), True),
            ("New Name (Optional)", "name", item['Name'], False),
            ("New description (Optional)", "description", item['Description'], False),
            ("New Price (Optional)", "price", str(item['Price']), False),
            ("New Category (Optional)", "category", item['Category'], False),
            ("New Image Path (Optional)", "imagePath", item['ImagePath'], False)
        ]
        
        # Dictionary to store entry widgets
        self.entries = {}
        
        # Create entry fields
        for label_text, key, default_value, readonly in fields:
            # Entry container
            container = ctk.CTkFrame(dialog, fg_color="transparent")
            container.pack(fill="x", padx=20, pady=5)
            
            # Entry widget
            entry = ctk.CTkEntry(
                container,
                placeholder_text=label_text,
                height=35,
                fg_color="white",
                border_color="#E0E0E0",
                corner_radius=5
            )
            entry.insert(0, default_value)
            if readonly:
                entry.configure(state="readonly")
            entry.pack(fill="x")
            
            # Store entry widget reference
            self.entries[key] = entry
        
        # Buttons frame
        buttons_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        buttons_frame.pack(fill="x", padx=20, pady=(20, 0))
        
        # Remove button
        ctk.CTkButton(
            buttons_frame,
            text="Remove Item",
            font=("Poppins", 13),
            fg_color="#FF0000",
            text_color="white",
            hover_color="#CC0000",
            height=35,
            command=lambda: self.show_remove_confirmation(dialog, item['MenuID'])
        ).pack(side="left", padx=(0, 10), expand=True)
        
        # Update button
        ctk.CTkButton(
            buttons_frame,
            text="+ Update Item",
            font=("Poppins", 13),
            fg_color="black",
            text_color="white",
            hover_color="#2B2B2B",
            height=35,
            command=lambda: self.update_menu_item(dialog, item['MenuID'])
        ).pack(side="left", expand=True)
        
        # Cancel button
        ctk.CTkButton(
            dialog,
            text="Cancel",
            font=("Poppins", 13),
            fg_color="white",
            text_color="black",
            hover_color="#E5E5E5",
            height=35,
            command=dialog.destroy
        ).pack(fill="x", padx=20, pady=10)

    def show_remove_confirmation(self, parent_dialog, menu_id):
        # Create confirmation dialog
        dialog = ctk.CTkToplevel(self)
        dialog.title("")
        dialog.geometry("300x200")
        dialog.resizable(False, False)
        
        # Make dialog modal
        dialog.grab_set()
        
        # Center the dialog
        dialog.update_idletasks()
        screen_width = dialog.winfo_screenwidth()
        screen_height = dialog.winfo_screenheight()
        x = (screen_width - 300) // 2
        y = (screen_height - 200) // 2
        dialog.geometry(f"300x200+{x}+{y}")
        
        # Configure dialog appearance
        dialog.configure(fg_color="white")
        
        # Warning icon and message
        ctk.CTkLabel(
            dialog,
            text="⚠️",
            font=("Poppins", 48),
            text_color="#FF0000"
        ).pack(pady=(20, 10))
        
        ctk.CTkLabel(
            dialog,
            text="Are you sure you want to\nremove this item?",
            font=("Poppins", 14, "bold"),
            text_color="black"
        ).pack(pady=10)
        
        # Buttons frame
        buttons_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        buttons_frame.pack(fill="x", padx=20, pady=(10, 0))
        
        # No button
        ctk.CTkButton(
            buttons_frame,
            text="No",
            font=("Poppins", 13),
            fg_color="#E5E5E5",
            text_color="black",
            hover_color="#D5D5D5",
            height=35,
            command=dialog.destroy
        ).pack(side="left", padx=(0, 10), expand=True)
        
        # Yes button
        ctk.CTkButton(
            buttons_frame,
            text="Yes",
            font=("Poppins", 13),
            fg_color="#FF0000",
            text_color="white",
            hover_color="#CC0000",
            height=35,
            command=lambda: self.remove_menu_item(dialog, parent_dialog, menu_id)
        ).pack(side="left", expand=True)

    def update_menu_item(self, dialog, menu_id):
        try:
            # Get values from entries
            updates = {
                'name': self.entries["name"].get().strip(),
                'description': self.entries["description"].get().strip(),
                'price': self.entries["price"].get().strip(),
                'category': self.entries["category"].get().strip(),
                'imagePath': self.entries["imagePath"].get().strip()
            }
            
            # Remove empty fields
            updates = {k: v for k, v in updates.items() if v}
            
            if not updates:
                self.show_error(dialog, "No changes made")
                return
            
            # Validate price format if provided
            if 'price' in updates:
                try:
                    updates['price'] = float(updates['price'])
                except ValueError:
                    self.show_error(dialog, "Price must be a valid number")
                    return
            
            # Connect to database
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor()
            
            # Build update query
            set_clause = ", ".join([f"{k} = %s" for k in updates.keys()])
            query = f"UPDATE Menu SET {set_clause} WHERE MenuID = %s"
            values = list(updates.values()) + [menu_id]
            
            cursor.execute(query, values)
            conn.commit()
            conn.close()
            
            # Close dialog
            dialog.destroy()
            
            # Refresh menu items
            self.load_menu_items()
            
        except mysql.connector.Error as err:
            self.show_error(dialog, f"Database Error: {err}")

    def remove_menu_item(self, confirm_dialog, parent_dialog, menu_id):
        try:
            # Connect to database
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor()
            
            # Delete menu item
            cursor.execute("DELETE FROM Menu WHERE MenuID = %s", (menu_id,))
            conn.commit()
            conn.close()
            
            # Close both dialogs
            confirm_dialog.destroy()
            parent_dialog.destroy()
            
            # Refresh menu items
            self.load_menu_items()
            
        except mysql.connector.Error as err:
            self.show_error(confirm_dialog, f"Database Error: {err}")
