from config import POPULATION_FILE
import pandas as pd

print("File:", POPULATION_FILE)
excel = pd.ExcelFile(POPULATION_FILE)
print("Sheets:", excel.sheet_names)
for i, sheet in enumerate(excel.sheet_names):
    df = pd.read_excel(POPULATION_FILE, sheet_name=sheet, nrows=5)
    print(f"\nSheet {i}: {sheet}")
    print(df.columns.tolist())
    print(df.head())
