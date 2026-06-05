# U.S. Wind Energy Potential and Tornado Risk Analysis

**Course:** DSCI 510 Final Project  
**Author:** Dezhen (Daisy) Zhang  
**Project type:** Solo class project / data analyst portfolio project

## Overview

This project analyzes U.S. state-level wind energy production and future wind development potential by combining historical wind generation, average wind speed, potential wind capacity, and tornado risk data. The goal is to identify states with strong wind energy opportunity while also considering climate and disaster risk.

The project demonstrates skills in data collection, data cleaning, exploratory data analysis, visualization, correlation analysis, and K-Means clustering.

## Research Questions

1. Which U.S. states have led wind energy production from 2001 to 2023?
2. Which states show the fastest wind energy growth over time?
3. How do average wind speed, potential wind capacity, and tornado frequency relate to each other?
4. Can states be grouped into wind development profiles based on wind resources and disaster risk?

## Data Sources

| Dataset | Purpose | Source |
|---|---|---|
| Wind Power Production, 2001–2023 | Historical monthly wind energy production by U.S. state | Kaggle: Wind Power Production US 2001–2023 |
| Average Wind Speeds by State | Wind speed indicator for turbine siting potential | LandGate, web scraped |
| Tornado Events by State, 1950–2022 | Disaster risk indicator based on tornado frequency and magnitude | Kaggle: Tornados Dataset |
| Total Potential Wind Capacity at 80m | State-level wind capacity potential in MW | U.S. Department of Energy WindExchange |

## Methods

### 1. Historical Wind Production Analysis

- Calculated total wind production by state.
- Identified top and bottom wind-producing states.
- Analyzed long-term wind production growth trends.
- Visualized top-producing states and their contribution to national wind generation.

### 2. Tornado Frequency and Magnitude Analysis

- Summarized tornado event counts by state.
- Compared tornado magnitude distributions for the most tornado-prone states.
- Used tornado frequency as a disaster-risk indicator for wind infrastructure planning.

### 3. Correlation and Clustering Analysis

- Merged wind production, wind speed, wind capacity, and tornado data.
- Built correlation heatmaps and regression plots.
- Used the Elbow Method to select a K-Means cluster count.
- Applied K-Means clustering to group states into wind development and risk profiles.

## Key Findings

- Texas, Iowa, California, Minnesota, Colorado, Oregon, Wyoming, Nebraska, New York, and South Dakota were identified as the top 10 wind-producing states.
- Texas led both total wind energy output and production growth from 2001 to 2023.
- Wind energy growth was strongest in Texas, Iowa, Oklahoma, Kansas, and Illinois.
- Tornado frequency was regionally concentrated, with Texas, Florida, and Kansas among the highest-risk states.
- Average wind speed showed a moderate positive relationship with potential wind capacity.
- Potential wind capacity showed a stronger positive relationship with tornado frequency, suggesting that some high-opportunity wind regions also face higher disaster risk.
- K-Means clustering identified a high-potential cluster containing Arizona, Kansas, Montana, Nebraska, Nevada, New Mexico, Texas, and Wyoming.

## Repository Structure

```text
us-wind-energy-potential-analysis/
├── README.md
├── data/
│   ├── README.md
│   ├── data_dictionary.md
│   ├── raw/
│   │   ├── tornados.csv
│   │   ├── total_wind_capacity_80m.csv
│   │   └── wind-power-production-us.csv
│   └── processed/
├── notebooks/
│   └── 01_wind_energy_potential_analysis.ipynb
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── get_kaggle.py
│   ├── get_data.py
│   └── data_analysis.py
├── visuals/
│   ├── README.md
│   ├── figure_01_top_wind_production_bar.png
│   └── figure_02_top_wind_production_pie.png
├── reports/
│   └── original_course_README.md
├── requirements.txt
├── .gitignore
└── GITHUB_UPLOAD_GUIDE.md
```

## How to Run

1. Clone this repository.
2. Create and activate a virtual environment.
3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. The included CSV files in `data/raw/` allow the notebook to run as a portfolio version.
5. Optional: to download fresh Kaggle data, add your Kaggle API token as `kaggle.json` locally in the project root. Do **not** upload this file to GitHub.
6. Open and run:

```text
notebooks/01_wind_energy_potential_analysis.ipynb
```

## Tools Used

- Python
- pandas
- matplotlib
- seaborn
- scikit-learn
- requests
- BeautifulSoup
- Kaggle API
- Jupyter Notebook

## Portfolio Notes

This project is useful for data analyst applications because it shows an end-to-end workflow: collecting public data, cleaning and merging datasets, creating visualizations, analyzing trends, exploring risk factors, and applying unsupervised machine learning to support decision-making.

## Future Improvements

- Improve the `src/` pipeline with automated figure saving and processed-data exports.
- Save all generated figures directly into the `visuals/` folder.
- Add a processed dataset with clear column definitions.
- Add an interactive map or dashboard of wind potential and tornado risk by state.
- Compare clustering results using different scaling methods and cluster counts.
