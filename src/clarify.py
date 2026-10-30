from langchain_core.prompts import ChatPromptTemplate

from llm_factory import get_llm
from schema_loader import load_schema, load_value_hints
from models import ClarificationSet

llm = get_llm()
structured_llm = llm.with_structured_output(ClarificationSet)

prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "A user question about a PostgreSQL database is ambiguous.\n"
        "Schema:\n\n{schema}\n\n"
        "Ambiguous terms: {terms}\n"
        "Reason: {reason}\n\n"
        "Write multiple-choice clarification questions, at most 3 in total.\n"
        "Rules:\n"
        "1. Write one question per ambiguous term.\n"
        "2. Offer only interpretations a business user would plausibly mean. "
        "Never add an option just to reach a count; 2 or 3 good options are "
        "better than 4.\n"
        "3. When ranking or measuring something ('top', 'best', 'biggest'), "
        "consider money (orders.total_amount or order_items quantity * "
        "unit_price), number of orders, and quantity of items "
        "(order_items.quantity) as possible measures.\n"
        "4. If the answer depends on orders, ALWAYS include one separate "
        "question about which orders should count, with options such as: "
        "completed orders only; completed and pending orders; all orders "
        "including cancelled. Use the exact status values from the example "
        "values in the schema.\n"
        "5. Every sql_hint must be precise: name the tables and columns, the "
        "aggregation, and any status filter. Do not write full SQL queries.\n"
        "6. Labels must be short and plain for a non-technical user."
    ),
    ("human", "{question}"),
])

chain = prompt | structured_llm


def generate_clarifications(question, terms, reason) -> ClarificationSet:
    """Turn an ambiguous question into multiple-choice clarification questions."""
    schema = load_schema() + "\n\n" + load_value_hints()
    return chain.invoke({
        "schema": schema,
        "question": question,
        "terms": ", ".join(terms),
        "reason": reason,
    })


if __name__ == "__main__":
    from ambiguity import check_ambiguity

    q = "Who is the top customer?"
    check = check_ambiguity(q)
    cset = generate_clarifications(q, check.ambiguous_terms, check.reason)
    for cq in cset.questions:
        print("\nQ:", cq.question)
        for i, opt in enumerate(cq.options, 1):
            print(f"  {i}. {opt.label}")
            print(f"     hint: {opt.sql_hint}")