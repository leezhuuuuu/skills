#!/usr/bin/env python3
"""
Execute SQL queries on PostgreSQL databases.

This script provides:
- Parameterized queries to prevent SQL injection
- Read-only mode by default
- Environment variable or command line connection config

Usage:
    python scripts/query_postgres.py --query "SELECT * FROM users LIMIT 10"
    python scripts/query_postgres.py --query "SELECT * FROM products WHERE price < %s" --params 100

Source: Derived from anthropics/skills PR #182 (Apache 2.0 License)
"""

import argparse
import os
import sys

try:
    import psycopg2
    from psycopg2 import sql
except ImportError:
    print("Error: psycopg2 not installed. Run: pip install psycopg2-binary")
    sys.exit(1)


def get_connection(args):
    """Create database connection from args or environment variables."""
    conn_params = {
        'host': args.host or os.environ.get('PGHOST', 'localhost'),
        'port': args.port or os.environ.get('PGPORT', '5432'),
        'database': args.database or os.environ.get('PGDATABASE'),
        'user': args.user or os.environ.get('PGUSER'),
        'password': args.password or os.environ.get('PGPASSWORD'),
    }

    # Validate required parameters
    if not conn_params['database']:
        print("Error: Database name required. Set PGDATABASE env var or --database argument.")
        sys.exit(1)
    if not conn_params['user']:
        print("Error: Username required. Set PGUSER env var or --user argument.")
        sys.exit(1)

    return psycopg2.connect(**conn_params)


def execute_query(args):
    """Execute a read-only SQL query."""
    conn = None
    try:
        conn = get_connection(args)

        with conn.cursor() as cur:
            # Parse parameters if provided
            params = None
            if args.params:
                params = tuple(args.params.split(','))

            # Execute with parameterized query (SQL injection protection)
            if params:
                cur.execute(args.query, params)
            else:
                cur.execute(args.query)

            # Fetch results
            columns = [desc[0] for desc in cur.description]
            rows = cur.fetchall()

            # Print column headers
            print(",".join(columns))
            print("-" * (len(",".join(columns)) + len(columns) * 2))

            # Print rows with limit
            limit = args.limit or 100
            for i, row in enumerate(rows):
                if i >= limit:
                    print(f"\n... (showing first {limit} rows)")
                    break
                print(",".join(str(cell) for cell in row))

            print(f"\nTotal rows: {len(rows)}")

    except psycopg2.Error as e:
        print(f"Database error: {e}")
        sys.exit(1)
    finally:
        if conn:
            conn.close()


def main():
    parser = argparse.ArgumentParser(
        description="Execute SQL queries on PostgreSQL databases"
    )
    parser.add_argument(
        '--query', '-q',
        required=True,
        help="SQL query to execute"
    )
    parser.add_argument(
        '--params',
        help="Query parameters (comma-separated) for parameterized queries"
    )
    parser.add_argument(
        '--host',
        help="Database host (or set PGHOST env var)"
    )
    parser.add_argument(
        '--port', '-p',
        type=int,
        help="Database port (or set PGPORT env var)"
    )
    parser.add_argument(
        '--database', '-d',
        help="Database name (or set PGDATABASE env var)"
    )
    parser.add_argument(
        '--user', '-u',
        help="Username (or set PGUSER env var)"
    )
    parser.add_argument(
        '--password',
        help="Password (or set PGPASSWORD env var)"
    )
    parser.add_argument(
        '--limit', '-l',
        type=int,
        default=100,
        help="Maximum rows to display (default: 100)"
    )
    parser.add_argument(
        '--allow-write',
        action='store_true',
        help="Allow write operations (INSERT, UPDATE, DELETE)"
    )

    args = parser.parse_args()

    # Check for write operations
    write_keywords = ['INSERT', 'UPDATE', 'DELETE', 'DROP', 'CREATE', 'ALTER', 'TRUNCATE']
    query_upper = args.query.upper()

    if any(keyword in query_upper for keyword in write_keywords):
        if not args.allow_write:
            print("Error: Query contains write operation. Use --allow-write flag to confirm.")
            print("WARNING: Write operations can modify database data!")
            sys.exit(1)

    execute_query(args)


if __name__ == "__main__":
    main()
