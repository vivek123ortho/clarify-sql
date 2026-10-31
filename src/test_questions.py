# (question, expected_is_ambiguous)
TEST_QUESTIONS = [
    # Clear
    ("List all products in the Electronics category", False),
    ("How many customers are there in each city?", False),
    ("Show all orders with status 'pending'", False),
    ("What is the price of the Laptop?", False),
    ("Show the 5 most expensive products", False),
    ("How many orders were placed in June 2025?", False),
    ("List customers from Pune", False),
    ("What is the sum of total_amount for completed orders?", False),
    ("Count the products in each category", False),
    ("Show orders placed by Aarav Sharma", False),
    # Ambiguous
    ("What is the total revenue?", True),
    ("Who is the top customer?", True),
    ("Show sales last quarter", True),
    ("What is our best selling product?", True),
    ("Show the biggest orders", True),
    ("Which city performs best?", True),
    ("Show recent orders", True),
    ("Who are our best customers?", True),
    ("What are our popular products?", True),
    ("How much did we sell?", True),
]