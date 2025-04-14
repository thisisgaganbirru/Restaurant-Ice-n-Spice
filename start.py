import customtkinter as ctk
from utils import resize_image
from  restaurantlogin import LoginPage 
from signup import SignupPage
from menu import MenuPage
from order import OrderPage
from ordertracking import OrderTrackingPage
from about import AboutPage
from contact import ContactPage
from account import CustomerAccountPage
from admin_dashboard import AdminHomePage
from admin_add_item import AddItemPage
from admin_update_item import UpdateItemPage
from admin_remove_item import RemoveItemPage
from admin_reports import ReportsPage
from admin_order_tracking import AdminOrderTrackingPage
# from admin_update_item import UpdateItemPage
# from admin_remove_item import RemoveItemPage
# from admin_reports import ReportsPage
# from admin_order_tracking import OrderTrackingPage
import os
import sys
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

    


# Main App Window
class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("600x700")
        self.title("Foodie - Ice & Spice")
        self.resizable(False, False)

        # Page container
        self.main_frame = ctk.CTkFrame(self, width=600, height=600)
        self.main_frame.pack(fill="both", expand=True)
        self.main_frame.pack_propagate(False)

        self.show_welcome_page()

    def clear_main_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def show_welcome_page(self):
        self.clear_main_frame()
        WelcomePage(self.main_frame, self.show_login_page).pack(fill="both", expand=True)

    def show_login_page(self):
        self.clear_main_frame()
        LoginPage(self.main_frame,self.show_signup_page, app =self).pack(fill="both", expand=True)
    
    def show_signup_page(self):
        self.clear_main_frame()
        SignupPage(self.main_frame, self.show_login_page).pack(fill="both", expand=True)
    
    def show_menu_page(self):
        self.clear_main_frame()
        menu_page = MenuPage(self.main_frame, app=self, user=self.logged_in_user)
        menu_page.pack(fill="both", expand=True)
        
    def show_order_page(self, user, cart):
        self.clear_main_frame()
        try:
            OrderPage(
                self.main_frame, 
                app=self, 
                user=user or {"username": "User"}, 
                cart=cart
            ).pack(fill="both", expand=True)
        except Exception as e:
            print(f"Error showing order page: {e}")

        
    def show_ordertracking_page(self):
        self.clear_main_frame()
        OrderTrackingPage(self.main_frame, app = self, user=self.logged_in_user).pack(fill="both", expand=True)
    
    # def show_menu_page(self):
    #     self.clear_main_frame()
    #     from menu import MenuPage
    #     MenuPage(self.main_frame, app=self).pack(fill="both", expand=True)

    def show_aboutus_page(self):
        self.clear_main_frame()
        AboutPage(self.main_frame, app=self).pack(fill="both", expand=True)

    def show_contact_page(self):
        self.clear_main_frame()
        ContactPage(self.main_frame, app=self).pack(fill="both", expand=True)

    def show_account_page(self):
        self.clear_main_frame()
        CustomerAccountPage(self.main_frame, app=self).pack(fill="both", expand=True)
    
    def show_adminHome_page(self):
        self.clear_main_frame()
        AdminHomePage(self.main_frame, app=self).pack(fill="both", expand=True)

    def show_adminAddItem_page(self):
        self.clear_main_frame()
        AddItemPage(self.main_frame, app=self).pack(fill="both", expand=True)

    def show_adminUpdateItem_page(self):
        self.clear_main_frame()
        UpdateItemPage(self.main_frame, app=self).pack(fill="both", expand=True)

    def show_adminRemoveItem_page(self):
        self.clear_main_frame()
        RemoveItemPage(self.main_frame, app=self).pack(fill="both", expand=True)

    def show_adminReports_page(self):
        self.clear_main_frame()
        ReportsPage(self.main_frame, app=self).pack(fill="both", expand=True)

    def show_adminOrderTracking_page(self):
        self.clear_main_frame()
        AdminOrderTrackingPage(self.main_frame, app=self).pack(fill="both", expand=True)

# Welcome Page Frame
class WelcomePage(ctk.CTkFrame):
    def __init__(self, parent, switch_to_login):
        super().__init__(parent)
        self.configure(width=600, height=600, fg_color="transparent")

        self.bg_img = resize_image((900,900),'images/backg.jpg')

        bg_label = ctk.CTkLabel(self, image=self.bg_img, text="")
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # All placed directly on the self frame
        ctk.CTkLabel(self, 
                                   text="Hey!\n    Foodie", 
                                   font=("Poppins", 32, "bold"), 
                                   text_color="black",bg_color="#EDEDED",
                                   fg_color="transparent").place(x=120, y=200)

        subtitle_label = ctk.CTkLabel(self, 
                                      text="Let's find your favorite food.", 
                                      font=("Poppins", 18), text_color="black",fg_color="transparent",
                                      bg_color="#EDEDED")
        subtitle_label.place(x=150, y=300)

        get_started_button = ctk.CTkButton(self, 
                                           text="GET STARTED →", 
                                           font=("Poppins", 16, "bold"), 
                                           fg_color="#F1D94B", text_color="black", bg_color="#EDEDED",
                                           corner_radius=25, width=180, height=50, 
                                           command=switch_to_login)
        get_started_button.place(x=250, y=350)

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
