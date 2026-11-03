# Clarify SQL

![tests](https://github.com/vivek123ortho/clarify-sql/actions/workflows/tests.yml/badge.svg)

A text-to-SQL assistant that **asks instead of guessing**. Ask "Who is the top
customer?" and it asks whether you mean total spend, number of orders, or items
bought, then writes the matching query.

![demo](docs/demo.gif)

## Why

Most text-to-SQL tools silently pick one interpretation of a vague question and
return a confident but possibly wrong answer. Clarify SQL detects the ambiguity,
asks schema-grounded multiple-choice questions, and uses the answers to write
the query.

## How it works

1. **Schema loader** reads tables, columns, foreign keys and example values from PostgreSQL
2. **Ambiguity detector** (LLM + Pydantic structured output) decides if a question has several valid meanings
3. **Clarification generator** turns each ambiguous term into a multiple-choice question; each option has a user-facing `label` and a precise `sql_hint`
4. **SQL generator** writes the query following the user's choices
5. **Safety layers**: sqlglot validation (one SELECT only, blocked functions), a read-only database user, and a 5-second statement timeout
6. **Memory** stores a user's past choices so the same question isn't asked twice
7. **Streamlit UI** for the chat flow

## Results

Evaluated on one 4-table shop database. All numbers come from labeled test sets
with gold SQL; the "user" is an LLM-simulated user, not real people.

| Metric | Result |
|---|---|
| Ambiguity detection (20 questions, 10 clear / 10 ambiguous) | 19/20 on first run (one debatable case) |
| Correct answers, no clarification (guessing) | 7/17 |
| Correct answers, full pipeline with clarification | 15 to 17 out of 17 across runs |
| Average questions asked per query | 2.0 |
| SQL validator test cases | 17/17 blocked/allowed as expected |

Failures seen: occasional malformed structured output from the LLM provider
(fixed with retries), and one debatable detection label ("orders placed" and
whether cancelled orders count).

## Setup

1. Clone the repo and create a virtual environment: `python -m venv venv`
2. `pip install -r requirements.txt`
3. Create a PostgreSQL database named `shopdb`
4. Run `db/schema.sql`, then `db/seed.sql`, then `db/readonly_user.sql`
5. Copy `.env.example` to `.env` and fill in your values (URL-encode special
   characters in passwords, e.g. `@` becomes `%40`)
6. `streamlit run src/app.py`

## Evaluate

```
python src/run_ambiguity_test.py
python src/eval_clarification.py
python src/eval_pipeline.py
pytest tests/
```

## Limitations

- Small test sets (20 detection questions, 17 correctness cases) on one small schema
- The simulated user is an LLM and is more lenient than a human
- `LIMIT 1` hides ties
- LLM output varies between runs
- Free-tier API limits apply; the provider is swappable via `LLM_PROVIDER`

## Stack

Python, PostgreSQL, LangChain, Pydantic, sqlglot, Streamlit, Groq / Gemini / OpenAI