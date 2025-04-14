print("Installing required packages for Ice'nSpice Restaurant...")

import os
os.system("pip install customtkinter")
print("✓ Installed customtkinter")

os.system("pip install pillow")
print("✓ Installed pillow (PIL)")

os.system("pip install mysql-connector-python")
print("✓ Installed mysql-connector")

os.system("pip install matplotlib")
print("✓ Installed matplotlib")

os.system("pip install tkcalendar")
print("✓ Installed tkcalendar")

os.system("pip install bcrypt")
print("✓ Installed bcrypt")

print("\nAll packages installed successfully!")
print("You can now run the application using 'python start.py'")


