import pandas as pd
from config import PROCESSED_DIR


def main():
    df = pd.read_csv(PROCESSED_DIR / "analysis_dataset.csv")

    # Group by region and calculate mean metrics
    summary = (
        df.groupby("region_name")
        .agg(
            {
                "birth_rate": "mean",
                "death_rate": "mean",
                "net_rate": "mean",
                "gva_per_business": "mean",
                "gva_per_capita": "mean",
            }
        )
        .round(2)
        .reset_index()
    )

    summary["churn_rate"] = summary["birth_rate"] + summary["death_rate"]

    summary = summary.sort_values(by="net_rate", ascending=False)
    print(summary.to_markdown())

    summary.to_csv(PROCESSED_DIR / "analysis_regional_league_table.csv")


if __name__ == "__main__":
    main()
