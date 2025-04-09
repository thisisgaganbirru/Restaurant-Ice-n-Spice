import customtkinter as ctk
from utils import resize_image
from dbconnection import DB_CONFIG
import mysql.connector
from signup import SignupPage

class LoginPage(ctk.CTkFrame):

            
    def authenticate_user(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        self.error_label.configure(text="", text_color="red")  # Clear previous message

        if not username or not password:
            self.error_label.configure(text="Please enter both username and password.")
            return

        try:
            db = mysql.connector.connect(**DB_CONFIG)
            cursor = db.cursor(dictionary=True)
            cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
            user = cursor.fetchone()
            db.close()
        except mysql.connector.Error as err:
            self.error_label.configure(text=f"Database error: {err}")
            return

        if user:
            if user["role"] == "customer":
                self.app.logged_in_user = user
                from menu import MenuPage  # Lazy import to avoid circular imports
                for widget in self.master.winfo_children():  
                    widget.destroy()
                self.app.show_menu_page() 
            else:
                self.error_label.configure(text="Access denied: Not a customer", text_color="red")
        else:
            self.error_label.configure(text="Incorrect username or password.")
    def toggle_password(self):
        self.password_entry.configure(show="" if self.show_password_var.get() else "*")

    def open_signup(self):
        self.switch_to_signup()

    def __init__(self, parent,switch_to_signup=None, app=None):
        super().__init__(parent)
        self.configure(width=600, height=600)
        self.app = app
        self.switch_to_signup = switch_to_signup

        # Load background image
        self.bg_img = resize_image((900, 900), 'images/backg.jpg')

        bg_label = ctk.CTkLabel(self, image=self.bg_img, text="")
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Login frame
        login_frame = ctk.CTkFrame(self, width=450, height=450, fg_color="#F9F0E5", corner_radius=10)
        login_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Title
        login_label = ctk.CTkLabel(login_frame, text="Welcome!", text_color="black", font=("Poppins", 24, "bold"))
        login_label.place(relx=0.5, y=50, anchor="center")

        # Error / Status Label (moved before username field)
        self.error_label = ctk.CTkLabel(login_frame, text="", text_color="red", font=("Poppins", 12))
        self.error_label.place(x=120, y=75)

        # Username
        ctk.CTkLabel(login_frame, text="Username", text_color="black", font=("Poppins", 14)).place(x=75, y=100)
        self.username_entry = ctk.CTkEntry(login_frame, width=300, height=40, fg_color="white", text_color="black")
        self.username_entry.place(x=75, y=130)

        # Password
        ctk.CTkLabel(login_frame, text="Password", text_color="black", font=("Poppins", 14)).place(x=75, y=170)
        self.password_entry = ctk.CTkEntry(login_frame, width=300, height=40, show="*", fg_color="white", text_color="black")
        self.password_entry.place(x=75, y=200)

        # Show password checkbox
        self.show_password_var = ctk.IntVar()
        show_checkbox = ctk.CTkCheckBox(login_frame, text="Show Password", variable=self.show_password_var,
                                        command=self.toggle_password, text_color="black", font=("Poppins", 12))
        show_checkbox.place(x=75, y=250)

        # Login button
        login_button = ctk.CTkButton(login_frame, text="Login", fg_color="black", text_color="white",
                                     width=300, height=40, corner_radius=5, command=self.authenticate_user,
                                     font=("Poppins", 14, "bold"))
        login_button.place(x=75, y=280)

        # Sign up
        ctk.CTkLabel(login_frame, text="New member?", text_color="black", font=("Poppins", 12, "bold", "underline")).place(x=190, y=350)
        signup_button = ctk.CTkButton(login_frame, text="Sign Up", fg_color="transparent", text_color="black",
                                      width=150, height=30, border_width=2,corner_radius=5, command=self.open_signup,
                                      font=("Poppins", 12))
        signup_button.place(x=150, y=380)