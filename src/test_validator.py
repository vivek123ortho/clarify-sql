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
    ("SELECT * FROM customers; SELECT * FROM orders", False),
    ("WITH d AS (DELETE FROM orders RETURNING *) SELECT * FROM d", False),
    ("SELECT * INTO new_table FROM customers", False),
    ("select pg_sleep(30)", False),
    ("SELECT * FROM customers WHERE 1=1 AND pg_sleep(1) IS NOT NULL", False),
    ("SELECT pg_catalog.pg_sleep(5)", False),
    ("SELECT name FROM customers WHERE city = 'Pune'", True),
    ("SELECT c.name, SUM(o.total_amount) FROM customers c JOIN orders o ON o.customer_id = c.customer_id GROUP BY c.name", True),
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