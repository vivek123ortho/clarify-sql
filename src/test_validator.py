from sql_validator import validate_sql, UnsafeSQLError

CASES = [
    ("SELECT * FROM customers", True),
    ("SELECT c.name FROM customers c JOIN orders o ON o.customer_id = c.customer_id", True),
    ("WITH t AS (SELECT 1 AS x) SELECT * FROM t", True),
    ("DROP TABLE orders", False),
    ("DELETE FROM orders", False),
    ("UPDATE orders SET status = 'x'", False),
    ("SELECT 1; DROP TABLE orders;", False),
    ("INSERT INTO customers (name) VALUES ('x')", False),
    ("", False),
]

ok_count = 0
for sql, should_pass in CASES:
    try:
        validate_sql(sql)
        passed = True
    except UnsafeSQLError:
        passed = False
    ok = passed == should_pass
    ok_count += ok
    print(f"[{'OK' if ok else 'WRONG'}] {sql!r} -> {'allowed' if passed else 'blocked'}")

print(f"\n{ok_count}/{len(CASES)}")