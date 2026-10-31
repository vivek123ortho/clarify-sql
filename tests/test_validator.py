import sys
sys.path.insert(0, "src")

import pytest
from sql_validator import validate_sql, UnsafeSQLError


@pytest.mark.parametrize("sql", [
    "SELECT * FROM customers",
    "WITH t AS (SELECT 1 AS x) SELECT * FROM t",
])
def test_allows_safe(sql):
    assert validate_sql(sql)


@pytest.mark.parametrize("sql", [
    "DROP TABLE orders",
    "SELECT 1; DROP TABLE orders;",
    "SELECT * INTO t FROM customers",
    "SELECT pg_catalog.pg_sleep(5)",
    "",
])
def test_blocks_unsafe(sql):
    with pytest.raises(UnsafeSQLError):
        validate_sql(sql)