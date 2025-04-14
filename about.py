import customtkinter as ctk
from utils import resize_image
from headerNav import NavigationHeader

class AboutPage(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.configure(width=600, height=700, fg_color="transparent")
        
        self.create_about_page()

    def create_about_page(self):
        # Add navigation header
        NavigationHeader(self, app=self.app).pack(side="top", fill="x")

        # Main body frame
        self.body_frame = ctk.CTkFrame(self, fg_color="#EDEDED")
        self.body_frame.pack(fill="both", expand=True)

        try:
            self.bg_image = resize_image((900, 900), "images/loginbackground.png")
            bg_label = ctk.CTkLabel(self.body_frame, image=self.bg_image, text="")
            bg_label.place(relx=0, rely=0, relwidth=1, relheight=1)
        except Exception as e:
            print("[Background Error]", e)

        # Content frame
        content_frame = ctk.CTkFrame(self.body_frame, fg_color="#F9F0E5")
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Center white frame
        center_frame = ctk.CTkFrame(content_frame, fg_color="#FFFFFF", corner_radius=15)
        center_frame.pack(fill="both", expand=True, padx=40, pady=40)

        # Title
        ctk.CTkLabel(
            center_frame,
            text="About Us",
            font=("Poppins", 32, "bold"),
            text_color="black"
        ).pack(pady=(30,20))

        # Welcome text
        ctk.CTkLabel(
            center_frame,
            text="Welcome to Ice & Spice!",
            font=("Poppins", 18),
            text_color="black"
        ).pack(pady=(0,20))

        # Description text
        description_frame = ctk.CTkFrame(center_frame, fg_color="transparent")
        description_frame.pack(fill="x", padx=50)

        descriptions = [
            "We are passionate about serving delicious food to satisfy your cravings.",
            "Our kitchen is open daily from 10:00 AM to 10:00 PM",
            "Come enjoy a great dining experience with us!"
        ]

        for desc in descriptions:
            ctk.CTkLabel(
                description_frame,
                text=desc,
                font=("Poppins", 14),
                text_color="black",
                wraplength=400,
                justify="center"
            ).pack(pady=5)

        # Restaurant tag
        ctk.CTkLabel(
            center_frame,
            text="@icenspicerestaurant",
            font=("Poppins", 12),
            text_color="gray"
        ).pack(side="bottom", pady=20)
