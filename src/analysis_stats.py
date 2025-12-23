# -- Imports --
import pandas as pd
import statsmodels.api as sm
from config import PROCESSED_DIR
import numpy as np


# -- Functions --
def descriptive_stats(df: pd.DataFrame) -> pd.DataFrame:
    """
    Descriptive statistics for key analysis variables.

    :param df: Analysis dataset
    :type df: DataFrame
    :return: Descriptive statistics
    :rtype: DataFrame
    """
    desc = df[
        ["birth_rate", "death_rate", "net_rate", "gva_per_capita", "gva_per_business"]
    ].describe()
    try:
        desc.to_csv(PROCESSED_DIR / "analysis_statistics_summary.csv")
        print(
            f"Saved descriptive statistics to {PROCESSED_DIR / 'analysis_statistics_summary.csv'}"
        )
    except Exception as e:
        print(f"Error saving descriptive statistics: {e}")

    return desc


def correlation(df: pd.DataFrame) -> pd.DataFrame:
    """
    Correlation matrix for key analysis variables.

    :param df: Analysis dataset
    :type df: DataFrame
    :return: Correlation matrix
    :rtype: DataFrame
    """
    desc = df[
        ["birth_rate", "death_rate", "net_rate", "gva_per_capita", "gva_per_business"]
    ].corr()
    try:
        desc.to_csv(PROCESSED_DIR / "analysis_statistics_correlation.csv")
        print(
            f"Saved correlation matrix to {PROCESSED_DIR / 'analysis_statistics_correlation.csv'}"
        )
    except Exception as e:
        print(f"Error saving correlation matrix: {e}")

    return desc


def regression_summary(df: pd.DataFrame) -> pd.DataFrame:
    """
    Regression summary of GVA per capita against birth rate, death rate, and net rate.

    :param df: Analysis dataset
    :type df: DataFrame
    :return: Regression summary
    :rtype: DataFrame
    """

    cols_to_check = ["gva_per_capita", "birth_rate", "death_rate"]

    df_clean = df[cols_to_check].replace(
        [np.inf, -np.inf], np.nan
    )  # rates can be infinite if population is zero / missing
    df_clean = df_clean.dropna()
    X = df_clean[["birth_rate", "death_rate"]]
    y = df_clean["gva_per_capita"]

    X = sm.add_constant(X)
    model = sm.OLS(y, X).fit()
    with open(PROCESSED_DIR / "analysis_statistics_regression.txt", "w") as f:
        f.write(model.summary().as_text())
        print(
            f"Saved regression summary to {PROCESSED_DIR / 'analysis_statistics_regression.txt'}"
        )

    return model.summary()


def main():
    df = pd.read_csv(PROCESSED_DIR / "analysis_dataset.csv")
    df_gva = df.dropna(subset=["gva_million"]).copy()  # Focus on rows with GVA data
    q99 = df["gva_per_capita"].quantile(0.99)
    df_trim = df[df["gva_per_capita"] <= q99].copy()

    descriptive_stats(df_trim)
    correlation(df_trim)
    regression_summary(df_trim)


if __name__ == "__main__":
    main()
