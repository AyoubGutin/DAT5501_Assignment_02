# Cleaning functions.

import pandas as pd


def clean_single_year(
    path_name: str, sheet_name: str, header: int, value_name: str
) -> pd.DataFrame:
    """
    Cleans excel sheets that are single years by region.
    It reads a sheet where the third column header is the year and the values are under it.

    Used in:
    - Business Demographics for birth / active / deaths

    :param sheet_name: Sheet name of the excel file
    :type sheet_name: str
    :param year: Description
    :type year: int
    :return: Description
    :rtype: DataFrame
    """
    df = pd.read_excel(path_name, sheet_name=sheet_name, header=header)

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


def clean_multi_year(
    path_name: str, sheet_name: str, header: int, value_name: str
) -> pd.DataFrame:
    """
    Read a sheet where columns 3+ are multiple years (e.g 2021, 2022, 2023)

    :param sheet_name: Description
    :type sheet_name: str
    :param value_name: Description
    """
    df = pd.read_excel(path_name, sheet_name=sheet_name, header=header)

    df = df.rename(
        columns={
            df.columns[0]: "geo_code",
            df.columns[1]: "geo_name",
        }
    )

    years_cols = [c for c in df.columns if str(c).isdigit() and len(str(c)) == 4]

    # change the dataframe from multiple year columns to one year column, with the relevant births/deaths etc as a separate column
    df = df.melt(
        id_vars=["geo_code", "geo_name"],  # identifiers that repeat in every row
        value_vars=years_cols,  # original year columns that hold value counts, melt stacks into two new columns instead of separate ones
        var_name="year",  # original column headers become values in a new column called year
        value_name=value_name,  # the values undr the year columns become a single column
    )
    df["year"] = df["year"].astype(int)

    return df[["geo_code", "geo_name", "year", value_name]]


def clean_wide_population(
    path_name: str, sheet_name: str, header: int, value_name: str
) -> pd.DataFrame:
    """
    Clean ONS population (named columns, ITL1 Region)

    1) Reads Excel File with passed parameters
    2) Renames the columns to be normalised with other processed datasets
    3) Automatically parses the year columns
    4) Melts from wide to long format so there is only one year column, and the associated values for population in this case
    5) Then, makes year integer columns, and drops null rows

    :param path_name: Description
    :type path_name: str
    :param sheet_name: Description
    :type sheet_name: str
    :param header: Description
    :type header: int
    :param value_name: Description
    :type value_name: str
    :return: Description
    :rtype: DataFrame

    """
    df = pd.read_excel(path_name, sheet_name=sheet_name, header=header)

    df = df.rename(columns={"LA code": "geo_code", "LA name": "geo_name"})

    years_cols = [c for c in df.columns if str(c).isdigit() and len(str(c)) == 4]

    df = pd.melt(
        df,
        id_vars=["geo_code", "geo_name"],
        value_vars=years_cols,
        var_name="year",
        value_name=value_name,
    )

    df["year"] = df["year"].astype(int)
    df = df.dropna(subset=["geo_code", "geo_name"])

    return df[["geo_code", "geo_name", "year", value_name]]


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
