# -- Imports --
from config import PROCESSED_DIR, GVA_DIR
from pathlib import Path
from cleaning_helpers import normalise_geo, check_duplicates
import pandas as pd


# -- Cleaning Functions --
def clean_single_gva(path_name: Path, sheet_name: str, header: int) -> pd.DataFrame:
    """
    Cleans a single GVA Excel sheet where columns from 3 onwards are multiple years (e.g 2021, 2022, 2023).

    1) Reads Excel File with passed parameters
    2) Renames the columns to be standardised with other processed datasets
    3) Filters to only the 'Total' SIC07 rows, representing the total GVA for the area
    4) Automatically parses the year columns
    5) Melts from wide to long format so there is only one year column, and the associated values for GVA in this case
    6) Then, makes year integer columns, and drops null rows

    :param path_name: File path of the excel file
    :type path_name: str
    :param sheet_name: Sheet name of the excel file
    :type sheet_name: str
    :param header: Row number to use as the column names
    :type header: int
    :return: Cleaned DataFrame
    :rtype: DataFrame
    """
    df = pd.read_excel(path_name, sheet_name=sheet_name, header=header)

    # Rename columns to standard names
    df = df.rename(columns={"LA code": "geo_code", "LA name": "geo_name"})

    # Filter to only the 'Total' SIC07 rows
    total_gva = df[df["SIC07"] == "Total"].copy()

    # Identify year columns automatically
    years_cols = [c for c in total_gva.columns if str(c).isdigit() and len(str(c)) == 4]

    # Melt from wide to long format
    total_gva = pd.melt(
        total_gva,
        id_vars=["geo_code", "geo_name"],
        value_vars=years_cols,
        var_name="year",
        value_name="gva_million",
    )

    total_gva["year"] = total_gva["year"].astype(int)
    total_gva["gva_million"] = pd.to_numeric(total_gva["gva_million"], errors="coerce")

    return total_gva[["geo_code", "geo_name", "year", "gva_million"]]


def build_gva() -> pd.DataFrame:
    """
    Build the cleaned GVA DataFrame by calling the relevant functions

    :return: Cleaned and normalised GVA DataFrame
    :rtype: DataFrame
    """
    # Combine all GVA files
    all_gva = []
    gva_files = list(GVA_DIR.glob("regionalgrossvalueadded*.xlsx"))
    print(f"Found {len(gva_files)} files")

    for gva_file in gva_files:
        print(f"Processing {gva_file}")
        gva = clean_single_gva(path_name=gva_file, sheet_name="Table 2", header=1)
        gva = normalise_geo(gva)
        all_gva.append(gva)

    return pd.concat(all_gva, ignore_index=True)


def main():
    """
    Main function to build and save the GVA dataset.

    :return: None
    :rtype: None
    """
    gva = build_gva()

    dup_rows = check_duplicates(gva)

    # Quality checks
    if len(dup_rows) > 0:
        print("Duplicate rows found")
        print(dup_rows)

    else:
        PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
        out_path = PROCESSED_DIR / "gva.csv"
        gva.to_csv(out_path, index=False)
        print(f"\nSaved {len(gva)} rows to {out_path}")


if __name__ == "__main__":
    main()
