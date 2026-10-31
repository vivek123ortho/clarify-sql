import json
import os

MEMORY_FILE = "definitions.json"


def _load() -> dict:
    if not os.path.exists(MEMORY_FILE):
        return {}
    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return {}


def _key(term: str, question: str) -> str:
    return f"{term.strip().lower()}||{question.strip().lower()}"


def get_definition(term: str, question: str):
    """Return the saved sql_hint for this clarification, or None."""
    return _load().get(_key(term, question))


def save_definition(term: str, question: str, sql_hint: str) -> None:
    data = _load()
    data[_key(term, question)] = sql_hint
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def clear_definitions() -> None:
    if os.path.exists(MEMORY_FILE):
        os.remove(MEMORY_FILE)