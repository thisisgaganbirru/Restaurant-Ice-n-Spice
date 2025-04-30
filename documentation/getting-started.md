# Getting Started

## System Requirements
- Python 3.10 or higher
- MySQL 8.0 or higher
- Windows 10/11 operating system
- Minimum 4GB RAM
- 500MB free disk space

## Installation Process
1. Clone the repository:
```bash
git clone https://github.com/thisisgaganbirru/Restaurant-Ice-n-Spice.git
cd IcenSpice_Restaurant
```

2. Create virtual environment:
```bash
python -m venv venv
.\venv\Scripts\activate
```

3. Run setup script:
```bash
python setupRun.py
```

## Database Setup
1. Install MySQL Server
2. Create new database:
```sql
CREATE DATABASE icenspice_db;
```
3. Import schema:
```bash
mysql -u your_username -p icenspice_db < schema.sql
```

## Configuration
1. Create .env file:
```env
DB_HOST=localhost
DB_USER=your_username
DB_PASSWORD=your_password
DB_NAME=icenspice_db
```

## Quick Start Guide
1. Start the application:
```bash
python start.py
```
2. Default admin credentials:
   - Username: admin
   - Password: admin@123