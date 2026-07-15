import sqlite3
import pandas as pd

DB_PATH = "data/nifty100.db"


class DatabaseManager:

    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH)

    def execute_query(self, query):
        cursor = self.conn.cursor()
        cursor.execute(query)
        return cursor.fetchall()

    def read_table(self, table_name):
        return pd.read_sql_query(
            f"SELECT * FROM {table_name}",
            self.conn
        )

    def row_count(self, table_name):
        cursor = self.conn.cursor()
        cursor.execute(
            f"SELECT COUNT(*) FROM {table_name}"
        )
        return cursor.fetchone()[0]

    def list_tables(self):
        cursor = self.conn.cursor()

        cursor.execute("""
            SELECT name
            FROM sqlite_master
            WHERE type='table'
            ORDER BY name
        """)

        return [row[0] for row in cursor.fetchall()]

    def close(self):
        self.conn.close()