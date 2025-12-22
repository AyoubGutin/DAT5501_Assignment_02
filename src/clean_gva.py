# -- Imports --
from config import PROCESSED_DIR, GVA_DIR
from pathlib import Path
from cleaning_helpers import normalise_geo, check_duplicates
import pandas as pd


def clean_single_gva(path_name: Path, sheet_name: str, header: int) -> pd.DataFrame:
    """
    Process one GVA Excel file

    :param path_name: Description
    :type path_name: Path
    :return: Description
    :rtype: DataFrame
    """

    df = pd.read_excel(path_name, sheet_name=sheet_name, header=header)
    df = df.rename(columns={"LA code": "geo_code", "LA name": "geo_name"})

    total_gva = df[df["SIC07"] == "Total"].copy()

    years_cols = [c for c in total_gva.columns if str(c).isdigit() and len(str(c)) == 4]

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
    Docstring for build_gva - todo

    :return: Description
    :rtype: DataFrame
    """
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
