## Data Sources

All raw data in `data/raw` are from the UK Office for National Statistics (ONS).

- **Business demography**: `business_demography_2024_ref_tables.xlsx`
  - [Births, deaths, active enterprises by local authority.](https://www.ons.gov.uk/businessindustryandtrade/business/activitysizeandlocation/datasets/businessdemographyreferencetable)
- **Population**: `populationestimatesbylocalauthority.xlsx`
  - [Mid-year population estimates by local authority, 1998–2023.](https://www.ons.gov.uk/economy/grossdomesticproductgdp/datasets/regionalgrossvalueaddedbalancedbyindustrylocalauthoritiesbyitl1region)
- **GVA**: `regionalgrossvalueaddedbalancedbyindustrylocalauthorities*.xlsx`
  - [Regional GVA balanced by industry and local authority, Table 2 chained volume measures, £ millions.](https://www.ons.gov.uk/economy/grossdomesticproductgdp/datasets/regionalgrossvalueaddedbalancedbyindustrylocalauthoritiesbyitl1region)

## Cleaning Pipeline

The pipeline is implemented as separate scripts in `src/`:

1. `clean_demography.py`

   - Reads births, deaths, and active businesses from multiple sheets.
   - Converts wide multi-year tables to long format
   - Normalises geographic codes/names
   - Keeps ONS supression intact (missing values for small counts due to PII) as 'NaN'
   - Outputs: `data/processed/business_demography_counts.csv`.

2. `clean_population.py`

   - Reads wide population table
   - Melts years into long format
   - Handles uncertainty flags by:
   - Converting to 'NaN'
   - Forward-filling within each `geo_code`
   - Adding a `is_unreliable` flag where original value was `[u]`.
   - Outputs: `data/processed/population.csv`.

3. `clean_gva.py`

   - Reads wide GVA table
   - Melts years into long format
   - From each, filter for total industries
   - Handles uncertainty flags by:
     - Converting to 'NaN'
     - Forward-filling within each `geo_code`
   - Outputs: `data/processed/gva.csv`.

4. `merge_datasets.py`
   - Loads the three processsed CSVSs
   - Joins on the common fields
   - Keeps years 2019-2023, where demography, population, and GVA overlap
   - Uses left joins so all demography rows are preserved, GVA is NaN where not available
   - Outputs `data/processed/final_dataset.csv`.

## Final Dataset

`data/processed/final_dataset.csv` has:

- **Rows**: 2126
- **Columns**:
  - `geo_code`: Local authority code.
  - `geo_name`: Local authority name.
  - `year`: Calendar year.
  - `births`: Business births
  - `deaths`: Business deaths
  - `active`: Active businesses
  - `population`: Mid-year population.
  - `gva_million`: GVA in 2022 prices, £ millions.
  - `is_unreliable`: Boolean flag where population was marked `[u]`

## Tests

Unit tests in `tests/` validate:

- No duplicate `(geo_code, year)` combinations in any processed dataset.
- Non-negative for counts and values.
- Schema of `final_dataset.csv` (columns, years 2019–2023 only, row count).

Run all tests with:

`pytest`
