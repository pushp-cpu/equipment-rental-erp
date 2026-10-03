import os
import sqlite3

import psycopg2


DATABASE_PATH = "erp.db"
DATABASE_URL = os.getenv("DATABASE_URL")


def using_postgres():
    return bool(DATABASE_URL)


def get_connection():
    if using_postgres():
        return psycopg2.connect(DATABASE_URL)

    return sqlite3.connect(DATABASE_PATH)


def set_database_path(path):
    global DATABASE_PATH
    DATABASE_PATH = path


def create_tables():
    connection = get_connection()
    cursor = connection.cursor()

    if using_postgres():
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS equipment (
                id SERIAL PRIMARY KEY,
                name TEXT NOT NULL,
                equipment_type TEXT NOT NULL,
                daily_rate DOUBLE PRECISION NOT NULL,
                available BOOLEAN NOT NULL
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS customers (
                id SERIAL PRIMARY KEY,
                name TEXT NOT NULL,
                phone TEXT NOT NULL,
                email TEXT NOT NULL
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS rentals (
                id SERIAL PRIMARY KEY,
                customer_id INTEGER NOT NULL,
                equipment_id INTEGER NOT NULL,
                days INTEGER NOT NULL,
                total_amount DOUBLE PRECISION NOT NULL,
                returned BOOLEAN NOT NULL DEFAULT FALSE
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL
            )
        """)

    else:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS equipment (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                equipment_type TEXT NOT NULL,
                daily_rate REAL NOT NULL,
                available INTEGER NOT NULL
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                phone TEXT NOT NULL,
                email TEXT NOT NULL
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS rentals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id INTEGER NOT NULL,
                equipment_id INTEGER NOT NULL,
                days INTEGER NOT NULL,
                total_amount REAL NOT NULL,
                returned INTEGER NOT NULL DEFAULT 0
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL
            )
        """)

        cursor.execute("PRAGMA table_info(rentals)")
        columns = [column[1] for column in cursor.fetchall()]

        if "returned" not in columns:
            cursor.execute("""
                ALTER TABLE rentals
                ADD COLUMN returned INTEGER NOT NULL DEFAULT 0
            """)

            cursor.execute("""
                UPDATE rentals
                SET returned = 1
                WHERE equipment_id IN (
                    SELECT id
                    FROM equipment
                    WHERE available = 1
                )
            """)

    connection.commit()
    connection.close()


# --------------------------------------------------
# Equipment
# --------------------------------------------------

def add_equipment_to_db(equipment):
    connection = get_connection()
    cursor = connection.cursor()

    if using_postgres():
        cursor.execute("""
            INSERT INTO equipment
            (name, equipment_type, daily_rate, available)
            VALUES (%s, %s, %s, %s)
            RETURNING id
        """, (
            equipment.name,
            equipment.equipment_type,
            equipment.daily_rate,
            equipment.available
        ))

        equipment_id = cursor.fetchone()[0]

    else:
        cursor.execute("""
            INSERT INTO equipment
            (name, equipment_type, daily_rate, available)
            VALUES (?, ?, ?, ?)
        """, (
            equipment.name,
            equipment.equipment_type,
            equipment.daily_rate,
            equipment.available
        ))

        equipment_id = cursor.lastrowid

    connection.commit()
    connection.close()

    return equipment_id


def get_all_equipment():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM equipment
    """)

    equipment = cursor.fetchall()

    connection.close()

    return equipment


def get_equipment_by_id(equipment_id):
    connection = get_connection()
    cursor = connection.cursor()

    placeholder = "%s" if using_postgres() else "?"

    cursor.execute(
        f"""
        SELECT *
        FROM equipment
        WHERE id = {placeholder}
        """,
        (equipment_id,)
    )

    equipment = cursor.fetchone()

    connection.close()

    return equipment


def update_equipment_availability(equipment_id, available):
    connection = get_connection()
    cursor = connection.cursor()

    placeholder = "%s" if using_postgres() else "?"

    cursor.execute(
        f"""
        UPDATE equipment
        SET available = {placeholder}
        WHERE id = {placeholder}
        """,
        (available, equipment_id)
    )

    connection.commit()
    connection.close()


# --------------------------------------------------
# Customers
# --------------------------------------------------

def add_customer_to_db(customer):
    connection = get_connection()
    cursor = connection.cursor()

    if using_postgres():
        cursor.execute("""
            INSERT INTO customers
            (name, phone, email)
            VALUES (%s, %s, %s)
            RETURNING id
        """, (
            customer.name,
            customer.phone,
            customer.email
        ))

        customer_id = cursor.fetchone()[0]

    else:
        cursor.execute("""
            INSERT INTO customers
            (name, phone, email)
            VALUES (?, ?, ?)
        """, (
            customer.name,
            customer.phone,
            customer.email
        ))

        customer_id = cursor.lastrowid

    connection.commit()
    connection.close()

    return customer_id


def get_all_customers():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM customers
    """)

    customers = cursor.fetchall()

    connection.close()

    return customers


def get_customer_by_id(customer_id):
    connection = get_connection()
    cursor = connection.cursor()

    placeholder = "%s" if using_postgres() else "?"

    cursor.execute(
        f"""
        SELECT *
        FROM customers
        WHERE id = {placeholder}
        """,
        (customer_id,)
    )

    customer = cursor.fetchone()

    connection.close()

    return customer


# --------------------------------------------------
# Rentals
# --------------------------------------------------

def add_rental_to_db(rental):
    connection = get_connection()
    cursor = connection.cursor()

    placeholder = "%s" if using_postgres() else "?"

    cursor.execute(
        f"""
        INSERT INTO rentals
        (id, customer_id, equipment_id, days, total_amount)
        VALUES ({placeholder}, {placeholder}, {placeholder}, {placeholder}, {placeholder})
        """,
        (
            rental.rental_id,
            rental.customer.customer_id,
            rental.equipment.equipment_id,
            rental.days,
            rental.total_amount
        )
    )

    connection.commit()
    connection.close()


def get_all_rentals():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM rentals
    """)

    rentals = cursor.fetchall()

    connection.close()

    return rentals


def get_all_rentals_detailed():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            rentals.id,
            rentals.customer_id,
            customers.name,
            rentals.equipment_id,
            equipment.name,
            rentals.days,
            rentals.total_amount,
            rentals.returned
        FROM rentals
        JOIN customers
            ON rentals.customer_id = customers.id
        JOIN equipment
            ON rentals.equipment_id = equipment.id
        ORDER BY rentals.id
    """)

    rentals = cursor.fetchall()

    connection.close()

    return rentals


def create_rental_transaction(
    customer_id,
    equipment_id,
    days,
    total_amount
):
    connection = get_connection()
    cursor = connection.cursor()

    placeholder = "%s" if using_postgres() else "?"

    try:
        if using_postgres():
            cursor.execute("""
                INSERT INTO rentals
                (customer_id, equipment_id, days, total_amount)
                VALUES (%s, %s, %s, %s)
                RETURNING id
            """, (
                customer_id,
                equipment_id,
                days,
                total_amount
            ))

            rental_id = cursor.fetchone()[0]

            cursor.execute("""
                UPDATE equipment
                SET available = FALSE
                WHERE id = %s
            """, (equipment_id,))

        else:
            cursor.execute("""
                INSERT INTO rentals
                (customer_id, equipment_id, days, total_amount)
                VALUES (?, ?, ?, ?)
            """, (
                customer_id,
                equipment_id,
                days,
                total_amount
            ))

            rental_id = cursor.lastrowid

            cursor.execute("""
                UPDATE equipment
                SET available = 0
                WHERE id = ?
            """, (equipment_id,))

        connection.commit()

        return rental_id

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


def get_rental_by_id(rental_id):
    connection = get_connection()
    cursor = connection.cursor()

    placeholder = "%s" if using_postgres() else "?"

    cursor.execute(
        f"""
        SELECT *
        FROM rentals
        WHERE id = {placeholder}
        """,
        (rental_id,)
    )

    rental = cursor.fetchone()

    connection.close()

    return rental


def return_rental(rental_id):
    connection = get_connection()
    cursor = connection.cursor()

    placeholder = "%s" if using_postgres() else "?"

    try:
        cursor.execute(
            f"""
            UPDATE rentals
            SET returned = {'TRUE' if using_postgres() else '1'}
            WHERE id = {placeholder}
            """,
            (rental_id,)
        )

        cursor.execute(
            f"""
            SELECT equipment_id
            FROM rentals
            WHERE id = {placeholder}
            """,
            (rental_id,)
        )

        result = cursor.fetchone()

        if result is None:
            connection.rollback()
            return None

        equipment_id = result[0]

        cursor.execute(
            f"""
            UPDATE equipment
            SET available = {'TRUE' if using_postgres() else '1'}
            WHERE id = {placeholder}
            """,
            (equipment_id,)
        )

        connection.commit()

        return equipment_id

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


# --------------------------------------------------
# Authentication
# --------------------------------------------------

def create_user(username, password_hash):
    connection = get_connection()
    cursor = connection.cursor()

    placeholder = "%s" if using_postgres() else "?"

    try:
        cursor.execute(
            f"""
            INSERT INTO users
            (username, password_hash)
            VALUES ({placeholder}, {placeholder})
            """,
            (
                username,
                password_hash
            )
        )

        connection.commit()

    finally:
        connection.close()


def get_user_by_username(username):
    connection = get_connection()
    cursor = connection.cursor()

    placeholder = "%s" if using_postgres() else "?"

    cursor.execute(
        f"""
        SELECT
            id,
            username,
            password_hash
        FROM users
        WHERE username = {placeholder}
        """,
        (username,)
    )

    user = cursor.fetchone()

    connection.close()

    return user