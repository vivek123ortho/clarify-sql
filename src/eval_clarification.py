import time
from text_to_sql import generate_sql, generate_sql_with_choices, run_sql

CASES = [
    {
        "question": "Who is the top customer?",
        "hints": ["Rank customers by SUM(orders.total_amount)",
                  "Only orders with status = 'completed'"],
        "expected_first_value": "Aarav Sharma",
    },
    {
        "question": "Who is the top customer?",
        "hints": ["Rank customers by COUNT of orders",
                  "Only orders with status = 'completed'"],
        "expected_first_value": "Sneha Joshi",
    },
]


def first_name_in_result(sql):
    cols, rows = run_sql(sql)
    return [str(v) for v in rows[0]] if rows else []


def run_eval():
    guess_ok = clarified_ok = 0
    for case in CASES:
        expected = case["expected_first_value"]

        try:
            guess = generate_sql(case["question"])
            guess_ok += expected in first_name_in_result(guess.sql)
        except Exception as e:
            print("guess failed:", e)
        time.sleep(3)

        try:
            clar = generate_sql_with_choices(case["question"], case["hints"])
            hit = expected in first_name_in_result(clar.sql)
            clarified_ok += hit
            print(f"[{'OK' if hit else 'WRONG'}] clarified: {case['question']} -> expected {expected}")
        except Exception as e:
            print("clarified failed:", e)
        time.sleep(3)

    n = len(CASES)
    print(f"\nGuessing (no clarification): {guess_ok}/{n}")
    print(f"With clarification:          {clarified_ok}/{n}")


if __name__ == "__main__":
    run_eval()