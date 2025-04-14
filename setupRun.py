print("Installing required packages for Ice'nSpice Restaurant...")

import os
os.system("pip3 install customtkinter")
print("✓ Installed customtkinter")

os.system("pip3 install pillow")
print("✓ Installed pillow (PIL)")

os.system("pip3 install mysql-connector-python")
print("✓ Installed mysql-connector")

os.system("pip3 install matplotlib")
print("✓ Installed matplotlib")

os.system("pip3 install tkcalendar")
print("✓ Installed tkcalendar")

os.system("pip3 install bcrypt")
print("✓ Installed bcrypt")

os.system("pip3 install watchdog")
print("✓ Installed watchdog")


print("\nAll packages installed successfully!")
print("You can now run the application using 'python start.py'")


