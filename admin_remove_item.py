import customtkinter as ctk
from tkinter import messagebox
from PIL import Image, ImageTk
import mysql.connector
import subprocess  # ✅ To reopen AdminHomePage
import os
from dbconnection import DB_CONFIG

class RemoveItemPage(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("🗑 Remove Menu Item")
        self.geometry("400x450")
        self.resizable(False, False)
        self.configure(fg_color="white")

        # ✅ Set Background Image
        self.set_background("loginbackground.png")

        # ✅ Create UI Components
        self.create_ui()

    def set_background(self, image_path):
        """Load and set a background image."""
        try:
            image = Image.open(image_path).resize((400, 450), Image.LANCZOS)
            self.bg_image = ImageTk.PhotoImage(image)

            bg_label = ctk.CTkLabel(self, image=self.bg_image, text="")
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        except Exception as e:
            print(f"⚠️ Error loading background image: {e}")

    def create_ui(self):
        """Create UI components for removing an item."""
        title_label = ctk.CTkLabel(self, text="🗑 Remove Menu Item", font=("Poppins", 18, "bold"), text_color="black")
        title_label.pack(pady=10)

        self.item_id_entry = ctk.CTkEntry(self, placeholder_text="Item ID to Remove", width=300)
        self.item_id_entry.pack(pady=20)

        remove_button = ctk.CTkButton(self, text="🗑 Remove Item", fg_color="#E53935", text_color="white",
                                      command=self.remove_item)
        remove_button.pack(pady=10)

        # ✅ Back Button
        back_button = ctk.CTkButton(self, text="⬅ Back to Dashboard", fg_color="#F1D94B", text_color="black",
                                    command=self.redirect_to_admin_home)
        back_button.pack(pady=10)

    def remove_item(self):
        """Delete an item from the database."""
        item_id = self.item_id_entry.get().strip()

        if not item_id:
            messagebox.showerror("Error", "⚠️ Item ID is required!")
            return

        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor()

            # First get the image path
            cursor.execute("SELECT imagePath FROM Menu WHERE MenuID = %s", (item_id,))
            result = cursor.fetchone()
            
            if result and result[0]:
                try:
                    # Delete the image file
                    if os.path.exists(result[0]):
                        os.remove(result[0])
                except Exception as e:
                    print(f"Error deleting image: {e}")

            # Delete from database
            cursor.execute("DELETE FROM Menu WHERE MenuID = %s", (item_id,))
            conn.commit()

            messagebox.showinfo("Success", f"✅ Item ID {item_id} removed successfully!")
            self.redirect_to_admin_home()

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"⚠️ {err}")
        finally:
            if 'conn' in locals():
                conn.close()

    def redirect_to_admin_home(self):
        """Close this window and return to Admin Dashboard."""
        self.destroy()  # ✅ Close Remove Item Page
        subprocess.Popen(["python", "admin_dashboard.py"])  # ✅ Reopen Admin Dashboard

# ✅ Open Remove Item Page
if __name__ == "__main__":
    app = RemoveItemPage()
    app.mainloop()
