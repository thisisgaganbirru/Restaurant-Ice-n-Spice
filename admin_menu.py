import customtkinter as ctk
from dbconnection import DB_CONFIG
import mysql.connector
from PIL import Image, ImageTk
import os
from tkinter import filedialog

class AdminMenuPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        self.create_menu_view()
    
    def create_menu_view(self):
        # Header with actions
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=20, pady=20)
        
        # Add item button
        ctk.CTkButton(
            header,
            text="Add New Item",
            fg_color="#4CAF50",
            command=self.show_add_item_dialog
        ).pack(side="left", padx=10)
        
        # Search bar
        self.search_var = ctk.StringVar()
        self.search_var.trace("w", lambda *args: self.filter_items())
        search_entry = ctk.CTkEntry(
            header,
            placeholder_text="Search items...",
            textvariable=self.search_var
        )
        search_entry.pack(side="right", padx=10)
        
        # Menu items grid
        self.items_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.items_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        self.load_menu_items()
    
    def load_menu_items(self):
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor(dictionary=True)
            
            cursor.execute("SELECT * FROM Menu ORDER BY name")
            items = cursor.fetchall()
            conn.close()
            
            self.display_menu_items(items)
            
        except mysql.connector.Error as err:
            print(f"Database Error: {err}")
    
    def display_menu_items(self, items):
        # Clear existing items
        for widget in self.items_frame.winfo_children():
            widget.destroy()
        
        # Create grid layout
        for i, item in enumerate(items):
            row = i // 3
            col = i % 3
            
            self.create_item_card(item, row, col)
    
    def create_item_card(self, item, row, col):
        card = ctk.CTkFrame(
            self.items_frame,
            fg_color="#2b2b2b",
            corner_radius=10,
            width=300,
            height=400
        )
        card.grid(row=row, column=col, padx=10, pady=10)
        card.grid_propagate(False)
        
        # Item image
        image_frame = ctk.CTkFrame(card, fg_color="transparent")
        image_frame.pack(fill="x", padx=10, pady=10)
        
        try:
            image = Image.open(item['image_path'])
            image = image.resize((280, 200), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(image)
            
            image_label = ctk.CTkLabel(image_frame, image=photo, text="")
            image_label.image = photo
            image_label.pack()
        except:
            ctk.CTkLabel(
                image_frame,
                text="No Image",
                font=("Poppins", 12)
            ).pack()
        
        # Item details
        details_frame = ctk.CTkFrame(card, fg_color="transparent")
        details_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(
            details_frame,
            text=item['name'],
            font=("Poppins", 16, "bold")
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            details_frame,
            text=f"${item['price']:.2f}",
            font=("Poppins", 14),
            text_color="#4CAF50"
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            details_frame,
            text=item['description'],
            font=("Poppins", 12),
            wraplength=280
        ).pack(anchor="w", pady=5)
        
        # Actions
        actions_frame = ctk.CTkFrame(card, fg_color="transparent")
        actions_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkButton(
            actions_frame,
            text="Edit",
            fg_color="#2196F3",
            command=lambda: self.show_edit_item_dialog(item)
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            actions_frame,
            text="Delete",
            fg_color="#F44336",
            command=lambda: self.delete_item(item['item_id'])
        ).pack(side="left", padx=5)
    
    def filter_items(self):
        search = self.search_var.get().lower()
        
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor(dictionary=True)
            
            query = "SELECT * FROM Menu WHERE 1=1"
            params = []
            
            if search:
                query += " AND (name LIKE %s OR description LIKE %s)"
                search_param = f"%{search}%"
                params.extend([search_param, search_param])
            
            query += " ORDER BY name"
            
            cursor.execute(query, params)
            items = cursor.fetchall()
            conn.close()
            
            self.display_menu_items(items)
            
        except mysql.connector.Error as err:
            print(f"Database Error: {err}")
    
    def show_add_item_dialog(self):
        dialog = ctk.CTkToplevel(self)
        dialog.title("Add New Menu Item")
        dialog.geometry("400x600")
        dialog.resizable(False, False)
        
        # Form fields
        name_var = ctk.StringVar()
        price_var = ctk.StringVar()
        description_var = ctk.StringVar()
        image_path = None
        
        # Name
        ctk.CTkLabel(
            dialog,
            text="Item Name:",
            font=("Poppins", 14)
        ).pack(pady=(20,5))
        
        name_entry = ctk.CTkEntry(
            dialog,
            textvariable=name_var
        )
        name_entry.pack(pady=5, padx=20)
        
        # Price
        ctk.CTkLabel(
            dialog,
            text="Price:",
            font=("Poppins", 14)
        ).pack(pady=(20,5))
        
        price_entry = ctk.CTkEntry(
            dialog,
            textvariable=price_var
        )
        price_entry.pack(pady=5, padx=20)
        
        # Description
        ctk.CTkLabel(
            dialog,
            text="Description:",
            font=("Poppins", 14)
        ).pack(pady=(20,5))
        
        description_entry = ctk.CTkTextbox(
            dialog,
            height=100
        )
        description_entry.pack(pady=5, padx=20)
        
        # Image
        ctk.CTkLabel(
            dialog,
            text="Image:",
            font=("Poppins", 14)
        ).pack(pady=(20,5))
        
        def select_image():
            nonlocal image_path
            image_path = filedialog.askopenfilename(
                filetypes=[("Image files", "*.png *.jpg *.jpeg")]
            )
        
        ctk.CTkButton(
            dialog,
            text="Select Image",
            command=select_image
        ).pack(pady=5, padx=20)
        
        # Submit button
        def submit():
            try:
                conn = mysql.connector.connect(**DB_CONFIG)
                cursor = conn.cursor()
                
                # Save image
                if image_path:
                    # Create images directory if it doesn't exist
                    os.makedirs("images/menu_items", exist_ok=True)
                    
                    # Copy image to menu_items directory
                    image_name = os.path.basename(image_path)
                    new_image_path = f"images/menu_items/{image_name}"
                    os.system(f"copy \"{image_path}\" \"{new_image_path}\"")
                else:
                    new_image_path = None
                
                # Insert into database
                cursor.execute("""
                    INSERT INTO Menu (name, price, description, image_path)
                    VALUES (%s, %s, %s, %s)
                """, (
                    name_var.get(),
                    float(price_var.get()),
                    description_entry.get("1.0", "end-1c"),
                    new_image_path
                ))
                
                conn.commit()
                conn.close()
                
                # Refresh menu items
                self.load_menu_items()
                
                # Close dialog
                dialog.destroy()
                
            except mysql.connector.Error as err:
                print(f"Database Error: {err}")
        
        ctk.CTkButton(
            dialog,
            text="Add Item",
            fg_color="#4CAF50",
            command=submit
        ).pack(pady=20, padx=20)
    
    def show_edit_item_dialog(self, item):
        dialog = ctk.CTkToplevel(self)
        dialog.title("Edit Menu Item")
        dialog.geometry("400x600")
        dialog.resizable(False, False)
        
        # Form fields
        name_var = ctk.StringVar(value=item['name'])
        price_var = ctk.StringVar(value=str(item['price']))
        description_var = ctk.StringVar(value=item['description'])
        image_path = item['image_path']
        
        # Name
        ctk.CTkLabel(
            dialog,
            text="Item Name:",
            font=("Poppins", 14)
        ).pack(pady=(20,5))
        
        name_entry = ctk.CTkEntry(
            dialog,
            textvariable=name_var
        )
        name_entry.pack(pady=5, padx=20)
        
        # Price
        ctk.CTkLabel(
            dialog,
            text="Price:",
            font=("Poppins", 14)
        ).pack(pady=(20,5))
        
        price_entry = ctk.CTkEntry(
            dialog,
            textvariable=price_var
        )
        price_entry.pack(pady=5, padx=20)
        
        # Description
        ctk.CTkLabel(
            dialog,
            text="Description:",
            font=("Poppins", 14)
        ).pack(pady=(20,5))
        
        description_entry = ctk.CTkTextbox(
            dialog,
            height=100
        )
        description_entry.insert("1.0", item['description'])
        description_entry.pack(pady=5, padx=20)
        
        # Image
        ctk.CTkLabel(
            dialog,
            text="Image:",
            font=("Poppins", 14)
        ).pack(pady=(20,5))
        
        def select_image():
            nonlocal image_path
            image_path = filedialog.askopenfilename(
                filetypes=[("Image files", "*.png *.jpg *.jpeg")]
            )
        
        ctk.CTkButton(
            dialog,
            text="Select New Image",
            command=select_image
        ).pack(pady=5, padx=20)
        
        # Submit button
        def submit():
            try:
                conn = mysql.connector.connect(**DB_CONFIG)
                cursor = conn.cursor()
                
                # Save image if new one selected
                if image_path and image_path != item['image_path']:
                    # Create images directory if it doesn't exist
                    os.makedirs("images/menu_items", exist_ok=True)
                    
                    # Copy image to menu_items directory
                    image_name = os.path.basename(image_path)
                    new_image_path = f"images/menu_items/{image_name}"
                    os.system(f"copy \"{image_path}\" \"{new_image_path}\"")
                else:
                    new_image_path = item['image_path']
                
                # Update database
                cursor.execute("""
                    UPDATE Menu
                    SET name = %s,
                        price = %s,
                        description = %s,
                        image_path = %s
                    WHERE item_id = %s
                """, (
                    name_var.get(),
                    float(price_var.get()),
                    description_entry.get("1.0", "end-1c"),
                    new_image_path,
                    item['item_id']
                ))
                
                conn.commit()
                conn.close()
                
                # Refresh menu items
                self.load_menu_items()
                
                # Close dialog
                dialog.destroy()
                
            except mysql.connector.Error as err:
                print(f"Database Error: {err}")
        
        ctk.CTkButton(
            dialog,
            text="Update Item",
            fg_color="#2196F3",
            command=submit
        ).pack(pady=20, padx=20)
    
    def delete_item(self, item_id):
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor()
            
            # Get image path before deleting
            cursor.execute("SELECT image_path FROM Menu WHERE item_id = %s", (item_id,))
            image_path = cursor.fetchone()[0]
            
            # Delete from database
            cursor.execute("DELETE FROM Menu WHERE item_id = %s", (item_id,))
            conn.commit()
            conn.close()
            
            # Delete image file if exists
            if image_path and os.path.exists(image_path):
                os.remove(image_path)
            
            # Refresh menu items
            self.load_menu_items()
            
        except mysql.connector.Error as err:
            print(f"Database Error: {err}") 