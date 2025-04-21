import customtkinter as ctk
from admin_nav import AdminNav
from dbconnection import DB_CONFIG
import mysql.connector
from datetime import datetime, timedelta
import pandas as pd
import numpy as np

class AdminStatsPage(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.configure(fg_color="#F1E8DD")
        self.pack(fill="both", expand=True)
        
        # Create main container
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.pack(fill="both", expand=True)
        
        # Create content area
        self.content_area = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.content_area.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Initialize stats
        self.stats_data = self.fetch_stats_data()
        self.create_stats_section()
        
    def create_stats_section(self):
        # Stats cards container
        stats_container = ctk.CTkFrame(self.content_area, fg_color="transparent")
        stats_container.pack(fill="x", pady=10)
        
        if self.stats_data:
            # Pending Orders Card
            pending_orders = self.stats_data['current']['pending_orders']
            pending_change = self.stats_data['changes']['pending']
            pending_text = f"{'increased' if pending_change >= 0 else 'decreased'} {abs(pending_change):.1f}% since past week"
            
            self.create_stat_card(
                stats_container,
                "Pending Orders",
                str(pending_orders),
                f"{'+' if pending_change >= 0 else ''}{pending_change:.1f}%",
                pending_text,
                "dark"
            )
            
            # Total Orders Card
            total_orders = self.stats_data['current']['total_orders']
            orders_change = self.stats_data['changes']['orders']
            orders_text = f"{'increased' if orders_change >= 0 else 'decreased'} {abs(orders_change):.1f}% since past week"
            
            self.create_stat_card(
                stats_container,
                "Total Orders",
                str(total_orders),
                f"{'+' if orders_change >= 0 else ''}{orders_change:.1f}%",
                orders_text,
                "light"
            )
            
            # Total Customers Card
            total_customers = self.stats_data['current']['total_customers']
            customers_change = self.stats_data['changes']['customers']
            customers_text = f"{'increased' if customers_change >= 0 else 'decreased'} {abs(customers_change):.1f}% since past week"
            
            self.create_stat_card(
                stats_container,
                "Total Customers",
                str(total_customers),
                f"{'+' if customers_change >= 0 else ''}{customers_change:.1f}%",
                customers_text,
                "light"
            )
            
            # Total Sales Card
            total_sales = self.format_currency(self.stats_data['current']['total_sales'])
            sales_change = self.stats_data['changes']['sales']
            sales_text = f"{'increased' if sales_change >= 0 else 'decreased'} {abs(sales_change):.1f}% since past week"
            
            self.create_stat_card(
                stats_container,
                "Total Sales",
                total_sales,
                f"{'+' if sales_change >= 0 else ''}{sales_change:.1f}%",
                sales_text,
                "light"
            )
        
    def create_stat_card(self, parent, title, value, percentage, subtitle, theme="light"):
        # Card container
        card = ctk.CTkFrame(
            parent,
            fg_color="#2B2B2B" if theme == "dark" else "white",
            corner_radius=10,
            width=250,
            height=150
        )
        card.pack(side="left", padx=10, fill="both", expand=True)
        card.pack_propagate(False)
        
        # Header with title and menu icon
        header = ctk.CTkFrame(card, fg_color="transparent")
        header.pack(fill="x", padx=15, pady=(15, 5))
        
        # Icon and title container
        icon_title = ctk.CTkFrame(header, fg_color="transparent")
        icon_title.pack(side="left")
        
        # Title icon (placeholder for now)
        icon = ctk.CTkLabel(
            icon_title,
            text="📊",
            font=("Poppins", 16),
            text_color="white" if theme == "dark" else "black"
        )
        icon.pack(side="left", padx=(0, 5))
        
        # Title
        title_label = ctk.CTkLabel(
            icon_title,
            text=title,
            font=("Poppins", 14),
            text_color="white" if theme == "dark" else "black"
        )
        title_label.pack(side="left")
        
        # Menu icon (three dots)
        menu_icon = ctk.CTkLabel(
            header,
            text="⋮",
            font=("Poppins", 16),
            text_color="white" if theme == "dark" else "gray"
        )
        menu_icon.pack(side="right")
        
        # Value and percentage container
        value_container = ctk.CTkFrame(card, fg_color="transparent")
        value_container.pack(fill="x", padx=15, pady=5)
        
        # Main value
        value_label = ctk.CTkLabel(
            value_container,
            text=value,
            font=("Poppins", 24, "bold"),
            text_color="white" if theme == "dark" else "black"
        )
        value_label.pack(side="left")
        
        # Percentage change
        percentage_label = ctk.CTkLabel(
            value_container,
            text=percentage,
            font=("Poppins", 12),
            text_color="#4CAF50" if "+" in percentage else "#FF5252"
        )
        percentage_label.pack(side="left", padx=10)
        
        # Subtitle
        subtitle_label = ctk.CTkLabel(
            card,
            text=subtitle,
            font=("Poppins", 12),
            text_color="gray70"
        )
        subtitle_label.pack(fill="x", padx=15, pady=(0, 15))
        
    def fetch_stats_data(self):
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor(dictionary=True)
            
            # Get current week's data
            current_week_query = """
                SELECT 
                    COUNT(*) as total_orders,
                    COUNT(CASE WHEN orderStatus = 'pending' THEN 1 END) as pending_orders,
                    COUNT(DISTINCT UserID) as total_customers,
                    SUM(Total_price) as total_sales
                FROM `Order`
                WHERE CreatedAT >= DATE_SUB(CURRENT_DATE(), INTERVAL WEEKDAY(CURRENT_DATE()) DAY)
                AND CreatedAT < DATE_ADD(DATE_SUB(CURRENT_DATE(), INTERVAL WEEKDAY(CURRENT_DATE()) DAY), INTERVAL 7 DAY)
            """
            
            # Get last week's data
            last_week_query = """
                SELECT 
                    COUNT(*) as total_orders,
                    COUNT(CASE WHEN orderStatus = 'pending' THEN 1 END) as pending_orders,
                    COUNT(DISTINCT UserID) as total_customers,
                    SUM(Total_price) as total_sales
                FROM `Order`
                WHERE CreatedAT >= DATE_SUB(CURRENT_DATE(), INTERVAL WEEKDAY(CURRENT_DATE()) + 7 DAY)
                AND CreatedAT < DATE_SUB(CURRENT_DATE(), INTERVAL WEEKDAY(CURRENT_DATE()) DAY)
            """
            
            # Get daily data for trend analysis
            daily_data_query = """
                SELECT 
                    DATE(CreatedAT) as order_date,
                    COUNT(*) as daily_orders,
                    COUNT(CASE WHEN orderStatus = 'pending' THEN 1 END) as daily_pending,
                    COUNT(DISTINCT UserID) as daily_customers,
                    SUM(Total_price) as daily_sales
                FROM `Order`
                WHERE CreatedAT >= DATE_SUB(CURRENT_DATE(), INTERVAL 14 DAY)
                GROUP BY DATE(CreatedAT)
                ORDER BY order_date
            """
            
            cursor.execute(current_week_query)
            current_stats = cursor.fetchone()
            
            cursor.execute(last_week_query)
            last_stats = cursor.fetchone()
            
            cursor.execute(daily_data_query)
            daily_data = cursor.fetchall()
            
            # Convert daily data to pandas DataFrame for trend analysis
            df = pd.DataFrame(daily_data)
            
            # Calculate week-over-week changes
            changes = {
                'pending': self.calculate_percentage_change(
                    last_stats['pending_orders'],
                    current_stats['pending_orders']
                ),
                'orders': self.calculate_percentage_change(
                    last_stats['total_orders'],
                    current_stats['total_orders']
                ),
                'customers': self.calculate_percentage_change(
                    last_stats['total_customers'],
                    current_stats['total_customers']
                ),
                'sales': self.calculate_percentage_change(
                    last_stats['total_sales'],
                    current_stats['total_sales']
                )
            }
            
            conn.close()
            
            return {
                'current': current_stats,
                'last': last_stats,
                'changes': changes,
                'trends': {
                    'orders': df['daily_orders'].tolist() if not df.empty else [],
                    'pending': df['daily_pending'].tolist() if not df.empty else [],
                    'customers': df['daily_customers'].tolist() if not df.empty else [],
                    'sales': df['daily_sales'].tolist() if not df.empty else []
                }
            }
            
        except mysql.connector.Error as err:
            print(f"Database Error: {err}")
            return None
            
    def calculate_percentage_change(self, old_value, new_value):
        if not old_value or not new_value:
            return 0
        try:
            old_val = float(old_value)
            new_val = float(new_value)
            if old_val == 0:
                return 100 if new_val > 0 else 0
            return ((new_val - old_val) / old_val) * 100
        except (ValueError, TypeError):
            return 0
            
    def format_currency(self, amount):
        if not amount:
            return "$0.00"
        try:
            return f"${float(amount):,.2f}"
        except (ValueError, TypeError):
            return "$0.00" 