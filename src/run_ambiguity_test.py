
import time
from ambiguity import check_ambiguity
from test_questions import TEST_QUESTIONS

correct = 0

for question, expected in TEST_QUESTIONS:
    try:
        result = check_ambiguity(question)

    except Exception as e:
        msg = str(e)

        if "PerDay" in msg:
            print("Daily quota exhausted. Stop and switch provider or wait.")
            break

        if "429" in msg or "RESOURCE_EXHAUSTED" in msg:
            print("Per-minute limit, waiting 30 seconds...")
            time.sleep(30)
            result = check_ambiguity(question)

        else:
            raise

    ok = result.is_ambiguous == expected
    correct += ok

    print(f"[{'OK' if ok else 'WRONG'}] {question} -> {result.is_ambiguous}")
    time.sleep(3)

print(f"\nAccuracy: {correct}/{len(TEST_QUESTIONS)}")
