import sqlite3
import pytest


@pytest.fixture
def test_db(tmp_path):
    db_path = tmp_path / "test_erp.db"

    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE equipment (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            equipment_type TEXT NOT NULL,
            daily_rate REAL NOT NULL,
            available INTEGER NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE customers (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            email TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE rentals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER NOT NULL,
            equipment_id INTEGER NOT NULL,
            days INTEGER NOT NULL,
            total_amount REAL NOT NULL,
            returned INTEGER NOT NULL DEFAULT 0
        )
    """)

    connection.commit()
    connection.close()

    return db_path