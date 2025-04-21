import customtkinter as ctk
from tkinter import messagebox
from PIL import Image, ImageTk
import mysql.connector
import subprocess  # ✅ To reopen AdminHomePage
from dbconnection import DB_CONFIG
import matplotlib.pyplot as plt

class ViewReportsPage(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("📊 Sales Reports")
        self.geometry("500x650")  # ✅ Increased height for chart
        self.resizable(False, False)
        self.configure(fg_color="white")

        # ✅ Set Background Image
        self.set_background("loginbackground.png")

        # ✅ Create UI Components
        self.create_ui()

    def set_background(self, image_path):
        """Load and set a background image."""
        try:
            image = Image.open(image_path).resize((500, 650), Image.LANCZOS)
            self.bg_image = ImageTk.PhotoImage(image)

            bg_label = ctk.CTkLabel(self, image=self.bg_image, text="")
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        except Exception as e:
            print(f"⚠️ Error loading background image: {e}")

    def create_ui(self):
        """Create UI components for viewing reports."""
        title_label = ctk.CTkLabel(self, text="📊 Sales Reports", font=("Poppins", 18, "bold"), text_color="black")
        title_label.pack(pady=10)

        self.report_frame = ctk.CTkFrame(self, fg_color="white", width=450, height=250)
        self.report_frame.pack(pady=10)

        self.load_reports()

        # ✅ Graph Frame for Price
        self.chart_frame = ctk.CTkFrame(self, fg_color="white", width=450, height=250)
        self.chart_frame.pack(pady=10)
        self.load_price_chart()

        # ✅ Back Button
        back_button = ctk.CTkButton(self, text="⬅ Back to Dashboard", fg_color="#F1D94B", text_color="black",
                                    command=self.redirect_to_admin_home)
        back_button.pack(pady=10)

    def load_reports(self):
        """Fetch and display sales reports."""
        for widget in self.report_frame.winfo_children():
            widget.destroy()

        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)

            # ✅ Get total revenue (ALL orders)
            cursor.execute("SELECT SUM(total_price) AS revenue FROM orders")
            revenue = cursor.fetchone()["revenue"] or 0

            # ✅ Get total orders
            cursor.execute("SELECT COUNT(*) AS order_count FROM orders")
            order_count = cursor.fetchone()["order_count"] or 0

            # ✅ Get most ordered items (last 5 orders)
            cursor.execute("SELECT items_list FROM orders ORDER BY id DESC LIMIT 5")
            recent_orders = cursor.fetchall()

            conn.close()

            # ✅ Display reports
            ctk.CTkLabel(self.report_frame, text=f"💰 Total Revenue: ${revenue:.2f}",
                        font=("Arial", 14, "bold"), text_color="#4CAF50").pack(anchor="w", padx=10, pady=5)

            ctk.CTkLabel(self.report_frame, text=f"📦 Total Orders: {order_count}",
                        font=("Arial", 14, "bold"), text_color="black").pack(anchor="w", padx=10, pady=5)

            ctk.CTkLabel(self.report_frame, text="📋 Recent Orders:", font=("Arial", 14, "bold"),
                        text_color="black").pack(anchor="w", padx=10, pady=5)

            for order in recent_orders:
                ctk.CTkLabel(self.report_frame, text=f"🛒 {order['items_list']}",
                            font=("Arial", 12), text_color="gray").pack(anchor="w", padx=20)

        except mysql.connector.Error as err:
            ctk.CTkLabel(self.report_frame, text=f"⚠️ Database Error: {err}",
                        font=("Arial", 12), text_color="red").pack(pady=20)

    def load_price_chart(self):
        """Fetch last 7 order prices and display a bar chart."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)

            # ✅ Get last 7 orders with total price
            cursor.execute("""
                SELECT id, total_price FROM orders 
                ORDER BY created_at DESC LIMIT 7
            """)
            data = cursor.fetchall()
            conn.close()

            if not data:
                ctk.CTkLabel(self.chart_frame, text="📉 No price data available.", 
                            font=("Arial", 12), text_color="gray").pack(pady=20)
                return

            # ✅ Prepare data for plotting
            order_ids = [str(row['id']) for row in data][::-1]  # Only show Order ID
            prices = [row["total_price"] for row in data][::-1]

            # ✅ Create Matplotlib Figure
            fig, ax = plt.subplots(figsize=(4.5, 2))  # ✅ Set figure size
            ax.bar(order_ids, prices, color="#4CAF50", alpha=0.85)  # ✅ Change color to greenish

            # ✅ Format plot
            ax.set_title("💰 Order Price Trend (Last 7 Orders)", fontsize=12, fontweight="bold")
            ax.set_xlabel("Order ID", fontsize=10, fontweight="bold")
            ax.set_ylabel("Total Price ($)", fontsize=10, fontweight="bold")
            ax.set_xticks(range(len(order_ids)))  # ✅ Fix x-axis spacing
            ax.set_xticklabels(order_ids, rotation=45, ha="right", fontsize=8)  # ✅ Rotate labels for better view

            ax.spines["top"].set_visible(False)  # ✅ Hide top border
            ax.spines["right"].set_visible(False)  # ✅ Hide right border
            ax.spines["left"].set_linewidth(1)  # ✅ Keep left border
            ax.spines["bottom"].set_linewidth(1)  # ✅ Keep bottom border
            ax.yaxis.set_tick_params(size=0)  # ✅ Remove y-axis ticks
            ax.xaxis.set_tick_params(size=0)  # ✅ Remove x-axis ticks
            ax.set_facecolor("white")  # ✅ Set background to white

            # ✅ Embed Matplotlib Figure into Tkinter
            canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
            canvas.draw()
            canvas.get_tk_widget().pack()

        except mysql.connector.Error as err:
            ctk.CTkLabel(self.chart_frame, text=f"⚠️ Database Error: {err}",
                        font=("Arial", 12), text_color="red").pack(pady=20)

    def redirect_to_admin_home(self):
        """Close this window and return to Admin Dashboard."""
        self.destroy()  # ✅ Close View Reports Page
        subprocess.Popen(["python", "admin_dashboard.py"])  # ✅ Reopen Admin Dashboard

# ✅ Open View Reports Page
if __name__ == "__main__":
    app = ViewReportsPage()
    app.mainloop()
