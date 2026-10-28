
INSERT INTO customers (name, email, city, signup_date) VALUES
('Aarav Sharma', 'aarav@example.com', 'Mumbai', '2025-01-15'),
('Priya Patil', 'priya@example.com', 'Pune', '2025-02-20'),
('Rahul Deshmukh', 'rahul@example.com', 'Nagpur', '2025-03-10'),
('Sneha Joshi', 'sneha@example.com', 'Nashik', '2025-04-05'),
('Vikram Singh', 'vikram@example.com', 'Mumbai', '2025-05-12'),
('Ananya Kulkarni', 'ananya@example.com', 'Pune', '2025-07-18'),
('Rohan Mehta', 'rohan@example.com', 'Aurangabad', '2025-09-22'),
('Isha Shah', 'isha@example.com', 'Nagpur', '2025-11-08');

INSERT INTO products (name, category, price) VALUES
('Laptop', 'Electronics', 65000.00),
('Wireless Mouse', 'Electronics', 799.00),
('Keyboard', 'Electronics', 1499.00),
('Office Chair', 'Furniture', 8500.00),
('Study Desk', 'Furniture', 12000.00),
('Water Bottle', 'Accessories', 499.00),
('Backpack', 'Accessories', 1999.00),
('Notebook Pack', 'Stationery', 299.00),
('Pen Set', 'Stationery', 149.00),
('Monitor', 'Electronics', 15000.00);

-- Insert orders
INSERT INTO orders (customer_id, order_date, total_amount, status) VALUES
(1, '2025-04-10', 65799.00, 'completed'),
(2, '2025-04-15', 8799.00, 'completed'),
(3, '2025-04-20', 1797.00, 'completed'),
(4, '2025-05-10', 12000.00, 'completed'),
(5, '2025-05-18', 15799.00, 'completed'),
(6, '2025-07-20', 66999.00, 'completed'),
(7, '2025-10-01', 2298.00, 'completed'),
(8, '2025-11-12', 16499.00, 'completed'),
(1, '2025-06-05', 8500.00, 'cancelled'),
(2, '2025-08-14', 1499.00, 'cancelled'),
(3, '2025-09-20', 15000.00, 'cancelled'),
(4, '2025-05-25', 12149.00, 'completed'),
(5, '2025-07-05', 2298.00, 'completed'),
(6, '2025-10-18', 65000.00, 'pending'),
(7, '2025-12-01', 1999.00, 'pending'),
(8, '2025-12-10', 149.00, 'pending'),
(1, '2025-06-28', 13299.00, 'completed'),
(2, '2025-06-22', 1247.00, 'completed'),
(3, '2025-08-30', 8799.00, 'completed'),
(4, '2025-11-25', 15499.00, 'completed');

INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES
-- Order 1: Laptop + Mouse = 65,799
(1, 1, 1, 65000.00),
(1, 2, 1, 799.00),

-- Order 2: Chair + Notebook Pack = 8,799
(2, 4, 1, 8500.00),
(2, 8, 1, 299.00),

-- Order 3: Keyboard + Water Bottle = 1,998; discount applied
(3, 3, 1, 1499.00),
(3, 6, 1, 499.00),

-- Order 4: Study Desk = 12,000
(4, 5, 1, 12000.00),

-- Order 5: Monitor + Mouse = 15,799
(5, 10, 1, 15000.00),
(5, 2, 1, 799.00),

-- Order 6: Laptop + Backpack = 66,999
(6, 1, 1, 65000.00),
(6, 7, 1, 1999.00),

-- Order 7: Backpack + Notebook Pack = 2,298
(7, 7, 1, 1999.00),
(7, 8, 1, 299.00),

-- Order 8: Monitor + Keyboard = 16,499
(8, 10, 1, 15000.00),
(8, 3, 1, 1499.00),

-- Order 9: Office Chair = 8,500
(9, 4, 1, 8500.00),

-- Order 10: Keyboard = 1,499
(10, 3, 1, 1499.00),

-- Order 11: Monitor = 15,000
(11, 10, 1, 15000.00),

-- Order 12: Study Desk + Pen Set = 12,149
(12, 5, 1, 12000.00),
(12, 9, 1, 149.00),

-- Order 13: Mouse + Keyboard = 2,298
(13, 2, 1, 799.00),
(13, 3, 1, 1499.00),

-- Order 14: Laptop = 65,000
(14, 1, 1, 65000.00),

-- Order 15: Backpack = 1,999
(15, 7, 1, 1999.00),

-- Order 16: Pen Set = 149
(16, 9, 1, 149.00),

-- Order 17: Study Desk + Backpack = 13,999
(17, 5, 1, 12000.00),
(17, 7, 1, 1999.00),

-- Order 18: Mouse + Notebook Pack + Pen Set = 1,247
(18, 2, 1, 799.00),
(18, 8, 1, 299.00),
(18, 9, 1, 149.00),

-- Order 19: Office Chair + Water Bottle = 8,999
(19, 4, 1, 8500.00),
(19, 6, 1, 499.00),

-- Order 20: Monitor + Mouse = 15,799
(20, 10, 1, 15000.00),
(20, 2, 1, 799.00);
