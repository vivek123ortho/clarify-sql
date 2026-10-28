from pydantic import BaseModel, Field


class SQLResult(BaseModel):
    sql: str = Field(description="A single read-only PostgreSQL SELECT query")
    explanation: str = Field(description="One sentence explaining what the query does")