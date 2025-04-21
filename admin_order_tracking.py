import customtkinter as ctk
import mysql.connector
from tkinter import messagebox
from dbconnection import DB_CONFIG
import subprocess  # ✅ To reopen AdminHomePage

class AdminOrderTrackingPage(ctk.CTk):
    def __init__(self, parent, app):
        super().__init__(parent, app, "Order Tracking")
        self.create_tracking_view()

    def create_tracking_view(self):
        # Create container
        tracking_card = self.create_content_card("Active Orders", height=500)
        tracking_card.pack(fill="both", expand=True, padx=20, pady=20)

        # Orders list
        self.orders_frame = ctk.CTkScrollableFrame(
            tracking_card,
            fg_color="transparent",
            height=400
        )
        self.orders_frame.pack(fill="both", expand=True, padx=20, pady=10)

        self.load_orders()

    def load_orders(self):
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor(dictionary=True)

            # Use correct table name with backticks
            cursor.execute("""
                SELECT OrderID, UserName, Item_list, Total_price, Status, CreatedAT
                FROM `Order`
                WHERE Status != 'delivered'
                ORDER BY CreatedAT DESC
            """)

            orders = cursor.fetchall()
            
            if not orders:
                self.show_no_orders()
            else:
                for order in orders:
                    self.create_order_card(order)

        except mysql.connector.Error as err:
            print(f"Database Error: {err}")
            self.show_error_message("Error loading orders")
        finally:
            if 'conn' in locals():
                conn.close()

    def create_order_card(self, order):
        """Create an order summary card with status update options."""
        frame = ctk.CTkFrame(self.orders_frame, fg_color="white", width=430, height=150, border_width=2, border_color="#F1D94B")
        frame.pack(pady=5, padx=5, fill="x")

        ctk.CTkLabel(frame, text=f"�� Order ID: {order['OrderID']}", font=("Arial", 12, "bold"), text_color="black").pack(anchor="w", padx=10)
        ctk.CTkLabel(frame, text=f"�� Customer: {order['UserName']}", font=("Arial", 12), text_color="black").pack(anchor="w", padx=10)
        ctk.CTkLabel(frame, text=f"📝 Items: {order['Item_list']}", font=("Arial", 12), text_color="black", wraplength=400).pack(anchor="w", padx=10)
        ctk.CTkLabel(frame, text=f"💲 Total: ${order['Total_price']:.2f}", font=("Arial", 12), text_color="#E53935").pack(anchor="w", padx=10)

        # ✅ Dropdown for status update
        status_var = ctk.StringVar(value=order['Status'])
        status_dropdown = ctk.CTkComboBox(frame, values=["pending", "preparing", "ready for pickup", "delivered"], variable=status_var)
        status_dropdown.pack(pady=5)

        update_button = ctk.CTkButton(frame, text="✔ Update Status", fg_color="#4CAF50", text_color="white",
                                      command=lambda: self.update_order_status(order["OrderID"], status_var.get()))
        update_button.pack(pady=5)

    def update_order_status(self, order_id, new_status):
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor()

            cursor.execute("""
                UPDATE `Order`
                SET Status = %s
                WHERE OrderID = %s
            """, (new_status, order_id))

            conn.commit()
            self.refresh_orders()

        except mysql.connector.Error as err:
            print(f"Database Error: {err}")
            self.show_error_message("Error updating order status")
        finally:
            if 'conn' in locals():
                conn.close()

    def redirect_to_admin_home(self):
        """Close this window and return to Admin Dashboard."""
        self.destroy()
        subprocess.Popen(["python", "admin_dashboard.py"])

# ✅ Open Order Tracking Page
if __name__ == "__main__":
    app = AdminOrderTrackingPage()
    app.mainloop()
