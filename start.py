import customtkinter as ctk
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os, sys
from utils import resize_image
from restaurantlogin import LoginPage
from signup import SignupPage
from customer_menu import MenuPage
from customer_order import OrderPage
from customer_ordertracking import OrderTrackingPage
from customer_account import CustomerAccountPage
from customer_about import AboutPage
from customer_contact import ContactPage
from admin_nav import AdminNav


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Foodie – Ice & Spice")
        self.geometry("600x700")
        self.resizable(False, False)

        # container for swapping frames
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(fill="both", expand=True)

        # track logged in user
        self.logged_in_user = None

        # start here
        self.show_welcome()

    def clear_main_frame(self):
        for w in self.main_frame.winfo_children():
            w.destroy()

    # ─── Flow Pages ──────────────────────────────────────────────────────────────

    def show_welcome(self):
        """Landing page → Get Started → Login"""
        self.clear_main_frame()
        WelcomePage(
            parent=self.main_frame,
            switch_to_login=self.show_login
        ).pack(fill="both", expand=True)

    def show_signup(self):
        """From Login: “Create account” → back to Login"""
        self.clear_main_frame()
        SignupPage(
            parent=self.main_frame,
            switch_to_login=self.show_login
        ).pack(fill="both", expand=True)

    def show_login(self):
        """From Welcome or Signup → Login → dispatch by role"""
        self.clear_main_frame()
        LoginPage(
            parent=self.main_frame,
            switch_to_signup=self.show_signup,
            app=self
        ).pack(fill="both", expand=True)

    # ─── after login Dashboards ──────────────────────────────────────────────────

    def show_customer_dashboard(self, user):
        """After login as customer → show MenuPage"""
        self.logged_in_user = user
        self.geometry("600x700")
        self.clear_main_frame()
        MenuPage(self.main_frame, app=self, user=self.logged_in_user).pack(fill="both", expand=True)
    
    def show_order_page(self, user, cart):
        self.clear_main_frame()
        OrderPage(self.main_frame, app=self, user=user, cart=cart).pack(fill="both", expand=True)
    
    def show_order_tracking_page(self):
        """Navigate to the Order Tracking page."""
        self.clear_main_frame()
        OrderTrackingPage(self.main_frame, app=self, user=self.logged_in_user).pack(fill="both", expand=True)
    
    def show_about_page(self):
        self.clear_main_frame()
        AboutPage(self.main_frame, app=self, user=self.logged_in_user).pack(fill="both", expand=True)
    
    def show_contact_page(self):
        self.clear_main_frame()
        ContactPage(self.main_frame, app=self, user=self.logged_in_user).pack(fill="both", expand=True)
    
    def show_account_page(self):
        self.clear_main_frame()
        CustomerAccountPage(self.main_frame, app=self, user=self.logged_in_user).pack(fill="both", expand=True)

    def show_admin_dashboard(self, user):
        """After login as admin → show AdminNav (with its own pages)"""
        self.logged_in_user = user
        self.geometry("1000x700")
        self.clear_main_frame()
        AdminNav(self.main_frame, self).pack(fill="both", expand=True)
        
    def logout(self):
        self.logged_in_user = None
        self.geometry("600x700")
        self.show_login()

# ─── Watchdog (auto-reload on .py changes) ────────────────────────────────────

class ChangeHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.endswith('.py'):
            print(f'{event.src_path} changed — restarting…')
            python = sys.executable
            os.execv(python, [python] + sys.argv)

# ─── Welcome Page ─────────────────────────────────────────────────────────────

class WelcomePage(ctk.CTkFrame):
    def __init__(self, parent, switch_to_login):
        super().__init__(parent)
        self.configure(fg_color="transparent")

        # background
        bg = resize_image((900,900), "images/backg.jpg")
        ctk.CTkLabel(self, image=bg, text="").place(x=0, y=0, relwidth=1, relheight=1)

        # title & subtitle
        ctk.CTkLabel(self, text="Hey!\n    Foodie",
                     font=("Poppins",32,"bold"),
                     text_color="black",  bg_color="#EDEDED",
                     fg_color="transparent").place(x=120,y=200)
        ctk.CTkLabel(self, text="Let's find your favorite food.",
                     font=("Poppins",18),
                     text_color="black", bg_color="#EDEDED",
                     fg_color="transparent").place(x=150,y=300)

        # Get Started → Login
        ctk.CTkButton(self,
            text="GET STARTED →",
            font=("Poppins",16,"bold"),
            fg_color="#F1D94B",  bg_color="#EDEDED",
            text_color="black",
            corner_radius=25,
            width=180, height=50,
            command=switch_to_login
        ).place(x=250,y=350)

# ─── Boot the App ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    # start auto-reload
    handler  = ChangeHandler()
    observer = Observer()
    observer.schedule(handler, ".", recursive=True)
    observer.start()

    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("green")

    try:
        app = App()
        app.mainloop()
    finally:
        observer.stop()
        observer.join()
