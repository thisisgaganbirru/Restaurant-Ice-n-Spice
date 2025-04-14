from admin_base import AdminBasePage
import customtkinter as ctk
from utils import resize_image
import mysql.connector
from dbconnection import DB_CONFIG
from PIL import Image
import os
from tkinter import filedialog

class AddItemPage(AdminBasePage):
    def __init__(self, parent, app):
        super().__init__(parent, app, "Add New Item")
        self.selected_image_path = None
        self.create_add_item_form()

    def create_add_item_form(self):
        # Create form container
        form_card = self.create_content_card("Add New Menu Item", height=500)
        form_card.pack(fill="both", expand=True, padx=20, pady=20)

        # Form content
        form_frame = ctk.CTkFrame(form_card, fg_color="transparent")
        form_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Image selection
        img_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
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
            text="Choose Image",
            command=self.select_image,
            fg_color="#2196F3",
            hover_color="#1976D2"
        ).pack(side="left", padx=10)

        # Form fields
        fields_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        fields_frame.pack(fill="x", pady=10)

        # Name field
        ctk.CTkLabel(
            fields_frame,
            text="Item Name:",
            font=("Poppins", 12),
            text_color="white"
        ).pack(anchor="w", pady=(0,5))
        
        self.name_entry = ctk.CTkEntry(
            fields_frame,
            placeholder_text="Enter item name",
            width=300
        )
        self.name_entry.pack(anchor="w")

        # Description field
        ctk.CTkLabel(
            fields_frame,
            text="Description:",
            font=("Poppins", 12),
            text_color="white"
        ).pack(anchor="w", pady=(10,5))
        
        self.desc_entry = ctk.CTkTextbox(
            fields_frame,
            width=300,
            height=100
        )
        self.desc_entry.pack(anchor="w")

        # Price field
        ctk.CTkLabel(
            fields_frame,
            text="Price ($):",
            font=("Poppins", 12),
            text_color="white"
        ).pack(anchor="w", pady=(10,5))
        
        self.price_entry = ctk.CTkEntry(
            fields_frame,
            placeholder_text="Enter price",
            width=300
        )
        self.price_entry.pack(anchor="w")

        # Category dropdown
        ctk.CTkLabel(
            fields_frame,
            text="Category:",
            font=("Poppins", 12),
            text_color="white"
        ).pack(anchor="w", pady=(10,5))
        
        self.category_var = ctk.StringVar(value="Select category")
        self.category_menu = ctk.CTkOptionMenu(
            fields_frame,
            values=["Biryani", "Pizza", "Burger", "Desserts", "Beverages"],
            variable=self.category_var,
            width=300
        )
        self.category_menu.pack(anchor="w")

        # Submit button
        ctk.CTkButton(
            fields_frame,
            text="Add Item",
            command=self.add_item,
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

    def add_item(self):
        try:
            if not all([
                self.name_entry.get(),
                self.desc_entry.get("1.0", "end-1c"),
                self.price_entry.get(),
                self.category_var.get() != "Select category",
                self.selected_image_path
            ]):
                self.show_status("Please fill all fields", "red")
                return

            # Save image to project directory
            img_filename = f"item_{self.name_entry.get().lower().replace(' ', '_')}.png"
            img_save_path = os.path.join("images", "menu_items", img_filename)
            
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(img_save_path), exist_ok=True)
            
            # Copy and resize image
            img = Image.open(self.selected_image_path)
            img.thumbnail((300, 300))
            img.save(img_save_path)

            # Save to database
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor()

            sql = """
            INSERT INTO Menu (name, description, price, category, imagePath)
            VALUES (%s, %s, %s, %s, %s)
            """
            values = (
                self.name_entry.get(),
                self.desc_entry.get("1.0", "end-1c"),
                float(self.price_entry.get()),
                self.category_var.get(),
                img_save_path
            )

            cursor.execute(sql, values)
            conn.commit()

            self.show_status("Item added successfully!", "#4CAF50")
            self.clear_form()

        except mysql.connector.Error as err:
            print(f"Database Error: {err}")
            self.show_status("Error adding item to database", "#FF5252")
        except Exception as e:
            print(f"Error: {e}")
            self.show_status("Error adding item", "#FF5252")
        finally:
            if 'conn' in locals():
                conn.close()

    def show_status(self, message, color):
        self.status_label.configure(text=message, text_color=color)

    def clear_form(self):
        self.name_entry.delete(0, 'end')
        self.desc_entry.delete("1.0", "end")
        self.price_entry.delete(0, 'end')
        self.category_var.set("Select category")
        self.selected_image_path = None
        self.img_preview.configure(image=None, text="No image selected")
