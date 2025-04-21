import customtkinter as ctk
from PIL import Image
import os
from utils import resize_image

class AdminNav(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.configure(fg_color="#2B2B2B", width=170)
        
        # Create main container
        self.nav_container = ctk.CTkFrame(self, fg_color="transparent")
        self.nav_container.pack(fill="both", expand=True, padx=10)
        
        # Logo section at top
        logo_frame = ctk.CTkFrame(self.nav_container, fg_color="transparent", height=100)
        logo_frame.pack(fill="x", pady=(20, 30))
        logo_frame.pack_propagate(False)
        
        # Load and display logo
        try:
            logo_path = os.path.join("images", "restaurantLogo.png")
            logo_img = resize_image((60, 60), logo_path)
            logo_label = ctk.CTkLabel(logo_frame, image=logo_img, text="")
            logo_label.place(relx=0.5, rely=0.5, anchor="center")
        except Exception as e:
            print(f"Error loading logo: {e}")
            ctk.CTkLabel(
                logo_frame,
                text="Ice'n Spice",
                font=("Poppins", 18, "bold"),
                text_color="white"
            ).place(relx=0.5, rely=0.5, anchor="center")
        
        # Navigation buttons with their respective icons
        nav_items = [
            ("Dashboard", "adminMenudashboard.png", lambda: self.app.show_page("admin_dashboard")),
            ("Orders", "adminOrders.png", lambda: self.app.show_page("admin_orders")),
            ("Reports", "adminReport.png", lambda: self.app.show_page("admin_reports")),
            ("Customers", "adminCustomers.png", lambda: self.app.show_page("admin_customers")),
            ("Support", "adminSupport.png", lambda: self.app.show_page("admin_support"))
        ]
        
        # Add navigation buttons with spacing
        for text, icon_path, command in nav_items:
            self.create_nav_button(text, icon_path, command)
            
        # Add flexible space before logout
        ctk.CTkFrame(self.nav_container, fg_color="transparent").pack(fill="both", expand=True)
        
        ctk.CTkButton(
            self.nav_container,
            text="Logout",
            font=("Poppins", 13),
            fg_color="#F1D94B",
            text_color="black",
            hover_color="#E5CE45",
            width=150,
            height=30,
            corner_radius=8,
            command=self.app.logout
        ).pack(pady=(0, 20))
    
    def create_nav_button(self, text, icon_path, command, is_logout=False):
        btn_container = ctk.CTkFrame(self.nav_container, fg_color="transparent", height=40)
        btn_container.pack(fill="x", pady=2)
        btn_container.pack_propagate(False)
        
        # Load and resize icon
        icon = None
        if not is_logout:
            try:
                icon_path = os.path.join("images", icon_path)
                icon_image = Image.open(icon_path)
                icon = ctk.CTkImage(light_image=icon_image, dark_image=icon_image, size=(18, 18))
            except Exception as e:
                print(f"Error loading icon {icon_path}: {e}")
        
        if is_logout:
            # Logout button with yellow background
            btn = ctk.CTkButton(
                btn_container,
                text=text,
                font=("Poppins", 14),
                fg_color="#F1D94B",
                text_color="black",
                hover_color="#E5CE45",
                height=35,
                corner_radius=8,
                command=command
            )
            btn.pack(padx=20, fill="x")
        else:
            # Regular nav button with icon
            btn = ctk.CTkButton(
                btn_container,
                text=text,
                image=icon,
                compound="left",
                anchor="w",
                font=("Poppins", 13),
                fg_color="transparent",
                text_color="white",
                hover_color="#3B3B3B",
                height=35,
                command=command
            )
            btn.pack(fill="x") 