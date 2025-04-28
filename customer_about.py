import customtkinter as ctk
from PIL import Image, ImageTk
from utils import resize_image
from customer_nav import NavigationHeader

class AboutPage(ctk.CTkFrame):
    def __init__(self, parent, app, user):
        super().__init__(parent)
        self.app = app
        self.user = user  
        self.configure(width=800, height=700, fg_color="#f5f0e9")
        
        # Store UI elements
        self.ui_elements = {}
        
        self.create_about_page()

    def create_about_page(self):
        # Add navigation header (using your existing NavigationHeader class)
        self.nav = NavigationHeader(self, app=self.app, user=self.user)
        self.nav.pack(side="top", fill="x")

        # Main content frame
        main_content = ctk.CTkFrame(self, fg_color="#f5f0e9", corner_radius=0)
        main_content.pack(fill="both", expand=True, padx=40, pady=40)
        
        # Create the white card
        about_card = ctk.CTkFrame(main_content, fg_color="white", corner_radius=20)
        about_card.pack(fill="both", expand=True, padx=0, pady=0)
        about_card.pack_propagate(False)
        
        # Content container (for center alignment)
        content_container = ctk.CTkFrame(about_card, fg_color="transparent")
        content_container.pack(padx=20, pady=40, fill="both", expand=True)
        
        # Section title
        title_label = ctk.CTkLabel(
            content_container,
            text="About Us",
            font=("Poppins", 36, "bold"),
            text_color="#333333"
        )
        title_label.pack(pady=(0, 25))
        
        # Welcome text
        welcome_label = ctk.CTkLabel(
            content_container,
            text="Welcome to Ice'n Spice!",
            font=("Poppins", 20, "italic", "bold"),
            text_color="#F1D94B" 
        )
        welcome_label.pack(pady=(0, 30))
        
        # Description
        description = ctk.CTkLabel(
            content_container,
            text="We are passionate about serving delicious food to satisfy your cravings. "
                 "Founded in 2020, our restaurant brings together the perfect blend of hot and cold "
                 "culinary delights from around the world.",
            font=("Poppins", 14),
            text_color="#555555",
            wraplength=400,
            justify="center"
        )
        description.pack(pady=(0, 20))
        
        # Hours frame with borders
        hours_frame = ctk.CTkFrame(content_container, fg_color="transparent", height=60)
        hours_frame.pack(fill="x", pady=20)
        
        # Add top border
        top_border = ctk.CTkFrame(hours_frame, height=1, fg_color="#f0f0f0")
        top_border.pack(fill="x", pady=(0, 15))
        
        # Hours text
        hours_label = ctk.CTkLabel(
            hours_frame,
            text="Our kitchen is open daily from 10:00 AM to 10:00 PM",
            font=("Poppins", 14, "bold"),
            text_color="#333333"
        )
        hours_label.pack(pady=5)
        
        # Add bottom border
        bottom_border = ctk.CTkFrame(hours_frame, height=1, fg_color="#f0f0f0")
        bottom_border.pack(fill="x", pady=(15, 0))
        
        # Call to action
        cta_label = ctk.CTkLabel(
            content_container,
            text="Come enjoy a great dining experience with us!",
            font=("Poppins", 16),
            text_color="#333333"
        )
        cta_label.pack(pady=(20, 40))
        
        # Social media handle
        social_frame = ctk.CTkFrame(content_container, fg_color="transparent")
        social_frame.pack(side="bottom", pady=10)
        
        # Try to create a circular @ icon
        social_icon_frame = ctk.CTkFrame(social_frame, width=24, height=24, corner_radius=12, fg_color="#F1D94B")
        social_icon_frame.pack(side="left", padx=(0, 8))
        
        social_icon = ctk.CTkLabel(social_icon_frame, text="@", font=("Poppins", 12, "bold"), text_color="white")
        social_icon.place(relx=0.5, rely=0.5, anchor="center")
        
        social_handle = ctk.CTkLabel(
            social_frame,
            text="icenspicerestaurant",
            font=("Poppins", 12),
            text_color="#999999"
        )
        social_handle.pack(side="left")