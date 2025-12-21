import pandas as pd
from src.config import PROCESSED_DIR

df = pd.read_csv(PROCESSED_DIR / "business_demography_counts.csv")
print(df["deaths"].min())
print(df[df["deaths"] < 0].head())


print(df["births"].min())
print(df[df["births"] < 0].head())

print(df["active"].min())
print(df[df["active"] < 0].head())
