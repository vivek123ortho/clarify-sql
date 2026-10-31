
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, inspect, text

load_dotenv()

def get_readonly_engine():
    return create_engine(
        os.getenv("READONLY_DATABASE_URL"),
        connect_args={
            "options": "-c statement_timeout=5000 -c default_transaction_read_only=on"
        },
    )

def get_engine():
    return create_engine(os.getenv("DATABASE_URL"))


def load_schema():
    engine = get_engine()
    inspector = inspect(engine)

    lines = []
    for table in sorted(inspector.get_table_names()):
        lines.append(f"Table: {table}")

        for col in inspector.get_columns(table):
            lines.append(f"  - {col['name']} ({col['type']})")

        for fk in inspector.get_foreign_keys(table):
            from_cols = ", ".join(fk["constrained_columns"])
            to_cols = ", ".join(fk["referred_columns"])
            lines.append(
                f"  FK: {from_cols} -> {fk['referred_table']}({to_cols})"
            )

        lines.append("")

    return "\n".join(lines)


def load_value_hints(limit=10):
    engine = get_engine()
    hints = [
        ("products", "category"),
        ("orders", "status"),
        ("customers", "city"),
        ("products", "name"),
    ]

    lines = ["Example values:"]

    with engine.connect() as conn:
        for table, col in hints:
            rows = conn.execute(
                text(f"SELECT DISTINCT {col} FROM {table} LIMIT :limit"),
                {"limit": limit}
            ).fetchall()

            values = ", ".join(str(r[0]) for r in rows)
            lines.append(f"  {table}.{col}: {values}")

    return "\n".join(lines)


if __name__ == "__main__":
    print(load_schema())
    print(load_value_hints())
