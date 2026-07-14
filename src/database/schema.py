import sqlite3


def create_tables(conn):
    """
    Create all database tables.
    """

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS companies (

            id TEXT PRIMARY KEY,

            company_logo TEXT,

            company_name TEXT,

            chart_link TEXT,

            about_company TEXT,

            website TEXT,

            nse_profile TEXT,

            bse_profile TEXT,

            face_value REAL,

            book_value REAL,

            roce_percentage REAL,

            roe_percentage REAL

        )
    """)

    conn.commit()