import pandas as pd
import os

DATA_PATH = "data/raw"

files = [f for f in os.listdir(DATA_PATH) if f.endswith(".xlsx")]

for file in files:

    print("\n" + "=" * 80)
    print(file)
    print("=" * 80)

    excel = pd.ExcelFile(os.path.join(DATA_PATH, file))

    for sheet in excel.sheet_names:

        print(f"\nSheet: {sheet}")

        # Read WITHOUT assuming any header
        df = pd.read_excel(
            os.path.join(DATA_PATH, file),
            sheet_name=sheet,
            header=None
        )

        print(df.head(10))