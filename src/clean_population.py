from config import PROCESSED_DIR, POPULATION_FILE
from cleaning_helpers import normalise_geo, check_duplicates
import pandas as pd


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


def build_population() -> pd.DataFrame:
    """
    Docstring for build_population - todo

    :return: Description
    :rtype: DataFrame
    """
    population = clean_wide_population(
        path_name=POPULATION_FILE,
        sheet_name="Population data",
        header=0,
        value_name="population",
    )
    population = normalise_geo(population)
    return population


def main():
    population = build_population()

    # Handle the uncertainity flags '[u]'
    population["population"] = pd.to_numeric(
        population["population"], errors="coerce"
    )  # convert the [u] flags to NaN
    population["is_unreliable"] = population[
        "population"
    ].isna()  # Flag the unreliable values

    population = population.sort_values(["geo_code", "year"])
    population["population"] = population.groupby("geo_code")[
        "population"
    ].ffill()  # forward fill the uncertain values

    print(f"After uncertainty handling: {len(population)} rows")
    print(
        f"Unreliable flags: {population['is_unreliable'].sum()} ({population['is_unreliable'].mean():.1%})"
    )

    # Check duplicates
    dup_rows = check_duplicates(population)
    if len(dup_rows) > 0:
        print("Duplicate rows found")
        print(dup_rows)

    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    path = PROCESSED_DIR / "population.csv"
    population.to_csv(path, index=False)
    print(f"Saved {len(population)} rows to {path}")


if __name__ == "__main__":
    main()
