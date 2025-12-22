# -- Imports --
import unittest
import pandas as pd
from src.config import PROCESSED_DIR


class TestFinalDataset(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """
        Load processed GVA dataframe, using cls.df so it's attatched to the class and can be accessed using self in tests.

        The classmethod decorator makes this run once for the whole class, as unittest creates a new instance of the class for each test method below

        Runs once before all tests
        """
        path = PROCESSED_DIR / "final_dataset.csv"
        assert path.exists(), f"Final dataset not found at {path}"
        cls.df = pd.read_csv(path)

    def test_unique_region_year(self):
        """
        Each geo_code and year combination should appear once
        """
        dup_mask = self.df.duplicated(subset=["geo_code", "year"])
        self.assertFalse(dup_mask.any(), "Duplicates found")

    def test_expected_shape(self):
        """
        Final dataset should have 2126 rows (439 Local Authorities x 5 years: 2019 - 2023)
        *Some LAs missing GVA data (81% coverage)
        """
        self.assertEqual(len(self.df), 2126, f"Expected 2126 rows, got {len(self.df)}")

    def test_expected_columns(self):
        """
        Final dataset should have the expected columns:
        - geo_code
        - geo_name
        - year
        - births
        - deaths
        - active
        - population
        - gva_million
        - is_unreliable
        """
        expected_cols = {
            "geo_code",
            "geo_name",
            "year",
            "births",
            "deaths",
            "active",
            "population",
            "gva_million",
            "is_unreliable",
        }
        actual_cols = set(self.df.columns)
        self.assertTrue(
            expected_cols.issubset(actual_cols),
            f"Missing columns: {expected_cols - actual_cols}",
        )

    def test_year_range(self):
        """
        Final dataset should have years between 2019 and 2023
        """
        self.assertTrue(
            self.df["year"].between(2019, 2023).all(),
            f"Years should be between 2019 and 2023, got {self.df['year'].min()} and {self.df['year'].max()}",
        )
