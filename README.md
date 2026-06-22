# Nassau Candy Optimizer (Streamlit)

Decision intelligence app to support **factory reallocation** and **shipping lead-time optimization** for Nassau Candy. The application loads a trained regression model that predicts shipping lead time from engineered distance and operational features, then presents recommendations across multiple interactive dashboards.

## What’s included

The Streamlit UI (see `app.py`) provides four pages:

1. **Factory Optimization Simulator** (`modules/page_1_simulator.py`)
   - Select a product and simulate predicted lead times under assignment to each factory.
   - Shows a ranked bar chart and an improvement estimate versus the current factory.

2. **What-If Scenario Analysis** (`modules/page_2_whatif.py`)
   - Compare _current_ vs _simulated_ lead time for a specific combination of **Product / Region / Ship Mode**.
   - Estimates improvement using predicted lead time for a best alternative factory (by distance heuristic).

3. **Recommendation Dashboard** (`modules/page_3_recommendations.py`)
   - Computes ranked reassignment suggestions for products based on model-predicted lead time improvements.

4. **Risk & Impact Panel** (`modules/page_4_risk.py`)
   - Applies simple rule-based risk heuristics to highlight alternatives that may be risky.

## Tech stack

- Python
- Streamlit
- pandas / numpy
- scikit-learn
- plotly
- zipcodes (used for postal-code geocoding)
- joblib (model persistence)

Dependencies are listed in `requirements.txt`.

## Project structure

```text
.
├─ app.py
├─ requirements.txt
├─ data/
│  └─ Nassau Candy Distributor.csv
├─ models/
│  ├─ lead_time_model.pkl
│  ├─ features.pkl
│  └─ train_model.py
├─ modules/
│  ├─ page_1_simulator.py
│  ├─ page_2_whatif.py
│  ├─ page_3_recommendations.py
│  └─ page_4_risk.py
├─ utils/
│  ├─ data_prep.py
│  ├─ distance.py
│  └─ factory_config.py
└─ README.md
```

## Quick start (run the app)

### 1) Install dependencies

Windows example:

```bat
py -m pip install -r requirements.txt
```

### 2) Ensure required files exist

This app expects:

- `data/Nassau Candy Distributor.csv`
- Trained artifacts in `models/`:
  - `models/lead_time_model.pkl`
  - `models/features.pkl`

If you changed the dataset or want to retrain, see **Training the model** below.

### 3) Run Streamlit

```bat
streamlit run app.py
```

Then open the local URL printed in the terminal.

## Training the model (optional)

Model training is implemented in `models/train_model.py`.

Run:

```bat
py models\train_model.py
```

This script:

1. Loads and prepares data via `utils/data_prep.py`.
2. Uses these base features:
   - `Units`
   - Distance features: `Dist_<FactoryName>` for each factory in `utils/factory_config.py`
3. Adds encoded categorical features:
   - `Ship_Mode_Enc`
   - `Region_Enc`
   - `Product_Enc`
4. Trains multiple regressors and selects the best by **R²**.
5. Saves:
   - `models/lead_time_model.pkl`
   - `models/features.pkl` (the final feature list)

## Data & pipeline details (code-level)

All data preparation happens in `utils/data_prep.py` (`prepare_data`).

### 1) Required input columns (CSV)

The code expects the following columns in `data/Nassau Candy Distributor.csv`:

- `Order Date`
- `Ship Date`
- `Postal Code`
- `Product Name`
- `Region`
- `Ship Mode`
- `Units`

It also references:

- `Lead Time` (derived, not required as an input column)
- `Sales` and `Gross Profit` are used by the **Risk & Impact Panel**.

If `Sales` / `Gross Profit` are missing, the app may error in the risk page.

### 2) Date parsing and lead time

- `Order Date` and `Ship Date` are parsed with format: **`%d-%m-%Y`**
- Lead time is computed as:

```python
Lead Time = (Ship Date - Order Date).dt.days
```

- Rows where `Lead Time <= 0` are filtered out.

### 3) Current factory mapping

`Current Factory` is derived from product name using `PRODUCT_FACTORY_MAP` in `utils/factory_config.py`.

### 4) Geocoding postal codes

Customer coordinates are derived from `Postal Code` using the `zipcodes` library:

- `Cust_Lat`, `Cust_Lon` are created
- If a postal code cannot be matched, the code falls back to `(0.0, 0.0)`.

### 5) Distance features

For each factory in `FACTORIES` (lat/lon defined in `utils/factory_config.py`), the pipeline computes:

- `Dist_<FactoryName>`

Distance uses the haversine formula implemented in `utils/distance.py`.

**Important naming detail**: factory names are sanitized in the code via:

- spaces → underscores
- apostrophes removed

So the expected feature column naming matches what `prepare_data()` generates.

### 6) Encoded categorical features

The pipeline produces:

- `Ship_Mode_Enc` (LabelEncoder)
- `Region_Enc` (LabelEncoder)
- `Product_Enc` (LabelEncoder)

These must align with the model’s saved `features.pkl`.

## Code-level notes & limitations

- **Simulation isolation**: the simulator page isolates the effect of one factory by setting distances for non-tested factories to `99999`.
- **Risk scoring**: `modules/page_4_risk.py` uses rule-based thresholds (e.g., lead-time deltas and a profit-margin heuristic) rather than a dedicated risk model.
- **Geocoding sensitivity**: distance features depend on postal-code matching quality.

## Troubleshooting

### Common errors

- **File not found**: ensure `data/Nassau Candy Distributor.csv` exists at the expected path.
- **Model artifacts missing**: ensure both `models/lead_time_model.pkl` and `models/features.pkl` exist.
- **Date parsing issues**: ensure date strings match `DD-MM-YYYY`.

## License

Add a license file if you plan to distribute the project.

## Contributing

Contributions are welcome via pull requests.
