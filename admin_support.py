import customtkinter as ctk
from admin_nav import AdminNav
from dbconnection import DB_CONFIG
import mysql.connector
from datetime import datetime
from tkinter import messagebox
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv
import logging
import traceback
import uuid
import json
from decimal import Decimal
from typing import Optional, Dict, Any

class AdminSupport(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.configure(fg_color="#F1E8DD")
        self.pack(fill="both", expand=True)
        
        # Initialize logging
        self.setup_logging()
        
        # Load email configuration
        load_dotenv()
        self.setup_email_config()
        
        # Create main container
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.pack(fill="both", expand=True)
        
        # Create layout
        self.create_header()
        self.create_support_body()
        
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
        """Initialize email configuration"""
        self.email_config = {
            'smtp_server': os.getenv('SMTP_SERVER', 'smtp.gmail.com'),
            'smtp_port': int(os.getenv('SMTP_PORT', '587')),
            'smtp_username': os.getenv('SMTP_USERNAME'),
            'smtp_password': os.getenv('SMTP_PASSWORD'),
            'from_email': os.getenv('FROM_EMAIL', 'support@icenspice.com'),
            'restaurant_name': os.getenv('RESTAURANT_NAME', "Ice'n Spice"),
            'support_team': os.getenv('SUPPORT_TEAM_NAME', "Ice'n Spice Support Team"),
            'support_phone': os.getenv('SUPPORT_PHONE', ''),
            'support_email': os.getenv('SUPPORT_EMAIL', ''),
            'support_hours': os.getenv('SUPPORT_HOURS', ''),
            'support_address': os.getenv('SUPPORT_ADDRESS', ''),
            'email_signature': os.getenv('EMAIL_SIGNATURE', ''),
            'templates': {
                'reply': os.getenv('REPLY_TEMPLATE', ''),
                'error': os.getenv('ERROR_TEMPLATE', '')
            }
        }

    def create_header(self):
        # Nav on left
        AdminNav(self.main_container, app=self.app).pack(side="left", fill="y")
        
    def create_support_body(self):
        # Main body frame
        self.body_frame = ctk.CTkFrame(self.main_container, fg_color="#F1E8DD")
        self.body_frame.pack(side="right", fill="both", expand=True)
        
        # Header with title and compose button
        header_frame = ctk.CTkFrame(self.body_frame, fg_color="transparent", height=60)
        header_frame.pack(fill="x", padx=20, pady=10)
        header_frame.pack_propagate(False)
        
        # Title
        ctk.CTkLabel(
            header_frame,
            text="Support",
            font=("Poppins", 24, "bold"),
            text_color="#2B2B2B"
        ).pack(side="left")
        
        # Compose button
        compose_button = ctk.CTkButton(
            header_frame,
            text="Compose New Mail",
            font=("Poppins", 13),
            fg_color="#F1D94B",
            text_color="black",
            hover_color="#E5CE45",
            height=35,
            command=self.show_compose_dialog
        )
        compose_button.pack(side="right")
        
        # Main content area
        content_frame = ctk.CTkFrame(self.body_frame, fg_color="white", corner_radius=15)
        content_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Create two-column layout
        # Left column - Folders
        folders_frame = ctk.CTkFrame(content_frame, fg_color="transparent", width=200)
        folders_frame.pack(side="left", fill="y", padx=0, pady=0)
        folders_frame.pack_propagate(False)
        
        # Folder buttons
        self.current_folder = ctk.StringVar(value="inbox")
        folders = [
            ("Inbox", "inbox", "#F1D94B"),
            ("Sent", "sent", "transparent"),
            ("Trash", "trash", "transparent")
        ]
        
        for text, value, color in folders:
            btn = ctk.CTkButton(
                folders_frame,
                text=text,
                font=("Poppins", 14),
                fg_color=color,
                text_color="black",
                hover_color="#F1E8DD",
                anchor="w",
                height=40,
                command=lambda v=value: self.switch_folder(v)
            )
            btn.pack(fill="x", pady=(0, 1))
            setattr(self, f"{value}_btn", btn)
        
        # Separator line
        separator = ctk.CTkFrame(content_frame, fg_color="#E0E0E0", width=2)
        separator.pack(side="left", fill="y", padx=0, pady=10)
        
        # Right panel - Messages
        messages_panel = ctk.CTkFrame(content_frame, fg_color="transparent")
        messages_panel.pack(side="left", fill="both", expand=True)
        
        # Create scrollable frame with custom styling
        self.messages_frame = ctk.CTkScrollableFrame(
            messages_panel,
            fg_color="transparent",
            scrollbar_fg_color="transparent",  # Make scrollbar background transparent
            scrollbar_button_color="transparent",  # Make scrollbar buttons transparent
            scrollbar_button_hover_color="#F1D94B",  # Yellow on hover
            scrollbar_thickness=8  # Thinner scrollbar
        )
        self.messages_frame.pack(fill="both", expand=True, padx=0, pady=0)
        
        # Configure scrollbar to be transparent when not in use
        scrollbar = self.messages_frame._scrollbar
        scrollbar.configure(width=8)  # Make scrollbar thinner
        
        # Bind hover events to show/hide scrollbar
        def on_enter(e):
            scrollbar.configure(fg_color="#E0E0E0")
        
        def on_leave(e):
            scrollbar.configure(fg_color="transparent")
        
        scrollbar.bind("<Enter>", on_enter)
        scrollbar.bind("<Leave>", on_leave)
        
        # Load initial messages
        self.load_messages()
        
    def switch_folder(self, folder):
        # Update button colors
        for f in ["inbox", "sent", "trash"]:
            btn = getattr(self, f"{f}_btn")
            btn.configure(fg_color="#F1D94B" if f == folder else "transparent")
        
        self.current_folder.set(folder)
        self.load_messages()
        
    def load_messages(self):
        # Clear existing messages
        for widget in self.messages_frame.winfo_children():
            widget.destroy()
            
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor(dictionary=True)
            
            folder = self.current_folder.get()
            
            # Query based on folder
            if folder == "inbox":
                query = """
                    SELECT * FROM contact_messages 
                    WHERE status = 'unread' AND parent_id IS NULL
                    ORDER BY created_at DESC
                """
            elif folder == "sent":
                query = """
                    SELECT * FROM contact_messages 
                    WHERE is_reply = 1
                    ORDER BY created_at DESC
                """
            else:  # trash
                query = """
                    SELECT * FROM contact_messages 
                    WHERE status = 'read' AND parent_id IS NULL
                    ORDER BY created_at DESC
                """
            
            cursor.execute(query)
            messages = cursor.fetchall()
            
            # Create message items
            for message in messages:
                self.create_message_item(message)
                
            conn.close()
            
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Failed to load messages: {err}")
            
    def create_message_item(self, message):
        # Message container
        item = ctk.CTkFrame(self.messages_frame, fg_color="transparent", height=60)
        item.pack(fill="x", pady=(0, 1))
        item.pack_propagate(False)
        
        # Hover effect
        item.bind("<Enter>", lambda e: item.configure(fg_color="#F8F9FA"))
        item.bind("<Leave>", lambda e: item.configure(fg_color="transparent"))
        
        # Message content
        content = ctk.CTkFrame(item, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=15)
        
        # Subject and sender
        header = ctk.CTkFrame(content, fg_color="transparent")
        header.pack(fill="x")
        
        # Format subject based on message type
        if message.get('is_reply') == 1:
            subject = f"Re: Contact Form Message"
        else:
            subject = "Contact Form Message"
            if message.get('status') == 'unread':
                subject = "Imp!!! " + subject
        
        ctk.CTkLabel(
            header,
            text=subject,
            font=("Poppins", 13, "bold" if message.get('status') == 'unread' else "normal"),
            text_color="#2B2B2B"
        ).pack(side="left")
        
        # Sender name and email
        sender_text = f"{message['name']} <{message['email']}>"
        ctk.CTkLabel(
            header,
            text=sender_text,
            font=("Poppins", 11),
            text_color="gray"
        ).pack(side="right")
        
        # Message preview
        preview = message['message'][:60] + "..." if len(message['message']) > 60 else message['message']
        ctk.CTkLabel(
            content,
            text=preview,
            font=("Poppins", 11),
            text_color="gray"
        ).pack(anchor="w", pady=(5, 0))
        
        # Time
        time_text = message['created_at'].strftime("%I:%M %p")
        ctk.CTkLabel(
            content,
            text=time_text,
            font=("Poppins", 10),
            text_color="gray"
        ).pack(anchor="w", pady=(5, 0))
        
        # Click handler
        item.bind("<Button-1>", lambda e: self.show_message_dialog(message))
        
    def show_message_dialog(self, message):
        dialog = ctk.CTkToplevel(self)
        dialog.title("Message Details")
        dialog.geometry("600x500")
        dialog.resizable(False, False)
        
        # Make dialog modal
        dialog.grab_set()
        
        # Center dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() - 600) // 2
        y = (dialog.winfo_screenheight() - 500) // 2
        dialog.geometry(f"600x500+{x}+{y}")
        
        # Configure appearance
        dialog.configure(fg_color="white")
        
        # Message header
        header = ctk.CTkFrame(dialog, fg_color="transparent")
        header.pack(fill="x", padx=30, pady=20)
        
        # From/Subject
        sender_text = f"{message['name']} <{message['email']}>"
        ctk.CTkLabel(
            header,
            text=sender_text,
            font=("Poppins", 18, "bold"),
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
        
        # Message content with custom scrollbar
        content = ctk.CTkTextbox(
            dialog,
            font=("Poppins", 12),
            text_color="#2B2B2B",
            wrap="word",
            height=200,
            scrollbar_fg_color="transparent",
            scrollbar_button_color="transparent",
            scrollbar_button_hover_color="#F1D94B",
            scrollbar_thickness=8
        )
        content.pack(fill="both", expand=True, padx=30, pady=10)
        
        # Configure scrollbar to be transparent when not in use
        scrollbar = content._scrollbar
        scrollbar.configure(width=8)
        
        # Bind hover events to show/hide scrollbar
        def on_enter(e):
            scrollbar.configure(fg_color="#E0E0E0")
        
        def on_leave(e):
            scrollbar.configure(fg_color="transparent")
        
        scrollbar.bind("<Enter>", on_enter)
        scrollbar.bind("<Leave>", on_leave)
        
        content.insert("1.0", message['message'])
        content.configure(state="disabled")
        
        # Buttons frame
        buttons = ctk.CTkFrame(dialog, fg_color="transparent")
        buttons.pack(fill="x", padx=30, pady=20)
        
        # Action buttons based on message type
        if not message.get('is_reply'):
            if message.get('status') == 'unread':
                ctk.CTkButton(
                    buttons,
                    text="Mark as Read",
                    font=("Poppins", 12),
                    fg_color="#4CAF50",
                    hover_color="#45a049",
                    text_color="white",
                    width=100,
                    command=lambda: self.mark_as_read(message['id'], dialog)
                ).pack(side="left")
            
            ctk.CTkButton(
                buttons,
                text="Reply",
                font=("Poppins", 12),
                fg_color="#F1D94B",
                text_color="black",
                hover_color="#E5CE45",
                width=100,
                command=lambda: self.show_reply_dialog(message, dialog)
            ).pack(side="right")
            
            ctk.CTkButton(
                buttons,
                text="Delete",
                font=("Poppins", 12),
                fg_color="#FF6B6B",
                hover_color="#FF5252",
                text_color="white",
                width=100,
                command=lambda: self.delete_message(message['id'], dialog)
            ).pack(side="right", padx=10)
        
        elif self.current_folder.get() == "trash":
            ctk.CTkButton(
                buttons,
                text="Restore",
                font=("Poppins", 12),
                fg_color="#4CAF50",
                hover_color="#45a049",
                text_color="white",
                width=100,
                command=lambda: self.restore_message(message['id'], dialog)
            ).pack(side="right")
        
    def show_compose_dialog(self):
        dialog = ctk.CTkToplevel(self)
        dialog.title("Compose New Mail")
        dialog.geometry("600x500")
        dialog.resizable(False, False)
        
        # Make dialog modal
        dialog.grab_set()
        
        # Center dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() - 600) // 2
        y = (dialog.winfo_screenheight() - 500) // 2
        dialog.geometry(f"600x500+{x}+{y}")
        
        # Configure appearance
        dialog.configure(fg_color="white")
        
        # Title
        ctk.CTkLabel(
            dialog,
            text="Compose New Mail",
            font=("Poppins", 20, "bold"),
            text_color="#2B2B2B"
        ).pack(pady=20)
        
        # Form fields
        fields = ctk.CTkFrame(dialog, fg_color="transparent")
        fields.pack(fill="x", padx=30, pady=10)
        
        # To field
        to_frame = ctk.CTkFrame(fields, fg_color="transparent")
        to_frame.pack(fill="x", pady=5)
        
        ctk.CTkLabel(
            to_frame,
            text="To:",
            font=("Poppins", 12),
            text_color="#2B2B2B",
            width=60
        ).pack(side="left")
        
        to_entry = ctk.CTkEntry(
            to_frame,
            font=("Poppins", 12),
            placeholder_text="Enter recipient email"
        )
        to_entry.pack(side="left", fill="x", expand=True)
        
        # Subject field
        subject_frame = ctk.CTkFrame(fields, fg_color="transparent")
        subject_frame.pack(fill="x", pady=5)
        
        ctk.CTkLabel(
            subject_frame,
            text="Subject:",
            font=("Poppins", 12),
            text_color="#2B2B2B",
            width=60
        ).pack(side="left")
        
        subject_entry = ctk.CTkEntry(
            subject_frame,
            font=("Poppins", 12),
            placeholder_text="Enter subject"
        )
        subject_entry.pack(side="left", fill="x", expand=True)
        
        # Message body
        message_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        message_frame.pack(fill="both", expand=True, padx=30, pady=10)
        
        message_text = ctk.CTkTextbox(
            message_frame,
            font=("Poppins", 12),
            wrap="word"
        )
        message_text.pack(fill="both", expand=True)
        
        # Buttons
        buttons = ctk.CTkFrame(dialog, fg_color="transparent")
        buttons.pack(fill="x", padx=30, pady=20)
        
        ctk.CTkButton(
            buttons,
            text="Cancel",
            font=("Poppins", 12),
            fg_color="#E0E0E0",
            text_color="black",
            hover_color="#D0D0D0",
            width=100,
            command=dialog.destroy
        ).pack(side="left")
        
        ctk.CTkButton(
            buttons,
            text="Send",
            font=("Poppins", 12),
            fg_color="#F1D94B",
            text_color="black",
            hover_color="#E5CE45",
            width=100,
            command=lambda: self.send_email(
                to_entry.get(),
                subject_entry.get(),
                message_text.get("1.0", "end-1c"),
                dialog
            )
        ).pack(side="right")
        
    def show_reply_dialog(self, original_message, parent_dialog):
        parent_dialog.destroy()
        
        dialog = ctk.CTkToplevel(self)
        dialog.title("Reply")
        dialog.geometry("600x500")
        dialog.resizable(False, False)
        
        # Make dialog modal
        dialog.grab_set()
        
        # Center dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() - 600) // 2
        y = (dialog.winfo_screenheight() - 500) // 2
        dialog.geometry(f"600x500+{x}+{y}")
        
        # Configure appearance
        dialog.configure(fg_color="white")
        
        # Title
        ctk.CTkLabel(
            dialog,
            text="Reply",
            font=("Poppins", 20, "bold"),
            text_color="#2B2B2B"
        ).pack(pady=20)
        
        # Original message info
        info_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        info_frame.pack(fill="x", padx=30, pady=10)
        
        ctk.CTkLabel(
            info_frame,
            text=f"To: {original_message['email']}",
            font=("Poppins", 12),
            text_color="gray"
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            info_frame,
            text=f"Subject: Re: {original_message.get('subject', 'Contact Form Submission')}",
            font=("Poppins", 12),
            text_color="gray"
        ).pack(anchor="w", pady=(5, 0))
        
        # Separator
        separator = ctk.CTkFrame(dialog, fg_color="#E0E0E0", height=1)
        separator.pack(fill="x", padx=30, pady=10)
        
        # Reply message
        message_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        message_frame.pack(fill="both", expand=True, padx=30, pady=10)
        
        message_text = ctk.CTkTextbox(
            message_frame,
            font=("Poppins", 12),
            wrap="word"
        )
        message_text.pack(fill="both", expand=True)
        
        # Add quoted original message
        quoted_message = f"\n\nOn {original_message['created_at'].strftime('%B %d, %Y at %I:%M %p')}, {original_message['email']} wrote:\n\n"
        quoted_message += "\n".join(f"> {line}" for line in original_message['message'].split('\n'))
        message_text.insert("1.0", quoted_message)
        
        # Buttons
        buttons = ctk.CTkFrame(dialog, fg_color="transparent")
        buttons.pack(fill="x", padx=30, pady=20)
        
        ctk.CTkButton(
            buttons,
            text="Cancel",
            font=("Poppins", 12),
            fg_color="#E0E0E0",
            text_color="black",
            hover_color="#D0D0D0",
            width=100,
            command=dialog.destroy
        ).pack(side="left")
        
        ctk.CTkButton(
            buttons,
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
        ).pack(side="right")
        
    def send_email(self, to_email, subject, message_text, dialog):
        try:
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
            
            # Send email
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
                
    def send_reply(self, original_id, to_email, message_text, dialog):
        try:
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
            
            # Update original message status
            cursor.execute("""
                UPDATE contact_messages 
                SET status = 'read' 
                WHERE id = %s
            """, (original_id,))
            
            conn.commit()
            
            # Send email
            if all([self.email_config['smtp_username'], self.email_config['smtp_password']]):
                msg = MIMEMultipart()
                msg['From'] = f"{self.email_config['restaurant_name']} <{self.email_config['from_email']}>"
                msg['To'] = to_email
                msg['Subject'] = "Re: Contact Form Submission"
                
                msg.attach(MIMEText(message_text, 'plain'))
                
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