import sqlite3
from schema import create_tables

conn = sqlite3.connect("data/nifty100.db")

create_tables(conn)

conn.close()

print("Database created successfully.")