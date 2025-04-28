import customtkinter as ctk
from utils import resize_image
from customer_nav import NavigationHeader
import mysql.connector
from dbconnection import DB_CONFIG

class ContactPage(ctk.CTkFrame):
    def __init__(self, parent, app=None, user=None):
        super().__init__(parent)
        self.app = app
        self.user = user

        self.configure(width=600, height=700, fg_color="transparent")
        self.create_contact_page()

    def create_contact_page(self):
        NavigationHeader(self, app=self.app, user=self.user).pack(side="top", fill="x")

        self.body_frame = ctk.CTkFrame(self, fg_color="#EDEDED")
        self.body_frame.pack(fill="both", expand=True)

        try:
            self.bg_image = resize_image((900, 900), "images/loginbackground.png")
            bg_label = ctk.CTkLabel(self.body_frame, image=self.bg_image, text="")
            bg_label.place(relx=0, rely=0, relwidth=1, relheight=1)
        except Exception as e:
            print("[Background Error]", e)

        # Main content frame - Exactly 500x500
        content_frame = ctk.CTkFrame(
            self.body_frame, 
            fg_color="#F9F0E5", 
            height=550, 
            width=550,
            corner_radius=0,
            border_width=1,
            border_color="#E0E0E0"
        )
        content_frame.place(relx=0.5, rely=0.5, anchor="center")
        content_frame.pack_propagate(False)

        # Main split frame with padding
        main_split_frame = ctk.CTkFrame(
            content_frame, 
            fg_color="transparent",
            width=530,
            height=530
        )
        main_split_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Image frame (Left side)
        image_frame = ctk.CTkFrame(
            main_split_frame, 
            fg_color="#FFFFFF", 
            width=200, height=530,
            corner_radius=0
        )
        image_frame.pack(side="left", fill="y")
        image_frame.pack_propagate(False)

        try:
            contact_img = resize_image((400, 850), "images/food contactus.jpg")
            ctk.CTkLabel(image_frame, image=contact_img, text="").pack(expand=True)
        except Exception as e:
            print("Image Error:", e)

        # Form container frame (Right side)
        form_container = ctk.CTkFrame(
            main_split_frame, 
            fg_color="#FFFFFF", 
            width=330,
            height=530,
            corner_radius=0
        )
        form_container.pack(side="right", fill="both", expand=True)
        form_container.pack_propagate(False)

        # Top 70% - Mail form frame
        mail_frame = ctk.CTkFrame(
            form_container, 
            fg_color="#FFFFFF",
            corner_radius=0,
            height=400  # 70% of 470
        )
        mail_frame.pack(fill="x")
        # mail_frame.pack_propagate(False)

        # Title and Message Section with accent
        title_frame = ctk.CTkFrame(
            mail_frame, 
            fg_color="#FFFFFF",
            corner_radius=0
        )
        title_frame.pack(fill="x", pady=(20, 0))

        ctk.CTkLabel(
            title_frame,
            text="Have any Questions?",
            font=("Poppins", 20, "bold"),
            text_color="black"
        ).pack(anchor="w", padx=20)
        
        # Yellow accent line
        accent_line = ctk.CTkFrame(
            title_frame,
            fg_color="#F1D94B",
            height=3,
            width=30,
            corner_radius=0
        )
        accent_line.pack(anchor="w", padx=20, pady=(0, 10))

        ctk.CTkLabel(
            title_frame,
            text="Send us a message below\n"
              "we'll get right back to you.",
            font=("Poppins", 12, "italic"),
            text_color="black"
        ).pack(anchor="w", padx=20)

        # Message display frame
        self.message_display_frame = ctk.CTkFrame(
            title_frame, 
            fg_color="#FAFAFA",
            height=20,
            corner_radius=0
        )
        self.message_display_frame.pack(fill="x", padx=20, pady=10)

        # Form Section
        form = ctk.CTkFrame(
            mail_frame, 
            fg_color="transparent",
            corner_radius=0
        )
        form.pack(fill="both", expand=True, padx=20)

        # Get user information using username
        user_info = self.get_user_info()

        # Name field (disabled)
        ctk.CTkLabel(
            form, 
            text="Name:", 
            anchor="w", 
            font=("Poppins", 13, "bold")
        ).pack(fill="x", pady=(5,0))
        
        self.name_entry = ctk.CTkEntry(
            form,
            height=30,
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
            font=("Poppins", 13, "bold")
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
            font=("Poppins", 13, "bold")
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
        self.submit_btn.pack(anchor="center", pady=5)

        # Divider line
        divider = ctk.CTkFrame(
            form_container,
            fg_color="#E5E5E5",
            height=1,
            corner_radius=0
        )
        divider.pack(fill="x")
        
        # Bottom 30% - Footer frame
        footer_frame = ctk.CTkFrame(
            form_container, 
            fg_color="#FFFFFF", 
            height=130,  
            corner_radius=0
        )
        footer_frame.pack(fill="x")
        footer_frame.pack_propagate(False)

        ctk.CTkLabel(
            footer_frame,
            text="------Or------",
            font=("Poppins", 12),
            text_color="#999999"
        ).pack(anchor="center")

        ctk.CTkLabel(
            footer_frame,
            text="reach us on",
            font=("Poppins", 13, "italic"),
            text_color="black"
        ).pack(pady=(5, 5))

        # Contact details with centered alignment
        contact_frame = ctk.CTkFrame(
            footer_frame,
            fg_color="transparent",
            corner_radius=0
        )
        contact_frame.pack(fill="both", expand=True)

        ctk.CTkLabel(
            contact_frame,
            text=
            "📞 Phone: +1 (123) 456-7890\n"
            "📧 Email: support@iceandspice.com\n"
            "📍 Address: 123 Food Street, Flavor Town",
            font=("Poppins", 13),
            text_color="black"
        ).pack()

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