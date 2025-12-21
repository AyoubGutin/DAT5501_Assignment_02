from config import DEMOGRAPHY_FILE, PROCESSED_DIR
from cleaning_helpers import clean_single_year, clean_multi_year, normalise_geo
import pandas as pd


def build_births() -> pd.DataFrame:
    """
    Docstring for build_births - todo

    :return: Description
    :rtype: DataFrame
    """
    births_2019 = clean_single_year(
        path_name=DEMOGRAPHY_FILE,
        sheet_name="Table 1.1a",
        header=3,
        value_name="births",
    )
    births_2020 = clean_single_year(
        path_name=DEMOGRAPHY_FILE,
        sheet_name="Table 1.1b",
        header=3,
        value_name="births",
    )
    births_21_23 = clean_multi_year(
        path_name=DEMOGRAPHY_FILE,
        sheet_name="Table 1.1c",
        header=3,
        value_name="births",
    )
    births_2024 = clean_single_year(
        path_name=DEMOGRAPHY_FILE,
        sheet_name="Table 1.1d",
        header=3,
        value_name="births",
    )

    births_all = pd.concat(
        [births_2019, births_2020, births_21_23, births_2024],
        ignore_index=True,
    )
    births_all = normalise_geo(births_all)
    return births_all


def build_deaths() -> pd.DataFrame:
    """
    Docstring for build_deaths - todo

    :return: Description
    :rtype: DataFrame
    """
    deaths_2019 = clean_single_year(
        path_name=DEMOGRAPHY_FILE,
        sheet_name="Table 2.1a",
        header=3,
        value_name="deaths",
    )
    deaths_2020 = clean_single_year(
        path_name=DEMOGRAPHY_FILE,
        sheet_name="Table 2.1b",
        header=3,
        value_name="deaths",
    )
    deaths_21_23 = clean_multi_year(
        path_name=DEMOGRAPHY_FILE,
        sheet_name="Table 2.1c",
        header=3,
        value_name="deaths",
    )
    deaths_2024 = clean_single_year(
        path_name=DEMOGRAPHY_FILE,
        sheet_name="Table 2.1d",
        header=3,
        value_name="deaths",
    )

    deaths_all = pd.concat(
        [deaths_2019, deaths_2020, deaths_21_23, deaths_2024],
        ignore_index=True,
    )
    deaths_all = normalise_geo(deaths_all)
    return deaths_all


def build_active() -> pd.DataFrame:
    """
    Docstring for build_active - todo

    :return: Description
    :rtype: DataFrame
    """
    active_2019 = clean_single_year(
        path_name=DEMOGRAPHY_FILE,
        sheet_name="Table 3.1a",
        header=3,
        value_name="active",
    )
    active_2020 = clean_single_year(
        path_name=DEMOGRAPHY_FILE,
        sheet_name="Table 3.1b",
        header=3,
        value_name="active",
    )
    active_21_23 = clean_multi_year(
        path_name=DEMOGRAPHY_FILE,
        sheet_name="Table 3.1c",
        header=3,
        value_name="active",
    )
    active_2024 = clean_single_year(
        path_name=DEMOGRAPHY_FILE,
        sheet_name="Table 3.1d",
        header=3,
        value_name="active",
    )

    active_all = pd.concat(
        [active_2019, active_2020, active_21_23, active_2024],
        ignore_index=True,
    )
    active_all = normalise_geo(active_all)
    return active_all


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


def main():
    births_all = build_births()
    deaths_all = build_deaths()
    active_all = build_active()

    demog_counts = (
        births_all.merge(deaths_all, on=["geo_code", "geo_name", "year"], how="left")
        .merge(active_all, on=["geo_code", "geo_name", "year"], how="left")
        .sort_values(["geo_code", "year"])
    )

    dup_rows = check_duplicates(demog_counts)
    if len(dup_rows) > 0:
        print("Duplicate rows found")
        print(dup_rows)

    else:
        PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
        path = PROCESSED_DIR / "business_demography_counts.csv"
        demog_counts.to_csv(path, index=False)
        print(f"Saved {len(demog_counts)} rows to {path}")


if __name__ == "__main__":
    main()
