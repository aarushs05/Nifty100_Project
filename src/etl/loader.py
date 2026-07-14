import os
import pandas as pd
from loguru import logger
from etl.normaliser import normalize_dataframe

DATA_PATH = "data/raw"

REPORT_FILES = {
    "companies.xlsx",
    "profitandloss.xlsx",
    "balancesheet.xlsx",
    "cashflow.xlsx",
    "analysis.xlsx",
    "documents.xlsx",
    "prosandcons.xlsx",
}


class ExcelLoader:

    def __init__(self, data_path=DATA_PATH):
        self.data_path = data_path
        self.dataframes = {}

    def load_all(self):

        files = [
            f for f in os.listdir(self.data_path)
            if f.endswith(".xlsx")
        ]

        logger.info(f"Found {len(files)} Excel files")

        for file in files:

            path = os.path.join(self.data_path, file)

            try:

                if file in REPORT_FILES:
                    df = pd.read_excel(path, header=1)

                else:
                    df = pd.read_excel(path)

                df = normalize_dataframe(df)
                self.dataframes[file] = df

                logger.success(
                    f"{file} loaded "
                    f"({len(df)} rows × {len(df.columns)} columns)"
                )

            except Exception as e:

                logger.error(f"Error loading {file}")

                logger.error(e)

        return self.dataframes


if __name__ == "__main__":

    loader = ExcelLoader()

    datasets = loader.load_all()

    print("\n")

    for name, df in datasets.items():

        print("=" * 70)

        print(name)

        print(df.head())

        print()