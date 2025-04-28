import customtkinter as ctk
from admin_nav import AdminNav
from dbconnection import DB_CONFIG
import mysql.connector
from datetime import datetime
from tkinter import messagebox
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from tkinter import filedialog
import os
from dotenv import load_dotenv
import logging
import traceback
import uuid
import json
from decimal import Decimal
from typing import Optional, Dict, Any

class AdminSupport(ctk.CTkFrame):
    # =============================================
    # INITIALIZATION AND SETUP
    # =============================================
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.configure(fg_color="white")
        
        # Load environment variables
        load_dotenv()
        
        # Setup logging
        self.setup_logging()
        
        # Setup email configuration
        self.setup_email_config()
        
        # Create support content
        self.create_support_ui()
    
    def setup_logging(self):
        """Initialize logging configuration"""
        log_level = getattr(logging, os.getenv('LOG_LEVEL', 'INFO'))
        log_file = os.getenv('LOG_FILE', 'support_logs.txt')
        
        # Create logger
        self.logger = logging.getLogger('AdminSupport')
        self.logger.setLevel(log_level)
        
        # Create formatters
        file_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        console_formatter = logging.Formatter(
            '%(levelname)s: %(message)s'
        )
        
        # File handler
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(log_level)
        file_handler.setFormatter(file_formatter)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)
        console_handler.setFormatter(console_formatter)
        
        # Add handlers
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
        
        self.logger.info('Logging initialized')
    
    def setup_email_config(self):
        self.email_config = {
            'smtp_server': os.getenv('SMTP_SERVER', 'smtp.gmail.com'),
            'smtp_port': int(os.getenv('SMTP_PORT', '587')),
            'smtp_username': os.getenv('SMTP_USERNAME'),
            'smtp_password': os.getenv('SMTP_PASSWORD'),
            'from_email': os.getenv('FROM_EMAIL', 'support@icenspice.com'),
            'restaurant_name': os.getenv('RESTAURANT_NAME', "Ice'n Spice"),
            'restaurant_website': os.getenv('RESTAURANT_WEBSITE', 'https://www.icenspice.com'),
            'support_team': os.getenv('SUPPORT_TEAM_NAME', "Ice'n Spice Support Team"),
            'support_phone': os.getenv('SUPPORT_PHONE', ''),
            'support_email': os.getenv('SUPPORT_EMAIL', ''),
            'support_hours': os.getenv('SUPPORT_HOURS', ''),
            'support_address': os.getenv('SUPPORT_ADDRESS', ''),
            'email_signature': os.getenv('EMAIL_SIGNATURE', ''),
            'templates': {
                'reply': os.getenv('REPLY_TEMPLATE', ''),
                'welcome': os.getenv('WELCOME_TEMPLATE', ''),
                'order_status': os.getenv('ORDER_STATUS_TEMPLATE', ''),
                'error': os.getenv('ERROR_TEMPLATE', '')
            }
        }
        
        self.logger.info("Email configuration loaded")
    
    # =============================================
    # UI CREATION
    # =============================================
    def create_support_ui(self):
        # Main body frame with border
        self.body_frame = ctk.CTkFrame(
            self,
            fg_color="#F1E8DD",
            border_width=1,
            border_color="#E0E0E0"
        )
        self.body_frame.pack(side="right", fill="both", expand=True, padx=5, pady=5)
        
        # Header with title and compose button
        header_frame = ctk.CTkFrame(
            self.body_frame, 
            fg_color="transparent", 
            height=60,
            border_width=1,
            border_color="#E0E0E0"
        )
        header_frame.pack(fill="x", padx=20)
        header_frame.pack_propagate(False)
        
        # Title with updated styling
        ctk.CTkLabel(
            header_frame,
            text="Admin Support",
            font=("Poppins", 24, "bold"),
            text_color="#2B2B2B"
        ).pack(side="left")
        
        # Header with title and compose button
        sub_frame = ctk.CTkFrame(
            self.body_frame, 
            fg_color="transparent", 
            height=60,
            border_width=1,
            border_color="#E0E0E0")
        sub_frame.pack(fill="x", padx=20, pady=10)
        sub_frame.pack_propagate(False)

        # Compose button with updated styling - MOVED TO LEFT
        compose_button = ctk.CTkButton(
            sub_frame,
            text="Compose New Mail",
            font=("Poppins", 13),
            fg_color="#F1D94B",
            text_color="black",
            hover_color="#E5CE45",
            height=35,
            command=self.show_compose_dialog
        )
        compose_button.pack(side="left")

        # Add sort options
        sort_frame = ctk.CTkFrame(sub_frame, fg_color="transparent")
        sort_frame.pack(side="right", padx=(0, 10))

        sort_label = ctk.CTkLabel(
            sort_frame, 
            text="Sort:", 
            font=("Poppins", 12),
            text_color="#2B2B2B"
        )
        sort_label.pack(side="left", padx=(0, 5))

        # Create StringVar for sort option
        self.sort_option = ctk.StringVar(value="newest")
        sort_values = ["newest", "oldest"]
        sort_dropdown = ctk.CTkOptionMenu(
            sort_frame,
            values=sort_values,
            variable=self.sort_option,
            width=120,
            font=("Poppins", 12),
            dropdown_font=("Poppins", 12),
            fg_color="#F1E8DD",
            text_color="black",
            button_color="#F1D94B",
            button_hover_color="#E5CE45",
            dropdown_hover_color="#F1E8DD",
            command=self.update_message_list
        )
        sort_dropdown.pack(side="left")

        # Add filter options
        filter_frame = ctk.CTkFrame(sub_frame, fg_color="transparent")
        filter_frame.pack(side="right", padx=(0, 10))

        filter_label = ctk.CTkLabel(
            filter_frame, 
            text="Filter:", 
            font=("Poppins", 12),
            text_color="#2B2B2B"
        )
        filter_label.pack(side="left", padx=(0, 5))

        # Create StringVar for filter option
        self.filter_option = ctk.StringVar(value="all")
        filter_values = ["all", "read", "unread"]
        filter_dropdown = ctk.CTkOptionMenu(
            filter_frame,
            values=filter_values,
            variable=self.filter_option,
            width=120,
            font=("Poppins", 12),
            dropdown_font=("Poppins", 12),
            fg_color="#F1E8DD",
            text_color="black",
            button_color="#F1D94B",
            button_hover_color="#E5CE45",
            dropdown_hover_color="#F1E8DD",
            command=self.update_message_list
        )
        filter_dropdown.pack(side="left")
        
        # Main content area with border
        content_frame = ctk.CTkFrame(
            self.body_frame, 
            fg_color="white", 
            corner_radius=15,
            border_width=1,
            border_color="#E0E0E0"
        )
        content_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Left column - Folders with border
        folders_frame = ctk.CTkFrame(
            content_frame, 
            fg_color="white",
            width=200,
            border_width=1,
            border_color="#E0E0E0"
        )
        folders_frame.pack(side="left", fill="y", padx=0, pady=0)
        folders_frame.pack_propagate(False)

        # Folder buttons with updated styling
        self.current_folder = ctk.StringVar(value="inbox")

        # Define the folders with their properties
        folders_config = [
            {"name": "Inbox", "value": "inbox", "color": "#F1D94B"},
            {"name": "Sent", "value": "sent", "color": "#4FD675"},
            {"name": "Trash", "value": "trash", "color": "#4FD675"},
        ]

        # Store references to the buttons
        self.folder_buttons = {}

        # Create a scrollable frame for folders
        folders_container = ctk.CTkScrollableFrame(
            folders_frame,
            fg_color="transparent",
            scrollbar_fg_color="#E0E0E0",
            scrollbar_button_color="#CCCCCC",
            width=200,
            height=len(folders_config) * 41,
        )
        folders_container.pack(fill="both", expand=True)

        # Create folder buttons dynamically based on the config
        for folder in folders_config:
            # Create a wrapper frame for the button to make it full width clickable
            mailbox_frame = ctk.CTkFrame(
                folders_container, 
                fg_color="transparent", 
                height=40,
                corner_radius=0
            )
            mailbox_frame.pack(fill="x", pady=(0, 1), padx=0)
            mailbox_frame.pack_propagate(False)
            
            # Indicator for selected item
            indicator = ctk.CTkFrame(
                mailbox_frame, 
                width=3, 
                height=30, 
                fg_color=folder["color"] if folder["value"] == "inbox" else "transparent"
            )
            indicator.place(x=0, rely=0.5, anchor="w", relheight=0.75)
            
            # Store reference to the indicator
            setattr(self, f"{folder['value']}_indicator", indicator)
            
            # Create button with text and folder icon
            btn = ctk.CTkButton(
                mailbox_frame,
                text=folder["name"],
                font=("Poppins", 14),
                fg_color=folder["color"] if folder["value"] == "inbox" else "transparent",
                text_color="black",
                hover_color="#F1E8DD",
                anchor="w",
                height=40,
                width=190,
                corner_radius=0,
                command=lambda v=folder["value"]: self.switch_folder(v)
            )
            btn.place(x=10, rely=0.5, anchor="w", relwidth=0.95)
            
            # Store references for later use
            self.folder_buttons[folder["value"]] = {
                "button": btn,
                "color": folder["color"],
                "indicator": indicator,
                "frame": mailbox_frame
            }
            
            # Add click event to the frame as well
            mailbox_frame.bind("<Button-1>", 
                            lambda e, v=folder["value"]: self.switch_folder(v))

        # Separator line
        separator = ctk.CTkFrame(content_frame, fg_color="#E0E0E0", width=2)
        separator.pack(side="left", fill="y", padx=0, pady=10)
        
        # Right panel - Messages with border
        messages_panel = ctk.CTkFrame(
            content_frame, 
            fg_color="white",
            border_width=1,
            border_color="#E0E0E0"
        )
        messages_panel.pack(side="left", fill="both", expand=True)
        
        # Create scrollable frame with custom styling
        self.messages_frame = ctk.CTkScrollableFrame(
            messages_panel,
            fg_color="white",
            scrollbar_fg_color="#E0E0E0",
            scrollbar_button_color="#CCCCCC",
            scrollbar_button_hover_color="#F1D94B"
        )
        self.messages_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Configure scrollbar
        scrollbar = self.messages_frame._scrollbar
        scrollbar.configure(width=8)
        
        # Load initial messages
        self.load_messages()
        
         
    # =============================================
    # FOLDER AND MESSAGE MANAGEMENT
    # =============================================
    def switch_folder(self, folder):
        # Update button colors and indicators
        for folder_value, components in self.folder_buttons.items():
            btn = components["button"]
            indicator = components["indicator"]
            color = components["color"]
            
            if folder_value == folder:
                # Selected folder
                btn.configure(fg_color=color)
                indicator.configure(fg_color=color)
            else:
                # Unselected folders
                btn.configure(fg_color="transparent")
                indicator.configure(fg_color="transparent")
        
        self.current_folder.set(folder)
        self.load_messages()
    
    def update_message_list(self, *args):
        self.logger.info(f"Updating message list: sort={self.sort_option.get()}, filter={self.filter_option.get()}")
        self.load_messages()

    def load_messages(self):
        # Clear existing messages
        for widget in self.messages_frame.winfo_children():
            widget.destroy()
            
        try:
            self.logger.info(f"Loading messages for folder: {self.current_folder.get()}")
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor(dictionary=True)
            
            folder = self.current_folder.get()
            sort_option = self.sort_option.get() if hasattr(self, 'sort_option') else "newest"
            filter_option = self.filter_option.get() if hasattr(self, 'filter_option') else "all"
            
            # Base query
            query = "SELECT * FROM contact_messages WHERE "
            
            # Folder conditions
            if folder == "inbox":
                folder_condition = "parent_id IS NULL"
                # Add condition that messages must be unread for inbox
                if filter_option == "all":
                    filter_condition = " AND status = 'unread'"
                elif filter_option == "read":
                    # For inbox, "read" doesn't make sense as they would be in trash
                    filter_condition = " AND 1=0"  # This will return no results
                elif filter_option == "unread":
                    filter_condition = " AND status = 'unread'"
            elif folder == "sent":
                folder_condition = "is_reply = 1"
                filter_condition = ""
            else:  # trash
                folder_condition = "status = 'read' AND parent_id IS NULL"
                if filter_option == "all":
                    filter_condition = ""
                elif filter_option == "read":
                    filter_condition = " AND status = 'read'"
                elif filter_option == "unread":
                    filter_condition = " AND status = 'unread'"
            
            # Combine conditions
            query += folder_condition + filter_condition
            
            # Sort order
            sort_order = "DESC" if sort_option == "newest" else "ASC"
            query += f" ORDER BY created_at {sort_order}"
            
            cursor.execute(query)
            messages = cursor.fetchall()
            
            self.logger.info(f"Found {len(messages)} messages")
            
            # Create message items
            for message in messages:
                self.create_message_item(message)
                
            conn.close()
            
        except mysql.connector.Error as err:
            self.logger.error(f"Database error: {err}")
            messagebox.showerror("Error", f"Failed to load messages: {err}")
    
    def create_message_item(self, message):
        # Main message container with hover effect and fixed height
        item = ctk.CTkFrame(
            self.messages_frame, 
            fg_color="white",
            height=150,
            border_width=2,
            border_color="grey",
            corner_radius=8
        )
        item.pack(fill="x", pady=10, padx=10)
        item.pack_propagate(False)
        
        # Hover effect
        def on_enter(e):
            item.configure(fg_color="#F8F9FA")
        
        def on_leave(e):
            item.configure(fg_color="white")
        
        item.bind("<Enter>", on_enter)
        item.bind("<Leave>", on_leave)
        item.bind("<Button-1>", lambda e: self.show_message_dialog(message))
        
        # Create left (content) and right (button) frames
        left_frame = ctk.CTkFrame(item, fg_color="transparent")
        left_frame.pack(side="left", fill="both", expand=True, padx=15, pady=15)
        left_frame.bind("<Button-1>", lambda e: self.show_message_dialog(message))
        
        right_frame = ctk.CTkFrame(item, fg_color="transparent", width=100)
        right_frame.pack(side="right", fill="y", padx=15, pady=15)
        right_frame.bind("<Button-1>", lambda e: self.show_message_dialog(message))
        
        # Subject line
        if message.get('status') == 'unread':
            subject_text = f"IMP!! Message from {message['name']}"
            subject_font = ("Poppins", 14, "bold")
        else:
            subject_text = f"Message from {message['name']}"
            subject_font = ("Poppins", 14)
        
        ctk.CTkLabel(
            left_frame,
            text=subject_text,
            font=subject_font,
            text_color="#2B2B2B",
            anchor="w"
        ).pack(fill="x", pady=(0, 5), anchor="w")
        
        # Email
        ctk.CTkLabel(
            left_frame,
            text=message['email'],
            font=("Poppins", 12),
            text_color="gray",
            anchor="w"
        ).pack(fill="x", pady=(0, 10), anchor="w")
        
        # Message preview - simple version
        preview = message['message'][:250] + "..." if len(message['message']) > 250 else message['message']
        
        preview_label = ctk.CTkLabel(
            left_frame,
            text=preview,
            font=("Poppins", 12),
            text_color="#555555",
            anchor="w",
            justify="left",
            wraplength=400
        )
        preview_label.pack(fill="both", expand=True, anchor="w")
        
        # Add Open button
        open_btn = ctk.CTkButton(
            right_frame,
            text="Open",
            font=("Poppins", 13),
            fg_color="#F1D94B",
            text_color="black",
            hover_color="#E5CE45",
            width=80,
            height=35,
            command=lambda: self.show_message_dialog(message)
        )
        open_btn.place(relx=0.5, rely=0.5, anchor="center")
        
        # =============================================
    # DIALOG BOXES
    # =============================================
    def show_message_dialog(self, message):
        dialog = self.create_dialog("Message Details", 600, 500)
        
        # Header
        header = ctk.CTkFrame(dialog, fg_color="transparent")
        header.pack(fill="x", padx=30, pady=20)
        
        # From
        sender_text = f"{message['name']} <{message['email']}>"
        ctk.CTkLabel(
            header,
            text=sender_text,
            font=("Poppins", 16, "bold"),
            text_color="#2B2B2B"
        ).pack(anchor="w")
        
        # Time
        time_text = message['created_at'].strftime("%B %d, %Y at %I:%M %p")
        ctk.CTkLabel(
            header,
            text=time_text,
            font=("Poppins", 12),
            text_color="gray"
        ).pack(anchor="w", pady=(5, 0))
        
        # Separator
        separator = ctk.CTkFrame(dialog, fg_color="#E0E0E0", height=1)
        separator.pack(fill="x", padx=30, pady=10)
        
        # Message content
        content_frame = ctk.CTkFrame(dialog, fg_color="transparent", height=300)
        content_frame.pack(fill="both", expand=True, padx=30, pady=0)
        
        # Use a regular label for shorter messages or a scrollable text widget for longer ones
        message_text = message.get('message', 'No message content')
        
        if len(message_text) > 500:  # For longer messages, use a scrollable text widget
            content = ctk.CTkTextbox(
                content_frame,
                font=("Poppins", 12),
                text_color="#2B2B2B",
                wrap="word",
                height=300,  # Adjust height as needed
                border_width=1,
                border_color="#E0E0E0",
                fg_color="white"
            )
            content.pack(fill="both", expand=True)

            # Insert content and disable editing if needed
            content.insert("1.0", message_text)
            content.configure(state="disabled")  # Optional: Disable editing
        else:  # For shorter messages, use a label
            content = ctk.CTkLabel(
                content_frame,
                text=message_text,
                font=("Poppins", 12),
                text_color="#2B2B2B",
                justify="left",
                wraplength=540,
                anchor="nw"
            )
            content.pack(fill="both", expand=True, padx=0, pady=10)
        
        # Buttons
        button_frame = ctk.CTkFrame(dialog, fg_color="transparent", height=60)
        button_frame.pack(fill="x", padx=30, pady=20)
        
        # Action buttons based on message type
        if not message.get('is_reply'):
            if message.get('status') == 'unread':
                ctk.CTkButton(
                    button_frame,
                    text="Mark as Read",
                    font=("Poppins", 12),
                    fg_color="#4CAF50",
                    hover_color="#45a049",
                    text_color="white",
                    width=100,
                    command=lambda: self.mark_as_read(message['id'], dialog)
                ).pack(side="left")
            
            ctk.CTkButton(
                button_frame,
                text="Reply",
                font=("Poppins", 12),
                fg_color="#F1D94B",
                text_color="black",
                hover_color="#E5CE45",
                width=100,
                command=lambda: self.show_reply_dialog(message, dialog)
            ).pack(side="right")
            
            ctk.CTkButton(
                button_frame,
                text="Delete",
                font=("Poppins", 12),
                fg_color="#FF6B6B",
                hover_color="#FF5252",
                text_color="white",
                width=100,
                command=lambda: self.delete_message(message['id'], dialog)
            ).pack(side="right", padx=10)
            
            ctk.CTkButton(
                button_frame,
                text="Cancel",
                font=("Poppins", 12),
                fg_color="#E0E0E0",
                text_color="black",
                hover_color="#D0D0D0",
                width=100,
                command=self.dialog.destroy
            ).pack(side="right", padx=10)
        
        elif self.current_folder.get() == "trash":
            ctk.CTkButton(
                button_frame,
                text="Restore",
                font=("Poppins", 12),
                fg_color="#4CAF50",
                hover_color="#45a049",
                text_color="white",
                width=100,
                command=lambda: self.restore_message(message['id'], dialog)
            ).pack(side="right")
        
        ctk.CTkButton(
            button_frame,
            text="Cancel",
            font=("Poppins", 12),
            fg_color="#E0E0E0",
            text_color="black",
            hover_color="#D0D0D0",
            width=100,
            command=self.dialog.destroy
        ).pack(side="right", padx=10)
    
    def show_compose_dialog(self):
        dialog = self.create_dialog("Compose New Mail")
        
        # HEADER SECTION
        header_frame = ctk.CTkFrame(dialog, fg_color="white", height=100)
        header_frame.pack(fill="x", padx=20, pady=10)
        header_frame.pack_propagate(False)
        
        ctk.CTkLabel(
            header_frame,
            text="Compose New Mail",
            font=("Poppins", 18, "bold"),
            text_color="#2B2B2B"
        ).pack(anchor="w", padx=10, pady=5)
        
        # Form fields
        fields_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        fields_frame.pack(fill="x", padx=10, pady=5)
        
        # To field
        to_frame = ctk.CTkFrame(fields_frame, fg_color="transparent")
        to_frame.pack(fill="x", pady=2)
        
        ctk.CTkLabel(
            to_frame,
            text="To:",
            font=("Poppins", 12, "bold"),
            text_color="#2B2B2B",
            width=50
        ).pack(side="left")
        
        to_entry = ctk.CTkEntry(
            to_frame,
            font=("Poppins", 12),
            placeholder_text="Enter recipient email"
        )
        to_entry.pack(side="left", fill="x", expand=True)
        
        # BODY SECTION
        body_frame = ctk.CTkFrame(dialog, fg_color="white")
        body_frame.pack(fill="both", expand=True, padx=20, pady=5)
        
        # Message text box
        message_text = ctk.CTkTextbox(
            body_frame,
            font=("Poppins", 12),
            wrap="word",
            border_width=1,
            border_color="#E0E0E0",
            fg_color="white"
        )
        message_text.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Add signature
        signature = f"\n\nBest regards,\n{self.email_config['restaurant_name']} Support Team"
        message_text.insert("1.0", signature)
        message_text.mark_set("insert", "1.0")
        
        # FOOTER SECTION
        footer_frame = ctk.CTkFrame(dialog, fg_color="white", height=80)
        footer_frame.pack(fill="x", padx=20, pady=10)
        footer_frame.pack_propagate(False)
        
        buttons_frame = ctk.CTkFrame(footer_frame, fg_color="transparent")
        buttons_frame.pack(side="right", padx=10, pady=20, anchor="e")
        
        ctk.CTkButton(
            buttons_frame,
            text="Cancel",
            font=("Poppins", 12),
            fg_color="#E0E0E0",
            text_color="black",
            hover_color="#D0D0D0",
            width=100,
            command=dialog.destroy
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            buttons_frame,
            text="Send",
            font=("Poppins", 12),
            fg_color="#F1D94B",
            text_color="black",
            hover_color="#E5CE45",
            width=100,
            command=lambda: self.send_email(
                to_entry.get(),
                "Subject",  # Add subject field if needed
                message_text.get("1.0", "end-1c"),
                dialog
            )
        ).pack(side="left", padx=5)
    
    def show_reply_dialog(self, original_message, parent_dialog):
        parent_dialog.destroy()
        
        dialog = self.create_dialog("Reply to Message")
        
        # HEADER SECTION
        header_frame = ctk.CTkFrame(dialog, fg_color="white", height=100)
        header_frame.pack(fill="x", padx=20, pady=10)
        header_frame.pack_propagate(False)
        
        # Dialog title
        recipient_name = original_message['name']
        ctk.CTkLabel(
            header_frame,
            text=f"Reply to Message: {recipient_name}",
            font=("Poppins", 18, "bold"),
            text_color="#2B2B2B"
        ).pack(anchor="w", padx=10, pady=5)
        
        # To field
        to_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        to_frame.pack(fill="x", padx=10, pady=2)
        
        ctk.CTkLabel(
            to_frame,
            text="To:",
            font=("Poppins", 12, "bold"),
            text_color="#2B2B2B",
            width=50
        ).pack(side="left")
        
        ctk.CTkLabel(
            to_frame,
            text=original_message['email'],
            font=("Poppins", 12),
            text_color="#2B2B2B"
        ).pack(side="left")
        
        # BODY SECTION
        body_frame = ctk.CTkFrame(dialog, fg_color="white")
        body_frame.pack(fill="both", expand=True, padx=20, pady=5)
        
        # Message text box
        message_text = ctk.CTkTextbox(
            body_frame,
            font=("Poppins", 12),
            wrap="word",
            border_width=1,
            border_color="#E0E0E0",
            fg_color="white"
        )
        message_text.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Add reply template
        reply_body = f"Dear {original_message['name']},\n\n\n\n"
        reply_body += f"\n\nBest regards,\n{self.email_config['restaurant_name']} Support Team"
        message_text.insert("1.0", reply_body)
        message_text.mark_set("insert", "3.0")
        message_text.focus_set()
        
        # FOOTER SECTION
        footer_frame = ctk.CTkFrame(dialog, fg_color="white", height=80)
        footer_frame.pack(fill="x", padx=20, pady=10)
        footer_frame.pack_propagate(False)
        
        buttons_frame = ctk.CTkFrame(footer_frame, fg_color="transparent")
        buttons_frame.pack(side="right", padx=10, pady=20, anchor="e")
        
        ctk.CTkButton(
            buttons_frame,
            text="Cancel",
            font=("Poppins", 12),
            fg_color="#E0E0E0",
            text_color="black",
            hover_color="#D0D0D0",
            width=100,
            command=dialog.destroy
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            buttons_frame,
            text="Send",
            font=("Poppins", 12),
            fg_color="#F1D94B",
            text_color="black",
            hover_color="#E5CE45",
            width=100,
            command=lambda: self.send_reply(
                original_message['id'],
                original_message['email'],
                message_text.get("1.0", "end-1c"),
                dialog
            )
        ).pack(side="left", padx=5)
    
    # =============================================
    # EMAIL FUNCTIONS
    # =============================================
    def format_email_signature(self, raw=False):
        """Format email signature with actual values"""
        return f"\n\nBest regards,\n{self.email_config['restaurant_name']} Support Team"
    
    def send_email(self, to_email, subject, message_text, dialog):
        try:
            if not to_email:
                messagebox.showerror("Error", "Please enter a recipient email address")
                return
                
            if not subject:
                messagebox.showerror("Error", "Please enter a subject")
                return
            
            # Save to database
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO contact_messages 
                (name, email, message, status, is_reply, created_at) 
                VALUES (%s, %s, %s, 'read', 1, NOW())
            """, (
                self.email_config['restaurant_name'],
                to_email,
                message_text
            ))
            
            conn.commit()
            
            # Try to send email if credentials exist
            if all([self.email_config['smtp_username'], self.email_config['smtp_password']]):
                msg = MIMEMultipart()
                msg['From'] = f"{self.email_config['restaurant_name']} <{self.email_config['from_email']}>"
                msg['To'] = to_email
                msg['Subject'] = subject
                
                msg.attach(MIMEText(message_text, 'plain'))
                
                with smtplib.SMTP(self.email_config['smtp_server'], self.email_config['smtp_port']) as server:
                    server.starttls()
                    server.login(self.email_config['smtp_username'], self.email_config['smtp_password'])
                    server.send_message(msg)
            
            dialog.destroy()
            messagebox.showinfo("Success", "Message sent successfully")
            self.load_messages()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to send message: {str(e)}")
        finally:
            if 'conn' in locals() and conn.is_connected():
                cursor.close()
                conn.close()
    
    def send_reply(self, original_id, to_email, message_text, dialog, attachments=None):
        try:
            # Save to database
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor()
            
            # Save reply in contact_messages
            cursor.execute("""
                INSERT INTO contact_messages 
                (name, email, message, status, parent_id, is_reply, created_at) 
                VALUES (%s, %s, %s, 'read', %s, 1, NOW())
            """, (
                self.email_config['restaurant_name'],
                self.email_config['from_email'],
                message_text,
                original_id
            ))
            
            # Get the newly inserted message ID for attachments
            message_id = cursor.lastrowid
            
            # Handle attachments if any
            if attachments and len(attachments) > 0:
                for file_path in attachments:
                    # Get file name from path
                    file_name = os.path.basename(file_path)
                    
                    # Read file content
                    with open(file_path, 'rb') as file:
                        file_content = file.read()
                    
                    # Save attachment to database
                    cursor.execute("""
                        INSERT INTO message_attachments 
                        (message_id, file_name, file_content, created_at) 
                        VALUES (%s, %s, %s, NOW())
                    """, (
                        message_id,
                        file_name,
                        file_content
                    ))
            
            # Update original message status
            cursor.execute("""
                UPDATE contact_messages 
                SET status = 'read' 
                WHERE id = %s
            """, (original_id,))
            
            conn.commit()
            
            # Try to send email if credentials exist
            if all([self.email_config['smtp_username'], self.email_config['smtp_password']]):
                msg = MIMEMultipart()
                msg['From'] = f"{self.email_config['restaurant_name']} <{self.email_config['from_email']}>"
                msg['To'] = to_email
                msg['Subject'] = "Re: Contact Form Submission"
                
                # Attach the message text
                msg.attach(MIMEText(message_text, 'plain'))
                
                # Attach files if any
                if attachments and len(attachments) > 0:
                    for file_path in attachments:
                        with open(file_path, 'rb') as file:
                            # Determine content type based on file extension
                            file_name = os.path.basename(file_path)
                            content_type = 'application/octet-stream'  # Default
                            
                            if file_name.lower().endswith(('.jpg', '.jpeg')):
                                content_type = 'image/jpeg'
                            elif file_name.lower().endswith('.png'):
                                content_type = 'image/png'
                            elif file_name.lower().endswith('.pdf'):
                                content_type = 'application/pdf'
                            elif file_name.lower().endswith(('.doc', '.docx')):
                                content_type = 'application/msword'
                            
                            # Create attachment
                            part = MIMEBase('application', 'octet-stream')
                            part.set_payload(file.read())
                            encoders.encode_base64(part)
                            part.add_header(
                                'Content-Disposition',
                                f'attachment; filename="{file_name}"'
                            )
                            part.add_header(
                                'Content-Type', 
                                content_type
                            )
                            msg.attach(part)
                
                with smtplib.SMTP(self.email_config['smtp_server'], self.email_config['smtp_port']) as server:
                    server.starttls()
                    server.login(self.email_config['smtp_username'], self.email_config['smtp_password'])
                    server.send_message(msg)
        
            dialog.destroy()
            messagebox.showinfo("Success", "Reply sent successfully")
            self.load_messages()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to send reply: {str(e)}")
        finally:
            if 'conn' in locals() and conn.is_connected():
                cursor.close()
                conn.close()
    
     # =============================================
    # MESSAGE MANAGEMENT FUNCTIONS
    # =============================================
    def mark_as_read(self, message_id, dialog):
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor()
            
            cursor.execute("""
                UPDATE contact_messages 
                SET status = 'read' 
                WHERE id = %s
            """, (message_id,))
            
            conn.commit()
            dialog.destroy()
            self.load_messages()
            
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Failed to mark message as read: {err}")
        finally:
            if 'conn' in locals() and conn.is_connected():
                cursor.close()
                conn.close()
                
    def delete_message(self, message_id, dialog):
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to move this message to trash?"):
            try:
                conn = mysql.connector.connect(**DB_CONFIG)
                cursor = conn.cursor()
                
                cursor.execute("""
                    UPDATE contact_messages 
                    SET status = 'read' 
                    WHERE id = %s
                """, (message_id,))
                
                conn.commit()
                dialog.destroy()
                self.load_messages()
                
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Failed to delete message: {err}")
            finally:
                if 'conn' in locals() and conn.is_connected():
                    cursor.close()
                    conn.close()
                    
    def restore_message(self, message_id, dialog):
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor()
            
            cursor.execute("""
                UPDATE contact_messages 
                SET status = 'unread' 
                WHERE id = %s
            """, (message_id,))
            
            conn.commit()
            dialog.destroy()
            self.load_messages()
            
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Failed to restore message: {err}")
        finally:
            if 'conn' in locals() and conn.is_connected():
                cursor.close()
                conn.close()
    
    def create_dialog(self, title, width=600, height=500):
        dialog = ctk.CTkToplevel(self)
        dialog.title(title)
        dialog.geometry(f"{width}x{height}")
        dialog.resizable(False, False)
        dialog.grab_set()

        # Center dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() - width) // 2
        y = (dialog.winfo_screenheight() - height) // 2
        dialog.geometry(f"{width}x{height}+{x}+{y}")
        dialog.configure(fg_color="white")

        return dialog