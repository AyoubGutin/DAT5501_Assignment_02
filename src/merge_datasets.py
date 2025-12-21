# -- Imports --
import pandas as pd
from config import PROCESSED_DIR


def merge_all_datasets():
    """
    Docstring for merge_all_datasets - todo

    :return: Description
    :rtype: DataFrame
    """
    demography = pd.read_csv(PROCESSED_DIR / "business_demography_counts.csv")
    population = pd.read_csv(PROCESSED_DIR / "population.csv")
    gva = pd.read_csv(PROCESSED_DIR / "gva.csv")

    merged = demography.merge(population, on=["geo_code", "year"], how="inner")
    merged = merged.merge(gva, on=["geo_code", "year"], how="inner")

    out_path = PROCESSED_DIR / "final_dataset.csv"
    merged.to_csv(out_path, index=False)

    print(f"Final dataset: {len(merged)} rows (2019-2023)")


merge_all_datasets()
