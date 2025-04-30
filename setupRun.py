import os
import sys
import subprocess

def install_package(package_name):
    """Install a package using pip and print status"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
        print(f"✓ Installed {package_name}")
    except subprocess.CalledProcessError:
        print(f"✗ Failed to install {package_name}")

print("Setting up Ice'nSpice Restaurant dependencies...")

# Upgrade pip first
print("\nUpgrading pip to latest version...")
subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
print("✓ Pip upgraded successfully")

# List of required packages with versions
packages = [
    "customtkinter==5.2.2",
    "pillow==10.2.0",
    "mysql-connector-python==8.3.0",
    "python-dotenv==1.0.1",
    "numpy==1.26.4",
    "pandas==2.2.1",
    "matplotlib==3.8.3",
    "seaborn==0.13.2",
    "tkcalendar==1.6.1",
    "bcrypt==4.1.2",
    "watchdog==3.0.0",
    "openpyxl==3.1.2",
    "reportlab==4.1.0",
    "scipy==1.12.0"
]

print("\nInstalling required packages...")
for package in packages:
    install_package(package)

print("\n✓ All packages installed successfully!")
print("You can now run the application using 'python start.py'")


