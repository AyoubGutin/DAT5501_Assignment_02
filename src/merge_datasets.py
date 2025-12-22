# -- Imports --
import pandas as pd
from config import PROCESSED_DIR


# -- Functions --
def merge_all_datasets():
    """
    Merges business demography, population, and GVA datasets into a final dataset for the years 2019-2023.

    :return: None
    :rtype: DataFrame
    """
    # Load datasets from csvs
    demography = pd.read_csv(PROCESSED_DIR / "business_demography_counts.csv")
    population = pd.read_csv(PROCESSED_DIR / "population.csv")
    gva = pd.read_csv(PROCESSED_DIR / "gva.csv")

    # Merge datasets using left joins on geo_code and year, to retain all demography records
    merged = demography.merge(
        population[["geo_code", "year", "population", "is_unreliable"]],
        on=["geo_code", "year"],
        how="left",
    )
    merged = merged.merge(
        gva[["geo_code", "year", "gva_million"]], on=["geo_code", "year"], how="left"
    )

    # Filter for years 2019-2023
    merged = merged[merged["year"].between(2019, 2023)]

    # Reorder columns
    merged = merged[
        [
            "geo_code",
            "geo_name",
            "year",
            "births",
            "deaths",
            "active",
            "population",
            "is_unreliable",
            "gva_million",
        ]
    ]

    # Save final dataset to csv
    out_path = PROCESSED_DIR / "final_dataset.csv"
    merged.to_csv(out_path, index=False)

    print(f"Final dataset: {len(merged)} rows (2019-2023)")


merge_all_datasets()
