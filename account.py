import customtkinter as ctk
from utils import resize_image
from headerNav import NavigationHeader

# Account Page
class CustomerAccountPage(ctk.CTkFrame):
    def __init__(self, parent, app=None):
        super().__init__(parent)
        self.app = app
        self.configure(width=700, height=600)

        self.create_header()
        self.create_account_body()

    def create_header(self):
        NavigationHeader(self, app=self.app).pack(side="top", fill="x")

    def create_account_body(self):
        body_frame = ctk.CTkFrame(self, fg_color="transparent")
        body_frame.pack(fill="both", expand=True)

        # Background Image
        try:
            self.bg_image = resize_image((800, 800), "images/loginbackground.png")
            bg_label = ctk.CTkLabel(body_frame, image=self.bg_image, text="")
            bg_label.pack(fill="both", expand=True)
        except:
            pass

        
        content_frame = ctk.CTkFrame(body_frame, fg_color="transparent")
        content_frame.place(relx=0.5, rely=0.05, anchor="n")

        
        ctk.CTkLabel(content_frame, text="Personal Information", font=("Poppins", 24, "bold"), text_color="#660033").pack(pady=(10, 20))

        
        def create_info_box(icon, label_text, value_text):
            box = ctk.CTkFrame(content_frame, fg_color="white", width=500, height=70, corner_radius=10)
            box.pack(pady=5)
            box.pack_propagate(False)

            row = ctk.CTkFrame(box, fg_color="transparent")
            row.pack(fill="x", padx=10, pady=10)

            # Icon
            ctk.CTkLabel(row, text=icon, font=("Arial", 16)).pack(side="left", padx=(0, 10))

            # Text Info
            text_column = ctk.CTkFrame(row, fg_color="transparent")
            text_column.pack(side="left", fill="both", expand=True)

            ctk.CTkLabel(text_column, text=label_text, font=("Poppins", 14, "bold"), text_color="black").pack(anchor="w")
            ctk.CTkLabel(text_column, text=value_text, font=("Poppins", 12), text_color="gray").pack(anchor="w")

            return box

        # Info Cards
        create_info_box("👤", "Name", "Jane Doe")
        create_info_box("📅", "Date of Birth", "10-10-1975")
        create_info_box("📍", "Address", "123 Deming Dr, Mount Pleasant, 49588")
        create_info_box("🆘", "Emergency Contact", "Haley Doe")

        # Update Password Section
        ctk.CTkLabel(content_frame, text="Update Password", font=("Poppins", 20, "bold"), text_color="#660033").pack(pady=(20, 5))

        password_entry = ctk.CTkEntry(content_frame, placeholder_text="enter new password", width=300, height=35)
        password_entry.pack(pady=5)

        confirm_entry = ctk.CTkEntry(content_frame, placeholder_text="confirm new password", width=300, height=35)
        confirm_entry.pack(pady=5)

        # Log out button
        logout_btn = ctk.CTkButton(content_frame, text="Log Out", fg_color="#660033", text_color="white", width=200, height=40, corner_radius=25)
        logout_btn.pack(pady=20)

