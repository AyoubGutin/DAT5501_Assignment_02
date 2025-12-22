# -- Imports --
from config import DEMOGRAPHY_FILE, PROCESSED_DIR
from cleaning_helpers import (
    normalise_geo,
    check_duplicates,
)
import pandas as pd


# -- Cleaning Functions --
def clean_single_year(
    path_name: str, sheet_name: str, header: int, value_name: str
) -> pd.DataFrame:
    """
    Cleans ONS Demographic Excel sheets that are of the format where there is a single year column with values under it.
    It reads a sheet where the third column header is the year and the values are under it.

    1) Reads Excel File with passed parameters
    2) Renames the columns to be normalised with other processed datasets
    3) Parses the year columns
    4) Melts from wide to long format so there is only one year column, and the associated values for births/deaths/actives in this case
    5) Then, makes year integer columns, and drops null rows


    :param path_name: File path of the excel file
    :type path_name: str
    :param sheet_name: Sheet name of the excel file
    :type sheet_name: str
    :param header: Row number to use as the column names
    :type header: int
    :param value_name: Name for the values column
    :type value_name: str
    :return: Cleaned DataFrame
    :rtype: DataFrame
    """
    df = pd.read_excel(path_name, sheet_name=sheet_name, header=header)

    # Identify columns based on format
    geo_code_col = df.columns[0]
    geo_name_col = df.columns[1]
    year_col = df.columns[2]
    year = int(year_col)

    # Rename columns to standardise names
    df = df.rename(
        columns={
            geo_code_col: "geo_code",
            geo_name_col: "geo_name",
            year_col: value_name,
        }
    )
    df["year"] = year  # add the current year to a new column year
    df = df.dropna(subset=["geo_code", "geo_name"])

    return df[["geo_code", "geo_name", "year", value_name]]


def clean_multi_year(
    path_name: str, sheet_name: str, header: int, value_name: str
) -> pd.DataFrame:
    """
    Read ONS Demographic Excel sheets where columns from  3 onwards are multiple years (e.g 2021, 2022, 2023)

    1) Reads Excel File with passed parameters
    2) Renames the columns to be normalised with other processed datasets
    3) Automatically parses the year columns
    4) Melts from wide to long format so there is only one year column, and the associated values for births/deaths/actives in this case
    5) Then, makes year integer columns, and drops null rows

    :param path_name: File path of the excel file
    :type path_name: str
    :param sheet_name: Sheet name of the excel file
    :type sheet_name: str
    :param header: Row number to use as the column names
    :type header: int
    :param value_name: Name for the values column
    :type value_name: str
    :return: Cleaned DataFrame
    :rtype: DataFrame

    :return: Cleaned DataFrame
    :rtype: DataFrame
    """
    df = pd.read_excel(path_name, sheet_name=sheet_name, header=header)

    # Rename columns to standardise names
    df = df.rename(
        columns={
            df.columns[0]: "geo_code",
            df.columns[1]: "geo_name",
        }
    )

    # Identify year columns automatically
    years_cols = [c for c in df.columns if str(c).isdigit() and len(str(c)) == 4]

    # Melt from wide to long format
    df = df.melt(
        id_vars=["geo_code", "geo_name"],
        value_vars=years_cols,
        var_name="year",  # original column headers become values in a new column called year
        value_name=value_name,  # the values undr the year columns become a single column
    )
    df["year"] = df["year"].astype(int)
    df = df.dropna(subset=["geo_code", "geo_name"])

    return df[["geo_code", "geo_name", "year", value_name]]


def build_births() -> pd.DataFrame:
    """
    Builds the births DataFrame by cleaning and combining multiple sheets from the DEMOGRAPHY_FILE. Calls the relevant cleaning functions.

    :return: Cleaned and standardised births DataFrame
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
    Cleans and combines multiple sheets from the DEMOGRAPHY_FILE to build the deaths DataFrame.

    :return: Cleaned and standardised deaths DataFrame
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
    Cleans and combines multiple sheets from the DEMOGRAPHY_FILE to build the active businesses DataFrame.

    :return: Cleaned and standardised active businesses DataFrame
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


def main():
    """
    Main function to build and save the combined demography dataset.

    :return: None
    :rtype: None
    """

    # Build individual datasets
    births_all = build_births()
    deaths_all = build_deaths()
    active_all = build_active()

    # Merge datasets on geo_code, geo_name, and year
    demog_counts = (
        births_all.merge(deaths_all, on=["geo_code", "geo_name", "year"], how="left")
        .merge(active_all, on=["geo_code", "geo_name", "year"], how="left")
        .sort_values(["geo_code", "year"])
    )

    # Check for duplicates
    dup_rows = check_duplicates(demog_counts)
    if len(dup_rows) > 0:
        print("Duplicate rows found")
        print(dup_rows)

    # Save the cleaned demography counts dataset as a csv file
    else:
        PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
        path = PROCESSED_DIR / "business_demography_counts.csv"
        demog_counts.to_csv(path, index=False)
        print(f"Saved {len(demog_counts)} rows to {path}")


if __name__ == "__main__":
    main()
