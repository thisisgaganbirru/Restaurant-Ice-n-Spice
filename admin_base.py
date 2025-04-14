import customtkinter as ctk
from utils import resize_image

class AdminBasePage(ctk.CTkFrame):
    def __init__(self, parent, app, title="Admin Panel"):
        super().__init__(parent)
        self.app = app
        self.title = title
        self.configure(fg_color="transparent")
        
        self.create_base_layout()

    def create_base_layout(self):
        # Main container
        self.main_frame = ctk.CTkFrame(self, fg_color="#1a1a1a")  # Dark theme
        self.main_frame.pack(fill="both", expand=True)

        # Sidebar
        self.sidebar = ctk.CTkFrame(self.main_frame, fg_color="#2b2b2b", width=200)
        self.sidebar.pack(side="left", fill="y", padx=2, pady=2)
        self.sidebar.pack_propagate(False)

        # Logo frame
        logo_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent", height=100)
        logo_frame.pack(fill="x", padx=10, pady=10)
        logo_frame.pack_propagate(False)

        try:
            logo = resize_image((50, 50), "images/logo.png")
            ctk.CTkLabel(logo_frame, image=logo, text="").pack(pady=10)
        except:
            pass

        ctk.CTkLabel(
            logo_frame,
            text="Admin Panel",
            font=("Poppins", 16, "bold"),
            text_color="white"
        ).pack()

        # Navigation buttons
        self.create_nav_button("Dashboard", self.app.show_adminHome_page)
        self.create_nav_button("Add Item", self.app.show_adminAddItem_page)
        self.create_nav_button("Update Item", self.app.show_adminUpdateItem_page)
        self.create_nav_button("Remove Item", self.app.show_adminRemoveItem_page)
        self.create_nav_button("Order Tracking", self.app.show_adminOrderTracking_page)
        self.create_nav_button("Reports", self.app.show_adminReports_page)

        # Logout button at bottom
        ctk.CTkButton(
            self.sidebar,
            text="Logout",
            fg_color="#FF5252",
            hover_color="#FF1A1A",
            height=40,
            command=self.app.show_login_page
        ).pack(side="bottom", padx=20, pady=20, fill="x")

        # Content area
        self.content_area = ctk.CTkFrame(self.main_frame, fg_color="#333333")
        self.content_area.pack(side="left", fill="both", expand=True, padx=2, pady=2)

        # Header in content area
        header = ctk.CTkFrame(self.content_area, fg_color="#2b2b2b", height=60)
        header.pack(fill="x", padx=2, pady=2)
        header.pack_propagate(False)

        ctk.CTkLabel(
            header,
            text=self.title,
            font=("Poppins", 20, "bold"),
            text_color="white"
        ).pack(side="left", padx=20, pady=10)

        # Main content frame
        self.main_content = ctk.CTkFrame(self.content_area, fg_color="#333333")
        self.main_content.pack(fill="both", expand=True, padx=2, pady=2)

    def create_nav_button(self, text, command):
        btn = ctk.CTkButton(
            self.sidebar,
            text=text,
            fg_color="transparent",
            hover_color="#404040",
            anchor="w",
            height=40,
            command=command
        )
        btn.pack(fill="x", padx=10, pady=5)

    def create_content_card(self, title, width=300, height=200):
        card = ctk.CTkFrame(
            self.main_content,
            fg_color="#2b2b2b",
            corner_radius=10,
            width=width,
            height=height
        )
        
        if title:
            ctk.CTkLabel(
                card,
                text=title,
                font=("Poppins", 14, "bold"),
                text_color="white"
            ).pack(anchor="w", padx=15, pady=10)
            
        return card 