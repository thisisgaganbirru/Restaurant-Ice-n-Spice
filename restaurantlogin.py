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

        # Forgot password text (italic and underlined)
        forgot_password_label = ctk.CTkLabel(
            login_frame,
            text="Forgot Password?",
            text_color="black",
            font=("Poppins", 12, "italic", "underline"),
            cursor="hand2" 
        )
        forgot_password_label.place(x=280, y=250)
        
        # Bind click event to the label
        forgot_password_label.bind("<Button-1>", lambda event: self.show_forgot_password_frame())

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
    
    def show_forgot_password_frame(self):
        # Hide error message if any
        self.error_label.configure(text="")
        
        # Create a new frame for forgot password
        self.forgot_frame = ctk.CTkFrame(self, width=450, height=450, fg_color="#FDF6E9", corner_radius=10)
        self.forgot_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        # Title
        ctk.CTkLabel(
            self.forgot_frame, 
            text="Reset Password", 
            text_color="black", 
            font=("Poppins", 24, "bold")
        ).place(relx=0.5, y=50, anchor="center")
        
        # Email Entry Section
        self.email_section = ctk.CTkFrame(self.forgot_frame, fg_color="transparent")
        self.email_section.place(x=0, y=100, relwidth=1)
        
        ctk.CTkLabel(
            self.email_section, 
            text="Enter your email", 
            text_color="black", 
            font=("Poppins", 14)
        ).place(x=75, y=0)
        
        self.email_entry = ctk.CTkEntry(
            self.email_section, 
            width=300, 
            height=40, 
            fg_color="white", 
            text_color="black"
        )
        self.email_entry.place(x=75, y=30)
        
        self.submit_button = ctk.CTkButton(
            self.email_section,
            text="Submit",
            fg_color="black",
            text_color="white",
            width=300,
            height=40,
            corner_radius=5,
            command=self.find_user_by_email,
            font=("Poppins", 14, "bold")
        )
        self.submit_button.place(x=75, y=80)
        
        # Reset Password Section (Initially Hidden)
        self.reset_section = ctk.CTkFrame(self.forgot_frame, fg_color="transparent")
        
        # Back button - centered in a dark border as shown in screenshot
        back_button = ctk.CTkButton(
            self.forgot_frame,
            text="Back to Login",
            fg_color="#F5F5F5",
            text_color="black",
            width=300,
            height=40,
            border_width=1,
            border_color="#CCCCCC",
            corner_radius=5,
            command=self.back_to_login,
            font=("Poppins", 12)
        )
        back_button.place(relx=0.5, y=410, anchor="center")

    def find_user_by_email(self):
        email = self.email_entry.get().strip()
        
        if not email:
            # Create a status label if it doesn't exist
            if not hasattr(self, 'status_label'):
                self.status_label = ctk.CTkLabel(
                    self.email_section, 
                    text="Please enter your email", 
                    text_color="red", 
                    font=("Poppins", 12)
                )
                self.status_label.place(x=75, y=130)
            else:
                self.status_label.configure(text="Please enter your email", text_color="red")
            return
        
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor(dictionary=True)
            
            # Get user with matching email
            cursor.execute(
                "SELECT username FROM users WHERE email = %s",
                (email,)
            )
            user = cursor.fetchone()
            conn.close()
            
            if user:
                # Show reset password form
                self.show_reset_password_form(user['username'])
            else:
                # Create a status label if it doesn't exist
                if not hasattr(self, 'status_label'):
                    self.status_label = ctk.CTkLabel(
                        self.email_section, 
                        text="Email not found", 
                        text_color="red", 
                        font=("Poppins", 12)
                    )
                    self.status_label.place(x=75, y=130)
                else:
                    self.status_label.configure(text="Email not found", text_color="red")
                
        except mysql.connector.Error as err:
            print(f"Database Error: {err}")
            # Create a status label if it doesn't exist
            if not hasattr(self, 'status_label'):
                self.status_label = ctk.CTkLabel(
                    self.email_section, 
                    text="Error connecting to database", 
                    text_color="red", 
                    font=("Poppins", 12)
                )
                self.status_label.place(x=75, y=130)
            else:
                self.status_label.configure(text="Error connecting to database", text_color="red")

    def show_reset_password_form(self, username):
        # Clear the email section
        self.email_section.place_forget()
        
        # Adjust the reset section height and placement
        self.reset_section.configure(height=330)  # Increased height
        self.reset_section.place(x=0, y=80, relwidth=1)
        
        # Success message
        success_label = ctk.CTkLabel(
            self.reset_section, 
            text="Username found! You can reset your password now.", 
            text_color="green", 
            font=("Poppins", 12)
        )
        success_label.place(relx=0.5, y=5, anchor="center")  # Adjusted placement
        
        # Username (disabled)
        ctk.CTkLabel(
            self.reset_section, 
            text="Username", 
            text_color="black", 
            font=("Poppins", 14)
        ).place(x=75, y=30)
        
        username_entry = ctk.CTkEntry(
            self.reset_section, 
            width=300, 
            height=40, 
            fg_color="white", 
            text_color="black"
        )
        username_entry.insert(0, username)
        username_entry.configure(state="disabled")
        username_entry.place(x=75, y=60)
        
        # New Password
        ctk.CTkLabel(
            self.reset_section, 
            text="New Password", 
            text_color="black", 
            font=("Poppins", 14)
        ).place(x=75, y=100)
        
        self.new_password_entry = ctk.CTkEntry(
            self.reset_section, 
            width=300, 
            height=40, 
            show="*", 
            fg_color="white", 
            text_color="black"
        )
        self.new_password_entry.place(x=75, y=130)
        
        # Confirm New Password
        ctk.CTkLabel(
            self.reset_section, 
            text="Confirm New Password", 
            text_color="black", 
            font=("Poppins", 14)
        ).place(x=75, y=180)
        
        self.confirm_password_entry = ctk.CTkEntry(
            self.reset_section, 
            width=300, 
            height=40, 
            show="*", 
            fg_color="white", 
            text_color="black"
        )
        self.confirm_password_entry.place(x=75, y=210)
        
        # Save Changes Button
        save_button = ctk.CTkButton(
            self.reset_section,
            text="Save Changes",
            fg_color="black",
            text_color="white",
            width=300,
            height=40,
            corner_radius=5,
            command=lambda: self.update_password(username),
            font=("Poppins", 14, "bold")
        )
        save_button.place(x=75, y=260)
        
        # Status label for password update
        self.password_status_label = ctk.CTkLabel(
            self.reset_section, 
            text="", 
            text_color="black", 
            font=("Poppins", 12)
        )
        self.password_status_label.place(relx=0.5, y=10, anchor="center")

    def update_password(self, username):
        new_password = self.new_password_entry.get().strip()
        confirm_password = self.confirm_password_entry.get().strip()
        
        if not new_password or not confirm_password:
            self.password_status_label.configure(text="Please fill in all fields", text_color="red")
            return
            
        if new_password != confirm_password:
            self.password_status_label.configure(text="Passwords do not match", text_color="red")
            return
        
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor()
            
            # Update user password
            cursor.execute(
                "UPDATE users SET password = %s WHERE username = %s",
                (new_password, username)
            )
            conn.commit()
            conn.close()
            
            self.password_status_label.configure(text="Password updated successfully!", text_color="green")
            # Auto return to login after 2 seconds
            self.after(2000, self.back_to_login)
                
        except mysql.connector.Error as err:
            print(f"Database Error: {err}")
            self.password_status_label.configure(text="Error updating password", text_color="red")

    def back_to_login(self):
        # Close forgot password frame and return to login
        if hasattr(self, 'forgot_frame'):
            self.forgot_frame.destroy()