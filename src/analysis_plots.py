# -- Imports --
import pandas as pd
import matplotlib.pyplot as plt
from config import FIGURES_DIR, PROCESSED_DIR


# -- Functions --
def plot_births_vs_gva(df: pd.DataFrame) -> None:
    """
    Scatter plot of births vs GVA per capita.

    :param df: Analysis dataset
    :type df: DataFrame
    :return: None
    :rtype: None
    """
    latest = df[df["year"] == df["year"].max()]

    # Plot without outlier
    plt.figure(figsize=(10, 6))
    plt.scatter(latest["birth_rate"], latest["gva_per_capita"], alpha=0.5)
    plt.title("Birth Rate vs GVA per Capita")
    plt.xlabel("Birth Rate (per 1,000 people)")
    plt.ylabel("GVA per Capita (£)")
    plt.grid(True)
    out_path = FIGURES_DIR / "births_vs_gva_per_capita.png"
    plt.savefig(out_path)
    plt.close()

    print(f"Saved plot to {out_path}")


def main():
    """
    Main function to load final dataset and generate analysis plots.

    :return: None
    :rtype: None
    """
    df = pd.read_csv(PROCESSED_DIR / "analysis_dataset.csv")
    q99 = df["gva_per_capita"].quantile(0.99)
    df_trim = df[df["gva_per_capita"] <= q99].copy()
    plot_births_vs_gva(df_trim)


if __name__ == "__main__":
    main()
