# -- Imports --
from pathlib import Path

# Project Root
PROJECT_ROOT = Path(__file__).resolve().parents[1]

# Folders
DATA_DIR = PROJECT_ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"

# Filenames
DEMOGRAPHY_FILE = RAW_DIR / "business_demography_2024_ref_tables.xlsx"
GVA_DIR = RAW_DIR
POPULATION_FILE = RAW_DIR / "populationestimatesbylocalauthority.xlsx"
