"""Utilities for downloading Kaggle datasets used in this project."""

from __future__ import annotations

import os
import subprocess
import zipfile
from pathlib import Path

from config import BASE_DATA_DIR, KAGGLE_DATASET_URLS, configure_kaggle_credentials


def get_data_from_kaggle(
    base_data_dir: str | Path = BASE_DATA_DIR,
    kaggle_dataset_urls: list[str] | None = None,
) -> None:
    """Download and unzip Kaggle datasets into the raw data folder.

    Parameters
    ----------
    base_data_dir:
        Folder where downloaded CSV files should be stored.
    kaggle_dataset_urls:
        Kaggle dataset IDs, such as "owner/dataset-name".
    """
    configure_kaggle_credentials()

    base_data_dir = Path(base_data_dir)
    dataset_urls = kaggle_dataset_urls or KAGGLE_DATASET_URLS
    base_data_dir.mkdir(parents=True, exist_ok=True)

    for kaggle_id in dataset_urls:
        subprocess.run(
            ["kaggle", "datasets", "download", "-d", kaggle_id, "-p", str(base_data_dir)],
            check=True,
        )

    for filename in os.listdir(base_data_dir):
        if filename.endswith(".zip"):
            zip_path = base_data_dir / filename
            with zipfile.ZipFile(zip_path, "r") as zip_ref:
                zip_ref.extractall(base_data_dir)
            zip_path.unlink()

    print(f"Finished downloading and extracting datasets to {base_data_dir}.")
