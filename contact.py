import customtkinter as ctk
from utils import resize_image
from headerNav import NavigationHeader
import mysql.connector
from dbconnection import DB_CONFIG

class ContactPage(ctk.CTkFrame):
    def __init__(self, parent, app=None):
        super().__init__(parent)
        self.app = app
        self.configure(width=600, height=700, fg_color="transparent")
        self.create_contact_page()

    def create_contact_page(self):
        NavigationHeader(self, app=self.app).pack(side="top", fill="x")

        self.body_frame = ctk.CTkFrame(self, fg_color="#EDEDED")
        self.body_frame.pack(fill="both", expand=True)

        try:
            self.bg_image = resize_image((900, 900), "images/loginbackground.png")
            bg_label = ctk.CTkLabel(self.body_frame, image=self.bg_image, text="")
            bg_label.place(relx=0, rely=0, relwidth=1, relheight=1)
        except Exception as e:
            print("[Background Error]", e)

        # Content frame
        content_frame = ctk.CTkFrame(
            self.body_frame, 
            fg_color="#F9F0E5", 
            height=500, 
            width=500,
            corner_radius=0
        )
        content_frame.pack(expand=True)
        content_frame.pack_propagate(False)

        # Main split frame
        main_split_frame = ctk.CTkFrame(
            content_frame, 
            fg_color="transparent",
            width=500,
            height=500
        )
        main_split_frame.pack(fill="both", expand=True)

        # Image frame (Left side)
        image_frame = ctk.CTkFrame(
            main_split_frame, 
            fg_color="#FFFFFF", 
            width=230, height=520
        )
        image_frame.pack(side="left", fill="y")
        image_frame.pack_propagate(False)

        try:
            contact_img = resize_image((350, 600), "images/food contactus.jpg")
            ctk.CTkLabel(image_frame, image=contact_img, text="").pack(expand=True)
        except Exception as e:
            print("Image Error:", e)

        # Form container frame (Right side)
        form_container = ctk.CTkFrame(
            main_split_frame, 
            fg_color="transparent", 
            width=300,
            height=500
        )
        form_container.pack(side="right", fill="both")
        form_container.pack_propagate(False)

        # Mail form frame
        mail_frame = ctk.CTkFrame(
            form_container, 
            fg_color="#FFFFFF",
            corner_radius=0
        )
        mail_frame.pack(fill="both", expand=True)

        # Title and Message Section
        title_frame = ctk.CTkFrame(
            mail_frame, 
            fg_color="#FFFFFF",
            corner_radius=0
        )
        title_frame.pack(fill="x")

        ctk.CTkLabel(
            title_frame,
            text="Have any Questions?",
            font=("Poppins", 20, "bold"),
            text_color="black"
        ).pack(pady=(10,0))

        ctk.CTkLabel(
            title_frame,
            text="Send us a message below\n"
              "we’ll get right back to you.",
            font=("Poppins", 12, "italic"),
            text_color="black"
        ).pack(pady=(0,2))

        # Message display frame
        self.message_display_frame = ctk.CTkFrame(
            title_frame, 
            fg_color="#FFFFFF",
            height=10,
            corner_radius=0
        )
        self.message_display_frame.pack(fill="x", pady=1)

        # Form Section
        form = ctk.CTkFrame(
            mail_frame, 
            fg_color="transparent",
            corner_radius=0
        )
        form.pack(fill="both", expand=True, padx=10)

        # Get user information using username
        user_info = self.get_user_info()

        # Name field (disabled)
        ctk.CTkLabel(
            form, 
            text="Name:", 
            anchor="w", 
            font=("Poppins", 12)
        ).pack(fill="x", pady=(5,0))
        
        self.name_entry = ctk.CTkEntry(
            form,
            height=20,
            fg_color="white",
            border_color="#E0E0E0",
            border_width=1,
            corner_radius=0
        )
        self.name_entry.pack(fill="x", pady=(0,5))
        self.name_entry.insert(0, f"{user_info['first_name']} {user_info['last_name']}")
        self.name_entry.configure(state="disabled")

        # Email field (disabled)
        ctk.CTkLabel(
            form, 
            text="Email:", 
            anchor="w", 
            font=("Poppins", 12)
        ).pack(fill="x", pady=(5,0))
        
        self.email_entry = ctk.CTkEntry(
            form,
            height=30,
            fg_color="white",
            border_color="#E0E0E0",
            border_width=1,
            corner_radius=0
        )
        self.email_entry.pack(fill="x", pady=(0,5))
        self.email_entry.insert(0, user_info['email'])
        self.email_entry.configure(state="disabled")

        # Message field (enabled)
        ctk.CTkLabel(
            form, 
            text="Message:", 
            anchor="w", 
            font=("Poppins", 12)
        ).pack(fill="x", pady=(5,0))
        
        self.message_entry = ctk.CTkTextbox(
            form,
            height=80,
            fg_color="white",
            border_color="#E0E0E0",
            border_width=1,
            corner_radius=0
        )
        self.message_entry.pack(fill="x", pady=(0,5))

        # Submit button
        self.submit_btn = ctk.CTkButton(
            form,
            text="SUBMIT",
            fg_color="#F1D94B",
            text_color="black",
            height=25,
            corner_radius=0,
            command=self.submit_form
        )
        self.submit_btn.pack(pady=5)

        # Footer frame
        footer_frame = ctk.CTkFrame(
            form_container, 
            fg_color="#FFFFFF", 
            height=100,
            corner_radius=0
        )
        footer_frame.pack(fill="x")
        footer_frame.pack_propagate(False)

        ctk.CTkLabel(
            footer_frame,
            text="------Or------",
            font=("Poppins", 8, "bold"),
            text_color="black"
        ).pack(expand=True)

        ctk.CTkLabel(
            footer_frame,
            text="reach us on",
            font=("Poppins", 12, "italic"),
            text_color="black"
        ).pack(expand=True)

        ctk.CTkLabel(
            footer_frame,
            text="📞 Phone: +1 (123) 456-7890\n"
            "📧 Email: support@iceandspice.com\n"
            "📍 Address: 123 Food Street, Flavor Town",
            font=("Poppins", 12),
            text_color="black"
        ).pack(expand=True)

        # Restaurant handle
        ctk.CTkLabel(
            footer_frame,
            text="@icenspicerestaurant",
            font=("Poppins", 12, "bold"),
            text_color="black"
        ).pack(expand=True)

    def get_user_info(self):
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor(dictionary=True)
            
            sql = """
            SELECT first_name, last_name, email 
            FROM users 
            WHERE userID = %s
            """
            cursor.execute(sql, (self.app.logged_in_user['userID'],))
            user_info = cursor.fetchone()
            
            cursor.close()
            conn.close()
            
            return user_info
        except Exception as e:
            print(f"Error fetching user info: {e}")
            return None

    def submit_form(self):
        try:
            self.submit_btn.configure(state="disabled")
            
            message = self.message_entry.get("1.0", "end-1c")
            if not message.strip():
                self.show_message("Please enter your message", "red")
                self.submit_btn.configure(state="normal")
                return

            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor()

            sql = """
            INSERT INTO contact_messages 
            (name, email, message, status, created_at, parent_id, is_reply) 
            VALUES (%s, %s, %s, %s, NOW(), NULL, 0)
            """
            name = self.name_entry.get()
            email = self.email_entry.get()
            values = (name, email, message, 'unread')

            cursor.execute(sql, values)
            conn.commit()

            self.show_message("Message sent successfully!", "green")
            self.message_entry.delete("1.0", "end")
            
            cursor.close()
            conn.close()

        except mysql.connector.Error as err:
            print(f"Database Error: {err}")
            self.show_message("Error sending message. Please try again.", "red")

        finally:
            self.submit_btn.configure(state="normal")

    def show_message(self, message, color):
        # Clear any existing message
        for widget in self.message_display_frame.winfo_children():
            widget.destroy()
            
        msg_label = ctk.CTkLabel(
            self.message_display_frame,
            text=message,
            text_color=color,
            font=("Poppins", 12, "bold")
        )
        msg_label.pack(expand=True)
        
        if message == "Message sent successfully!":
            self.after(3000, lambda: self.clear_message())

    def clear_message(self):
        for widget in self.message_display_frame.winfo_children():
            widget.destroy()
