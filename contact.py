import customtkinter as ctk
from utils import resize_image
from headerNav import NavigationHeader
import mysql.connector

class ContactPage(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.configure(width=600, height=700, fg_color="transparent")
        
        self.create_contact_page()

    def create_contact_page(self):
        # Add navigation header
        NavigationHeader(self, app=self.app).pack(side="top", fill="x")

        # Main body frame
        self.body_frame = ctk.CTkFrame(self, fg_color="#EDEDED")
        self.body_frame.pack(fill="both", expand=True)

        try:
            self.bg_image = resize_image((900, 900), "images/loginbackground.png")
            bg_label = ctk.CTkLabel(self.body_frame, image=self.bg_image, text="")
            bg_label.place(relx=0, rely=0, relwidth=1, relheight=1)
        except Exception as e:
            print("[Background Error]", e)

        # Content frame
        content_frame = ctk.CTkFrame(self.body_frame, fg_color="#F9F0E5")
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Center white frame
        center_frame = ctk.CTkFrame(content_frame, fg_color="#FFFFFF", corner_radius=15)
        center_frame.pack(fill="both", expand=True, padx=40, pady=40)

        # Title
        ctk.CTkLabel(
            center_frame,
            text="Contact Us",
            font=("Poppins", 32, "bold"),
            text_color="black"
        ).pack(pady=(20,30))

        # Split frame for left and right sections
        split_frame = ctk.CTkFrame(center_frame, fg_color="transparent")
        split_frame.pack(fill="both", expand=True, padx=20)

        # Left section
        left_frame = ctk.CTkFrame(split_frame, fg_color="transparent", width=250)
        left_frame.pack(side="left", fill="both", expand=True, padx=(0,10))

        # Image frame
        image_frame = ctk.CTkFrame(left_frame, fg_color="transparent")
        image_frame.pack(fill="x", pady=(0,20))
        
        try:
            contact_img = resize_image((200, 200), "images/contact_food.png")
            ctk.CTkLabel(image_frame, image=contact_img, text="").pack()
        except:
            pass

        # Contact info text
        info_frame = ctk.CTkFrame(left_frame, fg_color="transparent")
        info_frame.pack(fill="x")
        
        ctk.CTkLabel(
            info_frame,
            text="Use our contact form for all information requests or contact us directly.",
            font=("Poppins", 12),
            wraplength=250,
            justify="left"
        ).pack(fill="x")

        # Right section (Form)
        right_frame = ctk.CTkFrame(split_frame, fg_color="transparent", width=250)
        right_frame.pack(side="right", fill="both", expand=True, padx=(10,0))

        # Form title
        ctk.CTkLabel(
            right_frame,
            text="HAVE ANY QUESTIONS",
            font=("Poppins", 16, "bold"),
            text_color="black"
        ).pack(pady=(0,20))

        # Form fields
        self.name_entry = ctk.CTkEntry(
            right_frame, 
            placeholder_text="Enter your Name",
            height=35
        )
        self.name_entry.pack(fill="x", pady=5)

        self.email_entry = ctk.CTkEntry(
            right_frame, 
            placeholder_text="Enter a valid email address",
            height=35
        )
        self.email_entry.pack(fill="x", pady=5)

        self.message_entry = ctk.CTkTextbox(
            right_frame, 
            height=100,
            fg_color="white",
            border_color="#E0E0E0",
            border_width=1
        )
        self.message_entry.pack(fill="x", pady=5)

        # Submit button
        ctk.CTkButton(
            right_frame,
            text="SUBMIT",
            fg_color="#F1D94B",
            text_color="black",
            height=35,
            command=self.submit_form
        ).pack(pady=10)

    def submit_form(self):
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor()

            name = self.name_entry.get()
            email = self.email_entry.get()
            message = self.message_entry.get("1.0", "end-1c")

            sql = """
            INSERT INTO contact_messages (name, email, message, status)
            VALUES (%s, %s, %s, %s)
            """
            values = (name, email, message, 'unread')

            cursor.execute(sql, values)
            conn.commit()

            # Show success message
            self.show_message("Message sent successfully!", "green")
            
            # Clear form
            self.name_entry.delete(0, 'end')
            self.email_entry.delete(0, 'end')
            self.message_entry.delete("1.0", "end")

        except mysql.connector.Error as err:
            print(f"Database Error: {err}")
            self.show_message("Error sending message. Please try again.", "red")

        finally:
            if 'conn' in locals():
                conn.close()

    def show_message(self, message, color):
        msg_label = ctk.CTkLabel(
            self,
            text=message,
            text_color=color,
            font=("Poppins", 12)
        )
        msg_label.pack(pady=5)
        self.after(3000, msg_label.destroy)
