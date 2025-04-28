import customtkinter as ctk
from utils import resize_image


class NavigationHeader(ctk.CTkFrame):
    def __init__(self, parent, app, user):
        super().__init__(parent)
        self.app = app
        self.user = user  
        self.configure(height=80, fg_color="white")
        self.pack_propagate(False)

        # Logo
        try:
            logo_img = resize_image((70, 70), 'images/restaurantlogo.png')
            logo_label = ctk.CTkLabel(self, image=logo_img, text="", cursor="hand2")
            logo_label.image = logo_img  # Prevent image being garbage collected
            logo_label.bind("<Button-1>", lambda e: self.app.show_customer_dashboard(self.user) if self.app else None)
            logo_label.pack(side="left", padx=(10, 40))
        except Exception:
            ctk.CTkLabel(self, text="Ice & Spice", font=("Poppins", 20, "bold"),
                         text_color="black").pack(side="left", padx=20)

        # Navigation buttons
        nav_frame = ctk.CTkFrame(self, fg_color="transparent")
        nav_frame.pack(side="right", padx=10)

        # Home
        self.home_label = ctk.CTkLabel(nav_frame, text="Home", cursor="hand2", font=("Poppins", 14),
                                       text_color="black")
        self.home_label.bind("<Button-1>", lambda e: self.app.show_customer_dashboard(self.user) if self.app else None)
        self.home_label.pack(side="left", padx=20)

        # About Us
        self.about_label = ctk.CTkLabel(nav_frame, text="About Us", cursor="hand2", font=("Poppins", 14),
                                        text_color="black")
        self.about_label.bind("<Button-1>", lambda e: self.app.show_about_page() if self.app else None)
        self.about_label.pack(side="left", padx=20)

        # Contact Us
        self.contact_label = ctk.CTkLabel(nav_frame, text="Contact Us", cursor="hand2", font=("Poppins", 14),
                                          text_color="black")
        self.contact_label.bind("<Button-1>", lambda e: self.app.show_contact_page() if self.app else None)
        self.contact_label.pack(side="left", padx=20)

        # Account
        self.account_label = ctk.CTkLabel(nav_frame, text="Account", cursor="hand2", font=("Poppins", 14),
                                          text_color="black")
        self.account_label.bind("<Button-1>", lambda e: self.app.show_account_page() if self.app else None)
        self.account_label.pack(side="left", padx=20)
