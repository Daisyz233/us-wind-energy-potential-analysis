"""Project configuration for the U.S. wind energy analysis.

This file is safe to upload to GitHub because it does not contain private
credentials. Store your Kaggle API token locally as `kaggle.json` in the
project root, or set KAGGLE_USERNAME and KAGGLE_KEY as environment variables.
"""

from __future__ import annotations

import json
import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
BASE_DATA_DIR = PROJECT_ROOT / "data" / "raw"
KAGGLE_JSON_PATH = PROJECT_ROOT / "kaggle.json"

KAGGLE_DATASET_URLS = [
    "henriupton/wind-power-production-us-2001-2023",
    "sujaykapadnis/tornados",
]


def configure_kaggle_credentials(kaggle_json_path: str | Path = KAGGLE_JSON_PATH) -> None:
    """Load Kaggle credentials from a local kaggle.json file if needed.

    The Kaggle CLI can also read credentials from the environment variables
    KAGGLE_USERNAME and KAGGLE_KEY. This function only loads a local JSON file
    when those variables are missing.
    """
    if os.environ.get("KAGGLE_USERNAME") and os.environ.get("KAGGLE_KEY"):
        return

    kaggle_json_path = Path(kaggle_json_path)
    if not kaggle_json_path.exists():
        raise FileNotFoundError(
            "Kaggle credentials were not found. Add kaggle.json to the project "
            "root locally, or set KAGGLE_USERNAME and KAGGLE_KEY as environment variables. "
            "Do not upload kaggle.json to GitHub."
        )

    with kaggle_json_path.open("r", encoding="utf-8") as file:
        creds = json.load(file)

    os.environ["KAGGLE_USERNAME"] = creds["username"]
    os.environ["KAGGLE_KEY"] = creds["key"]
