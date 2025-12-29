---
name: postgresql-query
description: Execute SQL queries and explore PostgreSQL database structures. Use when Claude needs to connect to PostgreSQL databases, list tables, or run read-only queries. Supports parameterized queries to prevent SQL injection and environment variable configuration.
---

# PostgreSQL Query Skill

> **Source**: This skill is derived from [anthropics/skills PR #182](https://github.com/anthropics/skills/pull/182) by @kevics1.

Execute SQL queries and explore PostgreSQL database structures safely.

## Installation

```bash
pip install psycopg2-binary
```

## Connection Methods

### Environment Variables (Recommended)

```bash
export PGHOST=localhost
export PGPORT=5432
export PGDATABASE=mydb
export PGUSER=myuser
export PGPASSWORD=mypassword
```

### Command Line Arguments

```bash
python scripts/query_postgres.py \
    --host localhost \
    --port 5432 \
    --database mydb \
    --user myuser \
    --query "SELECT * FROM users LIMIT 10"
```

## Core Functions

### Execute Read-Only Query

```bash
python scripts/query_postgres.py --query "SELECT * FROM users LIMIT 10"
```

### List Database Tables

```bash
python scripts/list_tables.py
```

### Query with Parameters (SQL Injection Protection)

```python
import psycopg2
import os

conn = psycopg2.connect(
    host=os.environ.get('PGHOST', 'localhost'),
    port=os.environ.get('PGPORT', '5432'),
    database=os.environ['PGDATABASE'],
    user=os.environ['PGUSER'],
    password=os.environ['PGPASSWORD']
)

try:
    with conn.cursor() as cur:
        # Parameterized query prevents SQL injection
        cur.execute("SELECT * FROM users WHERE active = %s", (True,))
        rows = cur.fetchall()
        for row in rows:
            print(row)
finally:
    conn.close()
```

## Security Features

| Feature | Description |
|---------|-------------|
| **Parameterized Queries** | Prevents SQL injection with `%s` placeholders |
| **Read-Only by Default** | Write operations require `--allow-write` flag |
| **LIMIT Enforcement** | Default query limit prevents large result sets |
| **Connection Management** | Automatic cleanup with `with` statements |

## Example Workflows

### Explore Database Structure

```bash
# List all tables
python scripts/list_tables.py

# Get table schema
python scripts/query_postgres.py --query "
SELECT column_name, data_type, is_nullable
FROM information_schema.columns
WHERE table_name = 'users'
ORDER BY ordinal_position
"
```

### Query Data Safely

```bash
# Read-only query with limit
python scripts/query_postgres.py --query "SELECT * FROM products WHERE price < 100 LIMIT 20"

# Aggregation queries
python scripts/query_postgres.py --query "SELECT category, COUNT(*) FROM products GROUP BY category"
```

### Write Operations (Requires Explicit Flag)

```bash
# Requires --allow-write flag
python scripts/query_postgres.py \
    --allow-write \
    --query "INSERT INTO audit_log (action) VALUES ('test')"
```

## Best Practices

1. **Always use parameterized queries** for user input
2. **Limit result sets** with LIMIT clause
3. **Use environment variables** for credentials (not command line)
4. **Prefer read-only mode** for data exploration
5. **Handle large results** with `fetchmany()` for memory efficiency

## Resources

- **psycopg2 Documentation**: https://www.psycopg.org/docs/
- **PostgreSQL Python Interface**: https://www.postgresql.org/docs/current/libpq.html
