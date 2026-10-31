
import os
from dotenv import load_dotenv
from llm_factory import get_llm
from langchain_core.prompts import ChatPromptTemplate

from schema_loader import load_schema, load_value_hints
from models import AmbiguityCheck
from retry import invoke_with_retry

load_dotenv()

llm = get_llm()
structured_llm = llm.with_structured_output(AmbiguityCheck)

prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You review questions that a user wants to ask a PostgreSQL database.\n"
        "Decide whether the question is ambiguous given THIS schema:\n\n"
        "{schema}\n\n"
        "A question is ambiguous if there are two or more reasonable ways to "
        "answer it that would return different results. Common causes:\n"
        "- A vague term like 'top', 'best', 'biggest' with no stated measure\n"
        "- A business term like 'revenue' or 'sales' that several columns "
        "or tables could represent\n"
        "- Unclear status handling (should cancelled or pending orders count?)\n"
        "- Unclear time ranges like 'last quarter' with no dates\n\n"
        "A question is NOT ambiguous if it names the exact table, column, "
        "filter, or measure, or if only one interpretation is possible.\n"
        "Do not invent ambiguity. Do not write any SQL."
    ),
    ("human", "{question}"),
])

chain = prompt | structured_llm


def check_ambiguity(question: str) -> AmbiguityCheck:
    """Judge whether a question is ambiguous for this database schema."""
    schema = load_schema() + "\n\n" + load_value_hints()
    return invoke_with_retry(chain, {"schema": schema, "question": question})


if __name__ == "__main__":
    for q in [
        "List all products in the Electronics category",
        "What is the total revenue?",
        "Who is the top customer?",
    ]:
        r = check_ambiguity(q)
        print("\nQUESTION:", q)
        print("Ambiguous:", r.is_ambiguous)
        print("Terms:", r.ambiguous_terms)
        print("Reason:", r.reason)
