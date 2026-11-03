import time
from decimal import Decimal

from text_to_sql import generate_sql, generate_sql_with_choices, run_sql

PAUSE = 3  # seconds between LLM calls (rate limits)

# Each case: the question, the choices a user would make (as hints),
# and a gold SQL query whose first value is the correct answer.
CASES = [
    {
        "name": "top customer by spend",
        "question": "Who is the top customer?",
        "hints": [
            "Rank customers by SUM(orders.total_amount), highest first",
            "Only orders with status = 'completed'",
        ],
        "gold_sql": """
            SELECT c.name FROM customers c
            JOIN orders o ON o.customer_id = c.customer_id
            WHERE o.status = 'completed'
            GROUP BY c.customer_id, c.name
            ORDER BY SUM(o.total_amount) DESC LIMIT 1
        """,
    },
    {
        "name": "top customer by order count",
        "question": "Who is the top customer?",
        "hints": [
            "Rank customers by COUNT of orders, highest first",
            "Only orders with status = 'completed'",
        ],
        "gold_sql": """
            SELECT c.name FROM customers c
            JOIN orders o ON o.customer_id = c.customer_id
            WHERE o.status = 'completed'
            GROUP BY c.customer_id, c.name
            ORDER BY COUNT(*) DESC LIMIT 1
        """,
    },
    {
        "name": "revenue from order totals",
        "question": "What is the total revenue?",
        "hints": [
            "Revenue means SUM(orders.total_amount)",
            "Only orders with status = 'completed'",
        ],
        "gold_sql": """
            SELECT SUM(total_amount) FROM orders WHERE status = 'completed'
        """,
    },
    {
        "name": "revenue from line items",
        "question": "What is the total revenue?",
        "hints": [
            "Revenue means SUM(order_items.quantity * order_items.unit_price), "
            "joining order_items to orders",
            "Only orders with status = 'completed'",
        ],
        "gold_sql": """
            SELECT SUM(oi.quantity * oi.unit_price)
            FROM order_items oi JOIN orders o ON o.order_id = oi.order_id
            WHERE o.status = 'completed'
        """,
    },
    {
        "name": "revenue including all orders",
        "question": "What is the total revenue?",
        "hints": [
            "Revenue means SUM(orders.total_amount)",
            "Include all orders regardless of status",
        ],
        "gold_sql": """
            SELECT SUM(total_amount) FROM orders
        """,
    },
    {
        "name": "best selling product by revenue",
        "question": "What is our best selling product?",
        "hints": [
            "Rank products by SUM(order_items.quantity * order_items.unit_price), "
            "joining order_items to products and orders",
            "Only orders with status = 'completed'",
        ],
        "gold_sql": """
            SELECT p.name FROM products p
            JOIN order_items oi ON oi.product_id = p.product_id
            JOIN orders o ON o.order_id = oi.order_id
            WHERE o.status = 'completed'
            GROUP BY p.product_id, p.name
            ORDER BY SUM(oi.quantity * oi.unit_price) DESC LIMIT 1
        """,
    },
    {
        "name": "best city by revenue",
        "question": "Which city performs best?",
        "hints": [
            "Rank cities (customers.city) by SUM(orders.total_amount), highest first",
            "Only orders with status = 'completed'",
        ],
        "gold_sql": """
            SELECT c.city FROM customers c
            JOIN orders o ON o.customer_id = c.customer_id
            WHERE o.status = 'completed'
            GROUP BY c.city
            ORDER BY SUM(o.total_amount) DESC LIMIT 1
        """,
    },
        {
        "name": "best city by average order value",
        "question": "Which city performs best?",
        "hints": [
            "Rank cities (customers.city) by AVG(orders.total_amount), highest first",
            "Only orders with status = 'completed'",
        ],
        "gold_sql": """
            SELECT c.city FROM customers c
            JOIN orders o ON o.customer_id = c.customer_id
            WHERE o.status = 'completed'
            GROUP BY c.city
            ORDER BY AVG(o.total_amount) DESC LIMIT 1
        """,
    },
    {
        "name": "order count, completed only",
        "question": "How many orders do we have?",
        "hints": ["Count only orders with status = 'completed'"],
        "gold_sql": "SELECT COUNT(*) FROM orders WHERE status = 'completed'",
    },
    {
        "name": "order count, all statuses",
        "question": "How many orders do we have?",
        "hints": ["Count every order regardless of status"],
        "gold_sql": "SELECT COUNT(*) FROM orders",
    },
    {
        "name": "latest order date, completed only",
        "question": "When was our most recent order?",
        "hints": ["Only orders with status = 'completed'; use MAX(orders.order_date)"],
        "gold_sql": "SELECT MAX(order_date) FROM orders WHERE status = 'completed'",
    },
    {
        "name": "latest order date, all statuses",
        "question": "When was our most recent order?",
        "hints": ["Include all orders regardless of status; use MAX(orders.order_date)"],
        "gold_sql": "SELECT MAX(order_date) FROM orders",
    },
    {
        "name": "Q2 revenue, completed only",
        "question": "What was the revenue in Q2 2025?",
        "hints": [
            "Revenue means SUM(orders.total_amount)",
            "Q2 2025 means order_date from 2025-04-01 to 2025-06-30",
            "Only orders with status = 'completed'",
        ],
        "gold_sql": """
            SELECT SUM(total_amount) FROM orders
            WHERE status = 'completed'
              AND order_date BETWEEN '2025-04-01' AND '2025-06-30'
        """,
    },
    {
        "name": "Q2 revenue, all statuses",
        "question": "What was the revenue in Q2 2025?",
        "hints": [
            "Revenue means SUM(orders.total_amount)",
            "Q2 2025 means order_date from 2025-04-01 to 2025-06-30",
            "Include all orders regardless of status",
        ],
        "gold_sql": """
            SELECT SUM(total_amount) FROM orders
            WHERE order_date BETWEEN '2025-04-01' AND '2025-06-30'
        """,
    },
    {
        "name": "top customer by spend, all orders",
        "question": "Who is the top customer?",
        "hints": [
            "Rank customers by SUM(orders.total_amount), highest first",
            "Include all orders regardless of status",
        ],
        "gold_sql": """
            SELECT c.name FROM customers c
            JOIN orders o ON o.customer_id = c.customer_id
            GROUP BY c.customer_id, c.name
            ORDER BY SUM(o.total_amount) DESC LIMIT 1
        """,
    },
    {
        "name": "top customer by items bought, all orders",
        "question": "Who is the top customer?",
        "hints": [
            "Rank customers by SUM(order_items.quantity), highest first, "
            "joining customers, orders and order_items",
            "Include all orders regardless of status",
        ],
        "gold_sql": """
            SELECT c.name FROM customers c
            JOIN orders o ON o.customer_id = c.customer_id
            JOIN order_items oi ON oi.order_id = o.order_id
            GROUP BY c.customer_id, c.name
            ORDER BY SUM(oi.quantity) DESC LIMIT 1
        """,
    },
    {
        "name": "best selling product by units sold",
        "question": "What is our best selling product?",
        "hints": [
            "Rank products by SUM(order_items.quantity), highest first, "
            "joining order_items to products and orders",
            "Only orders with status = 'completed'",
        ],
        "gold_sql": """
            SELECT p.name FROM products p
            JOIN order_items oi ON oi.product_id = p.product_id
            JOIN orders o ON o.order_id = oi.order_id
            WHERE o.status = 'completed'
            GROUP BY p.product_id, p.name
            ORDER BY SUM(oi.quantity) DESC LIMIT 1
        """,
    },
]


def normalize(value):
    """Make 79098.00, Decimal('79098.00') and 79098 compare equal."""
    if isinstance(value, (int, float, Decimal)):
        return round(float(value), 2)
    return str(value).strip().lower()


def first_row(sql):
    """Run SQL and return the normalized values of the first row."""
    _, rows = run_sql(sql)
    return [normalize(v) for v in rows[0]] if rows else []


def is_correct(generated_sql, expected):
    """Correct if the expected value appears in the first result row."""
    try:
        return expected in first_row(generated_sql)
    except Exception as e:
        print("   query failed:", e)
        return False


def run_eval():
    guess_ok = clarified_ok = 0

    for case in CASES:
        gold_row = first_row(case["gold_sql"])
        expected = gold_row[0]
        print(f"\n{case['name']}  (expected: {expected})")

        # Path A: no clarification, the model guesses
        try:
            guess = generate_sql(case["question"])
            hit = is_correct(guess.sql, expected)
        except Exception as e:
            print("   guess failed:", e)
            hit = False
        guess_ok += hit
        print(f"   guessing:      {'OK' if hit else 'WRONG'}")
        time.sleep(PAUSE)

        # Path B: with the user's clarified choices
        try:
            clar = generate_sql_with_choices(case["question"], case["hints"])
            hit = is_correct(clar.sql, expected)
        except Exception as e:
            print("   clarified failed:", e)
            hit = False
        clarified_ok += hit
        print(f"   clarification: {'OK' if hit else 'WRONG'}")
        time.sleep(PAUSE)

    n = len(CASES)
    print("\n" + "=" * 50)
    print(f"Guessing (no clarification): {guess_ok}/{n}")
    print(f"With clarification:          {clarified_ok}/{n}")


if __name__ == "__main__":
    run_eval()