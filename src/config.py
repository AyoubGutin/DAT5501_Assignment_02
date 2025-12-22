# -- Imports --
from pathlib import Path

# -- Project Root --
PROJECT_ROOT = Path(__file__).resolve().parents[1]  # one level up from src/

# -- Folders --
DATA_DIR = PROJECT_ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"

# -- Filenames --
DEMOGRAPHY_FILE = RAW_DIR / "business_demography_2024_ref_tables.xlsx"
GVA_DIR = (
    RAW_DIR  # There are multiple GVA files in this directory, so point to the folder
)
POPULATION_FILE = RAW_DIR / "populationestimatesbylocalauthority.xlsx"
