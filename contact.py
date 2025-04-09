import customtkinter as ctk
from utils import resize_image
from headerNav import NavigationHeader

class ContactPage(ctk.CTkFrame):
    def __init__(self, parent, app=None):
        super().__init__(parent)
        self.app = app
        self.configure(width=600, height=600)

        self.create_header()
        self.create_contact_body()

    def create_header(self):
        """Create the navigation header."""
        NavigationHeader(self, app=self.app).pack(side="top", fill="x")

    def create_contact_body(self):

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
        ctk.CTkLabel(content_frame, text="Contact Us", font=("Poppins", 24, "bold"),
                     text_color="black").pack(pady=(20, 10))

        # Info content
        contact_info = (
            "📞 Phone: +1 (123) 456-7890\n"
            "📧 Email: support@iceandspice.com\n"
            "📍 Address: 123 Food Street, Flavor Town"
        )

        ctk.CTkLabel(content_frame, text=contact_info, font=("Poppins", 14),
                     text_color="black", justify="left", anchor="w", width=500).pack(pady=10)
