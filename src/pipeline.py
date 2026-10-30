from ambiguity import check_ambiguity
from clarify import generate_clarifications
from text_to_sql import generate_sql, generate_sql_with_choices, run_sql


def ask_choice(count: int) -> int:
    """Keep asking until the user types a valid option number."""
    while True:
        raw = input("Choose a number: ").strip()
        if raw.isdigit() and 1 <= int(raw) <= count:
            return int(raw) - 1
        print(f"Please type a number from 1 to {count}.")


def main():
    q = input("Question: ").strip()
    check = check_ambiguity(q)

    if not check.is_ambiguous:
        print("\nThe question is clear. Generating SQL...")
        result = generate_sql(q)
    else:
        print("\nThis question is ambiguous:", check.reason)
        cset = generate_clarifications(q, check.ambiguous_terms, check.reason)

        hints = []
        for cq in cset.questions[:3]:
            print("\n" + cq.question)
            for i, opt in enumerate(cq.options, 1):
                print(f"  {i}. {opt.label}")
            pick = ask_choice(len(cq.options))
            hints.append(cq.options[pick].sql_hint)

        print("\nYour choices:")
        for h in hints:
            print(" -", h)
        result = generate_sql_with_choices(q, hints)

    print("\nSQL:", result.sql)
    print("Why:", result.explanation)

    try:
        cols, rows = run_sql(result.sql)
    except Exception as e:
        print("\nThe query failed:", e)
        return

    print("\n" + " | ".join(cols))
    for row in rows:
        print(row)
    if not rows:
        print("No rows returned.")


if __name__ == "__main__":
    main()