from typing import List
from pydantic import BaseModel, Field


class SQLResult(BaseModel):
    sql: str = Field(description="A single read-only PostgreSQL SELECT query")
    explanation: str = Field(description="One sentence explaining what the query does")


class AmbiguityCheck(BaseModel):
    is_ambiguous: bool = Field(
        description="True only if the question has multiple reasonable "
                    "interpretations that would give different results"
    )
    reason: str = Field(description="One or two sentences explaining the decision")
    ambiguous_terms: List[str] = Field(
        description="Words or phrases in the question that are ambiguous. "
                    "Empty list if not ambiguous"
    )


class ClarificationOption(BaseModel):
    label: str = Field(description="Short user-facing choice, max 8 words")
    sql_hint: str = Field(
        description="Precise instruction for a SQL writer: which tables, "
                    "columns, aggregation and filters this choice means"
    )


class ClarificationQuestion(BaseModel):
    term: str = Field(description="The ambiguous term this question resolves")
    question: str = Field(description="A clear question to the user")
    options: List[ClarificationOption] = Field(
        description="2 to 4 mutually exclusive options, grounded in the schema"
    )


class ClarificationSet(BaseModel):
    questions: List[ClarificationQuestion] = Field(
        description="At most 3 questions, one per ambiguous term"
    )