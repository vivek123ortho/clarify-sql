from langchain_core.prompts import ChatPromptTemplate

from llm_factory import get_llm
from models import OptionSelection
from retry import invoke_with_retry

llm = get_llm()
structured_llm = llm.with_structured_output(OptionSelection)

prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You simulate a user answering clarification questions about a "
        "database query. The user's true intent is:\n{intent}\n\n"
        "For each question, pick the option number that best matches this "
        "intent. If no option matches exactly, pick the closest one."
    ),
    ("human", "{questions}"),
])

chain = prompt | structured_llm


def format_questions(cset) -> str:
    lines = []
    for i, cq in enumerate(cset.questions[:3], 1):
        lines.append(f"Question {i}: {cq.question}")
        for j, opt in enumerate(cq.options, 1):
            lines.append(f"  {j}. {opt.label} ({opt.sql_hint})")
    return "\n".join(lines)


def pick_hints(intent: str, cset) -> list:
    """Return the sql_hint of the option the simulated user would choose."""
    selection = invoke_with_retry(
        chain, {"intent": intent, "questions": format_questions(cset)}
    )
    hints = []
    for i, cq in enumerate(cset.questions[:3]):
        n = selection.choices[i] if i < len(selection.choices) else 1
        if not 1 <= n <= len(cq.options):
            n = 1
        hints.append(cq.options[n - 1].sql_hint)
    return hints