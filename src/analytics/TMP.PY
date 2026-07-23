import pandas as pd

df = pd.read_excel(
    "data/raw/balancesheet.xlsx",
    header=1      # <-- use the second row as the header
)

print(df[df["company_id"] == "BEL"].tail(10))