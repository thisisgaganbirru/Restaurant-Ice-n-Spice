import customtkinter as ctk
from dbconnection import DB_CONFIG
import mysql.connector
from datetime import datetime
from admin_nav import AdminNav
from tkinter import messagebox
import re

class AdminCustomersPage(ctk.CTkFrame):
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
        self.create_customers_body()
        
    def create_header(self):
        # Nav on left
        AdminNav(self.main_container, app=self.app).pack(side="left", fill="y")
        
    def create_customers_body(self):
        # Main body frame
        self.body_frame = ctk.CTkFrame(self.main_container, fg_color="#F1E8DD")
        self.body_frame.pack(side="right", fill="both", expand=True)
        
        # Header with title and search
        header_frame = ctk.CTkFrame(self.body_frame, fg_color="transparent", height=50)
        header_frame.pack(fill="x", padx=20, pady=10)
        
        # Title
        ctk.CTkLabel(
            header_frame,
            text="Customers",
            font=("Poppins", 24, "bold"),
            text_color="#2B2B2B"
        ).pack(side="left")
        
        # Search frame
        search_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        search_frame.pack(side="right")
        
        self.search_var = ctk.StringVar()
        search_entry = ctk.CTkEntry(
            search_frame,
            width=300,
            placeholder_text="Search...",
            textvariable=self.search_var
        )
        search_entry.pack(side="left", padx=5)
        
        ctk.CTkButton(
            search_frame,
            text="Search",
            font=("Poppins", 12),
            fg_color="#F1D94B",
            text_color="black",
            hover_color="#E5CE45",
            command=self.search_customers
        ).pack(side="left", padx=5)
        
        # Customers grid container
        self.customers_frame = ctk.CTkFrame(self.body_frame, fg_color="transparent")
        self.customers_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Load customers
        self.load_customers()
        
    def load_customers(self, search_term=None):
        # Clear existing customers
        for widget in self.customers_frame.winfo_children():
            widget.destroy()
            
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor(dictionary=True)
            
            query = """
                SELECT userID, first_name, last_name, username, email, phone_number, address, created_at
                FROM users
                WHERE role = 'customer'
            """
            
            if search_term:
                query += """ AND (first_name LIKE %s OR last_name LIKE %s OR username LIKE %s)"""
                search_pattern = f"%{search_term}%"
                cursor.execute(query, (search_pattern, search_pattern, search_pattern))
            else:
                cursor.execute(query)
                
            customers = cursor.fetchall()
            print(f"Found {len(customers)} customers")  # Debug print
            
            if not customers:
                # Show message when no customers found
                ctk.CTkLabel(
                    self.customers_frame,
                    text="No customers found",
                    font=("Poppins", 16),
                    text_color="gray"
                ).pack(pady=20)
                return
                
            # Configure grid layout for customer cards
            self.customers_frame.grid_columnconfigure((0,1,2), weight=1)
            row = 0
            col = 0
            
            for customer in customers:
                print(f"Creating card for customer: {customer['first_name']} {customer['last_name']}")  # Debug print
                card = self.create_customer_card(self.customers_frame, customer)
                card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
                
                col += 1
                if col > 2:  # After 3 cards, start new row
                    col = 0
                    row += 1
            
            conn.close()
            
        except mysql.connector.Error as err:
            print(f"Database Error: {err}")  # Debug print
            messagebox.showerror("Database Error", f"Failed to load customers: {err}")
            
    def create_customer_card(self, parent, customer):
        # Card frame with fixed size and shadow effect
        card = ctk.CTkFrame(parent, fg_color="white", border_color="#F1D94B", border_width=3, corner_radius=15)
        card.configure(width=300, height=180)  # Adjusted height for better spacing
        
        # Customer name
        name = f"{customer['first_name']} {customer['last_name']}"
        ctk.CTkLabel(
            card,
            text=name,
            font=("Poppins", 18, "bold"),
            text_color="#2B2B2B"
        ).pack(anchor="w", padx=20, pady=(20,5))
        
        # Username
        ctk.CTkLabel(
            card,
            text=f"@{customer['username']}",
            font=("Poppins", 13),
            text_color="gray"
        ).pack(anchor="w", padx=20, pady=2)
        
        # Member since
        created_date = datetime.strptime(str(customer['created_at']), '%Y-%m-%d %H:%M:%S')
        member_since = f"Member Since: {created_date.strftime('%b %Y')}"
        ctk.CTkLabel(
            card,
            text=member_since,
            font=("Poppins", 13),
            text_color="gray"
        ).pack(anchor="w", padx=20, pady=2)
        
        # Edit button with updated styling
        edit_button = ctk.CTkButton(
            card,
            text="Edit",
            font=("Poppins", 13),
            fg_color="#F1D94B",
            text_color="black",
            hover_color="#E5CE45",
            width=80,
            height=32,
            corner_radius=8,
            command=lambda: self.show_edit_dialog(customer)
        )
        edit_button.pack(anchor="w", padx=20, pady=(10,20))
        
        return card
        
    def show_edit_dialog(self, customer):
        dialog = ctk.CTkToplevel(self)
        dialog.title("Edit Customer")
        dialog.geometry("400x500")
        dialog.resizable(False, False)
        
        # Make dialog modal
        dialog.grab_set()
        
        # Center the dialog
        dialog.update_idletasks()
        screen_width = dialog.winfo_screenwidth()
        screen_height = dialog.winfo_screenheight()
        x = (screen_width - 400) // 2
        y = (screen_height - 500) // 2
        dialog.geometry(f"400x500+{x}+{y}")
        
        # Configure dialog appearance
        dialog.configure(fg_color="#F1D94B")
        
        # Title
        ctk.CTkLabel(
            dialog,
            text="Edit Customer",
            font=("Poppins", 20, "bold"),
            text_color="#2B2B2B"
        ).pack(padx=20, pady=(20,10))
        
        # Form fields
        fields = {}
        field_labels = {
            'first_name': 'First name',
            'last_name': 'Last Name',
            'username': 'UserName',
            'email': 'Email',
            'phone_number': 'Mobile number',
            'address': 'Address'
        }
        
        for field, label in field_labels.items():
            entry = ctk.CTkEntry(
                dialog,
                width=300,
                height=35,
                placeholder_text=label,
                fg_color="white",
                border_color="#E5E5E5"
            )
            entry.pack(padx=20, pady=5)
            entry.insert(0, customer[field] or '')
            fields[field] = entry
        
        # Buttons frame
        buttons_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        buttons_frame.pack(fill="x", padx=20, pady=20)
        
        # Remove Item button
        ctk.CTkButton(
            buttons_frame,
            text="Remove Item",
            font=("Poppins", 12),
            fg_color="#FF6B6B",
            text_color="white",
            hover_color="#FF5252",
            width=120,
            height=35,
            command=lambda: self.remove_customer(customer['userID'], dialog)
        ).pack(side="left", padx=5)
        
        # Update Item button
        ctk.CTkButton(
            buttons_frame,
            text="+ Update Item",
            font=("Poppins", 12),
            fg_color="black",
            text_color="white",
            hover_color="#1C1C1C",
            width=120,
            height=35,
            command=lambda: self.save_customer(customer['userID'], fields, dialog)
        ).pack(side="right", padx=5)
        
        # Cancel button
        ctk.CTkButton(
            dialog,
            text="Cancel",
            font=("Poppins", 12),
            fg_color="white",
            text_color="black",
            hover_color="#E5E5E5",
            width=120,
            height=35,
            command=dialog.destroy
        ).pack(pady=10)
        
    def save_customer(self, userID, fields, dialog):
        try:
            # Validate email
            if not re.match(r"[^@]+@[^@]+\.[^@]+", fields['email'].get()):
                messagebox.showerror("Validation Error", "Please enter a valid email address")
                return
                
            # Validate phone number
            if not re.match(r"^\+?1?\d{9,15}$", fields['phone_number'].get()):
                messagebox.showerror("Validation Error", "Please enter a valid phone number")
                return
                
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor()
            
            query = """
                UPDATE users 
                SET first_name = %s, last_name = %s, username = %s, 
                    email = %s, phone_number = %s, address = %s
                WHERE userID = %s
            """
            
            values = (
                fields['first_name'].get(),
                fields['last_name'].get(),
                fields['username'].get(),
                fields['email'].get(),
                fields['phone_number'].get(),
                fields['address'].get(),
                userID
            )
            
            cursor.execute(query, values)
            conn.commit()
            conn.close()
            
            dialog.destroy()
            self.load_customers()
            messagebox.showinfo("Success", "Customer updated successfully")
            
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Failed to update customer: {err}")
            
    def remove_customer(self, userID, dialog):
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to remove this customer?"):
            try:
                conn = mysql.connector.connect(**DB_CONFIG)
                cursor = conn.cursor()
                
                cursor.execute("DELETE FROM users WHERE userID = %s", (userID,))
                conn.commit()
                conn.close()
                
                dialog.destroy()
                self.load_customers()
                messagebox.showinfo("Success", "Customer removed successfully")
                
            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", f"Failed to remove customer: {err}")
                
    def search_customers(self):
        search_term = self.search_var.get().strip()
        self.load_customers(search_term if search_term else None)