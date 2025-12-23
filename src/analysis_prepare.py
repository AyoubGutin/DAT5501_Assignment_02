# -- Imports --
import pandas as pd
from config import PROCESSED_DIR


# -- Functions --
def build_analysis_dataset() -> pd.DataFrame:
    """
    Builds the analysis dataset from the final merged dataset.

    :return: DataFrame
    :rtype: DataFrame
    """

    path = PROCESSED_DIR / "final_dataset.csv"
    df = pd.read_csv(path)

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

    out_path = PROCESSED_DIR / "analysis_dataset.csv"
    df.to_csv(out_path, index=False)
    print(f"Saved {len(df)} rows to {out_path}")

    return


if __name__ == "__main__":
    build_analysis_dataset()
