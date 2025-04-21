import customtkinter as ctk
from utils import resize_image
from restaurantlogin import LoginPage
from signup import SignupPage
from menu import MenuPage
from order import OrderPage
from ordertracking import OrderTrackingPage
from about import AboutPage
from contact import ContactPage
from account import CustomerAccountPage
from admin_dashboard import AdminDashboard
from admin_orders import AdminOrdersPage
from admin_reports import AdminReportsPage
from admin_customers import AdminCustomersPage
from admin_support import AdminSupport
import os
import sys
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

    


# Main App Window
class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Foodie - Ice & Spice")
        self.geometry("600x700")
        self.resizable(False, False)
        
        # Create main container
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(fill="both", expand=True)
        
        # Initialize user data
        self.logged_in_user = None
        
        # Start with welcome page
        self.show_welcome_page()
    
    def show_welcome_page(self):
        self.clear_main_frame()
        WelcomePage(self.main_frame, self.show_login_page).pack(fill="both", expand=True)
    
    def show_login_page(self):
        self.clear_main_frame()
        LoginPage(self.main_frame, self.show_signup_page, app=self).pack(fill="both", expand=True)
    
    def show_signup_page(self):
        self.clear_main_frame()
        SignupPage(self.main_frame, self.show_login_page).pack(fill="both", expand=True)
    
    def show_customer_dashboard(self, user):
        self.logged_in_user = user
        self.geometry("600x700")
        self.clear_main_frame()
        MenuPage(self.main_frame, app=self, user=user).pack(fill="both", expand=True)
    
    def show_admin_dashboard(self, user):
        self.logged_in_user = user
        self.geometry("1000x600")
        self.clear_main_frame()
        AdminDashboard(self.main_frame, app=self).pack(fill="both", expand=True)
    
    def show_menu_page(self):
        self.clear_main_frame()
        MenuPage(self.main_frame, app=self, user=self.logged_in_user).pack(fill="both", expand=True)
    
    def show_order_page(self, user, cart):
        self.clear_main_frame()
        OrderPage(self.main_frame, app=self, user=user, cart=cart).pack(fill="both", expand=True)
    
    def show_ordertracking_page(self):
        self.clear_main_frame()
        OrderTrackingPage(self.main_frame, app=self, user=self.logged_in_user).pack(fill="both", expand=True)
    
    def show_about_page(self):
        self.clear_main_frame()
        AboutPage(self.main_frame, app=self).pack(fill="both", expand=True)
    
    def show_contact_page(self):
        self.clear_main_frame()
        ContactPage(self.main_frame, app=self).pack(fill="both", expand=True)
    
    def show_account_page(self):
        self.clear_main_frame()
        CustomerAccountPage(self.main_frame, app=self).pack(fill="both", expand=True)
    
    def show_page(self, page_name):
        self.clear_main_frame()
        
        # Set window size based on page type
        if page_name.startswith("admin_"):
            self.geometry("1000x600")
        else:
            self.geometry("600x700")
        
        # Show the requested page
        if page_name == "admin_dashboard":
            AdminDashboard(self.main_frame, self).pack(fill="both", expand=True)
        elif page_name == "admin_orders":
            AdminOrdersPage(self.main_frame, self).pack(fill="both", expand=True)
        elif page_name == "admin_reports":
            AdminReportsPage(self.main_frame, self).pack(fill="both", expand=True)
        elif page_name == "admin_customers":
            AdminCustomersPage(self.main_frame, self).pack(fill="both", expand=True)
        elif page_name == "admin_support":
            AdminSupport(self.main_frame, self).pack(fill="both", expand=True)
        elif page_name == "menu":
            self.show_menu_page()
    
    def clear_main_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()
    
    def logout(self):
        self.logged_in_user = None
        self.geometry("600x700")
        self.show_welcome_page()

class WelcomePage(ctk.CTkFrame):
    def __init__(self, parent, switch_to_login):
        super().__init__(parent)
        self.configure(fg_color="transparent")
        
        # Load background image
        self.bg_img = resize_image((900,900),'images/backg.jpg')
        bg_label = ctk.CTkLabel(self, image=self.bg_img, text="")
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        
        # Welcome text
        ctk.CTkLabel(
            self, 
            text="Hey!\n    Foodie", 
            font=("Poppins", 32, "bold"), 
            text_color="black",
            bg_color="#EDEDED",
            fg_color="transparent"
        ).place(x=120, y=200)
        
        # Subtitle
        ctk.CTkLabel(
            self, 
            text="Let's find your favorite food.", 
            font=("Poppins", 18),
            text_color="black",
            fg_color="transparent",
            bg_color="#EDEDED"
        ).place(x=150, y=300)
        
        # Get Started button
        ctk.CTkButton(
            self, 
            text="GET STARTED →", 
            font=("Poppins", 16, "bold"), 
            fg_color="#F1D94B",
            text_color="black",
            bg_color="#EDEDED",
            corner_radius=25,
            width=180,
            height=50, 
            command=switch_to_login
        ).place(x=250, y=350)

class ChangeHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.endswith('.py'):
            print(f'{event.src_path} has been modified. Restarting...')
            os.execv(sys.executable, ['python'] + sys.argv)

# Run the app
if __name__ == "__main__":
    # Start the watchdog observer
    path = '.'  # Directory to watch
    event_handler = ChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()

    try:
        # Run the Tkinter app
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("green")
        app = App()
        app.mainloop()
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
