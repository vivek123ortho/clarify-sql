import sqlglot
from sqlglot import exp

FORBIDDEN = (
    exp.Insert, exp.Update, exp.Delete, exp.Drop, exp.Create,
    exp.Alter, exp.Command, exp.TruncateTable, exp.Merge,
    exp.Into,  # SELECT ... INTO creates a table
)

# Functions that are never needed for analytics questions
BLOCKED_FUNCTIONS = {
    "pg_sleep", "pg_sleep_for", "pg_sleep_until",
    "pg_read_file", "pg_read_binary_file", "pg_ls_dir",
    "lo_import", "lo_export",
    "dblink", "dblink_exec",
    "pg_terminate_backend", "pg_cancel_backend",
    "set_config",
}


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

    for node in tree.walk():
        if isinstance(node, FORBIDDEN):
            raise UnsafeSQLError("Write or schema-changing statements are not allowed.")
        if isinstance(node, exp.Anonymous) and node.name.lower() in BLOCKED_FUNCTIONS:
            raise UnsafeSQLError(f"Function '{node.name}' is not allowed.")

    return tree.sql(dialect="postgres")