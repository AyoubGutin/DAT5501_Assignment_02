from config import PROCESSED_DIR, POPULATION_FILE
from cleaning_helpers import clean_wide_population, normalise_geo, check_duplicates
import pandas as pd


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
