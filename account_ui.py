import tkinter as tk
import customtkinter as ctk
import sqlite3
from PIL import Image

# Model: Database operations
class UserModel:
    @staticmethod
    def connect_db():
        return sqlite3.connect('users.db')

    @staticmethod
    def fetch_user_data(user_id):
        conn = UserModel.connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT name, dob, address, phone, password FROM users WHERE userId=?", (user_id,))
        user_data = cursor.fetchone()
        conn.close()
        return user_data

    @staticmethod
    def update_user_data(user_id, field, value):
        conn = UserModel.connect_db()
        cursor = conn.cursor()
        cursor.execute(f"UPDATE users SET {field}=? WHERE userId=?", (value, user_id))
        conn.commit()
        conn.close()

# View: UI components
class UserView:
    def __init__(self, root, user_data):
        self.root = root
        self.profile_frame = ctk.CTkFrame(root)
        self.name, self.dob, self.address, self.phone, self.password = user_data
        self.create_ui()

    def create_ui(self):
        self.create_editable_entry("Name", self.name, 46, "name")
        self.create_editable_entry("Date of Birth", self.dob, 106, "dob")
        self.create_editable_entry("Address", self.address, 166, "address")
        self.create_editable_entry("Phone Number", self.phone, 226, "phone")

    def create_editable_entry(self, label_text, value, y_position, field_name):
        # UI elements for editing user data
        ctk.CTkLabel(self.profile_frame, text=label_text, font=("Manrope", 12), text_color="black").place(x=20, y=y_position)
        entry = ctk.CTkEntry(self.profile_frame, width=300, height=25, corner_radius=30, fg_color="white", text_color="black")
        entry.insert(0, value)
        entry.configure(state="disabled")
        entry.place(x=20, y=y_position + 30)

        edit_button = ctk.CTkButton(self.profile_frame, text="✎", width=30, height=30, corner_radius=15, command=lambda: self.toggle_edit(entry, edit_button, field_name))
        edit_button.place(x=330, y=y_position + 30)

    def toggle_edit(self, entry, edit_button, field_name):
        entry.configure(state="normal")
        edit_button.configure(text="✓", command=lambda: self.confirm_edit(entry, edit_button, field_name))

    def confirm_edit(self, entry, edit_button, field_name):
        new_value = entry.get()
        UserModel.update_user_data(1, field_name, new_value)  # Assuming user_id is 1 for simplicity
        entry.configure(state="disabled")
        edit_button.configure(text="✎", command=lambda: self.toggle_edit(entry, edit_button, field_name))

# Controller: Application logic
class UserController:
    def __init__(self, root):
        self.user_id = 1  # Replace with actual userId from login
        self.user_data = UserModel.fetch_user_data(self.user_id)
        self.view = UserView(root, self.user_data)

def account_page_content(account_page):
    # Color and font definitions
    account_page_color_background_color = '#D3D3D3'  # Grey background
    pi_info_component_color = '#E5EDF0'
    pi_component_label_font = ("Manrope", 13, 'bold')
    pi_component_font = ("Manrope", 12)
    pi_info_component_border_color = '#F1D94B'  # Yellow border
    summary_number_font = ('SF Pro', 20, 'bold')
    summary_text_font = ('SF Pro', 12)
    summary_text_color = '#6C7071'
    page_heading_font = ('Manrope', 20)
    page_heading_color = "#6A0032"
    page_heading_description_font = ('Manrope', 14)
    page_heading_description_color = "gray"

    # Sample user data
    name = "Jane Doe"
    first_name = "Jane"
    dob = "10-10-1775"
    address = "123 Deming Dr. Mount Pleasant, 48858"
    phone = '123-456-7890'
    marital_status = "Single"
    emergency_contact = "Haley Doe"
    current_user_email = "janedoe@sample.edu"

    # Sample orders data
    orders = [
        {
            "title": "Cream Stone Ice Cream",
            "location": "Kukatpally",
            "order_number": "#195504689959255",
            "date": "Fri, Jan 10, 2025, 01:51 PM",
            "total_paid": "₹ 307",
            "items": [
                "1 x Biryani (₹150)",
                "2 x Pizza (₹200)"
            ]
        },
        {
            "title": "Nutty Delight",
            "location": "Banjara Hills",
            "order_number": "#195504689959256",
            "date": "Thu, Jan 9, 2025, 03:45 PM",
            "total_paid": "₹ 450",
            "items": [
                "1 x Nutty Ice Cream (₹250)",
                "1 x Chocolate Cake (₹200)"
            ]
        }
    ]

    # Main container
    account_container = ctk.CTkFrame(account_page, width=400, height=500, fg_color=account_page_color_background_color)
    account_container.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    # Top labels
    def switch_frame(frame_name):
        if frame_name == "Profile":
            profile_frame.tkraise()
        elif frame_name == "Orders":
            orders_frame.tkraise()

    profile_label = ctk.CTkLabel(
        master=account_container,
        text="Profile",
        font=page_heading_font,
        text_color=page_heading_color,
        width=200,
        height=40,
        fg_color=account_page_color_background_color,
        corner_radius=10,
        cursor="hand2"
    )
    profile_label.place(x=0, y=10)
    profile_label.bind("<Button-1>", lambda e: switch_frame("Profile"))

    orders_label = ctk.CTkLabel(
        master=account_container,
        text="Orders",
        font=page_heading_font,
        text_color=page_heading_color,
        width=200,
        height=40,
        fg_color=account_page_color_background_color,
        corner_radius=10,
        cursor="hand2"
    )
    orders_label.place(x=200, y=10)
    orders_label.bind("<Button-1>", lambda e: switch_frame("Orders"))

    # Shared frame for content
    shared_frame = ctk.CTkFrame(account_container, width=400, height=440, fg_color=account_page_color_background_color)
    shared_frame.place(x=0, y=60)

    # Profile frame
    profile_frame = ctk.CTkFrame(shared_frame, width=400, height=440, fg_color=account_page_color_background_color)
    profile_frame.place(x=0, y=0)

    # Orders frame (empty for now)
    orders_frame = ctk.CTkFrame(shared_frame, width=400, height=440, fg_color=account_page_color_background_color)
    orders_frame.place(x=0, y=0)

    # Scrollable canvas for orders
    canvas = tk.Canvas(orders_frame, width=400, height=440, bg=account_page_color_background_color, highlightthickness=0)
    scrollbar = tk.Scrollbar(orders_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = ctk.CTkFrame(canvas, width=400, fg_color=account_page_color_background_color)

    def configure_scrollbar(event):
        canvas.configure(scrollregion=canvas.bbox("all"))
        if scrollable_frame.winfo_height() > 440:
            scrollbar.pack(side="right", fill="y")
        else:
            scrollbar.pack_forget()

    scrollable_frame.bind("<Configure>", configure_scrollbar)

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)

    # Create food cards for each order
    for idx, order in enumerate(orders):
        y_position = 10 + idx * 220
        food_card = ctk.CTkFrame(scrollable_frame, width=380, height=200, fg_color='white', corner_radius=10)
        food_card.place(x=10, y=y_position)

        # Food image placeholder
        food_image = ctk.CTkLabel(food_card, text="Image", width=100, height=100, fg_color='#D3D3D3')
        food_image.place(x=10, y=10)

        # Food title and location
        food_title = ctk.CTkLabel(food_card, text=order["title"], font=("Manrope", 14, 'bold'), text_color="black")
        food_title.place(x=120, y=10)

        food_location = ctk.CTkLabel(food_card, text=order["location"], font=("Manrope", 12), text_color="black")
        food_location.place(x=120, y=35)

        # Order details
        order_details = ctk.CTkLabel(food_card, text=f"ORDER {order['order_number']} | {order['date']}", font=("Manrope", 10), text_color="gray")
        order_details.place(x=120, y=60)

        # Function to toggle order details
        def toggle_order_details(expanded_frame, label):
            if expanded_frame.winfo_ismapped():
                expanded_frame.place_forget()
                label.configure(text="VIEW DETAILS")
            else:
                expanded_frame.place(x=10, y=120)
                label.configure(text="BACK")

        # View details label
        view_details_label = ctk.CTkLabel(food_card, text="VIEW DETAILS", font=("Manrope", 10, 'underline'), text_color="#FF4500", cursor="hand2")
        view_details_label.place(x=120, y=90)
        
        # Order details expanded (initially hidden)
        order_details_expanded = ctk.CTkFrame(food_card, width=360, height=60, fg_color='white')
        order_details_expanded.place(x=10, y=120)
        order_details_expanded.place_forget()

        # Bind toggle function
        view_details_label.bind("<Button-1>", lambda e, f=order_details_expanded, l=view_details_label: toggle_order_details(f, l))

        # Example order items
        for item_idx, item in enumerate(order["items"]):
            order_item = ctk.CTkLabel(order_details_expanded, text=item, font=("Manrope", 10), text_color="black")
            order_item.place(x=10, y=5 + item_idx * 20)

        # Reorder button
        reorder_button = ctk.CTkButton(food_card, text="REORDER", width=100, height=25, corner_radius=5, fg_color="#FF4500", text_color="white")
        reorder_button.place(x=10, y=150)

        # Total paid
        total_paid = ctk.CTkLabel(food_card, text=f"Total Paid: {order['total_paid']}", font=("Manrope", 12, 'bold'), text_color="black")
        total_paid.place(x=250, y=150)

    # Personal information section
    personal_information_label = ctk.CTkLabel(
        profile_frame,
        text="Personal Information",
        text_color=page_heading_color,
        font=("Manrope", 20)
    )
    personal_information_label.place(x=25, y=10)

    # Function to create editable entry with edit button
    def create_editable_entry(frame, label_text, value, y_position):
        # Label
        ctk.CTkLabel(frame, text=label_text, font=pi_component_label_font, text_color="black").place(x=20, y=y_position)
        
        # Entry
        entry = ctk.CTkEntry(
            frame,
            width=300,  # Reduced width
            height=25,  # Reduced height
            corner_radius=30,
            fg_color="white",
            border_color=pi_info_component_border_color,
            border_width=1,
            show="*" if "password" in label_text.lower() else None,
            text_color="black"
        )
        entry.insert(0, value)
        entry.configure(state="disabled")
        entry.place(x=20, y=y_position + 30)

        # Edit button
        edit_button = ctk.CTkButton(
            frame,
            text="✎",
            width=30,
            height=30,
            corner_radius=15,
            fg_color=pi_info_component_border_color,
            hover_color="#E5DCD0",
            command=lambda: toggle_edit(entry, edit_button, confirm_button, cancel_button)
        )
        edit_button.place(x=330, y=y_position + 30)

        # Confirm button (initially hidden)
        confirm_button = ctk.CTkButton(
            frame,
            text="✓",
            width=30,
            height=30,
            corner_radius=15,
            fg_color="#4CAF50",
            hover_color="#45a049",
            command=lambda: confirm_edit(entry, edit_button, confirm_button, cancel_button)
        )
        confirm_button.place(x=330, y=y_position + 30)
        confirm_button.place_forget()

        # Cancel button (initially hidden)
        cancel_button = ctk.CTkButton(
            frame,
            text="✕",
            width=30,
            height=30,
            corner_radius=15,
            fg_color="#f44336",
            hover_color="#da190b",
            command=lambda: cancel_edit(entry, edit_button, confirm_button, cancel_button, value)
        )
        cancel_button.place(x=370, y=y_position + 30)
        cancel_button.place_forget()

        return entry

    def toggle_edit(entry, edit_button, confirm_button, cancel_button):
        entry.configure(state="normal")
        edit_button.place_forget()
        confirm_button.place(x=330, y=entry.winfo_y())
        cancel_button.place(x=370, y=entry.winfo_y())

    def confirm_edit(entry, edit_button, confirm_button, cancel_button):
        entry.configure(state="disabled")
        confirm_button.place_forget()
        cancel_button.place_forget()
        edit_button.place(x=330, y=entry.winfo_y())

    def cancel_edit(entry, edit_button, confirm_button, cancel_button, original_value):
        entry.delete(0, tk.END)
        entry.insert(0, original_value)
        entry.configure(state="disabled")
        confirm_button.place_forget()
        cancel_button.place_forget()
        edit_button.place(x=330, y=entry.winfo_y())

    # Create editable entries
    y_positions = [46, 106, 166, 226]
    fields = [
        ("Name", name),
        ("Date of Birth", dob),
        ("Address", address),
        ("Phone Number", phone)
    ]

    for i, (label, value) in enumerate(fields):
        create_editable_entry(profile_frame, label, value, y_positions[i])

    # Password Section
    password_label = ctk.CTkLabel(
        profile_frame,
        text="Password",
        text_color=page_heading_color,
        font=("Manrope", 20)
    )
    password_label.place(x=20, y=286)

    password_entry = ctk.CTkEntry(
        profile_frame,
        width=345,
        height=30,
        corner_radius=30,
        fg_color="white",
        border_color=pi_info_component_border_color,
        border_width=1,
        show="*",
        text_color="black"
    )
    password_entry.place(x=20, y=316)

    # Edit button for password
    password_edit_button = ctk.CTkButton(
        profile_frame,
        text="✎",
        width=30,
        height=30,
        corner_radius=15,
        fg_color=pi_info_component_border_color,
        hover_color="#E5DCD0",
        command=lambda: toggle_password_edit()
    )
    password_edit_button.place(x=375, y=316)

    # Function to toggle password edit
    def toggle_password_edit():
        password_entry.place_forget()  # Hide original password entry
        password_edit_button.place_forget()  # Hide edit button
        new_password_entry.place(x=20, y=316)
        confirm_password_entry.place(x=20, y=356)
        change_password_button.place(x=75, y=396)

    # Password entries (initially hidden)
    new_password_entry = ctk.CTkEntry(
        profile_frame,
        width=300,  # Reduced width
        height=25,  # Reduced height
        corner_radius=30,
        fg_color="white",
        border_color=pi_info_component_border_color,
        border_width=1,
        placeholder_text="enter new password",
        show="*",
        text_color="black"
    )

    confirm_password_entry = ctk.CTkEntry(
        profile_frame,
        width=300,  # Reduced width
        height=25,  # Reduced height
        corner_radius=30,
        fg_color="white",
        border_color=pi_info_component_border_color,
        border_width=1,
        placeholder_text="enter new password again",
        show="*",
        text_color="black"
    )

    change_password_button = ctk.CTkButton(
        profile_frame,
        width=200,  # Reduced width
        height=25,  # Reduced height
        corner_radius=30,
        text="Change Password",
        fg_color=page_heading_color
    )

    # Raise profile frame by default
    profile_frame.tkraise()

# Create and run the application
if __name__ == "__main__":
    root = ctk.CTk()
    root.title("Account Page")
    root.geometry("600x700")
    
    account_page_content(root)
    
    app = UserController(root)
    root.mainloop() 