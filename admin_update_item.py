from admin_base import AdminBasePage
import customtkinter as ctk
from utils import resize_image
import mysql.connector
from dbconnection import DB_CONFIG
from PIL import Image
import os
from tkinter import filedialog

class UpdateItemPage(AdminBasePage):
    def __init__(self, parent, app):
        super().__init__(parent, app, "Update Menu Item")
        self.selected_image_path = None
        self.current_item = None
        self.create_update_form()

    def create_update_form(self):
        # Create form container
        form_card = self.create_content_card("Update Menu Item", height=600)
        form_card.pack(fill="both", expand=True, padx=20, pady=20)

        # Search section
        search_frame = ctk.CTkFrame(form_card, fg_color="transparent")
        search_frame.pack(fill="x", padx=20, pady=10)

        self.search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="Enter item name to search",
            width=300
        )
        self.search_entry.pack(side="left", padx=5)

        ctk.CTkButton(
            search_frame,
            text="Search",
            command=self.search_item,
            fg_color="#2196F3",
            hover_color="#1976D2",
            width=100
        ).pack(side="left", padx=5)

        # Form content
        self.form_frame = ctk.CTkFrame(form_card, fg_color="transparent")
        self.form_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Initially hide the form
        self.hide_form()

    def show_form(self):
        # Image selection
        img_frame = ctk.CTkFrame(self.form_frame, fg_color="transparent")
        img_frame.pack(fill="x", pady=10)

        self.img_preview = ctk.CTkLabel(
            img_frame,
            text="No image selected",
            font=("Poppins", 12),
            text_color="gray",
            width=200,
            height=200
        )
        self.img_preview.pack(side="left", padx=10)

        ctk.CTkButton(
            img_frame,
            text="Choose New Image",
            command=self.select_image,
            fg_color="#2196F3",
            hover_color="#1976D2"
        ).pack(side="left", padx=10)

        # Form fields
        fields_frame = ctk.CTkFrame(self.form_frame, fg_color="transparent")
        fields_frame.pack(fill="x", pady=10)

        # Name field
        ctk.CTkLabel(fields_frame, text="Item Name:", font=("Poppins", 12), text_color="white").pack(anchor="w", pady=(0,5))
        self.name_entry = ctk.CTkEntry(fields_frame, width=300)
        self.name_entry.pack(anchor="w")

        # Description field
        ctk.CTkLabel(fields_frame, text="Description:", font=("Poppins", 12), text_color="white").pack(anchor="w", pady=(10,5))
        self.desc_entry = ctk.CTkTextbox(fields_frame, width=300, height=100)
        self.desc_entry.pack(anchor="w")

        # Price field
        ctk.CTkLabel(fields_frame, text="Price ($):", font=("Poppins", 12), text_color="white").pack(anchor="w", pady=(10,5))
        self.price_entry = ctk.CTkEntry(fields_frame, width=300)
        self.price_entry.pack(anchor="w")

        # Category dropdown
        ctk.CTkLabel(fields_frame, text="Category:", font=("Poppins", 12), text_color="white").pack(anchor="w", pady=(10,5))
        self.category_var = ctk.StringVar()
        self.category_menu = ctk.CTkOptionMenu(
            fields_frame,
            values=["Biryani", "Pizza", "Burger", "Desserts", "Beverages"],
            variable=self.category_var,
            width=300
        )
        self.category_menu.pack(anchor="w")

        # Update button
        ctk.CTkButton(
            fields_frame,
            text="Update Item",
            command=self.update_item,
            fg_color="#4CAF50",
            hover_color="#388E3C",
            width=300
        ).pack(anchor="w", pady=20)

        # Status message
        self.status_label = ctk.CTkLabel(
            fields_frame,
            text="",
            font=("Poppins", 12),
            text_color="white"
        )
        self.status_label.pack(anchor="w")

    def hide_form(self):
        for widget in self.form_frame.winfo_children():
            widget.destroy()

    def search_item(self):
        search_term = self.search_entry.get().strip()
        if not search_term:
            return

        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor(dictionary=True)

            cursor.execute("""
                SELECT * FROM Menu 
                WHERE name LIKE %s
            """, (f"%{search_term}%",))

            item = cursor.fetchone()
            
            if item:
                self.current_item = item
                self.hide_form()
                self.show_form()
                self.populate_form(item)
            else:
                self.hide_form()
                self.show_status("Item not found", "#FF5252")

        except mysql.connector.Error as err:
            print(f"Database Error: {err}")
            self.show_status("Error searching for item", "#FF5252")
        finally:
            if 'conn' in locals():
                conn.close()

    def populate_form(self, item):
        self.name_entry.delete(0, 'end')
        self.name_entry.insert(0, item['name'])
        
        self.desc_entry.delete("1.0", "end")
        self.desc_entry.insert("1.0", item['description'])
        
        self.price_entry.delete(0, 'end')
        self.price_entry.insert(0, str(item['price']))
        
        self.category_var.set(item['category'])

        try:
            if item['imagePath']:
                preview = resize_image((200, 200), item['imagePath'])
                self.img_preview.configure(image=preview, text="")
                self.selected_image_path = item['imagePath']
        except Exception as e:
            print(f"Error loading image: {e}")

    def select_image(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif *.bmp")]
        )
        if file_path:
            try:
                self.selected_image_path = file_path
                preview = resize_image((200, 200), file_path)
                self.img_preview.configure(image=preview, text="")
            except Exception as e:
                print(f"Error loading image: {e}")

    def update_item(self):
        if not self.current_item:
            return

        try:
            # Handle image update if new image selected
            img_path = self.current_item['imagePath']
            if self.selected_image_path and self.selected_image_path != self.current_item['imagePath']:
                img_filename = f"item_{self.name_entry.get().lower().replace(' ', '_')}.png"
                img_path = os.path.join("images", "menu_items", img_filename)
                
                os.makedirs(os.path.dirname(img_path), exist_ok=True)
                
                img = Image.open(self.selected_image_path)
                img.thumbnail((300, 300))
                img.save(img_path)

            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor()

            sql = """
            UPDATE Menu 
            SET name = %s, description = %s, price = %s, category = %s, imagePath = %s
            WHERE MenuID = %s
            """
            values = (
                self.name_entry.get(),
                self.desc_entry.get("1.0", "end-1c"),
                float(self.price_entry.get()),
                self.category_var.get(),
                img_path,
                self.current_item['MenuID']
            )

            cursor.execute(sql, values)
            conn.commit()

            self.show_status("Item updated successfully!", "#4CAF50")

        except mysql.connector.Error as err:
            print(f"Database Error: {err}")
            self.show_status("Error updating item", "#FF5252")
        except Exception as e:
            print(f"Error: {e}")
            self.show_status("Error updating item", "#FF5252")
        finally:
            if 'conn' in locals():
                conn.close()

    def show_status(self, message, color):
        self.status_label.configure(text=message, text_color=color)
