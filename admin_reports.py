import customtkinter as ctk
from dbconnection import DB_CONFIG
from adminreports_graph import FetchSalesGraph
from adminreports_graph import fetchHeatmapGraph
import mysql.connector
from datetime import datetime
import csv
from tkinter import messagebox, filedialog

class AdminReportsPage(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.configure(fg_color="#F1E8DD")
        
        # Initialize graph objects (imported from other file)
        self.sales_graph = FetchSalesGraph()
        self.customer_heatmap = fetchHeatmapGraph()
        
        # Current filter settings
        self.current_sort = "Category"  # Default sort
        self.months = self._get_month_list()
        self.categories = self._fetch_categories()
        
        # Create main layout sections
        self._create_title()
        self._create_main_content()
        self._create_footer()
        
        # Load initial data
        self.load_data()
        
    def _create_title(self):
        header_frame = ctk.CTkFrame(self, fg_color="#F1D94B", height=50)
        header_frame.pack(fill="x", padx=5, pady=10)
        header_frame.pack_propagate(False)
        
        # Title with updated styling
        ctk.CTkLabel(
            header_frame,
            text="Admin Reports Dashboard",
            font=("Poppins", 24, "bold"),
            text_color="black",
        ).pack(side="left", padx=10)
        
    def _create_main_content(self):
        """Create main content area with Two panels (left and right)"""
        content_frame = ctk.CTkFrame(self, fg_color="transparent", width=800, height=500)
        content_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        content_frame.pack_propagate(False)  # Prevent content frame from expanding
        
        # Left panel - Top Selling Items
        self.left_panel = ctk.CTkFrame(content_frame, fg_color="white", corner_radius=8)
        self.left_panel.pack(side="left", fill="both", expand=True, padx=(0, 5))
        self.left_panel.pack_propagate(False)  
        
        # Create top selling header with sort controls
        self.create_salesframe_header()
        
        # Create scrollable container for sales cards with custom styling
        self.cards_container = ctk.CTkScrollableFrame(
            self.left_panel,
            fg_color="transparent",
            scrollbar_fg_color="white",  # Match background color
            scrollbar_button_color="white",  # Match background color
            scrollbar_button_hover_color="#white",  # Light hover effect
            orientation="vertical",
            height=380  # Adjust height to fit within the panel
        )
        self.cards_container.pack(fill="both", expand=True, padx=0, pady=(0, 15))
        
        # Configure scrollbar to be outside the frame
        scrollbar = self.cards_container._scrollbar
        scrollbar.configure(width=8)  # Make scrollbar thinner
        
        # Right panel - Graphs
        self.right_panel = ctk.CTkFrame(content_frame, fg_color="white", corner_radius=8)
        self.right_panel.pack(side="right", fill="both", expand=True, padx=(10, 0))
        self.right_panel.pack_propagate(False)  # Prevent right panel from expanding
        self._create_graphs()
        
    def create_salesframe_header(self):
        """Create header for sales data table"""
        # Title Container
        title_container = ctk.CTkFrame(self.left_panel, fg_color="transparent")
        title_container.pack(fill="x", padx=15, pady=(15, 5))

        # Title
        ctk.CTkLabel(
            title_container,
            text="Top Selling items..",
            font=("Inter", 16, "bold"),
            text_color="black",
            anchor="w"
        ).pack(fill="x")

        # Create a new frame for dropdowns
        dropdown_frame = ctk.CTkFrame(self.left_panel, fg_color="white", height=50)
        dropdown_frame.pack(fill="x", padx=5, pady=(5, 5))
        dropdown_frame.pack_propagate(False)

        # Create left and right sections for dropdowns
        left_section = ctk.CTkFrame(dropdown_frame, fg_color="transparent")
        left_section.pack(side="left", padx=(10, 15), pady=10)

        right_section = ctk.CTkFrame(dropdown_frame, fg_color="transparent")
        right_section.pack(side="right", padx=(5, 15), pady=10)

        # Month Filter (Left Section)
        ctk.CTkLabel(
            left_section,
            text="Month:",
            font=("Inter", 13),
            text_color="black"
        ).pack(side="left", padx=(0, 5))

        self.month_combobox = ctk.CTkComboBox(
            left_section,
            values=self.months,
            width=120,
            height=28,
            font=("Inter", 13),
            fg_color="white",
            border_color="#E5E5E5",
            button_color="#E5E5E5",
            button_hover_color="#D5D5D5",
            dropdown_hover_color="#F5F5F5",
            command=self._handle_month_change
        )
        self.month_combobox.pack(side="left")
        self.month_combobox.set("All Time")

        # Category Filter (Right Section)
        ctk.CTkLabel(
            right_section,
            text="Category:",
            font=("Inter", 13),
            text_color="black"
        ).pack(side="left", padx=(0, 5))

        self.category_combobox = ctk.CTkComboBox(
            right_section,
            values=self.categories,
            width=120,
            height=28,
            font=("Inter", 13),
            fg_color="white",
            border_color="#E5E5E5",
            button_color="#E5E5E5",
            button_hover_color="#D5D5D5",
            dropdown_hover_color="#F5F5F5",
            command=self._handle_category_change
        )
        self.category_combobox.pack(side="left")
        self.category_combobox.set("All Categories")

        # Table Header frame with yellow background
        header_frame = ctk.CTkFrame(self.left_panel, fg_color="#F1D94B", height=35)
        header_frame.pack(fill="x", padx=15, pady=(5, 0))
        header_frame.pack_propagate(False)

        # Create columns in header
        columns = ["Category", "Month", "Orders", "Revenue", "Trend"]
        column_widths = [150, 100, 100, 100, 100]  # Proportional widths

        for i, (col, width) in enumerate(zip(columns, column_widths)):
            col_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
            col_frame.pack(side="left", fill="both", expand=True, padx=2)
            
            ctk.CTkLabel(
                col_frame,
                text=col,
                font=("Inter", 13, "bold"),
                text_color="black",
                anchor="w"
            ).pack(fill="both", expand=True, padx=5, pady=5)

    def create_sellframe_card(self, item_data):
        """Create a card showing sales data in table row format"""
        # Card frame
        card = ctk.CTkFrame(self.cards_container, fg_color="white", height=35)
        card.pack(fill="x", padx=15, pady=1)
        card.pack_propagate(False)

        # Category column
        category_frame = ctk.CTkFrame(card, fg_color="transparent", width=150)
        category_frame.pack(side="left", fill="both", expand=True, padx=2)
        ctk.CTkLabel(
            category_frame,
            text=item_data['Category'],
            font=("Inter", 13),
            text_color="black",
            anchor="w"
        ).pack(fill="both", expand=True, padx=5, pady=5)

        # Month column
        month_frame = ctk.CTkFrame(card, fg_color="transparent", width=150)
        month_frame.pack(side="left", fill="both", expand=True, padx=2)
        ctk.CTkLabel(
            month_frame,
            text=item_data['Month'],
            font=("Inter", 13),
            text_color="black",
            anchor="w"
        ).pack(fill="both", expand=True, padx=5, pady=5)

        # Orders column
        orders_frame = ctk.CTkFrame(card, fg_color="transparent", width=150)
        orders_frame.pack(side="left", fill="both", expand=True, padx=2)
        ctk.CTkLabel(
            orders_frame,
            text=str(item_data['Orders']),
            font=("Inter", 13),
            text_color="black",
            anchor="w"
        ).pack(fill="both", expand=True, padx=5, pady=5)

        # Revenue column
        revenue_frame = ctk.CTkFrame(card, fg_color="transparent", width=150)
        revenue_frame.pack(side="left", fill="both", expand=True, padx=2)
        ctk.CTkLabel(
            revenue_frame,
            text=f"$ {float(item_data['Revenue']):.2f}",
            font=("Inter", 13),
            text_color="black",
            anchor="w"
        ).pack(fill="both", expand=True, padx=5, pady=5)

        # Trend column
        trend_frame = ctk.CTkFrame(card, fg_color="transparent", width=150)
        trend_frame.pack(side="left", fill="both", expand=True, padx=2)
        
        # Calculate trend percentage
        prev_revenue = float(item_data.get('PrevRevenue', 0) or 0)
        current_revenue = float(item_data['Revenue'])
        if prev_revenue > 0:
            trend_pct = ((current_revenue - prev_revenue) / prev_revenue) * 100
            trend_text = f"↑ {trend_pct:.1f}%" if trend_pct > 0 else f"↓ {abs(trend_pct):.1f}%"
            trend_color = "#00B74A" if trend_pct > 0 else "#DC3545"
        else:
            if current_revenue > 0:
                trend_text = "↑ 100.0%"
                trend_color = "#00B74A"
            else:
                trend_text = "0.0%"
                trend_color = "gray"

        ctk.CTkLabel(
            trend_frame,
            text=trend_text,
            font=("Inter", 13),
            text_color=trend_color,
            anchor="w"
        ).pack(fill="both", expand=True, padx=5, pady=5)

    def _create_graphs(self):
        self.topgraph_frame = ctk.CTkFrame(self.right_panel, fg_color="transparent", height=250)
        self.topgraph_frame.pack(fill="x")  # Reduced padding
        self.topgraph_frame.pack_propagate(False)  # Prevent top graph frame from expanding

        # Sales by category graph container
        self.graphheader = ctk.CTkLabel(
            self.topgraph_frame,
            text="Sales by category:",
            font=("Inter", 16, "bold"),
            text_color="black",
            anchor="w"
        ).pack(fill="x", padx=2, pady=2)  # Reduced padding

        self.sales_graphcontainer = ctk.CTkFrame(self.topgraph_frame, fg_color="transparent")
        self.sales_graphcontainer.pack(fill="both", expand=True)  # Reduced padding
        self.sales_graphcontainer.pack_propagate(False)  # Prevent sales graph container from expanding
        
        # Call the graph method
        try:
            print("Creating sales graph...")
            self.sales_graph.create_graph(self.sales_graphcontainer)
            print("Sales graph created successfully")
        except Exception as e:
            print(f"Error creating sales graph: {e}")
            import traceback
            traceback.print_exc()
        
        # Bottom graph frame for customer heatmap
        self.bottomgraph_frame = ctk.CTkFrame(self.right_panel, fg_color="transparent", height=250)
        self.bottomgraph_frame.pack(fill="x")  # Reduced padding
        self.bottomgraph_frame.pack_propagate(False)  # Prevent bottom graph frame from expanding

        # Customer traffic heatmap container
        self.graphheader = ctk.CTkLabel(
            self.bottomgraph_frame,
            text="Customer by orderTime:",
            font=("Inter", 16, "bold"),
            text_color="black",
            anchor="w"
        ).pack(fill="x", padx=2, pady=2)  # Reduced padding

        self.traffic_graphcontainer = ctk.CTkFrame(self.bottomgraph_frame, fg_color="transparent")
        self.traffic_graphcontainer.pack(fill="both", expand=True)  # Reduced padding
        self.traffic_graphcontainer.pack_propagate(False)  # Prevent traffic graph container from expanding
        
        # Call the graph method
        try:
            print("Creating heatmap...")
            self.customer_heatmap.create_graph(self.traffic_graphcontainer)
            print("Heatmap created successfully")
        except Exception as e:
            print(f"Error creating heatmap: {e}")
            import traceback
            traceback.print_exc()
        
        def _update_graphs(self):
            try:
                # Clear and recreate sales graph
                if hasattr(self, 'sales_graphcontainer'):
                    for widget in self.sales_graphcontainer.winfo_children():
                        widget.destroy()
                    # Use create_graph instead of create_monthly_sales_graph
                    self.sales_graph.create_graph(self.sales_graphcontainer)

                # Clear and recreate heatmap
                if hasattr(self, 'traffic_graphcontainer'):
                    for widget in self.traffic_graphcontainer.winfo_children():
                        widget.destroy()
                    # Use create_graph instead of create_daily_heatmap
                    self.customer_heatmap.create_graph(self.traffic_graphcontainer)
                    
            except Exception as e:
                print(f"Error updating graphs: {e}")
                # Add more detailed error reporting
                import traceback
                traceback.print_exc()


        
    def _create_footer(self):
        """Create the footer with action buttons"""
        footer = ctk.CTkFrame(self, fg_color="transparent", height=40)
        footer.pack(fill="x", padx=20, pady=(0, 20))
        footer.pack_propagate(False)
        
        # Left side - Refresh button
        left_buttons = ctk.CTkFrame(footer, fg_color="transparent")
        left_buttons.pack(side="left")
        
        # Refresh button
        ctk.CTkButton(
            left_buttons,
            text="Refresh",
            font=("Inter", 13),
            fg_color="#0096FF",
            hover_color="#0084E0",
            height=35,
            width=100,
            corner_radius=5,
            command=self.load_data
        ).pack(side="left", padx=(0, 10))
        
        # Right side - Download controls
        download_frame = ctk.CTkFrame(footer, fg_color="transparent")
        download_frame.pack(side="right")
        
        # Filter label
        ctk.CTkLabel(
            download_frame,
            text="Download Filter by:",
            font=("Inter", 13),
            text_color="black"
        ).pack(side="left", padx=(0, 5))
        
        # Month filter combobox
        self.month_filter = ctk.CTkComboBox(
            download_frame,
            values=["All Time", "This Month", "Last Month", "This Year"],
            width=150,
            height=35,
            font=("Inter", 13),
            fg_color="white",
            border_color="#F1D94B",
            button_color="#F1D94B",
            button_hover_color="#E1C93B",
            dropdown_hover_color="#F5F5F5"
        )
        self.month_filter.pack(side="left", padx=(0, 10))
        self.month_filter.set("All Time")
        
        # Download button
        ctk.CTkButton(
            download_frame,
            text="Download Report",
            font=("Inter", 13),
            fg_color="#00B74A",
            hover_color="#00A040",
            height=35,
            width=140,
            corner_radius=5,
            command=self.download_report
        ).pack(side="right", padx=(10, 0))
        
    def _get_month_list(self):
        """Get list of months for filtering"""
        return ["All Time", "January", "February", "March", "April", "May", "June", 
                "July", "August", "September", "October", "November", "December"]

    def _fetch_categories(self):
        """Fetch all categories from the database"""
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor()
            cursor.execute("SELECT DISTINCT Category FROM Menu ORDER BY Category")
            categories = [row[0] for row in cursor.fetchall()]
            conn.close()
            return ["All Categories"] + categories
        except Exception as e:
            print(f"Error fetching categories: {e}")
            return ["All Categories"]

    def load_data(self):
        """Load data from database and display it"""
        try:
            # Clear existing cards
            for widget in self.cards_container.winfo_children():
                widget.destroy()
            
            # Connect to database
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor(dictionary=True)
            
            selected_month = self.month_combobox.get()
            selected_category = self.category_combobox.get()

            if selected_month == "All Time":
                # Base query for all-time view
                query = """
                    SELECT 
                        m.Category,
                        'All Time' as Month,
                        COUNT(o.OrderID) as Orders,
                        COALESCE(SUM(o.Total_price), 0) as Revenue,
                        (
                            SELECT COALESCE(SUM(o2.Total_price), 0)
                            FROM `Order` o2
                            WHERE EXISTS (
                                SELECT 1
                                FROM Menu m2
                                WHERE m2.Category = m.Category
                                AND JSON_CONTAINS(o2.Item_list, JSON_OBJECT('MenuID', m2.MenuID))
                            )
                            AND YEAR(o2.CreatedAT) = YEAR(CURDATE())
                            AND MONTH(o2.CreatedAT) = MONTH(CURDATE()) - 1
                        ) as PrevRevenue
                    FROM Menu m
                    LEFT JOIN `Order` o ON JSON_CONTAINS(o.Item_list, JSON_OBJECT('MenuID', m.MenuID))
                    WHERE YEAR(o.CreatedAT) = YEAR(CURDATE())
                """
                if selected_category != "All Categories":
                    query += f" AND m.Category = '{selected_category}'"
                query += " GROUP BY m.Category ORDER BY Revenue DESC"
                cursor.execute(query)
            else:
                # Query for specific month
                month_num = self.months.index(selected_month)
                query = """
                    WITH CurrentMonthData AS (
                        SELECT 
                            m.Category,
                            %s as Month,
                            COUNT(o.OrderID) as Orders,
                            COALESCE(SUM(o.Total_price), 0) as Revenue
                        FROM Menu m
                        LEFT JOIN `Order` o ON o.MenuID = m.MenuID
                        WHERE YEAR(o.CreatedAT) = YEAR(CURDATE())
                        AND MONTH(o.CreatedAT) = %s
                        GROUP BY m.Category
                    ),
                    PrevMonthData AS (
                        SELECT 
                            m.Category,
                            COALESCE(SUM(o.Total_price), 0) as PrevRevenue
                        FROM Menu m
                        LEFT JOIN `Order` o ON o.MenuID = m.MenuID
                        WHERE YEAR(o.CreatedAT) = YEAR(CURDATE())
                        AND MONTH(o.CreatedAT) = %s
                        GROUP BY m.Category
                    )
                    SELECT 
                        CASE 
                            WHEN cmd.Category IS NOT NULL THEN cmd.Category 
                            ELSE m.Category 
                        END as Category,
                        cmd.Month,
                        COALESCE(cmd.Orders, 0) as Orders,
                        COALESCE(cmd.Revenue, 0) as Revenue,
                        COALESCE(pmd.PrevRevenue, 0) as PrevRevenue
                    FROM Menu m
                    LEFT JOIN CurrentMonthData cmd ON cmd.Category = m.Category
                    LEFT JOIN PrevMonthData pmd ON pmd.Category = m.Category
                """
                if selected_category != "All Categories":
                    query += f" WHERE m.Category = '{selected_category}'"
                query += " GROUP BY m.Category ORDER BY Revenue DESC"
                cursor.execute(query, (selected_month, month_num, month_num - 1 if month_num > 1 else 12))
            
            self.current_data = cursor.fetchall()
            
            # Display cards
            if not self.current_data:
                ctk.CTkLabel(
                    self.cards_container,
                    text="No data available for the selected filters",
                    font=("Inter", 14),
                    text_color="gray"
                ).pack(pady=50)
            else:
                # Show cards sorted by revenue
                sorted_items = sorted(
                    self.current_data,
                    key=lambda x: x['Revenue'],
                    reverse=True
                )
                for item in sorted_items:
                    self.create_sellframe_card(item)
            
            # Update graphs with new data
            self._update_graphs()
            
            conn.close()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load data: {str(e)}")
            print(f"Error details: {str(e)}")  # For debugging

    def _update_graphs(self):
        """Update both graphs with current data"""
        try:
            # Update sales graph
            if hasattr(self, 'sales_graphcontainer'):
                for widget in self.sales_graphcontainer.winfo_children():
                    widget.destroy()
                self.sales_graph.create_monthly_sales_graph(self.sales_graphcontainer)

            # Update customer heatmap
            if hasattr(self, 'traffic_graphcontainer'):
                for widget in self.traffic_graphcontainer.winfo_children():
                    widget.destroy()
                self.customer_heatmap.create_daily_heatmap(self.traffic_graphcontainer)
        except Exception as e:
            print(f"Error updating graphs: {e}")

    def _handle_month_change(self, choice):
        """Handle month filter change"""
        self.load_data()

    def _handle_category_change(self, choice):
        """Handle category filter change"""
        self.load_data()

    def _handle_sort_change(self, choice):
        """Handle sort dropdown change"""
        self.load_data()
        
    def _show_month_options(self):
        """Show dropdown menu for month selection"""
        months = ["January", "February", "March", "April", "May", "June",
                 "July", "August", "September", "October", "November", "December"]
        
        # Create dropdown window
        dropdown = ctk.CTkToplevel(self)
        dropdown.attributes('-topmost', True)
        dropdown.overrideredirect(True)
        
        # Position dropdown below the month label
        x = self.month_label.winfo_rootx()
        y = self.month_label.winfo_rooty() + self.month_label.winfo_height()
        dropdown.geometry(f"120x{len(months)*30}+{x}+{y}")
        
        # Function to handle month selection
        def select_month(month):
            self.month_label.configure(text=month)
            self.current_month_filter = month
            dropdown.destroy()
            
            # Filter data by selected month
            if month != "Month" and hasattr(self, 'current_data'):
                self._filter_by_month(month)
        
        # Create buttons for each month
        for month in months:
            btn = ctk.CTkButton(
                dropdown,
                text=month,
                font=("Inter", 13),
                fg_color="white",
                text_color="black",
                hover_color="#F0F0F0",
                height=30,
                corner_radius=0,
                command=lambda m=month: select_month(m)
            )
            btn.pack(fill="x")
    
    def _filter_by_month(self, month):
        """Filter displayed cards by selected month"""
        # Get all data first
        self.load_data()
        
        # Then filter by month
        if month != "Month":
            # Clear existing cards
            for widget in self.cards_container.winfo_children():
                widget.destroy()
            
            # Filter the data to show only selected month
            filtered_data = [item for item in self.current_data if item['Month'] == month]
            
            if not filtered_data:
                ctk.CTkLabel(
                    self.cards_container,
                    text=f"No data available for {month}",
                    font=("Inter", 14),
                    text_color="gray"
                ).pack(pady=50)
            else:
                for item in filtered_data:
                    self.create_sellframe_card(item)
        
    def download_report(self):
        try:
            # Get the selected filter value
            filter_value = self.month_filter.get()
            
            # Import and initialize BusinessReportExporter
            from adminreport_download import BusinessReportExporter
            exporter = BusinessReportExporter()
            
            # Call the export method with the filter value
            exporter.export_business_report(filter_value)
            
            # Show success message
            messagebox.showinfo("Download", "Report downloaded successfully!")
        except Exception as e:
            # Show error message if something goes wrong
            messagebox.showerror("Error", f"Failed to download report: {str(e)}")
