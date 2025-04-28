import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import mysql.connector
from dbconnection import DB_CONFIG
import customtkinter as ctk
import traceback
import json
from datetime import datetime
import matplotlib.colors as mcolors
from matplotlib.patches import Patch
import traceback  # Add this at the top of the file

class fetchHeatmapGraph:
    def __init__(self):
        self.current_canvas = None
        
    def create_graph(self, parent_frame):
        # Clear existing content
        for widget in parent_frame.winfo_children():
            widget.destroy()
            
        try:
            # Connect to database
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor(dictionary=True)
            
            # Query for heatmap data
            query = """
                SELECT 
                    HOUR(CreatedAT) as hour,
                    DAYOFWEEK(CreatedAT) as day,
                    COUNT(*) as count
                FROM `Order`
                WHERE MONTH(CreatedAT) = MONTH(CURDATE())
                GROUP BY HOUR(CreatedAT), DAYOFWEEK(CreatedAT)
            """
            
            cursor.execute(query)
            results = cursor.fetchall()
            
            # Check if data exists
            if not results:
                no_data_label = ctk.CTkLabel(
                    parent_frame,
                    text="No customer data available",
                    font=("Inter", 14),
                    text_color="black"
                )
                no_data_label.pack(pady=80)
                return
            
            # Prepare data for heatmap with 2-hour intervals
            days = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
            
            # Define 2-hour time periods
            time_periods = ['8-10am', '10-12pm', '12-2pm', '2-4pm', '4-6pm', '6-8pm', '8-10pm']
            hour_ranges = [(8, 10), (10, 12), (12, 14), (14, 16), (16, 18), (18, 20), (20, 22)]
            
            # Initialize data array (time periods x days)
            data = [[0 for _ in range(7)] for _ in range(len(time_periods))]
            
            # Process results to combine hours into 2-hour periods
            for row in results:
                hour = row['hour']
                day = row['day'] - 1  # Convert from 1-7 to 0-6
                count = row['count']
                
                # Map hour to corresponding time period
                for i, (start_hour, end_hour) in enumerate(hour_ranges):
                    if start_hour <= hour < end_hour:
                        if 0 <= day < 7:
                            data[i][day] += count
                            break
            
            # Find max count for scaling
            max_count = 0
            for row in data:
                for cell in row:
                    if cell > max_count:
                        max_count = cell
            
            # Threshold levels for different styles
            thresholds = [0, max_count * 0.25, max_count * 0.5, max_count * 0.75]
            
            # Create a mask for zero values to not display them
            mask = np.zeros_like(data, dtype=bool)
            for i in range(len(data)):
                for j in range(len(data[i])):
                    if data[i][j] == 0:
                        mask[i][j] = True
            
            # Create figure with dark style
            plt.style.use('dark_background')
            fig, ax = plt.subplots(figsize=(8, 5))
            fig.patch.set_facecolor('#212121')  # Dark background
            ax.set_facecolor('#212121')  # Dark plot area
            
            # Create custom colormap for modern look
            colors = ["#1e3c59", "#2a5885", "#3498db", "#5dade2"]  # Dark to light blue
            n_bins = 4  # Number of color levels
            cmap = mcolors.LinearSegmentedColormap.from_list("custom_blues", colors, N=n_bins)
            
            # Plot heatmap
            heatmap = sns.heatmap(
                data,
                xticklabels=days,
                yticklabels=time_periods,
                cmap=cmap,
                annot=True,
                annot_kws={"color": "white", "fontweight": "bold", "size": 9},
                fmt="d",
                cbar=False,
                mask=mask,  # Mask zeros
                ax=ax
            )
            
            # Create legend
            legend_elements = [
                Patch(facecolor=colors[0], label='< 50 customers'),
                Patch(facecolor=colors[1], label='50+ customers'),
                Patch(facecolor=colors[2], label='100+ customers'),
                Patch(facecolor=colors[3], label='200+ customers')
            ]
            
            ax.legend(
                handles=legend_elements,
                loc='upper right',
                frameon=False,
                fontsize=8
            )
            
            # Customize appearance
            ax.set_title('Customers by time', color='white', fontsize=14, fontweight='bold', loc='left', pad=15)
            ax.set_xlabel('', color='white')  # Hide x-label
            ax.set_ylabel('', color='white')  # Hide y-label
            
            # Style the ticks
            ax.tick_params(axis='x', colors='white', rotation=0)
            ax.tick_params(axis='y', colors='white')
            
            # Remove spines
            for spine in ax.spines.values():
                spine.set_visible(False)
            
            # Add daily filter dropdown (visual element only)
            dropdown_ax = fig.add_axes([0.85, 0.85, 0.12, 0.05])
            dropdown_ax.set_facecolor('#333333')
            dropdown_ax.text(0.5, 0.5, 'Daily ▼', 
                             horizontalalignment='center',
                             verticalalignment='center',
                             color='white',
                             fontsize=9,
                             fontweight='bold')
            dropdown_ax.set_xticks([])
            dropdown_ax.set_yticks([])
            for spine in dropdown_ax.spines.values():
                spine.set_visible(True)
                spine.set_color('#555555')
                
            plt.tight_layout()
            
            # Create canvas and add to frame
            canvas = FigureCanvasTkAgg(fig, parent_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True, padx=15, pady=10)
            
            # Store current canvas
            self.current_canvas = canvas
            
            conn.close()
            
        except Exception as e:
            print(f"Error creating heatmap: {e}")
            error_label = ctk.CTkLabel(
                parent_frame,
                text=f"Error creating heatmap: {e}",
                font=("Inter", 12),
                text_color="red"
            )
            error_label.pack(pady=20)
            import traceback
            traceback.print_exc()
    
    # Add this method for backward compatibility
    def create_daily_heatmap(self, parent_frame):
        return self.create_graph(parent_frame)

class FetchSalesGraph:
    """A sales graph for revenue by category"""
    
    def __init__(self):
        self.current_canvas = None
        
    def create_graph(self, parent_frame, month_filter="All Time"):
        """Create a bar chart showing revenue by category"""
        # Clear existing content
        for widget in parent_frame.winfo_children():
            widget.destroy()
            
        try:
            # Connect to database
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor(dictionary=True)
            
            # Define months list
            months = ["January", "February", "March", "April", "May", "June", 
                     "July", "August", "September", "October", "November", "December"]
            
            # Fetch orders based on month filter
            query = """
                SELECT OrderID, Item_list 
                FROM `Order`
                WHERE Status != 'cancelled'
            """
            
            # Add month filter if needed
            if month_filter != "All Time" and month_filter in months:
                month_num = months.index(month_filter) + 1
                query += " AND MONTH(CreatedAT) = %s AND YEAR(CreatedAT) = YEAR(CURDATE())"
                cursor.execute(query, (month_num,))
            else:
                cursor.execute(query)
                
            orders = cursor.fetchall()
            
            if not orders:
                no_data_label = ctk.CTkLabel(
                    parent_frame,
                    text="No order data available",
                    font=("Inter", 14),
                    text_color="black"
                )
                no_data_label.pack(pady=80)
                return
            
            # Process orders for category revenue
            category_revenue = {}
            
            for order in orders:
                try:
                    # Parse Item_list JSON
                    items = json.loads(order['Item_list'])
                    
                    # Make sure items is a list
                    if not isinstance(items, list):
                        items = [items]
                    
                    # Process each item
                    for item in items:
                        if isinstance(item, dict):
                            # Try to get category
                            category = None
                            for field in ['category', 'Category']:
                                if field in item:
                                    category = item[field]
                                    break
                            
                            # If no category in the item, try to get it from MenuID
                            if not category and ('MenuID' in item or 'menuId' in item or 'id' in item):
                                menu_id = item.get('MenuID') or item.get('menuId') or item.get('id')
                                if menu_id:
                                    cat_query = "SELECT Category FROM Menu WHERE MenuID = %s"
                                    cursor.execute(cat_query, (menu_id,))
                                    cat_result = cursor.fetchone()
                                    if cat_result:
                                        category = cat_result['Category']
                            
                            if category:
                                # Get price and quantity
                                price = 0
                                for price_field in ['price', 'Price']:
                                    if price_field in item:
                                        try:
                                            price = float(item[price_field])
                                            break
                                        except:
                                            pass
                                
                                quantity = 1
                                for qty_field in ['quantity', 'Quantity']:
                                    if qty_field in item:
                                        try:
                                            quantity = int(item[qty_field])
                                            break
                                        except:
                                            pass
                                
                                # Add to category revenue
                                if category in category_revenue:
                                    category_revenue[category] += price * quantity
                                else:
                                    category_revenue[category] = price * quantity
                except Exception as e:
                    print(f"Error processing order: {e}")
                    continue
            
            # If no categories found, show message
            if not category_revenue:
                no_data_label = ctk.CTkLabel(
                    parent_frame,
                    text="No category data found",
                    font=("Inter", 14),
                    text_color="black"
                )
                no_data_label.pack(pady=80)
                return
            
            # Sort categories by revenue
            sorted_categories = sorted(
                category_revenue.items(),
                key=lambda x: x[1],
                reverse=True
            )
            
            categories = [item[0] for item in sorted_categories]
            values = [item[1] for item in sorted_categories]
            
            # Create figure and axis
            plt.style.use('dark_background')
            fig, ax = plt.subplots(figsize=(8, 4))
            fig.patch.set_facecolor('#212121')
            ax.set_facecolor('#212121')
            
            # Create bar chart with gradient colors
            colors = ['#3498db', '#2980b9', '#1abc9c', '#16a085', '#f1c40f', '#f39c12', '#e74c3c', '#c0392b']
            bars = ax.bar(categories, values, color=colors[:len(categories)])
            
            # Add value labels on top of each bar
            for bar in bars:
                height = bar.get_height()
                ax.text(
                    bar.get_x() + bar.get_width()/2.,
                    height + 1,
                    f"${height:.2f}",
                    ha='center', 
                    va='bottom',
                    color='white',
                    fontsize=9,
                    fontweight='bold'
                )
            
            # Set y-axis with $100 intervals
            max_value = max(values) if values else 0
            y_ticks = [i * 100 for i in range(int(max_value / 100) + 2)]
            ax.set_yticks(y_ticks)
            ax.set_yticklabels([f"${y}" for y in y_ticks])
            
            # Set labels and title
            ax.set_xlabel('Categories', color='white', fontsize=10, fontweight='bold')
            ax.set_ylabel('Revenue ($)', color='white', fontsize=10, fontweight='bold')
            
            title = f"Revenue by Category" if month_filter == "All Time" else f"Revenue by Category - {month_filter}"
            ax.set_title(title, color='white', fontsize=14, fontweight='bold', pad=15)
            
            # Style ticks - use separate calls for rotation
            ax.tick_params(axis='x', colors='white')
            plt.xticks(rotation=45)
            ax.tick_params(axis='y', colors='white')
            
            # Remove spines
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.spines['bottom'].set_color('#555555')
            ax.spines['left'].set_color('#555555')
            
            # Add grid for y-axis
            ax.grid(axis='y', linestyle='--', alpha=0.2, color='gray')
            
            # Add filter dropdown visual
            dropdown_ax = fig.add_axes([0.85, 0.85, 0.12, 0.05])
            dropdown_ax.set_facecolor('#333333')
            dropdown_ax.text(0.5, 0.5, f"{month_filter} ▼", 
                            horizontalalignment='center',
                            verticalalignment='center',
                            color='white',
                            fontsize=9,
                            fontweight='bold')
            dropdown_ax.set_xticks([])
            dropdown_ax.set_yticks([])
            for spine in dropdown_ax.spines.values():
                spine.set_visible(True)
                spine.set_color('#555555')
            
            plt.tight_layout(rect=[0, 0, 1, 0.95])
            
            # Create canvas
            canvas = FigureCanvasTkAgg(fig, parent_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True, padx=15, pady=10)
            
            # Store canvas
            self.current_canvas = canvas
            
            conn.close()
            
        except Exception as e:
            print(f"Error creating sales graph: {e}")
            import traceback
            traceback.print_exc()
            error_label = ctk.CTkLabel(
                parent_frame,
                text=f"Error creating sales graph: {e}",
                font=("Inter", 12),
                text_color="red"
            )
            error_label.pack(pady=20)
    
    # For backward compatibility
    def create_monthly_sales_graph(self, parent_frame):
        return self.create_graph(parent_frame)