import customtkinter as ctk
from PIL import Image
import os
import importlib

class AdminNav(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.parent = parent
        self.current_page = None
        self.page_instances = {}  # Store page instances
        
        # Create main container
        self.main_container = ctk.CTkFrame(parent, fg_color="transparent")
        self.main_container.pack(fill="both", expand=True)
        
        # Create and pack navigation sidebar
        self.sidebar = self.create_sidebar()
        self.sidebar.pack(in_=self.main_container, side="left", fill="y")
        
        # Create content frame
        self.content_frame = ctk.CTkFrame(self.main_container, fg_color="white")
        self.content_frame.pack(side="left", fill="both", expand=True)
        
        # Define available pages and their modules
        self.pages = {
            "admin_dashboard": {"module": "admin_dashboard", "class": "AdminDashboard"},
            "admin_orders": {"module": "admin_orders", "class": "AdminOrdersPage"},
            "admin_reports": {"module": "admin_reports", "class": "AdminReportsPage"},
            "admin_customers": {"module": "admin_customers", "class": "AdminCustomersPage"},
            "admin_support": {"module": "admin_support", "class": "AdminSupport"}
        }
        
        # Show dashboard by default
        self.show_page("admin_dashboard")
    
    def create_sidebar(self):
        sidebar = ctk.CTkFrame(self.main_container, fg_color="#2B2B2B", width=180, height=700)
        sidebar.pack_propagate(False)
        
        # Logo
        self.create_logo(sidebar)
        
        # Navigation buttons with icons
        nav_items = [
            ("Dashboard", "admin_dashboard", "images/adminMenu.png"),
            ("Orders", "admin_orders", "images/adminOrders.png"),
            ("Reports", "admin_reports", "images/adminReport.png"),
            ("Customers", "admin_customers", "images/adminCustomers.png"),
            ("Support", "admin_support", "images/adminSupport.png")
        ]
        
        # Create navigation buttons container
        nav_container = ctk.CTkFrame(sidebar, fg_color="transparent")
        nav_container.pack(fill="x", expand=False, pady=(20, 0))
        
        self.nav_buttons = {}
        for text, page_name, icon_path in nav_items:
            try:
                # Load and create icon
                icon_img = Image.open(icon_path)
                icon = ctk.CTkImage(light_image=icon_img, dark_image=icon_img, size=(20, 20))
            except Exception as e:
                print(f"Failed to load icon {icon_path}: {str(e)}")
                icon = None
            
            # Create button with icon
            btn = ctk.CTkButton(
                nav_container,
                text=text,
                image=icon if icon else None,
                font=("Poppins", 13),
                fg_color="transparent",
                text_color="white",
                hover_color="#F1D94B",
                anchor="w",
                height=40,
                compound="left",  # This makes the icon appear on the left of the text
                command=lambda p=page_name: self.show_page(p)
            )
            btn.pack(fill="x", padx=10, pady=2)
            self.nav_buttons[page_name] = btn
        
        # Create bottom frame for logout button
        bottom_frame = ctk.CTkFrame(sidebar, fg_color="transparent")
        bottom_frame.pack(side="bottom", fill="x", padx=10, pady=10)
        
        # Add logout button with icon
        try:
            logout_icon = Image.open("images/logout.png")
            logout_img = ctk.CTkImage(light_image=logout_icon, dark_image=logout_icon, size=(20, 20))
        except Exception as e:
            print(f"Failed to load logout icon: {str(e)}")
            logout_img = None
            
        logout_btn = ctk.CTkButton(
            bottom_frame,
            text="Logout",
            image=logout_img if logout_img else None,
            font=("Poppins", 13),
            fg_color="#F1D94B",
            text_color="black",
            hover_color="#E5CE45",
            height=35,
            corner_radius=8,
            compound="left",
            command=self.app.logout
        )
        logout_btn.pack(fill="x")
        
        return sidebar
    
    def create_logo(self, parent):
        logo_frame = ctk.CTkFrame(parent, fg_color="transparent", height=100)
        logo_frame.pack(fill="x", pady=(20, 30), padx=10)
        
        try:
            logo_img = Image.open("images/restaurantLogo.png")
            logo = ctk.CTkImage(light_image=logo_img, dark_image=logo_img, size=(60, 60))
            logo_label = ctk.CTkLabel(logo_frame, image=logo, text="")
            logo_label.place(relx=0.5, rely=0.5, anchor="center")
        except:
            ctk.CTkLabel(
                logo_frame,
                text="Ice'n Spice",
                font=("Poppins", 18, "bold"),
                text_color="white"
            ).place(relx=0.5, rely=0.5, anchor="center")
    
    def show_page(self, page_name):
        # If this is the same page, do nothing
        if self.current_page == page_name:
            return
            
        # Hide current page if it exists
        if self.current_page and self.current_page in self.page_instances:
            self.page_instances[self.current_page].pack_forget()
        
        # Update active button (highlight)
        for name, btn in self.nav_buttons.items():
            if name == page_name:
                btn.configure(fg_color="#F1D94B", text_color="black")
            else:
                btn.configure(fg_color="transparent", text_color="white")
        
        # Check if page instance already exists, if not create it
        if page_name not in self.page_instances:
            # Import the module and create an instance
            page_info = self.pages.get(page_name)
            if page_info:
                try:
                    # Try to reload the module for development purposes
                    module = importlib.import_module(page_info["module"])
                    # Reload in case there were changes
                    importlib.reload(module)
                    # Get the class from the module
                    page_class = getattr(module, page_info["class"])
                    # Create an instance of the page
                    self.page_instances[page_name] = page_class(self.content_frame, self.app)
                except Exception as e:
                    # Handle any errors
                    error_frame = ctk.CTkFrame(self.content_frame)
                    ctk.CTkLabel(
                        error_frame, 
                        text=f"Error loading {page_name}: {str(e)}", 
                        text_color="red"
                    ).pack(pady=20)
                    self.page_instances[page_name] = error_frame
        
        # Show the page
        self.page_instances[page_name].pack(fill="both", expand=True)
        self.current_page = page_name
    
    def refresh_current_page(self):
        """Refresh the content of the current page"""
        if self.current_page:
            # Remove existing instance
            if self.current_page in self.page_instances:
                self.page_instances[self.current_page].destroy()
                del self.page_instances[self.current_page]
            # Show the page again (which will recreate it)
            self.show_page(self.current_page)