use BIS698M1530_GRP14;

UPDATE Menu SET
	Name = 'BBQ Chicken Pizza', 
    Description = 'Smoky BBQ chicken on a crisp crust with rich cheese.', 
    Price = 8.99,
	ImagePath = 'images/Pizza/bbq_chicken.jpg'
WHERE MenuID = 1;

UPDATE Menu 
	SET Name = 'BBQ Chicken Bacon Pizza', 
    Description = 'Grilled chicken and bacon topped with tangy BBQ sauce.',
	ImagePath = 'images/Pizza/bbq-chicken-bacon.jpg',
    Price = 9.49 
WHERE MenuID = 2;
UPDATE Menu 
	SET Name = 'Cheesy Spicy Delight', 
    Description = 'A cheesy delight with a kick of spicy flavors.',
	ImagePath = 'images/Pizza/cheesy_spicy_delight.jpg',
    Price = 6.49 
WHERE MenuID = 3;

UPDATE Menu 
	SET Name = 'Kadhai Paneer', 
    Description = 'Indian spiced kadhai paneer on a cheesy base.', 
    ImagePath = 'images/Pizza/kadhai_paneer.jpg',
    Price = 7.99 
WHERE MenuID = 4;

UPDATE Menu 
	SET Name = 'Original Crust Cheese', 
    Description = 'Classic crust layered with rich mozzarella cheese.',
    ImagePath = 'images/Pizza/Original_Crust_Cheese.jpg',
    Price = 7.49 
WHERE MenuID = 5;

UPDATE Menu 
	SET Name = 'Original Crust Pepperoni', 
    Description = 'Pepperoni loaded on a classic crust with cheesy goodness.', 
    ImagePath = 'images/Pizza/Original_Crust_Pepperoni.jpg',
    Price = 10.99 
WHERE MenuID = 6;

UPDATE Menu 
	SET Name = 'Royal Spice Paneer', 
    Description = 'Paneer seasoned with royal spices on a golden crust.', 
    ImagePath = 'images/Pizza/royal_spice_paneer.jpg',
    Price = 9.49 
WHERE MenuID = 8;

UPDATE Menu 
	SET Name = 'Sausage Pizza', 
    Description = 'Sausage lovers’ dream with bold flavor on every bite.', 
    ImagePath = 'images/Pizza/sausage_cheese.jpg',
    Price = 9.49 
WHERE MenuID = 7;
