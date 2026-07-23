"""
SQLite Helper
Sprint 2
"""

from __future__ import annotations

import sqlite3
from pathlib import Path
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]

DATABASE = ROOT / "data" / "nifty100.db"


class SQLiteDB:

    def __init__(self):

        self.conn = sqlite3.connect(DATABASE)

        self.conn.row_factory = sqlite3.Row

        self.cursor = self.conn.cursor()


    # =====================================================
    # Read Table
    # =====================================================
    def read_table(self, table_name):

        return self.table(table_name)
    
    
    def get_connection():

        return sqlite3.connect(DATABASE)
    
    def table(self, table_name):

        query = f"SELECT * FROM {table_name}"

        return pd.read_sql_query(
            query,
            self.conn
        )


    # =====================================================
    # Execute Query
    # =====================================================

    def execute(
            self,
            sql,
            params=None
    ):

        if params is None:

            self.cursor.execute(sql)

        else:

            self.cursor.execute(
                sql,
                params
            )

        self.conn.commit()


    # =====================================================
    # Fetch All
    # =====================================================

    def fetchall(
            self,
            sql,
            params=None
    ):

        if params is None:

            self.cursor.execute(sql)

        else:

            self.cursor.execute(
                sql,
                params
            )

        return self.cursor.fetchall()


    # =====================================================
    # Fetch One
    # =====================================================

    def fetchone(
            self,
            sql,
            params=None
    ):

        if params is None:

            self.cursor.execute(sql)

        else:

            self.cursor.execute(
                sql,
                params
            )

        return self.cursor.fetchone()


    # =====================================================
    # Replace Table
    # =====================================================

    def replace_table(
            self,
            dataframe,
            table_name
    ):

        dataframe.to_sql(

            table_name,

            self.conn,

            if_exists="replace",

            index=False

        )


    # =====================================================
    # Append
    # =====================================================

    def append_table(
            self,
            dataframe,
            table_name
    ):

        dataframe.to_sql(

            table_name,

            self.conn,

            if_exists="append",

            index=False

        )


    # =====================================================
    # Row Count
    # =====================================================

    def row_count(
            self,
            table_name
    ):

        sql = f"""

        SELECT COUNT(*)

        FROM {table_name}

        """

        self.cursor.execute(sql)

        return self.cursor.fetchone()[0]


    # =====================================================
    # Company Years
    # =====================================================

    def company_years(self):

        sql = """

        SELECT company_id,

               year

        FROM profitandloss

        ORDER BY company_id, year

        """

        return pd.read_sql_query(

            sql,

            self.conn

        )


    # =====================================================
    # Close
    # =====================================================

    def close(self):

        self.conn.close()


# =========================================================
# Example
# =========================================================

if __name__ == "__main__":

    db = SQLiteDB()

    print(

        db.row_count(

            "profitandloss"

        )

    )

    db.close()