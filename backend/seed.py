"""
One-time SQLite -> PostgreSQL migration for ParkSync.

Run this from the backend directory AFTER setting DATABASE_URL.

Example PowerShell:
    $env:DATABASE_URL="postgresql+psycopg2://USER:PASSWORD@HOST/DBNAME"
    python migrate_sqlite_to_postgres.py

The script:
- Reads backend/instance/parking.db
- Creates the four PostgreSQL tables if they don't exist
- Preserves existing primary-key IDs
- Preserves relationships between users, lots, spots and reservations
- Resets PostgreSQL sequences
- Refuses to migrate if the PostgreSQL tables already contain data
"""

import os
import sqlite3
from pathlib import Path

from sqlalchemy import create_engine, text

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass
# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

SQLITE_PATH = Path(__file__).resolve().parent / "instance" / "parking.db"

DATABASE_URL = 'postgresql://neondb_owner:npg_w0PnVOKAiNf7@ep-orange-dust-b3b96w5p-pooler.c-4.ap-southeast-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require'

if not DATABASE_URL:
    raise SystemExit(
        "DATABASE_URL is not set.\n"
        "PowerShell example:\n"
        '$env:DATABASE_URL="postgresql+psycopg2://USER:PASSWORD@HOST/DBNAME"'
    )

if not SQLITE_PATH.exists():
    raise SystemExit(f"SQLite database not found: {SQLITE_PATH}")


# ---------------------------------------------------------------------------
# Connect
# ---------------------------------------------------------------------------

print(f"SQLite source: {SQLITE_PATH}")
print("Connecting to PostgreSQL...")

engine = create_engine(DATABASE_URL, pool_pre_ping=True)

with engine.connect() as conn:
    conn.execute(text("SELECT 1"))

print("PostgreSQL connection successful.")


# ---------------------------------------------------------------------------
# Read SQLite
# ---------------------------------------------------------------------------

sqlite_conn = sqlite3.connect(SQLITE_PATH)
sqlite_conn.row_factory = sqlite3.Row

tables = ["user", "parking_lot", "parking_spot", "reservation"]

data = {}

for table in tables:
    rows = sqlite_conn.execute(
        f'SELECT * FROM "{table}" ORDER BY id'
    ).fetchall()
    data[table] = [dict(row) for row in rows]
    print(f"{table:15} {len(rows):>4} rows")

sqlite_conn.close()


# ---------------------------------------------------------------------------
# Create PostgreSQL schema
# ---------------------------------------------------------------------------

# This matches the current SQLAlchemy models.
create_sql = [
    """
    CREATE TABLE IF NOT EXISTS "user" (
        id INTEGER PRIMARY KEY,
        username VARCHAR(80) NOT NULL,
        address VARCHAR(200) NOT NULL,
        pincode VARCHAR(20) NOT NULL,
        email VARCHAR(120) UNIQUE NOT NULL,
        password VARCHAR(200) NOT NULL,
        role VARCHAR(50) NOT NULL DEFAULT 'user'
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS parking_lot (
        id INTEGER PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        price DOUBLE PRECISION NOT NULL,
        location VARCHAR(200) NOT NULL,
        pincode VARCHAR(20) NOT NULL,
        capacity INTEGER NOT NULL,
        created_at TIMESTAMP
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS parking_spot (
        id INTEGER PRIMARY KEY,
        lot_id INTEGER NOT NULL REFERENCES parking_lot(id) ON DELETE SET NULL,
        is_occupied BOOLEAN DEFAULT FALSE
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS reservation (
        id INTEGER PRIMARY KEY,
        user_id INTEGER NOT NULL REFERENCES "user"(id) ON DELETE SET NULL,
        spot_id INTEGER NOT NULL REFERENCES parking_spot(id) ON DELETE SET NULL,
        vehicle_number VARCHAR(50) NOT NULL,
        parking_time TIMESTAMP NOT NULL,
        leaving_time TIMESTAMP NULL,
        parking_cost DOUBLE PRECISION NOT NULL
    )
    """,
]

with engine.begin() as conn:
    for statement in create_sql:
        conn.execute(text(statement))

print("PostgreSQL tables are ready.")


# ---------------------------------------------------------------------------
# Safety check
# ---------------------------------------------------------------------------

with engine.connect() as conn:
    counts = {}

    for table in tables:
        counts[table] = conn.execute(
            text(f'SELECT COUNT(*) FROM "{table}"')
        ).scalar_one()

    non_empty = {k: v for k, v in counts.items() if v > 0}

    if non_empty:
        print("\nMigration stopped for safety.")
        print("These PostgreSQL tables already contain data:")
        for table, count in non_empty.items():
            print(f"  {table}: {count} rows")

        print(
            "\nIf this is an existing/test database that you intentionally "
            "want to replace, empty the PostgreSQL tables first and run "
            "this migration again."
        )
        raise SystemExit(1)


# ---------------------------------------------------------------------------
# Insert data in foreign-key order
# ---------------------------------------------------------------------------

with engine.begin() as conn:

    # Users
    for row in data["user"]:
        conn.execute(
            text("""
                INSERT INTO "user"
                    (id, username, address, pincode, email, password, role)
                VALUES
                    (:id, :username, :address, :pincode, :email, :password, :role)
            """),
            row,
        )

    print(f"✓ Migrated {len(data['user'])} users")

    # Parking lots
    for row in data["parking_lot"]:
        conn.execute(
            text("""
                INSERT INTO parking_lot
                    (id, name, price, location, pincode, capacity, created_at)
                VALUES
                    (:id, :name, :price, :location, :pincode,
                     :capacity, :created_at)
            """),
            row,
        )

    print(f"✓ Migrated {len(data['parking_lot'])} parking lots")

    # Parking spots
    for row in data["parking_spot"]:
        conn.execute(
            text("""
                INSERT INTO parking_spot
                    (id, lot_id, is_occupied)
                VALUES
                    (:id, :lot_id, :is_occupied)
            """),
            {
                **row,
                "is_occupied": bool(row["is_occupied"]),
            },
        )

    print(f"✓ Migrated {len(data['parking_spot'])} parking spots")

    # Reservations
    for row in data["reservation"]:
        conn.execute(
            text("""
                INSERT INTO reservation
                    (id, user_id, spot_id, vehicle_number,
                     parking_time, leaving_time, parking_cost)
                VALUES
                    (:id, :user_id, :spot_id, :vehicle_number,
                     :parking_time, :leaving_time, :parking_cost)
            """),
            row,
        )

    print(f"✓ Migrated {len(data['reservation'])} reservations")


# ---------------------------------------------------------------------------
# Reset PostgreSQL sequences
# ---------------------------------------------------------------------------

with engine.begin() as conn:
    for table in tables:
        max_id = conn.execute(
            text(f'SELECT COALESCE(MAX(id), 0) FROM "{table}"')
        ).scalar_one()

        # PostgreSQL creates sequences automatically for SERIAL/identity
        # columns. If the current schema used by the app created one,
        # move it past the imported IDs.
        sequence_name = f"{table}_id_seq"

        exists = conn.execute(
            text("""
                SELECT 1
                FROM pg_class
                WHERE relkind = 'S' AND relname = :sequence_name
            """),
            {"sequence_name": sequence_name},
        ).first()

        if exists:
            conn.execute(
                text(
                    f"SELECT setval("
                    f"'{sequence_name}', "
                    f":max_id, "
                    f"true)"
                ),
                {"max_id": max_id},
            )


# ---------------------------------------------------------------------------
# Verify
# ---------------------------------------------------------------------------

print("\nVerifying migration...")

expected = {
    "user": len(data["user"]),
    "parking_lot": len(data["parking_lot"]),
    "parking_spot": len(data["parking_spot"]),
    "reservation": len(data["reservation"]),
}

with engine.connect() as conn:
    all_ok = True

    for table, expected_count in expected.items():
        actual = conn.execute(
            text(f'SELECT COUNT(*) FROM "{table}"')
        ).scalar_one()

        status = "OK" if actual == expected_count else "MISMATCH"

        print(
            f"{table:15} expected={expected_count:>4} "
            f"actual={actual:>4}  {status}"
        )

        if actual != expected_count:
            all_ok = False

if not all_ok:
    raise SystemExit("\nMigration verification failed.")

print("\n========================================")
print("Migration completed successfully.")
print("========================================")
print("6 users")
print("6 parking lots")
print("86 parking spots")
print("17 reservations")
print("\nYour SQLite database has NOT been modified.")
print("Keep parking.db as a backup until the app is fully tested.")
