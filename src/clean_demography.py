from config import DEMOGRAPHY_FILE, PROCESSED_DIR
import pandas as pd


def clean_single_year(sheet_name: str, value_name: str) -> pd.DataFrame:
    """
    Cleans excel sheets that are single years by region.
    It reads a sheet where the third column header is the year and the values are under it

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
    """
    Docstring for build_births - todo

    :return: Description
    :rtype: DataFrame
    """
    births_2019 = clean_single_year("Table 1.1a", "births")
    births_2020 = clean_single_year("Table 1.1b", "births")
    births_21_23 = clean_multi_year("Table 1.1c", "births")
    births_2024 = clean_single_year("Table 1.1d", "births")

    births_all = pd.concat(
        [births_2019, births_2020, births_21_23, births_2024],
        ignore_index=True,
    )
    return births_all


def build_deaths() -> pd.DataFrame:
    """
    Docstring for build_deaths - todo

    :return: Description
    :rtype: DataFrame
    """
    deaths_2019 = clean_single_year("Table 2.1a", "deaths")
    deaths_2020 = clean_single_year("Table 2.1b", "deaths")
    deaths_21_23 = clean_multi_year("Table 2.1c", "deaths")
    deaths_2024 = clean_single_year("Table 2.1d", "deaths")

    deaths_all = pd.concat(
        [deaths_2019, deaths_2020, deaths_21_23, deaths_2024],
        ignore_index=True,
    )
    return deaths_all


def build_active() -> pd.DataFrame:
    """
    Docstring for build_active - todo

    :return: Description
    :rtype: DataFrame
    """
    active_2019 = clean_single_year("Table 3.1a", "active")
    active_2020 = clean_single_year("Table 3.1b", "active")
    active_21_23 = clean_multi_year("Table 3.1c", "active")
    active_2024 = clean_single_year("Table 3.1d", "active")

    active_all = pd.concat(
        [active_2019, active_2020, active_21_23, active_2024],
        ignore_index=True,
    )
    return active_all


def main():
    births_all = build_births()
    deaths_all = build_deaths()
    active_all = build_active()

    demog_counts = (
        births_all.merge(deaths_all, on=["geo_code", "geo_name", "year"], how="left")
        .merge(active_all, on=["geo_code", "geo_name", "year"], how="left")
        .sort_values(["geo_code", "year"])
    )

    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    path = PROCESSED_DIR / "business_demography_counts.csv"
    demog_counts.to_csv(path, index=False)
    print(f"Saved {len(demog_counts)} rows to {path}")


if __name__ == "__main__":
    main()
