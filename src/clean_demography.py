from config import DEMOGRAPHY_FILE, PROCESSED_DIR
import pandas as pd


def clean_single_year(sheet_name: str, value_name: str) -> pd.DataFrame:
    """
    Cleans excel sheets 1.1a - d that are single years, which represents the births of enterprises each year, by region.
    It reads a sheet where the third column header is the year and the values are births/deaths/active

    :param sheet_name: Sheet name of the excel file
    :type sheet_name: str
    :param year: Description
    :type year: int
    :return: Description
    :rtype: DataFrame
    """
    df = pd.read_excel(
        DEMOGRAPHY_FILE, sheet_name=sheet_name, header=3
    )  # header is 3 as row 4 is where the data starts

    geo_code_col = df.columns[0]
    geo_name_col = df.columns[1]
    year_col = df.columns[2]
    year = int(year_col)

    df = df.rename(
        columns={
            geo_code_col: "geo_code",
            geo_name_col: "geo_name",
            year_col: value_name,
        }
    )
    df["year"] = year  # add the current year to a new column year

    return df[["geo_code", "geo_name", "year", value_name]]


def clean_multi_year(sheet_name: str, value_name: str) -> pd.DataFrame:
    """
    Read a sheet where columns 3+ are multiple years (e.g 2021, 2022, 2023)

    :param sheet_name: Description
    :type sheet_name: str
    :param value_name: Description
    """
    df = pd.read_excel(DEMOGRAPHY_FILE, sheet_name=sheet_name, header=3)

    df = df.rename(
        columns={
            df.columns[0]: "geo_code",
            df.columns[1]: "geo_name",
        }
    )

    years_cols = [c for c in df.columns if isinstance(c, int)]  # auto detect the years

    # change the dataframe from multiple year columns to one year column, with the relevant births/deaths etc as a separate column
    df = df.melt(
        id_vars=["geo_code", "geo_name"],  # identifiers that repeat in every row
        value_vars=years_cols,  # original year columns that hold birth counts, melt stacks into two new columns instead of separate ones
        var_name="year",  # original column headers become values in a new column called year
        value_name=value_name,  # the values undr the year columns become a single column
    )
    df["year"] = df["year"].astype(int)

    return df[["geo_code", "geo_name", "year", value_name]]


def build_births() -> pd.DataFrame:
    births_2019 = clean_single_year("Table 1.1a", "births")
    births_2020 = clean_single_year("Table 1.1b", "births")
    births_21_23 = clean_multi_year("Table 1.1c", "births")
    births_2024 = clean_single_year("Table 1.1d", "births")

    births_all = pd.concat(
        [births_2019, births_2020, births_21_23, births_2024],
        ignore_index=True,
    )
    return births_all


births_all = build_births()
