import sqlite3
from datetime import datetime


DATABASE_NAME = "bmi_tracker.db"


def get_connection():
    return sqlite3.connect(DATABASE_NAME)


def initialize_database():
    connection = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS bmi_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                weight REAL NOT NULL,
                height REAL NOT NULL,
                bmi REAL NOT NULL,
                category TEXT NOT NULL,
                recorded_at TEXT NOT NULL,

                FOREIGN KEY (user_id)
                REFERENCES users(id)
            )
        """)

        connection.commit()

    except sqlite3.Error as error:
        raise RuntimeError(
            f"Could not initialize the database: {error}"
        )

    finally:
        if connection:
            connection.close()


def get_users():
    connection = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT id, name
            FROM users
            ORDER BY name
        """)

        return cursor.fetchall()

    except sqlite3.Error as error:
        raise RuntimeError(
            f"Could not read users from the database: {error}"
        )

    finally:
        if connection:
            connection.close()


def add_user(name):
    connection = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            "INSERT INTO users (name) VALUES (?)",
            (name,)
        )

        connection.commit()

        return cursor.lastrowid

    except sqlite3.IntegrityError:
        raise RuntimeError(
            f"The username '{name}' already exists. "
            "Please choose a different name."
        )

    except sqlite3.Error as error:
        raise RuntimeError(
            f"Could not add user: {error}"
        )

    finally:
        if connection:
            connection.close()


def save_bmi_record(user_id, weight, height, bmi, category):
    connection = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        recorded_at = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        cursor.execute("""
            INSERT INTO bmi_records
            (user_id, weight, height, bmi, category, recorded_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            user_id,
            weight,
            height,
            bmi,
            category,
            recorded_at
        ))

        connection.commit()

    except sqlite3.Error as error:
        raise RuntimeError(
            f"Could not save BMI record: {error}"
        )

    finally:
        if connection:
            connection.close()


def get_bmi_history(user_id):
    connection = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT bmi, category, recorded_at, weight, height
            FROM bmi_records
            WHERE user_id = ?
            ORDER BY recorded_at
        """, (user_id,))

        return cursor.fetchall()

    except sqlite3.Error as error:
        raise RuntimeError(
            f"Could not read BMI history: {error}"
        )

    finally:
        if connection:
            connection.close()