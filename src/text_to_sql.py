
import os

from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from sqlalchemy import text
from llm_factory import get_llm
from schema_loader import load_schema, load_value_hints, get_engine
from models import SQLResult


# Load environment variables
load_dotenv()

# Initialize the LLM
llm = get_llm()

# Require structured output matching SQLResult
structured_llm = llm.with_structured_output(SQLResult)


# Create the prompt
prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You write PostgreSQL queries.\n"
        "Use only the tables and columns in this schema:\n\n"
        "{schema}\n\n"
        "Rules:\n"
        "1. Return one SELECT query only.\n"
        "2. Never modify, insert, or delete data.\n"
        "3. Use only tables and columns provided in the schema.\n"
    ),
    ("human", "{question}"),
])

# Connect the prompt to the LLM
chain = prompt | structured_llm


def generate_sql(question: str) -> SQLResult:
    schema = load_schema() + "\n\n" + load_value_hints()
    return chain.invoke({"schema": schema, "question": question})


def run_sql(sql: str):
    """Execute the generated SQL and return column names and rows."""
    # Basic safety check: only allow SELECT queries.
    if not sql.strip().lower().startswith("select"):
        raise ValueError("Only SELECT queries are allowed.")

    with get_engine().connect() as conn:
        result = conn.execute(text(sql))
        return result.keys(), result.fetchall()


if __name__ == "__main__":
    questions = [
        "List all products in the Electronics category",
        "What is the total revenue?",
        "Who is the top customer?",
    ]

    for q in questions:
        print("\n" + "=" * 60)
        print("QUESTION:", q)

        try:
            result = generate_sql(q)

            print("\nSQL:", result.sql)
            print("Why:", result.explanation)

            cols, rows = run_sql(result.sql)

            print("\nCOLUMNS:", list(cols))

            for row in rows:
                print(row)

            if not rows:
                print("No rows returned.")

        except Exception as e:
            print("ERROR:", e)
