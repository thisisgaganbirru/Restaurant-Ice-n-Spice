import customtkinter as ctk
from PIL import Image
from utils import resize_image
from dbconnection import DB_CONFIG
import mysql.connector

class CustomerHomePage(ctk.CTkFrame):
    def __init__(self, parent, user, switch_to_login):
        super().__init__(parent)
        self.user = user
        self.switch_to_login = switch_to_login
        self.configure(width=500, height=650, fg_color="transparent")

        self.bg_img = resize_image((700, 600), "images/loginbackground.png")
        bg_label = ctk.CTkLabel(self, image=self.bg_img, text="")
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.create_home_frame()

    def create_home_frame(self):
        home_frame = ctk.CTkFrame(self, width=320, height=350, fg_color="#F9F0E5", corner_radius=20)
        home_frame.place(relx=0.5, rely=0.5, anchor="center")

        welcome_text = f"Welcome, {self.user.get('username', 'Guest')}!"
        home_label = ctk.CTkLabel(home_frame, text=welcome_text, text_color="black", font=("Poppins", 22, "bold"))
        home_label.place(relx=0.5, y=30, anchor="center")

        menu_button = ctk.CTkButton(home_frame, text="Menu", fg_color="black", text_color="white",
                                    width=240, height=50, corner_radius=10,
                                    command=self.open_menu, font=("Poppins", 16, "bold"))
        menu_button.place(x=40, y=80)

        order_tracking_button = ctk.CTkButton(home_frame, text="Order Tracking", fg_color="#4CAF50", text_color="white",
                                              width=240, height=50, corner_radius=10,
                                              command=self.open_order_tracking, font=("Poppins", 16, "bold"))
        order_tracking_button.place(x=40, y=150)

        logout_button = ctk.CTkButton(home_frame, text="🚪 Logout", fg_color="#F1D94B", text_color="black",
                                      width=100, height=35, corner_radius=5,
                                      command=self.logout, font=("Poppins", 14, "bold"))
        logout_button.place(relx=0.5, y=320, anchor="center")

    def open_menu(self):
        from menu import MenuPage
        self.master.clear_main_frame()
        MenuPage(self.master, self.user).pack(fill="both", expand=True)

    def open_order_tracking(self):
        from order_tracking import OrderTrackingPage
        self.master.clear_main_frame()
        OrderTrackingPage(self.master, self.user).pack(fill="both", expand=True)

    def logout(self):
        self.switch_to_login()

# Function to fetch user (if still needed elsewhere)
def get_user_from_id(user_id):
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, username, role FROM users WHERE id = %s", (user_id,))
    user = cursor.fetchone()
    conn.close()
    return user
