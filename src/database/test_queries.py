from database_manager import DatabaseManager

db = DatabaseManager()

print("=" * 60)
print("DATABASE TEST")
print("=" * 60)

print("\nTables")
print(db.list_tables())

print("\nCompanies:", db.row_count("companies"))
print("Stock Prices:", db.row_count("stock_prices"))
print("Market Cap:", db.row_count("market_cap"))

print("\nFirst Five Companies")
print(db.read_table("companies").head())

db.close()