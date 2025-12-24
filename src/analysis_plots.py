# -- Imports --
import pandas as pd
import matplotlib.pyplot as plt
from config import FIGURES_DIR, PROCESSED_DIR
import seaborn as sns


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


def plot_churn_scatter(df: pd.DataFrame) -> None:
    """
    Figure 1: Scatter plot of Birth Rate vs Death Rate, coloured by region
    Identifies high churn vs stable regions

    :param df: Analysis dataset
    :type df: DataFrame
    :return: None
    :rtype: None
    """
    latest = df[df["year"] == df["year"].max()].copy()

    plt.figure(figsize=(10, 7))
    sns.scatterplot(
        data=latest,
        x="birth_rate",
        y="death_rate",
        hue="region_name",
        palette="tab10",
        s=100,
        alpha=0.88,
    )

    # Break even line
    max_val = max(latest["birth_rate"].max(), latest["death_rate"].max())
    plt.plot(
        [0, max_val],
        [0, max_val],
        color="red",
        linestyle="--",
        alpha=0.5,
        label="Breakeven (Net 0)",
    )

    plt.title("Regional Churn: Birth Rate vs Death Rate (2023)")
    plt.xlabel("Birth Rate (%)")
    plt.ylabel("Death Rate (%)")
    plt.legend(bbox_to_anchor=(1.05, 1), loc="upper left", title="Region")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    out_path = FIGURES_DIR / "fig1_business_churn.png"
    plt.savefig(out_path, dpi=300)
    print(f"Saved plot to {out_path}")


def plot_net_growth_boxplot(df: pd.DataFrame) -> None:
    """
    Figure 2: Boxplot of Net Business Growth Rate by Region.
    Shows variance and median performance differences.
    """
    # Avg over 5 years
    df_grouped = (
        df.groupby(["region_name", "geo_code"])["net_rate"].mean().reset_index()
    )
    order = (
        df_grouped.groupby("region_name")["net_rate"]
        .median()
        .sort_values(ascending=False)
        .index
    )

    plt.figure(figsize=(12, 6))
    sns.boxplot(
        x="region_name", y="net_rate", data=df_grouped, order=order, palette="viridis"
    )
    plt.title("Net Business Growth by Region (2019-2023 Average)")
    plt.xlabel("Region")
    plt.ylabel("Avg Net Growth Rate (%)")
    plt.xticks(rotation=45)
    plt.grid(axis="y", alpha=0.3)
    plt.tight_layout()

    out_path = FIGURES_DIR / "fig2_net_growth_boxplot.png"
    plt.savefig(out_path, dpi=300)
    print(f"Saved plot to {out_path}")


def plot_productivity_vs_growth(df: pd.DataFrame) -> None:
    """
    Figure 3: GVA per Business vs Net Rate
    Directly tests the hypothesis: 'Does higher efficiency = better survival?'
    """
    latest = df[df["year"] == df["year"].max()].copy()

    plt.figure(figsize=(10, 6))
    sns.regplot(
        data=latest,
        x="gva_per_business",
        y="net_rate",
        scatter_kws={"alpha": 0.3},
        line_kws={"color": "red"},
    )

    plt.title("Efficiency vs Growth (2023)")
    plt.xlabel("GVA per Business (£)")
    plt.ylabel("Net Growth Rate (%)")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    out_path = FIGURES_DIR / "fig3_productivity_over_growth.png"
    plt.savefig(out_path, dpi=300)
    print(f"Saved plot to {out_path}")


def main():
    """
    Main function to load final dataset and generate analysis plots.

    :return: None
    :rtype: None
    """
    df = pd.read_csv(PROCESSED_DIR / "analysis_dataset.csv")

    df = df[df["is_unreliable"] == False]
    q99 = df["gva_per_capita"].quantile(0.99)
    df_trim = df[df["gva_per_capita"] <= q99]

    plot_churn_scatter(df_trim)
    plot_line(df_trim)
    plot_net_growth_boxplot(df_trim)
    plot_productivity_vs_growth(df_trim)


if __name__ == "__main__":
    main()
