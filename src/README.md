# Source Code

This folder contains the reusable Python scripts for the wind energy potential analysis.

| File | Purpose |
|---|---|
| `config.py` | Stores project paths and Kaggle dataset IDs. This version is safe for GitHub and does not include private API keys. |
| `get_kaggle.py` | Downloads Kaggle datasets into `data/raw/` when local Kaggle credentials are configured. |
| `get_data.py` | Cleans and merges wind production, wind speed, tornado, and wind capacity datasets. |
| `data_analysis.py` | Contains plotting, correlation, and K-Means clustering functions used by the notebook. |

Do not upload `kaggle.json` or any private API keys to GitHub.
