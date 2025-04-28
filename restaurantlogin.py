import customtkinter as ctk
from utils import resize_image
from dbconnection import DB_CONFIG
import mysql.connector
from signup import SignupPage

class LoginPage(ctk.CTkFrame):
    def __init__(self, parent, switch_to_signup=None, app=None):
        super().__init__(parent)
        self.configure(fg_color="transparent")
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

        # Error / Status Label
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
        show_checkbox = ctk.CTkCheckBox(
            login_frame,
            text="Show Password",
            variable=self.show_password_var,
            command=self.toggle_password,
            text_color="black",
            font=("Poppins", 12)
        )
        show_checkbox.place(x=75, y=250)

        # Login button
        login_button = ctk.CTkButton(
            login_frame,
            text="Login",
            fg_color="black",
            text_color="white",
            width=300,
            height=40,
            corner_radius=5,
            command=self.authenticate_user,
            font=("Poppins", 14, "bold")
        )
        login_button.place(x=75, y=280)

        # Sign up
        ctk.CTkLabel(
            login_frame,
            text="New member?",
            text_color="black",
            font=("Poppins", 12, "bold", "underline")
        ).place(x=190, y=350)
        
        signup_button = ctk.CTkButton(
            login_frame,
            text="Sign Up",
            fg_color="transparent",
            text_color="black",
            width=150,
            height=30,
            border_width=2,
            corner_radius=5,
            command=self.open_signup,
            font=("Poppins", 12)
        )
        signup_button.place(x=150, y=380)
            
    def authenticate_user(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not username or not password:
            self.show_error("Please fill in all fields")
            return
            
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor(dictionary=True)
            
            # Get user with matching username and password
            cursor.execute(
                "SELECT * FROM users WHERE username = %s AND password = %s",
                (username, password)
            )
            user = cursor.fetchone()
            conn.close()
            
            if user:
                # Navigate based on role
                if user.get('role') == 'admin':
                    # Use the existing app methods to navigate
                    self.app.show_admin_dashboard(user)
                else:
                    # Use the existing app methods to navigate
                    self.app.show_customer_dashboard(user)
            else:
                self.show_error("Invalid username or password")
                
        except mysql.connector.Error as err:
            print(f"Database Error: {err}")
            self.show_error("Error connecting to database")

    def show_error(self, message):
        self.error_label.configure(text=message)

    def toggle_password(self):
        self.password_entry.configure(show="" if self.show_password_var.get() else "*")

    def open_signup(self):
        if self.switch_to_signup:
            self.switch_to_signup()