-- Create database if not exists
CREATE DATABASE IF NOT EXISTS BIS698M1530_GRP14;
USE BIS698M1530_GRP14;

-- Drop existing tables if they exist
DROP TABLE IF EXISTS contact_messages;
DROP TABLE IF EXISTS Order_Items;
DROP TABLE IF EXISTS `Order`;
DROP TABLE IF EXISTS Menu;
DROP TABLE IF EXISTS User_roles;
DROP TABLE IF EXISTS users;

-- Create Users table
CREATE TABLE users (
    userID INT NOT NULL AUTO_INCREMENT,
    first_name VARCHAR(50) DEFAULT NULL,
    last_name VARCHAR(50) DEFAULT NULL,
    username VARCHAR(50) DEFAULT NULL,
    email VARCHAR(100) DEFAULT NULL,
    phone_number VARCHAR(20) DEFAULT NULL,
    address TEXT DEFAULT NULL,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(20) DEFAULT 'customer',
    created_at TIMESTAMP NOT NULL DEFAULT current_timestamp(),
    PRIMARY KEY (userID),
    UNIQUE KEY UserName (username),
    UNIQUE KEY Email (email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Create User_roles table
CREATE TABLE User_roles (
    RollID INT NOT NULL,
    userID INT NOT NULL,
    Role ENUM('Customer','Admin') NOT NULL,
    PRIMARY KEY (RollID),
    KEY User_roles_ibfk_1 (userID),
    CONSTRAINT User_roles_ibfk_1 FOREIGN KEY (userID) 
    REFERENCES users (userID) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Create Menu table
CREATE TABLE Menu (
    MenuID INT NOT NULL AUTO_INCREMENT,
    Name VARCHAR(255) NOT NULL,
    Description TEXT DEFAULT NULL,
    Price DECIMAL(10,2) NOT NULL,
    ImagePath VARCHAR(255) DEFAULT NULL,
    Category VARCHAR(100) DEFAULT NULL,
    Available TINYINT(1) DEFAULT 1,
    PRIMARY KEY (MenuID)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Create Order table
CREATE TABLE `Order` (
    OrderID INT(7) NOT NULL AUTO_INCREMENT,
    UserID INT NOT NULL,
    orderIDByUser INT NOT NULL,
    UserName VARCHAR(255) DEFAULT NULL,
    Item_list TEXT DEFAULT NULL,
    Total_price DECIMAL(10,2) NOT NULL,
    Status VARCHAR(50) DEFAULT NULL,
    CreatedAT DATETIME DEFAULT current_timestamp(),
    orderStatus ENUM('pending','preparing','ready for pickup','delivered') DEFAULT 'pending',
    statusUpdateAt TIMESTAMP NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
    PRIMARY KEY (OrderID),
    KEY Order_ibfk_1 (UserID),
    CONSTRAINT Order_ibfk_1 FOREIGN KEY (UserID) 
    REFERENCES users (userID) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Create contact_messages table
CREATE TABLE contact_messages (
    id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    message TEXT NOT NULL,
    status ENUM('unread','read') DEFAULT 'unread',
    created_at TIMESTAMP NOT NULL DEFAULT current_timestamp(),
    parent_id INT DEFAULT NULL,
    is_reply TINYINT(1) DEFAULT 0,
    PRIMARY KEY (id),
    KEY parent_id (parent_id),
    CONSTRAINT contact_messages_ibfk_1 FOREIGN KEY (parent_id) 
    REFERENCES contact_messages (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Create Order sequence trigger
DELIMITER ;;
CREATE TRIGGER trg_order_seq_by_user
BEFORE INSERT ON `Order`
FOR EACH ROW
BEGIN
    DECLARE last_seq INT;
    SELECT COALESCE(MAX(orderIDByUser),0)
    INTO last_seq
    FROM `Order`
    WHERE UserID = NEW.UserID;
    SET NEW.orderIDByUser = last_seq + 1;
END;;
DELIMITER ;

-- Add indexes for better performance
CREATE INDEX idx_user_role ON users(role);
CREATE INDEX idx_menu_category ON Menu(Category);
CREATE INDEX idx_order_status ON `Order`(orderStatus);
CREATE INDEX idx_contact_status ON contact_messages(status);

-- Insert admin user
INSERT INTO users (first_name, last_name, username, email, phone_number, address, password, role) 
VALUES ('Admin', 'User', 'admin', 'admin@example.com', '9999999999', 'Admin Street', 'admin@123', 'admin');

-- Insert sample menu items
INSERT INTO Menu (Name, Description, Price, ImagePath, Category) VALUES
('BBQ Chicken Pizza', 'Smoky BBQ chicken on a crisp crust with rich cheese.', 8.99, 'images/Pizza/bbq_chicken.jpg', 'Pizza'),
('Chicken Dum Biryani', 'Tasty Chicken Dum Biryani made with Style and Spices', 17.99, 'images/Biryani/chicken_biryani.jpg', 'Biryani');

-- Add more sample data as needed