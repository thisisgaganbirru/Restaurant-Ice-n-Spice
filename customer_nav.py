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

        # Logout
        self.logout_label = ctk.CTkLabel(nav_frame, text="Logout", cursor="hand2", font=("Poppins", 14),
                                         text_color="red")
        self.logout_label.bind("<Button-1>", lambda e: self.logout())
        self.logout_label.pack(side="left", padx=20)

    def logout(self):
        # Create a popup frame
        popup = ctk.CTkToplevel(self)
        popup.title("Logout Successful")
        popup.geometry("500x500")
        popup.resizable(False, False)

        # Center the popup on the screen
        popup.update_idletasks()
        x = (popup.winfo_screenwidth() - 500) // 2
        y = (popup.winfo_screenheight() - 500) // 2
        popup.geometry(f"500x500+{x}+{y}")

        # Configure the popup appearance
        popup.configure(fg_color="white")

        # Add a success message
        ctk.CTkLabel(
            popup,
            text="Logout Successful!",
            font=("Poppins", 24, "bold"),
            text_color="green"
        ).pack(pady=(100, 20))

        ctk.CTkLabel(
            popup,
            text="Returning to login page...",
            font=("Poppins", 16),
            text_color="black"
        ).pack(pady=(0, 20))

        # Schedule the popup to close and navigate to the login page
        popup.after(3000, lambda: [popup.destroy(), self.app.show_login()])

        # Debugging message
        print("User logged out")
