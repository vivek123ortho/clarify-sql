import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, inspect

load_dotenv()


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


if __name__ == "__main__":
    print(load_schema())
    