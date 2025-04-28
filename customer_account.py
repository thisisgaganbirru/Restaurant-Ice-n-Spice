import customtkinter as ctk
from utils import resize_image
from customer_nav import NavigationHeader
import mysql.connector
from dbconnection import DB_CONFIG
from customer_orderhistory import OrderHistory
import json
from decimal import Decimal

class CustomerAccountPage(ctk.CTkFrame):
    def __init__(self, parent, app=None, user=None):
        super().__init__(parent)
        self.app = app
        self.user = user
        self.configure(width=600, height=700)

        self.edit_icon = resize_image((20, 20), "images/edit_entry.png")
        self.check_icon = resize_image((20, 20), "images/checkmark.png")

        self.create_header()
        self.create_account_body()

    def create_header(self):
        NavigationHeader(self, app=self.app, user=self.user).pack(side="top", fill="x")

    def create_account_body(self):
        body_frame = ctk.CTkFrame(self, fg_color="transparent")
        body_frame.pack(fill="both", expand=True)
        body_frame.pack_propagate(False)

        try:
            self.bg_image = resize_image((800, 800), "images/backg.jpg")
            bg_label = ctk.CTkLabel(body_frame, image=self.bg_image, text="")
            bg_label.pack(fill="both", expand=True)
        except:
            pass

        self.content_frame = ctk.CTkFrame(body_frame, fg_color="#F9F0E5", width=500, height=500, corner_radius=5)
        self.content_frame.place(relx=0.5, rely=0.05, anchor="n")
        self.content_frame.pack_propagate(False)

        self.create_tabs()

        self.views = {
            "Profile": self.create_profile_view(),
            "Orders": self.create_orders_view(),
            "Requests": self.create_requests_view()
        }

        # Show default view
        self.show_view("Profile")

        self.logout_button = ctk.CTkButton(
            body_frame,
            text="Logout ⮕",
            text_color="black",
            fg_color="#F1D94B",
            hover_color="#f7e565",
            font=("Poppins", 14, "bold"),
            width=140,
            height=40,
            anchor="center",
            command=self.logout
        )
        self.logout_button.place(relx=0.5, rely=0.92, anchor="center")

    def create_tabs(self):
        # Header frame for segments
        self.header_frame = ctk.CTkFrame(self.content_frame, height=45, fg_color="#F5F5F5", corner_radius=0)
        self.header_frame.pack(fill="x")
        self.header_frame.pack_propagate(False)

        # Create segmented button that fills the width
        self.tab_segments = ctk.CTkSegmentedButton(
            self.header_frame,
            values=["Profile", "Orders", "Requests"],
            command=self.show_view,
            selected_color="#F1D94B",
            selected_hover_color="#f7e565",
            unselected_color="#F5F5F5",
            unselected_hover_color="#E5E5E5",
            fg_color="#F5F5F5",
            text_color="black",
            height=45,
            font=("Arial", 14),
            dynamic_resizing=False,
            border_width=1
        )
        self.tab_segments.pack(fill="x", expand=True)
        self.tab_segments.set("Profile")  # Set default selection

        # Content frame for views
        self.content_frame_inner = ctk.CTkFrame(self.content_frame, fg_color="#F9F0E5", corner_radius=0)
        self.content_frame_inner.pack(fill="both", expand=True)

    def show_view(self, view_name):
        # Hide all views
        for view in self.views.values():
            view.pack_forget()

        # Show selected view
        self.views[view_name].pack(fill="both", expand=True)

        # Update segment selection
        self.tab_segments.set(view_name)

    def create_profile_view(self):
        # Main outer frame
        frame = ctk.CTkFrame(self.content_frame_inner, fg_color="transparent")
        frame.pack(fill="both", expand=True)

        # Welcome section at top
        welcome_frame = ctk.CTkFrame(frame, fg_color="transparent")
        welcome_frame.pack(fill="x", padx=20, pady=(5, 5))

        name = self.app.logged_in_user.get("first_name", "User")
        ctk.CTkLabel(
            welcome_frame, 
            text=f"Welcome {name}", 
            font=("Arial", 24, "bold"), 
            text_color="#660033"
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            welcome_frame, 
            text="Manage your profile information", 
            font=("Arial", 14), 
            text_color="gray"
        ).pack(anchor="w", pady=(5, 0))

        # Message label for success/error
        self.message_label = ctk.CTkLabel(
            welcome_frame, 
            text="", 
            font=("Arial", 12, "bold"), 
            text_color="green"
        )
        self.message_label.pack(padx=20, pady=(5, 0), anchor="w")

        # Main container for profile section
        mainprofile_frame = ctk.CTkFrame(frame, fg_color="transparent")
        mainprofile_frame.pack(fill="both", expand=True, padx=20, pady=(10, 0))
        mainprofile_frame.pack_propagate(False)

        # Left frame (60%) - Form fields
        form_frame = ctk.CTkFrame(mainprofile_frame, fg_color="transparent", width=300)
        form_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))
        form_frame.pack_propagate(False)

        # Right frame (40%) - Buttons
        button_frame = ctk.CTkFrame(mainprofile_frame, fg_color="transparent", width=200)
        button_frame.pack(side="right", fill="y", padx=(10, 0))
        button_frame.pack_propagate(False)

        # Create form fields in left frame
        self.create_form_fields(form_frame)

        # Create buttons in right frame
        self.create_button_panel(button_frame)

        # Note text at bottom
        note_text = "Mobile, Address and Password fields can be changed. For other changes, please contact management"
        note_label = ctk.CTkLabel(
            frame,
            text=note_text,
            font=("Poppins", 11),
            text_color="gray",
            wraplength=400
        )
        note_label.pack(pady=(15, 10), padx=20, anchor="center")

        return frame

    def create_form_fields(self, parent):
        # Fetch user data
        user_id = self.app.logged_in_user.get("userID", 0)
        user_data = self.fetch_user_data(user_id)

        if user_data:
            name, username, mobile, email, address, password = user_data
        else:
            name, username, mobile, email, address, password = ("N/A",)*6

        # Create entries dictionary to track changes
        self.entries = {}
        
        # Create fields
        fields = [
            ("USERNAME", username, False),
            ("NAME", name, False),
            ("EMAIL", email, False),
            ("MOBILE", mobile, True),
            ("ADDRESS", address, True),
            ("PASSWORD", "******", True)
        ]

        # Create form fields
        for field_name, value, is_editable in fields:
            self.create_entry_row(parent, field_name, value)

    def create_entry_row(self, parent, label, value):
        # Main row container
        row = ctk.CTkFrame(parent, fg_color="transparent", height=45)
        row.pack(pady=(0, 5), fill="x")
        row.pack_propagate(False)

        # Label (left side)
        label_frame = ctk.CTkFrame(row, fg_color="transparent", width=100)
        label_frame.pack(side="left", padx=(0, 5))
        label_frame.pack_propagate(False)
        
        ctk.CTkLabel(
            label_frame,
            text=label,
            font=("Arial", 12, "bold"),
            text_color="black",
            anchor="w"
        ).pack(side="left")

        # Entry field
        entry = ctk.CTkEntry(
            row,
            width=200,
            height=32,
            font=("Poppins", 12),
            corner_radius=3,
            border_width=1,
            border_color="#E0E0E0"
        )
        entry.insert(0, value)
        entry.configure(state="disabled")
        entry.pack(side="left", padx=(0, 5))

        self.entries[label] = entry

    def create_button_panel(self, parent):
        # Common button style
        button_style = {
            "font": ("Arial", 12),
            "fg_color": "#F1D94B",
            "text_color": "black",
            "hover_color": "#f7e565",
            "height": 30,
            "width": 150,
            "corner_radius": 3,
            "border_width": 1,
            "border_color": "black"
        }

        # Main buttons frame (for Edit and Update Password)
        self.main_buttons_frame = ctk.CTkFrame(parent, fg_color="transparent")
        self.main_buttons_frame.pack(fill="x", pady=(0, 10))

        # Edit button
        self.edit_button = ctk.CTkButton(
            self.main_buttons_frame,
            text="Edit Profile",
            command=self.start_editing,
            **button_style
        )
        self.edit_button.pack(pady=(0, 10))

        # Update Password button
        self.update_password_button = ctk.CTkButton(
            self.main_buttons_frame,
            text="Update Password",
            command=self.start_password_update,
            **button_style
        )
        self.update_password_button.pack(pady=(0, 10))

        # Password update frame (initially hidden)
        self.password_update_frame = ctk.CTkFrame(parent, fg_color="transparent")
        self.password_update_frame.pack(fill="x", pady=(0, 10))
        self.password_update_frame.pack_forget()

        # Password update fields
        ctk.CTkLabel(
            self.password_update_frame,
            text="Enter New Password",
            font=("Arial", 11),
            anchor="w"
        ).pack(fill="x", pady=(0, 2))

        self.new_password_entry = ctk.CTkEntry(
            self.password_update_frame,
            width=160,
            height=32,
            font=("Poppins", 12),
            show="*",
            corner_radius=3
        )
        self.new_password_entry.pack(pady=(0, 5))

        ctk.CTkLabel(
            self.password_update_frame,
            text="Confirm New Password",
            font=("Arial", 11),
            anchor="w"
        ).pack(fill="x", pady=(0, 2))

        self.confirm_password_entry = ctk.CTkEntry(
            self.password_update_frame,
            width=160,
            height=32,
            font=("Poppins", 12),
            show="*",
            corner_radius=3
        )
        self.confirm_password_entry.pack(pady=(0, 10))

        # Action buttons frame (for Save and Cancel)
        self.action_buttons_frame = ctk.CTkFrame(parent, fg_color="transparent")
        self.action_buttons_frame.pack(fill="x", pady=(0, 10))
        self.action_buttons_frame.pack_forget()

        # Cancel Changes button
        self.cancel_button = ctk.CTkButton(
            self.action_buttons_frame,
            text="Cancel Changes",
            fg_color="#FF6B6B",
            text_color="white",
            hover_color="#FF5252",
            command=self.cancel_changes,
            **{k: v for k, v in button_style.items() if k not in ["fg_color", "text_color", "hover_color"]}
        )
        self.cancel_button.pack(pady=(0, 10))

        # Save Changes button
        self.save_button = ctk.CTkButton(
            self.action_buttons_frame,
            text="Save Changes",
            command=self.save_changes,
            **button_style
        )
        self.save_button.pack(pady=(0, 10))

    def start_editing(self):
        # Enable editable fields
        for field in ["MOBILE", "ADDRESS"]:
            if field in self.entries:
                self.entries[field].configure(state="normal")
        
        # Hide main buttons, show action buttons
        self.main_buttons_frame.pack_forget()
        self.action_buttons_frame.pack(fill="x", pady=(0, 10))

    def start_password_update(self):
        # Show password update frame and action buttons
        self.main_buttons_frame.pack_forget()
        self.password_update_frame.pack(fill="x", pady=(0, 10))
        self.action_buttons_frame.pack(fill="x", pady=(0, 10))
        
        # Clear password fields
        self.new_password_entry.delete(0, "end")
        self.confirm_password_entry.delete(0, "end")

    def cancel_changes(self):
        # Reset all fields to original values
        user_id = self.app.logged_in_user.get("userID", 0)
        user_data = self.fetch_user_data(user_id)
        
        if user_data:
            name, username, mobile, email, address, password = user_data
            
            if "MOBILE" in self.entries:
                self.entries["MOBILE"].delete(0, "end")
                self.entries["MOBILE"].insert(0, mobile)
                self.entries["MOBILE"].configure(state="disabled")
            
            if "ADDRESS" in self.entries:
                self.entries["ADDRESS"].delete(0, "end")
                self.entries["ADDRESS"].insert(0, address)
                self.entries["ADDRESS"].configure(state="disabled")

        # Hide password update frame and action buttons
        self.password_update_frame.pack_forget()
        self.action_buttons_frame.pack_forget()
        
        # Show main buttons
        self.main_buttons_frame.pack(fill="x", pady=(0, 10))

    def save_changes(self):
        try:
            user_id = self.app.logged_in_user.get("userID", 0)
            updates = {}
            
            # Check if we're updating password
            if self.password_update_frame.winfo_manager():
                new_pass = self.new_password_entry.get()
                confirm_pass = self.confirm_password_entry.get()
                
                if new_pass != confirm_pass:
                    self.show_message("Passwords do not match!", "red")
                    return
                if new_pass.strip() == "":
                    self.show_message("Password cannot be empty!", "red")
                    return
                updates["password"] = new_pass
            else:
                # Check for mobile and address updates
                if self.entries["MOBILE"].cget("state") == "normal":
                    updates["phone_number"] = self.entries["MOBILE"].get()
                if self.entries["ADDRESS"].cget("state") == "normal":
                    updates["address"] = self.entries["ADDRESS"].get()

            if updates:
                if self.update_user_data(user_id, updates):
                    self.show_message("Profile updated successfully!", "green")
                    # Reset UI state
                    self.cancel_changes()
                else:
                    self.show_message("Failed to update profile!", "red")
            else:
                self.show_message("No changes to save!", "orange")

        except Exception as e:
            self.show_message(f"Error: {str(e)}", "red")

    def show_message(self, message, color):
        self.message_label.configure(text=message, text_color=color)
        # Clear message after 3 seconds
        self.after(3000, lambda: self.message_label.configure(text=""))

    def update_user_data(self, user_id, updates):
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor()

            # Build the update query dynamically
            set_clause = ", ".join([f"{field} = %s" for field in updates.keys()])
            query = f"UPDATE users SET {set_clause} WHERE userID = %s"
            
            # Create values tuple for the query
            values = tuple(updates.values()) + (user_id,)
            
            cursor.execute(query, values)
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print("Update Error:", e)
            return False

    def fetch_user_data(self, user_id):
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor()
            query = """
                SELECT CONCAT(first_name, ' ', last_name) as name, 
                       username, phone_number, email, address, password 
                FROM users 
                WHERE userID = %s
            """
            cursor.execute(query, (user_id,))
            user_data = cursor.fetchone()
            conn.close()
            return user_data if user_data else ("N/A",)*6
        except Exception as e:
            print("Database Error:", e)
            return ("N/A",)*6

    def logout(self):
        self.app.show_login_page()

    def show_order_history(self):
        # Clear current content
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # Show order history
        OrderHistory(self.content_frame, self.app, self.user).pack(fill="both", expand=True)

    def create_requests_view(self):
        frame = ctk.CTkFrame(self.content_frame_inner, fg_color="transparent")

        welcome_frame = ctk.CTkFrame(frame, fg_color="transparent")
        welcome_frame.pack(fill="x", padx=20, pady=(5, 5))

        name = self.app.logged_in_user.get("first_name", "User")
        ctk.CTkLabel(welcome_frame, text=f"Welcome {name}", font=("Arial", 24, "bold"), text_color="#660033").pack(anchor="w")
        ctk.CTkLabel(welcome_frame, text="View your contact requests", font=("Arial", 14), text_color="gray").pack(anchor="w", pady=(5, 0))

        # Requests container with automatic scrolling
        requests_container = ctk.CTkFrame(frame, fg_color="transparent")
        requests_container.pack(fill="both", expand=True, padx=20, pady=(20,0))

        # Requests frame that will scroll if content exceeds height
        self.requests_frame = ctk.CTkScrollableFrame(
            requests_container,
            fg_color="transparent",
            height=350,  # Fixed height
            width=460    # Fixed width
        )
        self.requests_frame.pack(fill="both", expand=True)

        requests = self.fetch_requests(self.app.logged_in_user["userID"])
        if requests:
            for request in requests:
                self.create_requestcard(self.requests_frame, request)
        else:
            ctk.CTkLabel(
                self.requests_frame,
                text="No requests yet",
                font=("Poppins", 16, "italic"),
                text_color="gray"
            ).pack(pady=20)

        return frame

    def create_requestcard(self, parent, request):
        # Main card frame
        card = ctk.CTkFrame(
            parent,
            fg_color="white",
            corner_radius=10,
            border_width=1,
            border_color="#F1D94B",
            height=120  # Fixed height for the card
        )
        card.pack(fill="x", pady=5)
        card.pack_propagate(False)

        # Header frame
        header_frame = ctk.CTkFrame(card, fg_color="transparent", height=30)
        header_frame.pack(fill="x", padx=15, pady=(10,5))
        header_frame.pack_propagate(False)

        # Request Date
        date_str = f"Sent on {request['created_at'].strftime('%a, %b %d, %Y, %I:%M %p')}"
        ctk.CTkLabel(
            header_frame,
            text=date_str,
            font=("Poppins", 12),
            text_color="gray"
        ).pack(side="right")

        # Status indicator
        status_color = "#4CAF50" if request['status'] == 'read' else "#FF9800"
        status_text = "Answered" if request['status'] == 'read' else "Pending"
        
        status_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        status_frame.pack(side="left")
        
        status_dot = ctk.CTkLabel(
            status_frame,
            text="●",
            font=("Poppins", 14),
            text_color=status_color
        )
        status_dot.pack(side="left")
        
        ctk.CTkLabel(
            status_frame,
            text=status_text,
            font=("Poppins", 12),
            text_color=status_color
        ).pack(side="left", padx=5)

        # Separator line
        separator = ctk.CTkFrame(card, height=1, fg_color="#E5E5E5")
        separator.pack(fill="x", padx=15, pady=5)

        # Message content
        message_frame = ctk.CTkFrame(card, fg_color="transparent")
        message_frame.pack(fill="x", padx=15)

        ctk.CTkLabel(
            message_frame,
            text=request['message'][:100] + "..." if len(request['message']) > 100 else request['message'],
            font=("Poppins", 12),
            text_color="black",
            anchor="w",
            justify="left",
            wraplength=400
        ).pack(fill="x")

    def fetch_requests(self, user_id):
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor(dictionary=True)
            
            # Join with users table to get the requests for this user
            query = """
            SELECT cm.* 
            FROM contact_messages cm
            JOIN users u ON cm.email = u.email
            WHERE u.userID = %s
            ORDER BY cm.created_at DESC
            """
            cursor.execute(query, (user_id,))
            requests = cursor.fetchall()
            
            cursor.close()
            conn.close()
            
            return requests
        except Exception as e:
            print(f"Error fetching requests: {e}")
            return []

    def create_orders_view(self):
        frame = ctk.CTkFrame(self.content_frame_inner, fg_color="transparent")

        welcome_frame = ctk.CTkFrame(frame, fg_color="transparent")
        welcome_frame.pack(fill="x", padx=20, pady=(5, 5))

        name = self.app.logged_in_user.get("first_name", "User")
        ctk.CTkLabel(welcome_frame, text=f"Welcome {name}", font=("Arial", 24, "bold"), text_color="#660033").pack(anchor="w")
        ctk.CTkLabel(welcome_frame, text="View your order history", font=("Arial", 14), text_color="gray").pack(anchor="w", pady=(5, 0))

        # Orders container with automatic scrolling
        orders_container = ctk.CTkFrame(frame, fg_color="transparent")
        orders_container.pack(fill="both", expand=True, padx=20, pady=(20,0))

        # Orders frame that will scroll if content exceeds height
        self.orders_frame = ctk.CTkScrollableFrame(
            orders_container,
            fg_color="transparent",
            height=350,  # Fixed height
            width=460    # Fixed width
        )
        self.orders_frame.pack(fill="both", expand=True)

        orders = self.fetch_orders(self.app.logged_in_user["userID"])
        if orders:
            for order in orders:
                self.create_ordercard(self.orders_frame, order)
        else:
            ctk.CTkLabel(
                self.orders_frame,
                text="No orders yet",
                font=("Poppins", 16, "italic"),
                text_color="gray"
            ).pack(pady=20)

        return frame

    def create_ordercard(self, parent, order):
        # Main card frame
        card = ctk.CTkFrame(
            parent,
            fg_color="white",
            corner_radius=10,
            border_width=1,
            border_color="#F1D94B",
            height=150  # Fixed height for the card
        )
        card.pack(fill="x", pady=5)
        card.pack_propagate(False)

        # Header frame
        header_frame = ctk.CTkFrame(card, fg_color="transparent", height=50)
        header_frame.pack(fill="x", padx=15, pady=(10,0))
        header_frame.pack_propagate(False)

        # Order ID and Date
        formatted_id = f"Order Id: #{order['OrderID']:07d}"
        ctk.CTkLabel(
            header_frame,
            text=formatted_id,
            font=("Poppins", 14, "bold"),
            text_color="black"
        ).pack(side="left")
        
        # Reorder button
        reorder_btn = ctk.CTkButton(
            header_frame,
            text="Reorder",
            font=("Poppins", 12),
            fg_color="#F1D94B",
            text_color="black",
            width=100,
            height=30,
            command=lambda: self.reorder(order)
        )
        reorder_btn.pack(side="right")
        
        header_frame2 = ctk.CTkFrame(card, fg_color="transparent", height=10)
        header_frame2.pack(fill="x",padx=15)
        header_frame2.pack_propagate(False)

        date_str = f"Ordered on {order['CreatedAT'].strftime('%a, %b %d, %Y, %I:%M %p')}"
        ctk.CTkLabel(
            header_frame2,
            text=date_str,
            font=("Poppins", 12),
            text_color="gray"
        ).pack(side="left", pady=(0,1))

        # Separator line
        separator = ctk.CTkFrame(card, height=2, fg_color="#E5E5E5")
        separator.pack(fill="x", padx= 15,pady=5)

        # Items list
        items = json.loads(order['Item_list'])
        items_frame = ctk.CTkFrame(card, fg_color="transparent")
        items_frame.pack(fill="x",expand=True, padx=15, pady=(0,5))
        items_frame.pack_propagate(False)

        for item in items:
            item_text = f"{item['name']} x {item['quantity']}"
            ctk.CTkLabel(
                items_frame,
                text=item_text,
                font=("Poppins", 12),
                text_color="black",
                anchor="w",
                justify="left"
            ).pack(side="left", pady=(2,0))

        # # Total amount
        # total_frame = ctk.CTkFrame(card, fg_color="transparent")
        # total_frame.pack(fill="x", padx=15, pady=5)

        ctk.CTkLabel(
            items_frame,
            text=f"Total Paid: $ {float(order['Total_price']):.2f}",
            font=("Poppins", 12, "bold"),
            text_color="black"
        ).pack(side="right")

        

    def reorder(self, order):
        try:
            # Parse the stored items from Item_list
            items = json.loads(order['Item_list'])
            
            # Create a new cart with the items
            cart = {}
            for item in items:
                cart[item['id']] = {
                    'name': item['name'],
                    'price': Decimal(item['price']),
                    'quantity': item['quantity'],
                    'image_path': item.get('image_path', '')
                }
            
            # Redirect to order page with the recreated cart
            self.app.show_order_page(user=self.app.logged_in_user, cart=cart)

        except Exception as e:
            print(f"Error reordering items: {e}")

    def fetch_orders(self, user_id):
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM `Order` WHERE UserID = %s ORDER BY CreatedAT DESC", (user_id,))
        orders = cursor.fetchall()
        conn.close()
        return orders
