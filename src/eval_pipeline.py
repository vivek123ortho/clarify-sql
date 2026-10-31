import os
import time

from ambiguity import check_ambiguity
from clarify import generate_clarifications
from text_to_sql import generate_sql, generate_sql_with_choices
from simulated_user import pick_hints
from eval_clarification import CASES, first_row, is_correct, PAUSE


def run_case(case):
    """Run the full pipeline for one case. Returns (correct, questions_asked, flagged)."""
    question = case["question"]
    intent = "; ".join(case["hints"])
    expected = first_row(case["gold_sql"])[0]

    check = check_ambiguity(question)
    time.sleep(PAUSE)

    if not check.is_ambiguous:
        result = generate_sql(question)
        asked = 0
    else:
        cset = generate_clarifications(question, check.ambiguous_terms, check.reason)
        time.sleep(PAUSE)
        hints = pick_hints(intent, cset)
        if os.getenv("DEBUG_EVAL"):
            print("   options:", [[o.label for o in q.options] for q in cset.questions])
            print("   picked hints:", hints)
        time.sleep(PAUSE)
        result = generate_sql_with_choices(question, hints)
        asked = len(cset.questions[:3])

    time.sleep(PAUSE)
    return is_correct(result.sql, expected), asked, check.is_ambiguous


def main():
    correct = flagged = total_asked = errors = completed = 0
    for case in CASES:
        try:
            ok, asked, was_flagged = run_case(case)
        except Exception as e:
            print(f"[ERROR] {case['name']}: {e}")
            errors += 1
            continue
        completed += 1
        correct += ok
        flagged += was_flagged
        total_asked += asked
        print(f"[{'OK' if ok else 'WRONG'}] {case['name']} "
              f"(flagged: {was_flagged}, questions asked: {asked})")

    print("\n" + "=" * 50)
    print(f"Full pipeline correct:      {correct}/{completed}")
    print(f"Provider errors:             {errors}")
    print(f"Flagged as ambiguous:       {flagged}/{completed}")
    print(
        f"Avg questions per query:    "
        f"{total_asked / completed:.1f}" if completed else
        "Avg questions per query:    n/a"
    )


if __name__ == "__main__":
    main()