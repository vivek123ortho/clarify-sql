import sqlglot
from sqlglot import exp

FORBIDDEN = (
    exp.Insert, exp.Update, exp.Delete, exp.Drop, exp.Create,
    exp.Alter, exp.Command, exp.TruncateTable, exp.Merge,
)


class UnsafeSQLError(ValueError):
    pass


def validate_sql(sql: str) -> str:
    """Return the cleaned SQL if it is one safe SELECT, else raise UnsafeSQLError."""
    try:
        statements = sqlglot.parse(sql, read="postgres")
    except sqlglot.errors.ParseError as e:
        raise UnsafeSQLError(f"SQL could not be parsed: {e}")

    statements = [s for s in statements if s is not None]

    if len(statements) != 1:
        raise UnsafeSQLError("Exactly one SQL statement is allowed.")

    tree = statements[0]

    if not isinstance(tree, (exp.Select, exp.Union, exp.With)) and tree.find(exp.Select) is None:
        raise UnsafeSQLError("Only SELECT queries are allowed.")

    if isinstance(tree, FORBIDDEN):
        raise UnsafeSQLError("Write or schema-changing statements are not allowed.")

    for node in tree.walk():
        if isinstance(node, FORBIDDEN):
            raise UnsafeSQLError("Write or schema-changing statements are not allowed.")

    return tree.sql(dialect="postgres")