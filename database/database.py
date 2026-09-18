import sqlite3
import os
from contextlib import contextmanager
from pathlib import Path
from config.config import DB_PATH
from utils.logger import get_logger

logger = get_logger(__name__)

@contextmanager
def get_connection(db_path=None):
    """
    Context manager to yield a database connection.
    Ensures that foreign keys are enabled and connection is closed properly.
    """
    db_path = db_path or DB_PATH
    conn = None
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        yield conn
    except sqlite3.Error as e:
        logger.error(f"Database connection error: {e}")
        raise
    finally:
        if conn:
            conn.close()

def execute_query(query: str, params: tuple = (), db_path=None):
    """Execute a query that modifies the database (INSERT, UPDATE, DELETE)."""
    db_path = db_path or DB_PATH
    with get_connection(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        return cursor.lastrowid

def fetch_one(query: str, params: tuple = (), db_path=None):
    """Execute a query and fetch a single row."""
    db_path = db_path or DB_PATH
    with get_connection(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        row = cursor.fetchone()
        return dict(row) if row else None

def fetch_all(query: str, params: tuple = (), db_path=None):
    """Execute a query and fetch all rows."""
    db_path = db_path or DB_PATH
    with get_connection(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        rows = cursor.fetchall()
        return [dict(row) for row in rows]

def initialize_database(db_path=None):
    """Initialize the database schema from schema.sql."""
    schema_path = Path(__file__).resolve().parent / "schema.sql"
    
    if not schema_path.exists():
        logger.error(f"Schema file not found at {schema_path}")
        raise FileNotFoundError(f"Schema file not found at {schema_path}")
        
    with open(schema_path, "r") as f:
        schema_sql = f.read()

    db_path = db_path or DB_PATH
    with get_connection(db_path) as conn:
        try:
            conn.executescript(schema_sql)
            conn.commit()
            logger.info("Database initialized successfully.")
        except sqlite3.Error as e:
            logger.error(f"Error initializing database: {e}")
            raise
