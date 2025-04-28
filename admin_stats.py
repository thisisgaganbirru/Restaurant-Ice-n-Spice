import customtkinter as ctk
from dbconnection import DB_CONFIG
import mysql.connector
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import threading
import time
from tkcalendar import DateEntry

class AdminStatsPage(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.configure(width=800, height=200, fg_color="#F1E8DD")
        self.pack(fill="both", expand=True)
        
        # Date range options
        self.date_range = "week"  # Default to weekly view
        
        # Create main container
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.pack(fill="both", expand=True)
        self.main_container.pack_propagate(False)
        
        # Create filter frame at the top
        self.filter_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.filter_frame.pack(fill="x", pady=(10, 3))
        
        # Create date filter in the filter frame (placed at top right)
        self.create_date_filter()
        
        # Create content area for stats cards
        self.content_area = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.content_area.pack(fill="both", expand=True, padx=5, pady=(0, 5))
        
        # Initialize stats
        self.stats_data = self.fetch_stats_data()
        self.create_stats_section()
        
        # Start live indicator blinking
        self.blink_thread = threading.Thread(target=self.blink_live_indicator, daemon=True)
        self.blink_thread.start()
        
    def create_date_filter(self):        
        # Create a container that will be pushed to the right
        right_container = ctk.CTkFrame(self.filter_frame, fg_color="transparent")
        right_container.pack(side="right", padx=(0, 15))
        
        # Left container for label and dropdown (inside the right container)
        filter_container = ctk.CTkFrame(right_container, fg_color="transparent")
        filter_container.pack(side="left")
        
        # Label
        filter_label = ctk.CTkLabel(
            filter_container, 
            text="Filter by:", 
            font=("Poppins", 14, "bold"),
            text_color="black"
        )
        filter_label.pack(side="left", padx=(0, 5), pady=(0, 5))
        
        # Create dropdown for date ranges
        range_options = ["Day", "Week", "Month", "Custom"]
        range_values = {"Day": "day", "Week": "week", "Month": "month", "Custom": "custom"}
        
        # Set default selected value based on self.date_range
        default_option = next((key for key, value in range_values.items() if value == self.date_range), "Week")
        
        # Create the dropdown
        self.range_dropdown = ctk.CTkOptionMenu(
            filter_container,
            values=range_options,
            command=self.handle_dropdown_change,
            width=120,
            height=30,
            fg_color="#2B2B2B",
            button_color="#808080",
            button_hover_color="#F1D94B",
            dropdown_hover_color="#F1D94B",
            text_color="white",
            font=("Poppins", 12)
        )
        self.range_dropdown.set(default_option)
        self.range_dropdown.pack(side="left", padx=5)
        
        # Calendar container (initially hidden)
        self.calendar_frame = ctk.CTkFrame(right_container, fg_color="transparent")
        self.calendar_frame.pack(side="left", padx=(20, 0))
        
        # From date
        from_frame = ctk.CTkFrame(self.calendar_frame, fg_color="transparent")
        from_frame.pack(side="left", padx=(0, 5))
        
        ctk.CTkLabel(
            from_frame,
            text="From:",
            font=("Poppins", 12),
            text_color="black"
        ).pack(side="left", padx=(0, 5))
        
        self.from_cal = DateEntry(
            from_frame,
            width=12,
            background='#F1D94B',
            foreground='black',
            borderwidth=2,
            date_pattern='yyyy-mm-dd',
            maxdate=datetime.now()
        )
        self.from_cal.pack(side="left")
        
        # To date
        to_frame = ctk.CTkFrame(self.calendar_frame, fg_color="transparent")
        to_frame.pack(side="left", padx=5)
        
        ctk.CTkLabel(
            to_frame,
            text="To:",
            font=("Poppins", 12),
            text_color="black"
        ).pack(side="left", padx=(0, 5))
        
        self.to_cal = DateEntry(
            to_frame,
            width=12,
            background='#F1D94B',
            foreground='black',
            borderwidth=2,
            date_pattern='yyyy-mm-dd',
            maxdate=datetime.now()
        )
        self.to_cal.pack(side="left")
        
        # Apply button
        apply_btn = ctk.CTkButton(
            self.calendar_frame,
            text="Apply",
            width=60,
            height=25,
            fg_color="#2B2B2B",
            hover_color="#F1D94B",
            command=self.apply_custom_dates
        )
        apply_btn.pack(side="left", padx=10)
        
        # Set initial calendar values
        self.from_cal.set_date(datetime.now() - timedelta(days=30))
        self.to_cal.set_date(datetime.now())
        
        # Calendar is hidden by default
        self.calendar_visible = False
        self.calendar_frame.pack_forget()

    def handle_dropdown_change(self, selection):
        # Map the display text back to value
        range_values = {"Day": "day", "Week": "week", "Month": "month", "Custom": "custom"}
        range_type = range_values.get(selection, "week")
        
        # If custom is selected, show calendar
        if range_type == "custom":
            if not self.calendar_visible:
                self.calendar_frame.pack(side="left", padx=(20, 0))
                self.calendar_visible = True
        else:
            # Hide calendar if not custom
            if self.calendar_visible:
                self.calendar_frame.pack_forget()
                self.calendar_visible = False
            
            # Update date range and refresh stats
            self.date_range = range_type
            self.stats_data = self.fetch_stats_data()
            
            # Clear content area and rebuild stats
            for widget in self.content_area.winfo_children():
                widget.destroy()
                
            self.create_stats_section()

    def apply_custom_dates(self):
        try:
            self.custom_start_date = datetime.strptime(self.from_cal.get(), "%Y-%m-%d")
            self.custom_end_date = datetime.strptime(self.to_cal.get(), "%Y-%m-%d")
            
            # Validate date range
            if self.custom_end_date < self.custom_start_date:
                # You might want to show an error message here
                return
                    
            if self.custom_end_date > datetime.now():
                self.custom_end_date = datetime.now()
                self.to_cal.set_date(self.custom_end_date)
            
            # Set date range to custom and refresh stats
            self.date_range = "custom"
            self.stats_data = self.fetch_stats_data()
            
            # Clear content area and rebuild stats
            for widget in self.content_area.winfo_children():
                widget.destroy()
                
            self.create_stats_section()
        except ValueError as e:
            print(f"Date parsing error: {e}")
            # You might want to show an error message here
        
    def create_stats_section(self):
        # Stats cards container
        stats_container = ctk.CTkFrame(self.content_area, fg_color="transparent")
        stats_container.pack(fill="x", pady=10)
        
        if self.stats_data:
            # Pending Orders Card
            pending_orders = self.stats_data['current']['pending_orders']
            pending_change = self.stats_data['changes']['pending']
            time_period = self.get_time_period_text()
            pending_text = f"{'increased' if pending_change >= 0 else 'decreased'} {abs(pending_change):.1f}% {time_period}"
            
            self.pending_card, self.live_label = self.create_stat_card(
                stats_container,
                "Pending Orders",
                str(pending_orders),
                f"{'+' if pending_change >= 0 else ''}{pending_change:.1f}%",
                pending_text,
                "dark",
                live=True
            )
            
            # Total Orders Card
            total_orders = self.stats_data['current']['total_orders']
            orders_change = self.stats_data['changes']['orders']
            orders_text = f"{'increased' if orders_change >= 0 else 'decreased'} {abs(orders_change):.1f}% {time_period}"
            
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
            customers_text = f"{'increased' if customers_change >= 0 else 'decreased'} {abs(customers_change):.1f}% {time_period}"
            
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
            sales_text = f"{'increased' if sales_change >= 0 else 'decreased'} {abs(sales_change):.1f}% {time_period}"
            
            self.create_stat_card(
                stats_container,
                "Total Sales",
                total_sales,
                f"{'+' if sales_change >= 0 else ''}{sales_change:.1f}%",
                sales_text,
                "light"
            )
        
    def create_stat_card(self, parent, title, value, percentage, subtitle, theme="light", live=False):
        # Card container
        card = ctk.CTkFrame(
            parent,
            fg_color="#2B2B2B" if theme == "dark" else "white",
            corner_radius=8,
            width=200,
            height=120
        )
        card.pack(side="left", padx=5, fill="none", expand=True)
        card.pack_propagate(False)
        
        # Header with title and menu icon
        header = ctk.CTkFrame(card, fg_color="transparent")
        header.pack(fill="x", padx=5, pady=(0, 5))
        
        # Icon and title container
        stat_title = ctk.CTkFrame(header, fg_color="transparent")
        stat_title.pack(side="left")
        
        # Title
        title_label = ctk.CTkLabel(
            stat_title,
            text=title,
            font=("Helvetica", 14),
            text_color="white" if theme == "dark" else "black"
        )
        title_label.pack(side="left")
        
        # Live indicator (only for pending orders)
        live_label = None
        if live:
            live_frame = ctk.CTkFrame(header, fg_color="#FF5252", corner_radius=4, height=16)
            live_frame.pack(side="right", padx=2)
            
            live_label = ctk.CTkLabel(
                live_frame,
                text="LIVE",
                font=("Poppins", 10, "bold"),
                text_color="white",
                padx=5
            )
            live_label.pack()
        
        # Value and percentage container
        value_container = ctk.CTkFrame(card, fg_color="transparent")
        value_container.pack(fill="x", padx=3, pady=5)
        
        # Main value
        value_label = ctk.CTkLabel(
            value_container,
            text=value,
            font=("Poppins", 20, "bold"),
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
        percentage_label.pack(side="left", padx=8)
        
        # Subtitle
        subtitle_label = ctk.CTkLabel(
            card,
            text=subtitle,
            font=("Poppins", 11),
            text_color="gray70",
            wraplength=180
        )
        subtitle_label.pack(fill="x", padx=12, pady=(0, 5))
        
        if live:
            return card, live_label
        return card
        
    def blink_live_indicator(self):
        visible = True
        while True:
            if hasattr(self, 'live_label') and self.live_label:
                try:
                    if visible:
                        self.live_label.pack()
                    else:
                        self.live_label.pack_forget()
                    visible = not visible
                except:
                    pass  # Handle case where widget might be destroyed
            time.sleep(0.7)  # Blink interval
        
    def get_time_period_text(self):
        if self.date_range == "day":
            return "since yesterday"
        elif self.date_range == "week":
            return "since last week"
        elif self.date_range == "month":
            return "since last month"
        else:
            return "in selected period"
        
    def fetch_stats_data(self):
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor(dictionary=True)
            
            # Determine date ranges based on selected filter
            current_start, current_end, previous_start, previous_end = self.get_date_ranges()
            
            # Get current period data
            current_query = """
                SELECT 
                    COUNT(*) as total_orders,
                    COUNT(CASE WHEN orderStatus = 'pending' THEN 1 END) as pending_orders,
                    COUNT(DISTINCT UserID) as total_customers,
                    SUM(Total_price) as total_sales
                FROM `Order`
                WHERE CreatedAT >= %s AND CreatedAT < %s
            """
            
            # Get previous period data
            previous_query = """
                SELECT 
                    COUNT(*) as total_orders,
                    COUNT(CASE WHEN orderStatus = 'pending' THEN 1 END) as pending_orders,
                    COUNT(DISTINCT UserID) as total_customers,
                    SUM(Total_price) as total_sales
                FROM `Order`
                WHERE CreatedAT >= %s AND CreatedAT < %s
            """
            
            cursor.execute(current_query, (current_start, current_end))
            current_stats = cursor.fetchone()
            
            cursor.execute(previous_query, (previous_start, previous_end))
            previous_stats = cursor.fetchone()
            
            # Calculate period-over-period changes
            changes = {
                'pending': self.calculate_percentage_change(
                    previous_stats['pending_orders'],
                    current_stats['pending_orders']
                ),
                'orders': self.calculate_percentage_change(
                    previous_stats['total_orders'],
                    current_stats['total_orders']
                ),
                'customers': self.calculate_percentage_change(
                    previous_stats['total_customers'],
                    current_stats['total_customers']
                ),
                'sales': self.calculate_percentage_change(
                    previous_stats['total_sales'],
                    current_stats['total_sales']
                )
            }
            
            conn.close()
            
            return {
                'current': current_stats,
                'previous': previous_stats,
                'changes': changes
            }
            
        except mysql.connector.Error as err:
            print(f"Database Error: {err}")
            return None
            
    def get_date_ranges(self):
        now = datetime.now()
        
        if self.date_range == "day":
            # Current day vs previous day
            current_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
            current_end = now
            previous_start = current_start - timedelta(days=1)
            previous_end = current_start
            
        elif self.date_range == "week":
            # Current week vs previous week
            weekday = now.weekday()
            current_start = (now - timedelta(days=weekday)).replace(hour=0, minute=0, second=0, microsecond=0)
            current_end = now
            previous_start = current_start - timedelta(days=7)
            previous_end = current_start
            
        elif self.date_range == "month":
            # Current month vs previous month
            current_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            current_end = now
            
            # Previous month
            if current_start.month == 1:
                previous_start = current_start.replace(year=current_start.year-1, month=12)
            else:
                previous_start = current_start.replace(month=current_start.month-1)
            previous_end = current_start
            
        else:  # Custom date range
            # For custom date range, we use the same length of time for comparison
            if hasattr(self, 'custom_start_date') and hasattr(self, 'custom_end_date'):
                current_start = self.custom_start_date
                current_end = self.custom_end_date
                
                # Previous period of same length
                date_diff = (current_end - current_start).days
                previous_start = current_start - timedelta(days=date_diff)
                previous_end = current_start
            else:
                # Default to weekly if custom dates not set
                weekday = now.weekday()
                current_start = (now - timedelta(days=weekday)).replace(hour=0, minute=0, second=0, microsecond=0)
                current_end = now
                previous_start = current_start - timedelta(days=7)
                previous_end = current_start
                
        return current_start, current_end, previous_start, previous_end
            
    def calculate_percentage_change(self, old_value, new_value):
        if old_value is None or new_value is None:
            return 0
        try:
            old_val = float(old_value) if old_value else 0
            new_val = float(new_value) if new_value else 0
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