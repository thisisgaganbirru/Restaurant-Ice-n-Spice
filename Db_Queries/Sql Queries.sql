use BIS698M1530_GRP14;

-- Create Order Table
CREATE TABLE `Order` (
    OrderID INT PRIMARY KEY,
    UserID INT NOT NULL,
    MenuID INT NOT NULL,
    UserName VARCHAR(255), -- Denormalized for reporting
    Item_list TEXT,
    Total_price DECIMAL(10,2) NOT NULL,
    Status VARCHAR(50),
    CreatedAT DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (UserID) REFERENCES User(userID) ON DELETE CASCADE,
    FOREIGN KEY (MenuID) REFERENCES Menu(MenuID) ON DELETE CASCADE
);

INSERT INTO Menu (name, description, price, imagePath, category) VALUES 
('Biryani  Dum Chicken', 'Tasty Biryani  Dum Chicken from our Biryani selection', 8.0, 'images/Biryani/Biryani/Biryani  Dum Chicken.jpg', 'Biryani'),
('Biryani 4 Types', 'Tasty Biryani 4 Types from our Biryani selection', 8.0, 'images/Biryani/Biryani/Biryani 4 Types.jpeg', 'Biryani'),
('Biryani Chicken', 'Tasty Biryani Chicken from our Biryani selection', 8.0, 'images/Biryani/Biryani/Biryani Chicken.jpg', 'Biryani'),
('Biryani Combo', 'Tasty Biryani Combo from our Biryani selection', 8.0, 'images/Biryani/Biryani/Biryani Combo.jpeg', 'Biryani'),
('biryani Mutton', 'Tasty biryani Mutton from our Biryani selection', 8.0, 'images/Biryani/Biryani/biryani Mutton.jpg', 'Biryani'),
('Biryani Prawns', 'Tasty Biryani Prawns from our Biryani selection', 8.0, 'images/Biryani/Biryani/Biryani Prawns.jpeg', 'Biryani'),
('Biryani Veg', 'Tasty Biryani Veg from our Biryani selection', 8.0, 'images/Biryani/Biryani/Biryani Veg.jpg', 'Biryani');

INSERT INTO Menu (Name, Description, Price, ImagePath, Category) VALUES
('Bbq Chicken', 'Tasty Bbq Chicken from our Pizza selection', 9.00, 'images/Pizza/bbq chicken.jpg', 'Pizza'),
('Bbq-Chicken-Bacon', 'Tasty Bbq-Chicken-Bacon from our Pizza selection', 9.00, 'images/Pizza/bbq-chicken-bacon.jpg', 'Pizza'),
('Cheesy-Spicy-Delight', 'Tasty Cheesy-Spicy-Delight from our Pizza selection', 9.00, 'images/Pizza/cheesy-spicy-delight.jpg', 'Pizza'),
('Kadhai-Paneer', 'Tasty Kadhai-Paneer from our Pizza selection', 7.00, 'images/Pizza/kadhai-paneer.jpg', 'Pizza'),
('Original-Crust-Cheese', 'Tasty Original-Crust-Cheese from our Pizza selection', 7.00, 'images/Pizza/Original-Crust-Cheese.jpg', 'Pizza'),
('Original-Crust-Pepperoni', 'Tasty Original-Crust-Pepperoni from our Pizza selection', 7.00, 'images/Pizza/Original-Crust-Pepperoni.jpg', 'Pizza'),
('Pizza', 'Tasty Pizza from our Pizza selection', 9.00, 'images/Pizza/pizza.jpg', 'Pizza'),
('Royal-Spice-Paneer', 'Tasty Royal-Spice-Paneer from our Pizza selection', 14.00, 'images/Pizza/Royal-Spice-Paneer.jpg', 'Pizza');

-- Create Menu Table
CREATE TABLE Menu (
    MenuID INT PRIMARY KEY,
    Name VARCHAR(255) NOT NULL,
    Description TEXT,
    Price DECIMAL(10,2) NOT NULL,
    ImagePath VARCHAR(255),
    Category VARCHAR(100)
);

-- Create User Table
CREATE TABLE User (
    userID INT PRIMARY KEY,
    UserName VARCHAR(255) UNIQUE NOT NULL,
    Email VARCHAR(255) UNIQUE NOT NULL,
    PhoneNumber VARCHAR(20),
    Address TEXT
);

use BIS698M1530_GRP14;
-- Create User_roles Table (1:M Relationship with User)
CREATE TABLE User_roles (
    RollID INT PRIMARY KEY,
    userID INT NOT NULL,
    Role ENUM('Customer', 'Admin') NOT NULL,
    FOREIGN KEY (userID) REFERENCES User(userID) ON DELETE CASCADE
);