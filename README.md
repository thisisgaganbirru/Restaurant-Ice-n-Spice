# Ice & Spice Restaurant Management System

## About
Ice & Spice Restaurant Management System is a comprehensive solution for managing restaurant operations. Built with Python and CustomTkinter, it provides separate interfaces for customers and administrators, handling everything from menu browsing to order management and analytics.

## Contributors
- [GAGANSAI BIRRU](https://github.com/thisisgaganbirru)
- [Other Contributors]

## Features
### Authentication System
- Welcome page with getting started flow
- User login with role-based access
- New user registration
- Password recovery system
    - Email verification
    - Security question verification
    - Password reset functionality

### Welcome Page
![Welcome Page](documentation/screenshots/1_welcome_page.png)
- Initial landing page
- Get Started button to begin

### Login System
![Login Page](documentation/screenshots/2_login_page.png)
- User authentication
- Role-based access (Customer/Admin)
![Password Recovery step1](documentation/screenshots/4_forgot_password.png)
(![Password Recovery step2](documentation/screenshots/5-forgot_password.png))
- Forgot password recovery:
    1. Email verification
    2. Security validation
    3. New password setup
    4. Automatic login after reset

### Customer Features
- Browse restaurant menu 
![Customer Menu](documentation/screenshots/customer_menu_page.png)

- Place and customize orders
![Place order](documentation/screenshots/customer_order_page.png)

- Track order status
![Track Order](documentation/screenshots/customer_ordertracking_page.png)

### About Us
![About Page](documentation/screenshots/customer_about.png)
- Restaurant history and vision
- Team information
- Location details
- Operating hours
- Special events and announcements

### Contact Support
![Contact Page](documentation/screenshots/customer_contact_page.png)
- Direct message support
- Support ticket creation
- Track support requests
- View previous communications

### Account Management
![Account Profile](documentation/screenshots/customer_account_page.png)
- Personal Profile Management

    - Edit profile information
    - Update contact details
    ![Edit_profile](documentation/screenshots/customer_account_profile_edit_details_page.png)

    
    - Change password
    ![Change Password](documentation/screenshots/customer_account_profile_change_password_page.png)

    ### Order History
    ![Order History](documentation/screenshots/customer_orderhistory_page.png)
    - View all previous orders
    - Filter by date range
    - Order details and status
    - Reorder functionality

    ### Support Request History
    ![Support History](documentation/screenshots/customer_account_requests_page.png)
    - View all support tickets
    - Track ticket status
    - Response history
    - Follow-up options


### Admin Features
- Menu management
![Admin Menu Dashboard](documentation/screenshots/admin_dashboard.png)


- Order management
![Admin Orders Dashboard](documentation/screenshots/admin_order_page.png)

- Customer management
![Admin Customer Dashboard](documentation/screenshots/admin_customer_page.png)

- Reports and analytics
![Admin Reports Dashboard](documentation/screenshots/admin_reports_page.png)

- Support ticket system
![Admin Support Inbox Dashboard](documentation/screenshots/admin_support_inbox_page.png)
![Admin Support Sent Dashboard](documentation/screenshots/admin_support_sent_page.png)
![Admin Support Trash Dasboard](documentation/screenshots/admin_support_trash_page.png)



## Installation & Setup

1. Clone the repository:
```bash
git clone https://github.com/thisisgaganbirru/Restaurant-Ice-n-Spice.git
cd IcenSpice_Restaurant
```

2. Create and activate virtual environment:
```bash
python -m venv venv
.\venv\Scripts\activate
```

3. Run the setup script to install dependencies:
```bash
python setupRun.py
```
   Or manually install using requirements:
```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

4. Set up the MySQL database using the provided schema

5. Run the application:
```bash
python start.py
```

## Technologies Used
- Python 3.10+
- CustomTkinter for GUI
- MySQL Database
- Pillow for image processing
- Watchdog for development auto-reload

## Project Structure
```
IcenSpice_Restaurant/
├── images/
├── documentation/
│   └── screenshots/
├── *.py (Application source files)
├── requirements.txt
├── .gitignore
└── README.md
```


## Screenshots
Here are some key features of the application:

## Application Interfaces

### Customer Interface
| Feature | Screenshot | Description |
|---------|------------|-------------|
| Menu Browsing | ![Menu](documentation/screenshots/customer_menu_page.png) | - Browse full menu<br>- View item details<br>- Check prices |
| Order Management | ![Order](documentation/screenshots/customer_order_page.png) | - Place new orders<br>- Customize items<br>- Add to cart |
| Order Tracking | ![Tracking](documentation/screenshots/customer_ordertracking_page.png) | - Real-time status<br>- Delivery estimates<br>- Order details |
| Account Profile | ![Profile](documentation/screenshots/customer_account_page.png) | - Personal details<br>- Edit profile<br>- Security settings |
| Order History | ![History](documentation/screenshots/customer_orderhistory_page.png) | - Past orders<br>- Filter by date<br>- Reorder option |
| Support System | ![Support](documentation/screenshots/customer_account_requests_page.png) | - Create tickets<br>- Track status<br>- View responses |
| About Us | ![About](documentation/screenshots/customer_about.png) | - Restaurant info<br>- Location details<br>- Operating hours |
| Contact | ![Contact](documentation/screenshots/customer_contact_page.png) | - Support requests<br>- Direct messaging<br>- Feedback |

### Admin Interface
| Feature | Screenshot | Description |
|---------|------------|-------------|
| Dashboard | ![Dashboard](documentation/screenshots/admin_dashboard.png) | - Overview stats<br>- Quick actions<br>- Recent activity |
| Orders | ![Orders](documentation/screenshots/admin_order_page.png) | - Order management<br>- Status updates<br>- Order details |
| Menu | ![Menu](documentation/screenshots/admin_menu_page.png) | - Item management<br>- Price updates<br>- Category control |
| Customers | ![Customers](documentation/screenshots/admin_customer_page.png) | - Customer database<br>- Profile management<br>- Order history |
| Reports | ![Reports](documentation/screenshots/admin_reports_page.png) | - Sales analytics<br>- Customer insights<br>- Performance metrics |
| Support | ![Support](documentation/screenshots/admin_support_inbox_page.png) | - Ticket management<br>- Customer communication<br>- Response tracking |


## Version Control
### .gitignore Configuration
The project includes a `.gitignore` file to exclude unnecessary files:
```
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment
venv/
ENV/

# IDE
.vscode/
.idea/
*.swp
*.swo

# Environment Variables
.env

# Database
*.sqlite3
*.db

# Logs
*.log
logs/

# Media
media/
uploads/

# Local development
local_settings.py
db.sqlite3
db.sqlite3-journal

# Distribution
*.spec
```

This configuration helps maintain a clean repository by excluding:
- Compiled Python files
- Virtual environments
- IDE settings
- Environment variables
- Database files
- Log files
- Media uploads
- Local development files
