import customtkinter as ctk
from utils import resize_image
from dbconnection import DB_CONFIG
import mysql.connector
import re

class SignupPage(ctk.CTkFrame):
    def validate_name(self, name):
        return bool(re.match(r'^[A-Za-z ]+$', name))

    def validate_email(self, email):
        return bool(re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email))

    def validate_phone(self, phone):
        return phone.isdigit() and len(phone) >= 10

    def register_user(self):
        first_name = self.first_name_entry.get().strip()
        last_name = self.last_name_entry.get().strip()
        username = self.username_entry.get().strip()
        email = self.email_entry.get().strip()
        phone_number = self.phone_entry.get().strip()
        address = self.address_entry.get().strip()
        password = self.password_entry.get().strip()
        confirm_password = self.confirm_password_entry.get().strip()
        role = "customer"

        self.error_label.configure(text="")

        if not first_name or not last_name or not username or not email or not phone_number or not address or not password or not confirm_password:
            self.error_label.configure(text="All fields are required.", text_color="red")
            return

        if not self.validate_name(first_name) or not self.validate_name(last_name):
            self.error_label.configure(text="Invalid name: only letters and spaces allowed.", text_color="red")
            return

        if not self.validate_email(email):
            self.error_label.configure(text="Invalid email format.", text_color="red")
            return

        if not self.validate_phone(phone_number):
            self.error_label.configure(text="Invalid phone number: must be at least 10 digits.", text_color="red")
            return

        if password != confirm_password:
            self.error_label.configure(text="Passwords do not match.", text_color="red")
            return

        try:
            db = mysql.connector.connect(**DB_CONFIG)
            cursor = db.cursor()
            cursor.execute("""
                INSERT INTO users (first_name, last_name, username, email, phone_number, address, password, role)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (first_name, last_name, username, email, phone_number, address, password, role))
            db.commit()
            db.close()

            self.error_label.configure(text="Account created successfully!", text_color="green")
            self.after(1500, self.switch_to_login)
        except mysql.connector.IntegrityError:
            self.error_label.configure(text="Username or email already exists. Choose a different one.", text_color="red")
        except mysql.connector.Error as err:
            self.error_label.configure(text=f"Database error: {err}", text_color="red")

    def __init__(self, parent, switch_to_login):
        super().__init__(parent)
        self.switch_to_login = switch_to_login
        self.configure(width=600, height=700)

        self.bg_img = resize_image((900, 900), 'images/backg.jpg')

        bg_label = ctk.CTkLabel(self, image=self.bg_img, text="")
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        form = ctk.CTkFrame(self, width=450, height=450, fg_color="#F9F0E5", corner_radius=10)
        form.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(form, text="Create Account", text_color="black", font=("Poppins", 24, "bold"))\
            .place(relx=0.5, y=40, anchor="center")

        self.error_label = ctk.CTkLabel(form, text="", text_color="red", font=("Poppins", 12))
        self.error_label.place(x=40, y=50)

        ctk.CTkLabel(form, text="First Name", text_color="black", font=("Poppins", 14)).place(x=40, y=90)
        self.first_name_entry = ctk.CTkEntry(form, width=180,border_width=2, fg_color="white", text_color="black")
        self.first_name_entry.place(x=40, y=120)

        ctk.CTkLabel(form, text="Last Name", text_color="black", font=("Poppins", 14)).place(x=230, y=90)
        self.last_name_entry = ctk.CTkEntry(form, width=180,border_width=2, fg_color="white", text_color="black")
        self.last_name_entry.place(x=230, y=120)

        ctk.CTkLabel(form, text="Username", text_color="black", font=("Poppins", 14)).place(x=40, y=150)
        self.username_entry = ctk.CTkEntry(form, width=180,border_width=2, fg_color="white", text_color="black")
        self.username_entry.place(x=40, y=180)

        ctk.CTkLabel(form, text="Email", text_color="black", font=("Poppins", 14)).place(x=230, y=150)
        self.email_entry = ctk.CTkEntry(form, width=180, border_width=2, fg_color="white", text_color="black")
        self.email_entry.place(x=230, y=180)

        ctk.CTkLabel(form, text="Phone Number", text_color="black", font=("Poppins", 14)).place(x=40, y=210)
        self.phone_entry = ctk.CTkEntry(form, width=180,border_width=2, fg_color="white", text_color="black")
        self.phone_entry.place(x=40, y=240)

        ctk.CTkLabel(form, text="Address", text_color="black", font=("Poppins", 14)).place(x=230, y=210)
        self.address_entry = ctk.CTkEntry(form, width=180,border_width=2, fg_color="white", text_color="black")
        self.address_entry.place(x=230, y=240)

        ctk.CTkLabel(form, text="Password", text_color="black", font=("Poppins", 14)).place(x=40, y=270)
        self.password_entry = ctk.CTkEntry(form, width=180, show="*",border_width=2, fg_color="white", text_color="black")
        self.password_entry.place(x=40, y=300)

        ctk.CTkLabel(form, text="Confirm Password", text_color="black", font=("Poppins", 14)).place(x=230, y=270)
        self.confirm_password_entry = ctk.CTkEntry(form, width=180, show="*",border_width=2, fg_color="white", text_color="black")
        self.confirm_password_entry.place(x=230, y=300)

        register_btn = ctk.CTkButton(form, text="Sign Up", fg_color="black", text_color="white",
                                     width=380, height=40, corner_radius=5, command=self.register_user,
                                     font=("Poppins", 14, "bold"))
        register_btn.place(x=40, y=340)

        login_back_btn = ctk.CTkButton(form, text="Back to Login", fg_color="transparent", border_width=2,
                                       text_color="black", width=380, height=40, corner_radius=5, command=switch_to_login,
                                       font=("Poppins", 12))
        login_back_btn.place(x=40, y=390)
