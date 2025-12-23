# -- Imports --
import pandas as pd
import matplotlib.pyplot as plt
from config import FIGURES_DIR, PROCESSED_DIR


# -- Functions --
def plot_scatter(df: pd.DataFrame) -> None:
    """
    Scatter plot of births vs GVA per capita.

    :param df: Analysis dataset
    :type df: DataFrame
    :return: None
    :rtype: None
    """
    latest = df[df["year"] == df["year"].max()]

    # Plot without outlier
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.scatter(
        latest["birth_rate"],
        latest["gva_per_capita"],
        s=15,
        alpha=0.6,
        edgecolor="none",
    )

    candidates = pd.concat(
        [
            latest.nlargest(3, "gva_per_capita"),
            latest.nsmallest(3, "gva_per_capita"),
            latest.nlargest(3, "birth_rate"),
        ]
    )
    for _, row in candidates.drop_duplicates("geo_code").iterrows():
        ax.annotate(
            row["geo_name"],
            (row["birth_rate"], row["gva_per_capita"]),
            xytext=(3, 3),
            textcoords="offset points",
            fontsize=6,
        )
    ax.set_title("Birth Rate vs GVA per Capita")
    ax.set_xlabel("Birth Rate (per 1,000 people)")
    ax.set_ylabel("GVA per Capita (£)")
    ax.grid(True)
    out_path = FIGURES_DIR / "births_vs_gva_per_capita.png"
    plt.savefig(out_path)
    plt.close()

    print(f"Saved plot to {out_path}")


def plot_line(df: pd.DataFrame) -> None:
    """
    Line plot of average birth rate over time.


    :param df: Analysis dataset
    :type df: DataFrame
    :return: None
    :rtype: None
    """
    yearly = (
        df.groupby("year")
        .agg(birth_rate=("birth_rate", "mean"), death_rate=("death_rate", "mean"))
        .reset_index()
    )

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(yearly["year"], yearly["birth_rate"], marker="o", label="Birth Rate")
    ax.plot(yearly["year"], yearly["death_rate"], marker="o", label="Death Rate")

    ax.set_title("Average Birth and Death Rates Over Time")
    ax.set_xlabel("Year")
    ax.set_ylabel("Average rate (% of active businesses)")
    ax.grid(True, axis="y", alpha=0.3)
    ax.legend()
    fig.tight_layout()
    fig.savefig(FIGURES_DIR / "avg_birth_death_rates_over_time.png")
    plt.close()


def main():
    """
    Main function to load final dataset and generate analysis plots.

    :return: None
    :rtype: None
    """
    df = pd.read_csv(PROCESSED_DIR / "analysis_dataset.csv")
    # Remove extreme outliers
    q99 = df["gva_per_capita"].quantile(0.99)
    df_trim = df[df["gva_per_capita"] <= q99].copy()
    # Filter out unreliable
    df_trim = df_trim[df_trim["is_unreliable"] == False].copy()
    plot_scatter(df_trim)
    plot_line(df_trim)


if __name__ == "__main__":
    main()
