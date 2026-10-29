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
    reason: str = Field(
        description="One or two sentences explaining the decision"
    )
    ambiguous_terms: List[str] = Field(
        description="Words or phrases in the question that are ambiguous. "
                    "Empty list if not ambiguous"
    )