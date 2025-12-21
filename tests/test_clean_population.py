# -- Imports --
import unittest as ut
import pandas as pd
from src.config import PROCESSED_DIR


class TestCleanPopulation(ut.TestCase):
    @classmethod
    def setUpClass(cls):
        path = PROCESSED_DIR / "population.csv"
        assert path.exists(), f"Processed population files not found at {path}"
        cls.df = pd.read_csv(path)

    def test_unique_region_year(self):
        """
        Each geo_code and year combination should appear once
        """
        dup_mask = self.df.duplicated(subset=["geo_code", "year"])
        self.assertFalse(dup_mask.any(), "Duplicates found")

    def test_non_negative_counts(self):
        """
        Births, deaths, and active counts should all be positive
        """
        non_null = self.df["population"].dropna()
        self.assertTrue(
            non_null.empty or (non_null >= 0).all(),
            f"Negative values found in population: {non_null[non_null < 0]}",
        )

    def test_no_missing_geo_info(self):
        """
        Geo code and geo name should not be missing
        """
        self.assertTrue(
            self.df["geo_code"].notna().all(), "Geo code missing in some rows"
        )
        self.assertTrue(
            self.df["geo_name"].notna().all(), "Geo name missing in some rows"
        )


if __name__ == "__main__":
    ut.main()
