from admin_base import AdminBasePage
import customtkinter as ctk
from utils import resize_image 
import os

class AdminHomePage(AdminBasePage):
    def __init__(self, parent, app):
        super().__init__(parent, app, "Dashboard")
        self.create_dashboard()

    def create_dashboard(self):
        # Stats container
        stats_frame = ctk.CTkFrame(self.main_content, fg_color="transparent")
        stats_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Create stat cards
        self.create_stat_card(stats_frame, "Total Orders", "156", "#4CAF50")
        self.create_stat_card(stats_frame, "Pending Orders", "23", "#FFA000")
        self.create_stat_card(stats_frame, "Total Revenue", "$2,345", "#2196F3")
        self.create_stat_card(stats_frame, "Total Items", "45", "#9C27B0")

        # Recent orders section
        orders_card = self.create_content_card("Recent Orders", height=300)
        orders_card.pack(fill="x", padx=20, pady=20)

        # Create scrollable frame for orders
        orders_list = ctk.CTkScrollableFrame(
            orders_card,
            fg_color="transparent",
            height=250
        )
        orders_list.pack(fill="both", expand=True, padx=15, pady=(0,10))

        # Sample orders (replace with actual data)
        for i in range(5):
            self.create_order_row(orders_list, f"#00000{i+1}", "Pending", f"${20+i}.99")

    def create_stat_card(self, parent, title, value, color):
        card = ctk.CTkFrame(
            parent,
            fg_color="#2b2b2b",
            corner_radius=10,
            width=200,
            height=100
        )
        card.pack(side="left", padx=10, pady=10)
        card.pack_propagate(False)

        ctk.CTkLabel(
            card,
            text=title,
            font=("Poppins", 14),
            text_color="gray"
        ).pack(anchor="w", padx=15, pady=(15,5))

        ctk.CTkLabel(
            card,
            text=value,
            font=("Poppins", 24, "bold"),
            text_color=color
        ).pack(anchor="w", padx=15)

    def create_order_row(self, parent, order_id, status, amount):
        row = ctk.CTkFrame(parent, fg_color="#333333", height=50)
        row.pack(fill="x", pady=2)
        row.pack_propagate(False)

        ctk.CTkLabel(
            row,
            text=order_id,
            font=("Poppins", 12),
            text_color="white"
        ).pack(side="left", padx=15)

        status_color = "#4CAF50" if status == "Completed" else "#FFA000"
        ctk.CTkLabel(
            row,
            text=status,
            font=("Poppins", 12),
            text_color=status_color
        ).pack(side="left", padx=15)

        ctk.CTkLabel(
            row,
            text=amount,
            font=("Poppins", 12),
            text_color="white"
        ).pack(side="right", padx=15)
