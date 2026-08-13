import os

import pandas as pd
from loguru import logger

from src.etl.normaliser import normalize_dataframe

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
        self.audit_records = []

    def load_all(self):
        files = [
            file
            for file in os.listdir(self.data_path)
            if file.endswith(".xlsx")
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

                self.audit_records.append(
                    {
                        "file": file,
                        "status": "SUCCESS",
                        "rows": len(df),
                        "columns": len(df.columns),
                        "error": "",
                    }
                )

                logger.success(
                    f"{file} loaded "
                    f"({len(df)} rows × {len(df.columns)} columns)"
                )

            except (OSError, ValueError, ImportError) as e:
                self.audit_records.append(
                    {
                        "file": file,
                        "status": "FAILED",
                        "rows": 0,
                        "columns": 0,
                        "error": str(e),
                    }
                )

                logger.error(f"Error loading {file}")
                logger.error(e)

        self._write_audit()

        return self.dataframes

    def _write_audit(self):
        output_dir = "output"
        os.makedirs(output_dir, exist_ok=True)

        audit_df = pd.DataFrame(self.audit_records)

        audit_path = os.path.join(
            output_dir,
            "load_audit.csv",
        )

        audit_df.to_csv(
            audit_path,
            index=False,
        )

        logger.success(
            f"Load audit written to {audit_path}"
        )


if __name__ == "__main__":
    loader = ExcelLoader()

    datasets = loader.load_all()

    print("\n")

    for name, df in datasets.items():
        print("=" * 70)
        print(name)
        print(df.head())
        print()