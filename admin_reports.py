import customtkinter as ctk
from dbconnection import DB_CONFIG
import mysql.connector
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime, timedelta
import calendar
from admin_nav import AdminNav
import json
from decimal import Decimal
import pandas as pd
import csv
import os
from tkinter import messagebox

class AdminReportsPage(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.configure(fg_color="white")
        self.pack(fill="both", expand=True)
        
        # Create main container
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.pack(fill="both", expand=True)
        
        # Create header and body
        self.create_header()
        self.create_reports_body()
        
    def create_header(self):
        # Nav on left
        AdminNav(self.main_container, app=self.app).pack(side="left", fill="y")
        
    def create_reports_body(self):
        # Main body frame
        self.body_frame = ctk.CTkFrame(self.main_container, fg_color="#F1E8DD")
        self.body_frame.pack(side="right", fill="both", expand=True)
        
        # Stats Frame at top
        self.create_stats_frame()
        
        # Header with title and controls
        self.create_header_controls()
        
        # Content container
        content_frame = ctk.CTkFrame(self.body_frame, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Left frame (60%)
        left_frame = ctk.CTkFrame(content_frame, fg_color="white", corner_radius=10)
        left_frame.pack(side="left", fill="both", expand=True, padx=(0,10), pady=0)
        
        # Right frame container (40%)
        right_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        right_frame.pack(side="right", fill="both", expand=True, padx=(10,0), pady=0)
        
        # Create content in frames
        self.create_top_selling_items(left_frame)
        self.create_category_chart(right_frame)
        self.create_customer_heatmap(right_frame)
        
    def create_stats_frame(self):
        stats_frame = ctk.CTkFrame(self.body_frame, fg_color="transparent", height=120)
        stats_frame.pack(fill="x", padx=20, pady=20)
        
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor(dictionary=True)

            cursor.execute("""
                SELECT 
                    SUM(Total_price) as total_income,
                    COUNT(*) as total_sales,
                    COUNT(DISTINCT UserName) as total_customers
                FROM `Order`
            """)
            result = cursor.fetchone()
            
            total_income = result['total_income'] or 0
            total_expenses = total_income * Decimal("0.2")
            total_sales = result['total_sales'] or 0
            total_customers = result['total_customers'] or 0
            
            # Create stat cards
            stats = [
                ("Total Income", f"£{total_income:.2f}", "+15.5%"),
                ("Total Expenses", f"£{total_expenses:.2f}", "+8.5%"),
                ("Total Sales", str(total_sales), "+8.1%"),
                ("Customers", str(total_customers), "+25.8%")
            ]
            
            for title, value, change in stats:
                card = self.create_stat_card(stats_frame, title, value, change)
                card.pack(side="left", fill="both", expand=True, padx=5)

            conn.close()

        except mysql.connector.Error as err:
            print(f"Database Error: {err}")
            
    def create_header_controls(self):
        header_frame = ctk.CTkFrame(self.body_frame, fg_color="transparent", height=50)
        header_frame.pack(fill="x", padx=20, pady=10)
        
        # Title
        ctk.CTkLabel(
            header_frame,
            text="Reports",
            font=("Poppins", 24, "bold"),
            text_color="#2B2B2B"
        ).pack(side="left")
        
        # Download button
        ctk.CTkButton(
            header_frame,
            text="Download Report",
            font=("Poppins", 12),
            fg_color="#7747FF",
            text_color="white",
            hover_color="#5F35D5",
            command=self.download_report
        ).pack(side="right", padx=5)
        
        # Filter dropdown
        self.filter_var = ctk.StringVar(value="All Time")
        ctk.CTkOptionMenu(
            header_frame,
            values=["All Time", "Today", "This Week", "This Month"],
            variable=self.filter_var,
            font=("Poppins", 12),
            fg_color="white",
            text_color="black",
            button_color="#F1D94B",
            button_hover_color="#E5CE45",
            command=self.update_reports
        ).pack(side="right", padx=5)
        
    def create_stat_card(self, parent, title, value, change):
        card = ctk.CTkFrame(parent, fg_color="#2B2B2B", corner_radius=15)
        
        ctk.CTkLabel(
            card,
            text=title,
            font=("Poppins", 14),
            text_color="#8B8D93"
        ).pack(anchor="w", padx=15, pady=(15,5))
        
        ctk.CTkLabel(
            card,
            text=value,
            font=("Poppins", 24, "bold"),
            text_color="white"
        ).pack(anchor="w", padx=15, pady=2)
        
        ctk.CTkLabel(
            card,
            text=f"Increased {change} from last month",
            font=("Poppins", 10),
            text_color="#8B8D93"
        ).pack(anchor="w", padx=15, pady=(2,15))
        
        return card
        
    def create_top_selling_items(self, parent):
        # Title
        ctk.CTkLabel(
            parent,
            text="Top Selling Items",
            font=("Poppins", 16, "bold"),
            text_color="#2B2B2B"
        ).pack(anchor="w", padx=15, pady=10)
        
        # Headers
        headers_frame = ctk.CTkFrame(parent, fg_color="transparent")
        headers_frame.pack(fill="x", padx=15)
        headers = ["Product", "Sales", "Revenue", "Status"]
        
        # Configure grid columns
        headers_frame.grid_columnconfigure(0, weight=3)  # Product
        headers_frame.grid_columnconfigure(1, weight=2)  # Sales
        headers_frame.grid_columnconfigure(2, weight=2)  # Revenue
        headers_frame.grid_columnconfigure(3, weight=2)  # Status
        
        for i, text in enumerate(headers):
            ctk.CTkLabel(
                headers_frame,
                text=text,
                font=("Poppins", 12, "bold"),
                text_color="gray"
            ).grid(row=0, column=i, sticky="w", padx=5)
            
        # Items container
        items_frame = ctk.CTkScrollableFrame(parent, fg_color="transparent", height=500)
        items_frame.pack(fill="both", expand=True, padx=15, pady=10)
        
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor(dictionary=True)

            cursor.execute("""
                SELECT 
                    m.Name,
                    COUNT(*) as sales_count,
                    SUM(m.Price) as revenue,
                    m.Status
                FROM Menu m
                JOIN `Order` o ON m.MenuID IN (
                    SELECT JSON_EXTRACT(SUBSTRING_INDEX(SUBSTRING_INDEX(Item_list, '}}', 1), '{{', -1), '$.id')
                    FROM `Order`
                )
                GROUP BY m.MenuID, m.Name, m.Status
                ORDER BY sales_count DESC
            """)
            
            for item in cursor.fetchall():
                row = ctk.CTkFrame(items_frame, fg_color="transparent", height=40)
                row.pack(fill="x", pady=5)
                
                # Configure grid columns to match headers
                row.grid_columnconfigure(0, weight=3)
                row.grid_columnconfigure(1, weight=2)
                row.grid_columnconfigure(2, weight=2)
                row.grid_columnconfigure(3, weight=2)
                
                ctk.CTkLabel(
                    row,
                    text=item['Name'],
                    font=("Poppins", 12)
                ).grid(row=0, column=0, sticky="w", padx=5)
                
                ctk.CTkLabel(
                    row,
                    text=f"{item['sales_count']} pcs",
                    font=("Poppins", 12)
                ).grid(row=0, column=1, sticky="w", padx=5)
                
                ctk.CTkLabel(
                    row,
                    text=f"£{float(item['revenue']):.2f}",
                    font=("Poppins", 12)
                ).grid(row=0, column=2, sticky="w", padx=5)
                
                status_color = "#4CAF50" if item['Status'] == 'available' else "#FF9800"
                ctk.CTkLabel(
                    row,
                    text=item['Status'],
                    font=("Poppins", 12),
                    text_color=status_color
                ).grid(row=0, column=3, sticky="w", padx=5)

            conn.close()

        except mysql.connector.Error as err:
            print(f"Database Error: {err}")
            
    def create_category_chart(self, parent):
        chart_frame = ctk.CTkFrame(parent, fg_color="#2B2B2B", corner_radius=10)
        chart_frame.pack(fill="x", expand=True, pady=(0,10))
        
        ctk.CTkLabel(
            chart_frame,
            text="Category Sales",
            font=("Poppins", 16, "bold"),
            text_color="white"
        ).pack(anchor="w", padx=15, pady=10)
        
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor(dictionary=True)

            cursor.execute("""
                SELECT 
                    m.Category,
                    COUNT(*) as sales_count
                FROM Menu m
                JOIN `Order` o ON m.MenuID IN (
                    SELECT JSON_EXTRACT(SUBSTRING_INDEX(SUBSTRING_INDEX(Item_list, '}}', 1), '{{', -1), '$.id')
                    FROM `Order`
                )
                GROUP BY m.Category
                ORDER BY sales_count DESC
            """)
            
            results = cursor.fetchall()
            categories = [r['Category'] for r in results]
            counts = [r['sales_count'] for r in results]
            
            fig, ax = plt.subplots(figsize=(8, 4))
            fig.patch.set_facecolor('#2B2B2B')
            ax.set_facecolor('#2B2B2B')
            
            # Create bar chart
            bars = ax.bar(categories, counts, color='#F1D94B')
            
            # Customize appearance
            ax.set_xlabel('Categories', color='white')
            ax.set_ylabel('Sales Count', color='white')
            ax.tick_params(colors='white', which='both')
            plt.setp(ax.get_xticklabels(), color='white', rotation=45)
            plt.setp(ax.get_yticklabels(), color='white')
            
            # Remove spines
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.spines['bottom'].set_color('white')
            ax.spines['left'].set_color('white')
            
            plt.tight_layout()
            
            canvas = FigureCanvasTkAgg(fig, chart_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True, padx=15, pady=10)
            
            conn.close()

        except mysql.connector.Error as err:
            print(f"Database Error: {err}")
            
    def create_customer_heatmap(self, parent):
        heatmap_frame = ctk.CTkFrame(parent, fg_color="#2B2B2B", corner_radius=10)
        heatmap_frame.pack(fill="x", expand=True, pady=(10,0))
        
        header_frame = ctk.CTkFrame(heatmap_frame, fg_color="transparent")
        header_frame.pack(fill="x", padx=15, pady=10)
        
        ctk.CTkLabel(
            header_frame,
            text="Customers by time",
            font=("Poppins", 16, "bold"),
            text_color="white"
        ).pack(side="left")
        
        self.view_var = ctk.StringVar(value="Daily")
        ctk.CTkOptionMenu(
            header_frame,
            values=["Daily", "Weekly", "Monthly"],
            variable=self.view_var,
            font=("Poppins", 12),
            fg_color="#1C1C1C",
            text_color="white",
            button_color="#1C1C1C",
            button_hover_color="#2B2B2B",
            dropdown_fg_color="#1C1C1C",
            command=self.update_heatmap
        ).pack(side="right")
        
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor(dictionary=True)

            cursor.execute("""
                SELECT 
                    HOUR(CreatedAT) as hour,
                    DAYOFWEEK(CreatedAT) as day,
                    COUNT(*) as count
                FROM `Order`
                GROUP BY HOUR(CreatedAT), DAYOFWEEK(CreatedAT)
            """)
            
            results = cursor.fetchall()
            
            # Prepare data for heatmap
            days = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
            hours = ['10am', '12pm', '2pm', '4pm']
            data = [[0] * 7 for _ in range(4)]
            
            for row in results:
                hour_idx = (row['hour'] - 10) // 2  # Convert hour to index
                if 0 <= hour_idx < 4:  # Only include business hours
                    day_idx = row['day'] - 1
                    data[hour_idx][day_idx] = row['count']
            
            # Create heatmap
            fig, ax = plt.subplots(figsize=(8, 4))
            fig.patch.set_facecolor('#2B2B2B')
            ax.set_facecolor('#2B2B2B')
            
            # Create custom colormap
            colors = ['#1C1C1C', '#2B4C7E', '#4169E1']
            n_bins = 3
            cmap = plt.cm.Blues
            
            # Plot heatmap
            sns.heatmap(
                data,
                xticklabels=days,
                yticklabels=hours,
                cmap=cmap,
                annot=True,
                fmt='g',
                cbar=True,
                cbar_kws={'label': 'Customers'},
                ax=ax
            )
            
            # Customize appearance
            ax.set_title('Customer Traffic Pattern', color='white', pad=20)
            ax.tick_params(colors='white', which='both')
            plt.setp(ax.get_xticklabels(), color='white')
            plt.setp(ax.get_yticklabels(), color='white')
            
            # Customize colorbar
            cbar = ax.collections[0].colorbar
            cbar.ax.tick_params(colors='white')
            plt.setp(cbar.ax.get_yticklabels(), color='white')
            cbar.set_label('Customers', color='white')
            
            plt.tight_layout()
            
            canvas = FigureCanvasTkAgg(fig, heatmap_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True, padx=15, pady=10)
            
            conn.close()

        except mysql.connector.Error as err:
            print(f"Database Error: {err}")
            
    def update_reports(self, value=None):
        # Refresh all sections
        for widget in self.body_frame.winfo_children()[1:]:  # Skip header
            widget.destroy()
        self.create_reports_body()
        
    def update_heatmap(self, value=None):
        # Refresh heatmap with new view
        pass
        
    def download_report(self):
        try:
            # Create reports directory if it doesn't exist
            if not os.path.exists('reports'):
                os.makedirs('reports')
            
            # Connect to database
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor(dictionary=True)
            
            # Get orders data
            cursor.execute("""
                SELECT 
                    o.OrderID,
                    o.UserName,
                    o.Total_price,
                    o.Status,
                    o.CreatedAT,
                    m.Name as ItemName,
                    m.Category
                FROM `Order` o
                JOIN Menu m ON m.MenuID IN (
                    SELECT JSON_EXTRACT(SUBSTRING_INDEX(SUBSTRING_INDEX(Item_list, '}}', 1), '{{', -1), '$.id')
                    FROM `Order`
                    WHERE OrderID = o.OrderID
                )
            """)
            
            orders = cursor.fetchall()
            
            # Save to CSV
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'reports/orders_report_{timestamp}.csv'
            
            with open(filename, 'w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=orders[0].keys())
                writer.writeheader()
                writer.writerows(orders)
            
            # Save charts
            plt.figure(figsize=(10, 6))
            # Add chart generation code here
            plt.savefig(f'reports/charts_{timestamp}.png')
            
            conn.close()
            
            messagebox.showinfo("Success", f"Report downloaded successfully!\nLocation: {filename}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to download report: {str(e)}")
