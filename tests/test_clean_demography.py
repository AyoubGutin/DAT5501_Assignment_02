# -- Imports --
import unittest as ut
import pandas as pd
from src.config import PROCESSED_DIR


# -- Test Suite --
class TestCleanGVA(ut.TestCase):
    @classmethod
    def setUpClass(cls):
        """
        Load processed GVA dataframe, using cls.df so it's attatched to the class and can be accessed using self in tests.

        The classmethod decorator makes this run once for the whole class, as unittest creates a new instance of the class for each test method below

        Runs once before all tests
        """
        path = PROCESSED_DIR / "gva.csv"
        assert path.exists(), f"Processed GVA files not found at {path}"
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
        non_null = self.df["gva_million"].dropna()
        self.assertTrue(
            non_null.empty or (non_null >= 0).all(),
            f"Negative values found in {'gva_million'}: {non_null[non_null < 0]}",
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
