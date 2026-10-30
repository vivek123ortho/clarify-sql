
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from sqlalchemy import text
from sql_validator import validate_sql

from llm_factory import get_llm
from schema_loader import (
    load_schema,
    load_value_hints,
    get_readonly_engine
)
from models import SQLResult

load_dotenv()

llm = get_llm()
structured_llm = llm.with_structured_output(SQLResult)

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
        "4. If the user gave clarified choices, follow them exactly."
    ),
    ("human", "{question}"),
])

chain = prompt | structured_llm


def generate_sql(question: str) -> SQLResult:
    """Generate a SQL query from a natural-language question."""
    schema = load_schema() + "\n\n" + load_value_hints()
    return chain.invoke({"schema": schema, "question": question})


def generate_sql_with_choices(question: str, hints: list[str]) -> SQLResult:
    """Generate SQL after the user answered clarification questions."""
    guidance = "\n".join(f"- {h}" for h in hints)

    full_question = (
        f"{question}\n\n"
        f"The user clarified these choices. Follow them exactly:\n{guidance}"
    )

    return generate_sql(full_question)


def run_sql(sql: str):
    """Validate, then execute SQL using a read-only database connection."""
    safe_sql = validate_sql(sql)

    with get_readonly_engine().connect() as conn:
        result = conn.execute(text(safe_sql))
        return result.keys(), result.fetchall()


if __name__ == "__main__":
    q = "List all products in the Electronics category"

    result = generate_sql(q)

    print("SQL:", result.sql)

    cols, rows = run_sql(result.sql)

    print(list(cols))

    for row in rows:
        print(row)
