#!/usr/bin/env python3
"""
List all tables in a PostgreSQL database.

This script displays:
- All tables in the public schema
- Row counts for each table
- Table sizes

Usage:
    python scripts/list_tables.py

Source: Derived from anthropics/skills PR #182 (Apache 2.0 License)
"""

import argparse
import os
import sys

try:
    import psycopg2
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

    if not conn_params['database']:
        print("Error: Database name required. Set PGDATABASE env var or --database argument.")
        sys.exit(1)
    if not conn_params['user']:
        print("Error: Username required. Set PGUSER env var or --user argument.")
        sys.exit(1)

    return psycopg2.connect(**conn_params)


def list_tables(args):
    """List all tables in the database."""
    conn = None
    try:
        conn = get_connection(args)

        with conn.cursor() as cur:
            # Get all table names
            cur.execute("""
                SELECT
                    table_name
                FROM information_schema.tables
                WHERE table_schema = 'public'
                ORDER BY table_name
            """)

            tables = [row[0] for row in cur.fetchall()]

            if not tables:
                print("No tables found in public schema.")
                return

            # Display table list
            print("Tables in database:")
            print("-" * 50)
            for table in tables:
                print(f"  - {table}")
            print("-" * 50)
            print(f"Total: {len(tables)} tables")

            # Get detailed info
            if args.verbose:
                print("\nDetailed table information:")
                print("-" * 80)
                for table in tables:
                    # Get row count
                    cur.execute(f"SELECT COUNT(*) FROM {table}")
                    count = cur.fetchone()[0]

                    # Get table size
                    cur.execute("""
                        SELECT pg_size_pretty(pg_total_relation_size(%s))
                    """, (table,))
                    size = cur.fetchone()[0]

                    print(f"  {table}: {count:,} rows ({size})")

    except psycopg2.Error as e:
        print(f"Database error: {e}")
        sys.exit(1)
    finally:
        if conn:
            conn.close()


def main():
    parser = argparse.ArgumentParser(
        description="List all tables in a PostgreSQL database"
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
        '--verbose', '-v',
        action='store_true',
        help="Show detailed information including row counts"
    )

    args = parser.parse_args()
    list_tables(args)


if __name__ == "__main__":
    main()
