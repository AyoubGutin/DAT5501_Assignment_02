# -- Imports --
import pandas as pd
from config import PROCESSED_DIR, RAW_DIR


def attach_regions(df: pd.DataFrame) -> pd.DataFrame:
    lookup = pd.read_excel(RAW_DIR / "lasregionew2021lookup.xlsx", header=4)
    lookup = lookup.rename(
        columns={
            "LA code": "geo_code",
            "LA name": "geo_name",
            "Region code": "region_code",
            "Region name": "region_name",
        }
    )

    df = df.merge(
        lookup[["geo_code", "region_code", "region_name"]], on="geo_code", how="left"
    )

    # Lookup fallbacks for missing regions
    df.loc[df["geo_code"].str.startswith("S"), "region_name"] = "Scotland"
    df.loc[df["geo_code"].str.startswith("N"), "region_name"] = "Northern Ireland"
    df.loc[df["geo_code"].str.startswith("W"), "region_name"] = "Wales"

    return df


def build_analysis_dataset() -> pd.DataFrame:
    """
    Builds the analysis dataset from the final merged dataset.

    :return: DataFrame
    :rtype: DataFrame
    """

    path = PROCESSED_DIR / "final_dataset.csv"
    df = pd.read_csv(path)

    # Only want Local Authorities (E06, E07, E08, E09, N09, S12, W06), individual region rows are removed.
    # This prevents double-counting and massive outliers in the plots.

    prefixes_to_keep = ["E06", "E07", "E08", "E09", "N09", "S12", "W06"]
    pattern = "|".join(prefixes_to_keep)
    df = df[df["geo_code"].str.contains(f"^({pattern})", regex=True)].copy()

    print(f"Filtered dataset to Local Authorities only: {len(df)} rows.")

    # Rates and Counts
    df["birth_rate"] = (
        df["births"] / df["active"] * 100
    )  # Births per 100 active businesses
    df["death_rate"] = (
        df["deaths"] / df["active"] * 100
    )  # Deaths per 100 active businesses
    df["net_change"] = (
        df["births"] - df["deaths"]
    )  # Net change in business counts for that year
    df["net_rate"] = (
        df["net_change"] / df["active"] * 100
    )  # Net change rate per 100 active businesses

    # Productivity measures
    df["gva_per_capita"] = (
        df["gva_million"] * 1_000_000 / df["population"]
    )  # GVA per person
    df["gva_per_business"] = (
        df["gva_million"] * 1_000_000 / df["active"]
    )  # GVA per active business

    analysis_df = attach_regions(df)

    # some rows (18) still have missing regions - likely defunct authorities
    before_len = len(analysis_df)
    analysis_df = analysis_df.dropna(subset=["region_name"])
    dropped = before_len - len(analysis_df)

    if dropped > 0:
        print(f"Dropped {dropped} rows belonging to defunct authorities.")

    out_path = PROCESSED_DIR / "analysis_dataset.csv"
    analysis_df.to_csv(out_path, index=False)
    print(f"Saved {len(analysis_df)} rows to {out_path}")
    return analysis_df


if __name__ == "__main__":
    build_analysis_dataset()
