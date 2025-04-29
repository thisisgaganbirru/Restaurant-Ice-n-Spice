import customtkinter as ctk
from dbconnection import DB_CONFIG
import mysql.connector
from datetime import datetime
from tkinter import messagebox
import re
from openpyxl import Workbook
from openpyxl.utils import get_column_letter
from openpyxl.styles import Font
from tkinter import filedialog
from adminreport_download import BusinessReportExporter
import openpyxl
class AdminCustomersPage(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.configure(fg_color="#F1E8DD")
        
        
        # Main body frame
        self.main_frame = ctk.CTkFrame(self, fg_color="#F1E8DD")
        self.main_frame.pack(fill="both", expand=True)
        self.main_frame.pack_propagate(False)    
        
        # Create customers content
        self.create_header()
        self.create_customers_content()
        self.create_footer()  # Add footer creation

    

    def create_header(self):
        # Header frame
        header_frame = ctk.CTkFrame(self.main_frame, fg_color="#F1D94B", height=50)
        header_frame.pack(fill="x", padx=5, pady=10)
        header_frame.pack_propagate(False)
        
        # Title
        ctk.CTkLabel(
            header_frame,
            text="Admin Customers Dashboard",
            font=("Poppins", 24, "bold"),
            text_color="Black"
        ).pack(side="left", padx=10)
        
        sub_frame = ctk.CTkFrame(self.main_frame, fg_color="#F1E8DD", height=50)
        sub_frame.pack(fill="x", padx=10, pady=10)
        sub_frame.pack_propagate(False)
        
        # Search frame (moved to left)
        search_frame = ctk.CTkFrame(sub_frame, fg_color="#F1E8DD")
        search_frame.pack(side="left")
        
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

        # Time frame dropdown (in middle)
        time_frame = ctk.CTkFrame(sub_frame, fg_color="#F1E8DD")
        time_frame.pack(side="left", padx=20)
        
        self.time_var = ctk.StringVar(value="All Time")
        time_options = ["All Time", "Last Week", "Last Month", "Last Year"]
        
        time_dropdown = ctk.CTkOptionMenu(
            time_frame,
            values=time_options,
            variable=self.time_var,
            font=("Poppins", 12),
            fg_color="#F1D94B",
            text_color="black",
            button_color="#E5CE45",
            button_hover_color="#D4BD34",
            command=self.filter_by_time
        )
        time_dropdown.pack(side="left")

        # Add Customer button (on right)
        ctk.CTkButton(
            sub_frame,
            text="+ Add Customer",
            font=("Poppins", 12),
            fg_color="#F1D94B",
            text_color="black",
            hover_color="#E5CE45",
            width=130,
            height=32,
            command=self.show_add_customer_dialog
        ).pack(side="right", padx=5)
        
    def create_customers_content(self): 
        
        # Customers grid container
        self.customers_frame = ctk.CTkFrame(
            self.main_frame, 
            fg_color="#F1E8DD"
        )
        self.customers_frame.pack(
            fill="both", 
            expand=True, 
            padx=20, 
            pady=(10, 0)  # Reduced bottom padding to accommodate footer
        )
        
        # Load customers
        self.load_customers()
        
    def create_footer(self):
        """Create footer frame with export button"""
        self.footer_frame = ctk.CTkFrame(
            self.main_frame, 
            fg_color="#F1E8DD",
            height=50
        )
        self.footer_frame.pack(fill="x", side="bottom", padx=10, pady=10)
        self.footer_frame.pack_propagate(False)

        # Export button
        ctk.CTkButton(
            self.footer_frame,
            text="Export Customer Data",
            font=("Poppins", 12),
            fg_color="#F1D94B",
            text_color="black",
            hover_color="#E5CE45",
            width=150,
            height=35,
            command=self.export_customer_data
        ).pack(side="right", padx=10)
        
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
        # Modern card with subtle border
        card = ctk.CTkFrame(
            parent, 
            fg_color="white", 
            border_width=1, 
            border_color="#e5e7eb", 
            corner_radius=8
        )
        card.configure(width=300, height=150)
        
        # Top info frame
        info_frame = ctk.CTkFrame(card, fg_color="#FFFFFF", width=300, height=60)
        info_frame.pack(fill="x", padx=10, pady=10)
        
        # Avatar circle with first letter
        avatar_frame = ctk.CTkFrame(
            info_frame, 
            width=50, 
            height=50, 
            corner_radius=20, 
            fg_color="#fef3c7"
        )
        avatar_frame.pack(side="left", padx=(5, 10))
        avatar_frame.pack_propagate(False)
        
        # Avatar letter
        avatar_letter = customer['first_name'][0] if customer['first_name'] else "?"
        ctk.CTkLabel(
            avatar_frame,
            text=avatar_letter,
            font=("Poppins", 14, "bold"),
            text_color="#d97706"
        ).place(relx=0.5, rely=0.5, anchor="center")
        
        # Customer details
        details_frame = ctk.CTkFrame(info_frame, fg_color="#FFFFFF")
        details_frame.pack(side="right", fill="x", expand=True)
        
        # Full name
        name = f"{customer['first_name']} {customer['last_name']}"
        ctk.CTkLabel(
            details_frame,
            text=name,
            font=("Poppins", 16, "bold"),
            text_color="#1f2937",
            anchor="w"
        ).pack(anchor="w")
        
        # Username and member since section
        details_section = ctk.CTkFrame(card, fg_color="#FFFFFF", width=300, height=50)
        details_section.pack(fill="x", padx=10, pady=(0, 5))
        
        # Username
        ctk.CTkLabel(
            details_section,
            text=f"@{customer['username']}",
            font=("Poppins", 12),
            text_color="gray",
            anchor="w"
        ).pack(anchor="w")
        
        # Member since
        created_date = datetime.strptime(str(customer['created_at']), '%Y-%m-%d %H:%M:%S')
        member_since = f"Member since: {created_date.strftime('%b %Y')}"
        ctk.CTkLabel(
            details_section,
            text=member_since,
            font=("Poppins", 10),
            text_color="gray",
            anchor="w"
        ).pack(anchor="w", pady=(5,0))
        
        # Separator
        separator = ctk.CTkFrame(card, height=1, fg_color="gray")
        separator.pack(fill="x", padx=10, pady=5)
        
        # Action buttons
        actions_frame = ctk.CTkFrame(card, fg_color="white", width=300, height=50)
        actions_frame.pack(fill="x", padx=10, pady=5)

        # View profile button
        view_btn = ctk.CTkButton(
            actions_frame,
            text="View profile",
            font=("Poppins", 11),
            fg_color="#FFFFFF",
            text_color="#eab308",
            hover_color="#f3f4f6",
            border_width=0,
            command=lambda: self.show_customer_profile(customer)
        )
        view_btn.pack(side="left")

        # Edit button (replacing Order history)
        edit_btn = ctk.CTkButton(
            actions_frame,
            text="Edit",
            font=("Poppins", 11),
            fg_color="#FFFFFF",
            text_color="#6b7280",
            hover_color="#f3f4f6",
            border_width=0,
            command=lambda: self.show_edit_dialog(customer)
        )
        edit_btn.pack(side="right")

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
        buttons_frame = ctk.CTkFrame(dialog, fg_color="#F1D94B")
        buttons_frame.pack(fill="x", padx=20, pady=20)
        
        # Remove Item button
        ctk.CTkButton(
            buttons_frame,
            text="Remove Customer",
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
            text="+ Update Details",
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

    def export_customer_data(self):
        """Export customer data using BusinessReportExporter"""
        try:
            # Create default filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            default_filename = f"IcenSpice_Customers_{timestamp}.xlsx"
            
            # Ask for save location with default filename
            file_path = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                filetypes=[("Excel files", "*.xlsx")],
                initialfile=default_filename,
                title="Ice'n Spice Customer Data Export"
            )
            
            if not file_path:
                return

            # Create workbook
            workbook = openpyxl.Workbook()
            
            # Connect to database
            conn = mysql.connector.connect(**DB_CONFIG)
            
            # Create instance of BusinessReportExporter and use its method
            exporter = BusinessReportExporter()
            exporter._create_customer_sheet(conn, workbook, "All Time")
            
            # Save workbook
            workbook.save(file_path)
            
            # Close database connection
            conn.close()
            
            messagebox.showinfo(
                "Export Successful", 
                f"Customer data exported successfully to:\n{file_path}"
            )

        except mysql.connector.Error as err:
            messagebox.showerror(
                "Export Error", 
                f"Failed to export customer data: {err}"
            )
        except Exception as e:
            messagebox.showerror(
                "Export Error", 
                f"An error occurred while exporting: {e}"
            )
    
    def show_customer_profile(self, customer):
        """Show detailed customer profile view"""
        # Create a toplevel window for the profile
        profile_window = ctk.CTkToplevel(self)
        profile_window.title(f"Customer Profile - {customer['first_name']} {customer['last_name']}")
        profile_window.geometry("900x700")
        profile_window.resizable(True, True)
        profile_window.grab_set()  # Make modal
        
        # Center the window
        profile_window.update_idletasks()
        screen_width = profile_window.winfo_screenwidth()
        screen_height = profile_window.winfo_screenheight()
        x = (screen_width - 900) // 2
        y = (screen_height - 700) // 2
        profile_window.geometry(f"900x700+{x}+{y}")
        
        # Create the profile view
        profile_view = CustomerProfileView(
            profile_window, 
            customer_id=customer['userID'],
            on_back=profile_window.destroy
        )
        profile_view.pack(fill="both", expand=True)

    def filter_by_time(self, time_frame):
        """Filter customers by time frame"""
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor(dictionary=True)
            
            query = """
                SELECT userID, first_name, last_name, username, email, 
                       phone_number, address, created_at
                FROM users
                WHERE role = 'customer'
            """
            
            if time_frame != "All Time":
                if time_frame == "Last Week":
                    query += " AND created_at >= DATE_SUB(NOW(), INTERVAL 1 WEEK)"
                elif time_frame == "Last Month":
                    query += " AND created_at >= DATE_SUB(NOW(), INTERVAL 1 MONTH)"
                elif time_frame == "Last Year":
                    query += " AND created_at >= DATE_SUB(NOW(), INTERVAL 1 YEAR)"
            
            cursor.execute(query)
            customers = cursor.fetchall()
            
            # Clear and reload customers
            for widget in self.customers_frame.winfo_children():
                widget.destroy()
                
            if not customers:
                ctk.CTkLabel(
                    self.customers_frame,
                    text="No customers found in selected time frame",
                    font=("Poppins", 16),
                    text_color="gray"
                ).pack(pady=20)
                return
                
            # Configure grid layout
            self.customers_frame.grid_columnconfigure((0,1,2), weight=1)
            row = 0
            col = 0
            
            for customer in customers:
                card = self.create_customer_card(self.customers_frame, customer)
                card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
                
                col += 1
                if col > 2:
                    col = 0
                    row += 1
                    
            conn.close()
            
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Failed to filter customers: {err}")

    def show_add_customer_dialog(self):
        """Show dialog to add a new customer"""
        dialog = ctk.CTkToplevel(self)
        dialog.title("Add New Customer")
        dialog.geometry("400x500")
        dialog.resizable(False, False)
        
        # Make dialog modal
        dialog.grab_set()
        
        # Center the dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() - 400) // 2
        y = (dialog.winfo_screenheight() - 500) // 2
        dialog.geometry(f"400x500+{x}+{y}")
        
        # Configure dialog appearance
        dialog.configure(fg_color="#F1D94B")
        
        # Title
        ctk.CTkLabel(
            dialog,
            text="Add New Customer",
            font=("Poppins", 20, "bold"),
            text_color="#2B2B2B"
        ).pack(padx=20, pady=(20,10))
        
        # Form fields
        fields = {}
        field_labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'username': 'Username',
            'email': 'Email',
            'phone_number': 'Mobile Number',
            'address': 'Address',
            'password': 'Password'  # Added password field for new customer
        }
        
        for field, label in field_labels.items():
            entry = ctk.CTkEntry(
                dialog,
                width=300,
                height=35,
                placeholder_text=label,
                fg_color="white",
                border_color="#E5E5E5",
                show="*" if field == 'password' else ""
            )
            entry.pack(padx=20, pady=5)
            fields[field] = entry
        
        # Add Customer button
        ctk.CTkButton(
            dialog,
            text="Add Customer",
            font=("Poppins", 12),
            fg_color="black",
            text_color="white",
            hover_color="#1C1C1C",
            width=120,
            height=35,
            command=lambda: self.add_new_customer(fields, dialog)
        ).pack(pady=10)
        
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
        ).pack(pady=5)

    def add_new_customer(self, fields, dialog):
        """Add a new customer to the database"""
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
                INSERT INTO users (
                    first_name, last_name, username, email, 
                    phone_number, address, password, role
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, 'customer')
            """
            
            values = (
                fields['first_name'].get(),
                fields['last_name'].get(),
                fields['username'].get(),
                fields['email'].get(),
                fields['phone_number'].get(),
                fields['address'].get(),
                fields['password'].get()  # In production, hash this password
            )
            
            cursor.execute(query, values)
            conn.commit()
            conn.close()
            
            dialog.destroy()
            self.load_customers()
            messagebox.showinfo("Success", "Customer added successfully")
            
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Failed to add customer: {err}")