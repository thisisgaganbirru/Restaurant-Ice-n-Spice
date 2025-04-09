import customtkinter as ctk
from utils import resize_image
from headerNav import NavigationHeader
from decimal import Decimal
import mysql.connector
from dbconnection import DB_CONFIG

class OrderPage(ctk.CTkFrame):
    def __init__(self, parent, app, user, cart):
        super().__init__(parent)
        self.app = app
        self.user = user
        self.cart = cart
        self.configure(width=600, height=700, fg_color="transparent")
        
        
        self.create_header()
        self.create_order_body()

    def create_header(self):
        NavigationHeader(self, app=self.app).pack(side="top", fill="x")

    def create_order_body(self):
        body_frame = ctk.CTkFrame(self, fg_color="transparent")
        body_frame.pack(fill="both", expand=True)

        self.bg_image = resize_image((800, 800), "images/backg.jpg")
        bg_label = ctk.CTkLabel(body_frame, image=self.bg_image, text="")
        bg_label.pack(fill="both", expand=True)

        content_frame = ctk.CTkFrame(body_frame, width=500, height=600, fg_color="#F9F0E5", corner_radius=10)
        content_frame.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(content_frame, text="Your Cart", font=("Poppins", 20, "bold"), text_color="black").pack(pady=(10, 0))

        self.cart_frame = ctk.CTkScrollableFrame(content_frame, fg_color="white", width=450, height=200)
        self.cart_frame.pack(pady=(0, 0), padx=10)
        self.load_cart_items()

        self.summary_frame = ctk.CTkFrame(content_frame, width=450, height=200, fg_color="white")
        self.summary_frame.pack(padx=10, pady=0)
        self.summary_frame.pack_propagate(False)
        self.create_summary(self.summary_frame)
        

    def load_cart_items(self):
        for widget in self.cart_frame.winfo_children():
            widget.destroy()

        for item_id, details in self.cart.items():
            self.create_food_card(item_id, details)


    def create_food_card(self,item_id, details):
        

        card = ctk.CTkFrame(
                self.cart_frame,
                fg_color="transparent",
                border_width=2,
                border_color="#F1D94B",
                width=400,
                height=200,
                corner_radius=10
            )
        card.pack(pady=(5, 0), padx=5, fill="x")
        card.pack_propagate(False) 

        cardimage_frame = ctk.CTkFrame(card, fg_color="white")
        cardimage_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        cardimage_frame.pack_propagate(False) 

        try:
            # print("Trying image:", item["image"])
            
            menu_img = resize_image((200,200),details["imagePath"])
            self.image_refs.append(menu_img)
            ctk.CTkLabel(cardimage_frame, image=menu_img, text="").pack(side="left",padx=10, pady=10)
        except Exception as e:
            print("Image Error:", e)
            menu_img = None
            ctk.CTkLabel(cardimage_frame, text="Image not found", font=("poppins", 10, "italic")).pack(padx=10)

        carddetail_frame = ctk.CTkFrame(card, fg_color="white")
        carddetail_frame.pack(side="left", fill="both", expand=True, padx=2, pady=10)
        carddetail_frame.pack_propagate(False) 
        
        
        ctk.CTkLabel(carddetail_frame, text=details["name"], font=("Poppins", 14, "bold"), text_color="black").pack(anchor="w")
        ctk.CTkLabel(carddetail_frame, text=details.get("description", ""), font=("Poppins", 10), text_color="gray").pack(anchor="w")
        ctk.CTkLabel(carddetail_frame, text=f"${details['price']} × {details['quantity']}", font=("Poppins", 12), text_color="#E53935").pack(anchor="w", pady=(5, 5))

        ctk.CTkButton(carddetail_frame, text="Remove", fg_color="#D9534F", text_color="white",
                        width=100, height=25, corner_radius=8,
                        command=lambda: self.remove_item(item_id)).pack(anchor="w")
        
        
        
        
        
        # # Name
        # ctk.CTkLabel(
        #         carddetail_frame, text=item["name"],
        #         font=("Inter", 16, "bold"), text_color="black", wraplength=120,anchor="w", justify="left"
        #     ).pack(anchor="w", fill="x")

        # # Description
        # ctk.CTkLabel(
        #         carddetail_frame, text=item["description"][:80] + "...",
        #         font=("Inter", 10), text_color="gray",
        #         wraplength=200, anchor="w", justify="left"
        #     ).pack(anchor="w", fill="x", pady=(2, 5))

        # # Price
        # ctk.CTkLabel(
        #         carddetail_frame, text=f"$ {item['price']}",
        #         font=("Inter", 16), text_color="black",anchor="w", justify="left"
        #     ).pack(anchor="w",  fill="x",pady=(0, 15))

        # # Add to Cart Button
        # ctk.CTkButton(
        #         carddetail_frame, text="Add to Cart",
        #         fg_color="#F1D94B", text_color="black",width=150,
        #         command=lambda: self.update_cart(item, 1, None)
        #     ).pack(anchor="w", pady=(10, 5))



    # def create_cart_card(self, item_id, details):
        
    #     card = ctk.CTkFrame(
    #             self.cart_frame,
    #             fg_color="transparent",
    #             border_width=2,
    #             border_color="#F1D94B",
    #             width=400,
    #             height=200,
    #             corner_radius=10
    #         )
    #     card.pack(side="left", padx=10, pady=10)
    #     card.pack_propagate(False) 

    #     cartimage_frame = ctk.CTkFrame(card, fg_color="white")
    #     cartimage_frame.pack(side="left", fill="both", expand=True, padx=5, pady=5)
    #     cartimage_frame.pack_propagate(False) 

    #     try:
    #         # print("Trying image:", item["image"])
            
    #         cart_img = resize_image((200,200),details["imagePath"])
    #         self.image_refs.append(cart_img)
    #         ctk.CTkLabel(cartimage_frame, image=cart_img, text="").pack(side="left",padx=5, pady=5)
    #     except Exception as e:
    #         print("Image Error:", e)
    #         cart_img = None
    #         ctk.CTkLabel(cartimage_frame, text="Image not found", font=("poppins", 10, "italic")).pack(padx=10)

    #         info_frame = ctk.CTkFrame(card, fg_color="white")
    #         info_frame.place(x=250, y=15)
    #         info_frame.pack_propagate(False) 

    #         ctk.CTkLabel(info_frame, text=details["name"], font=("Poppins", 14, "bold"), text_color="black").pack(anchor="w")
    #         ctk.CTkLabel(info_frame, text=details.get("description", ""), font=("Poppins", 10), text_color="gray").pack(anchor="w")
    #         ctk.CTkLabel(info_frame, text=f"${details['price']} × {details['quantity']}", font=("Poppins", 12), text_color="#E53935").pack(anchor="w", pady=(5, 5))

    #         ctk.CTkButton(info_frame, text="Remove", fg_color="#D9534F", text_color="white",
    #                     width=100, height=25, corner_radius=8,
    #                     command=lambda: self.remove_item(item_id)).pack(anchor="w")

    def remove_item(self, item_id):
        if item_id in self.cart:
            del self.cart[item_id]
            self.load_cart_items()
            self.create_summary(self.cart_frame.master)


    def create_summary(self, parent):
        
        #  to Destroy previous summary_frame
        if hasattr(self, "summary_frame") and self.summary_frame:
            for widget in self.summary_frame.winfo_children():
                widget.destroy()


        subtotal = Decimal("0.00")
        for item in self.cart.values():
            subtotal += Decimal(str(item["price"])) * item["quantity"]

        tax = subtotal * Decimal("0.06")  # 6% tax
        total = subtotal + tax


        self.summary_frame = ctk.CTkFrame(parent, width=450, height=200, fg_color="white")
        self.summary_frame.pack(pady=0)


        ctk.CTkLabel(self.summary_frame, text=f"Sub Total: ${subtotal:.2f}",
                    font=("Poppins", 14), text_color="black").pack(anchor="e", padx=20, pady=(5, 0))

        ctk.CTkLabel(self.summary_frame, text=f"Estimated Taxes (6%): ${tax:.2f}",
                    font=("Poppins", 12), text_color="gray").pack(anchor="e", padx=20)

        ctk.CTkLabel(self.summary_frame, text=f"Total: ${total:.2f}",
                    font=("Poppins", 16, "bold"), text_color="black").pack(anchor="e", pady=5, padx=20)

        ctk.CTkButton(self.summary_frame, text="Order", fg_color="#F1D94B", text_color="black",
                    width=120, command=self.place_order).pack(pady=10)

    def place_order(self):
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor(dictionary=True)
            items_list = ", ".join([f"{item['name']} (x{item['quantity']})" for item in self.cart.values()])
            total_price = sum(item["price"] * item["quantity"] for item in self.cart.values())

            cursor.execute("""
                INSERT INTO orders (user_id, username, items_list, total_price, status)
                VALUES (%s, %s, %s, %s, 'pending')
            """, (self.user["id"], self.user["username"], items_list, total_price))

            conn.commit()
            conn.close()
            self.app.show_frame("CustomerHomePage", user=self.user)

        except mysql.connector.Error as err:
            print(f"Error placing order: {err}")
