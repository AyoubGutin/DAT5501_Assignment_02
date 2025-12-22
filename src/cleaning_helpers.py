# Cleaning functions used more than once
import pandas as pd


def normalise_geo(df: pd.DataFrame) -> pd.DataFrame:
    """
    Docstring for _normalise_geo - todo
    :param df: Description
    :type df: pd.

    DataFrame
    :return: Description
    :rtype: DataFrame
    """
    df["geo_code"] = df["geo_code"].astype(str).str.strip()
    df["geo_name"] = df["geo_name"].astype(str).str.strip()
    return df


def check_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """
    Docstring for check_duplicates - todo

    :param df: Description
    :type df: pd.DataFrame
    :return: Description
    :rtype: DataFrame
    """
    dup_mask = df.duplicated(subset=["geo_code", "year"], keep=False)
    dup_rows = df[dup_mask].sort_values(["geo_code", "year"])
    return dup_rows[["geo_code", "geo_name", "year"]]
