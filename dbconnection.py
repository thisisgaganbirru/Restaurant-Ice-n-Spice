import mysql.connector

#  MySQL Connection Details
DB_CONFIG = {
    "host": "141.209.241.57",    
    "port": 3306,           
    "user": "birru1g",         
    "password": "SQL@9530",     
    "database": "BIS698M1530_GRP14"
}

#  Function to connect to MySQL
def get_db_connection():
    return mysql.connector.connect(DB_CONFIG)

if __name__ == "__main__":
    print(" Database initialized successfully!")
