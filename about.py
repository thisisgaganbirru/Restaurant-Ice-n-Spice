import customtkinter as ctk
from utils import resize_image
from headerNav import NavigationHeader

class AboutPage(ctk.CTkFrame):
    def __init__(self, parent, app=None):
        super().__init__(parent)
        self.app = app
        self.configure(width=600, height=700)

        self.create_header()
        self.create_about_body()

    def create_header(self):
        NavigationHeader(self, app=self.app).pack(side="top", fill="x")

    def create_about_body(self):

        # frame to hold the background image and content
        body_frame = ctk.CTkFrame(self, fg_color="transparent")
        body_frame.pack(fill="both", expand=True)

        # Background image
        self.bg_image = resize_image((800, 800), "images/loginbackground.png")
        bg_label = ctk.CTkLabel(body_frame, image=self.bg_image, text="")
        bg_label.pack(fill="both", expand=True)

        # Overlay content frame on top of the background
        content_frame = ctk.CTkFrame(body_frame, fg_color="transparent")
        content_frame.place(relx=0.5, rely=0.5, anchor="center")  # Center the content

        # Title
        ctk.CTkLabel(
            content_frame,
            text="About Us",
            font=("Poppins", 24, "bold"),
            text_color="black"
        ).pack(pady=(10, 15))

        # Description
        about_text = (
            "Welcome to Ice & Spice!\n"
            "We are passionate about serving delicious food to satisfy your cravings.\n"
            "Our kitchen is open daily from 10:00 AM to 10:00 PM.\n"
            "Come enjoy a great dining experience with us!"
        )

        ctk.CTkLabel(
            content_frame,
            text=about_text,
            font=("Poppins", 14),
            text_color="black",
            justify="center",
            width=500
        ).pack()
