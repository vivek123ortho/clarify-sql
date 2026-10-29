# (question, expected_is_ambiguous)
TEST_QUESTIONS = [
    # Clear questions: should NOT be flagged
    ("List all products in the Electronics category", False),
    ("How many customers are there in each city?", False),
    ("Show all orders with status 'pending'", False),
    ("What is the price of the Laptop?", False),
    # Ambiguous questions: SHOULD be flagged
    ("What is the total revenue?", True),
    ("Who is the top customer?", True),
    ("Show sales last quarter", True),
    ("What is our best selling product?", True),
    ("Show the biggest orders", True),
    ("Which city performs best?", True),
]