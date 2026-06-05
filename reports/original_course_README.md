# Analysis of U.S. Wind Energy Potential by States
DSCI 510

Final Project

Dezhen Zhang

## Introduction

Wind energy is the second-largest source of renewable electricity in the United States, generated through wind turbines. As a naturally occurring and inexhaustible resource, wind provides a reliable and sustainable long-term energy solution. However, the strategic placement of wind turbines is critical to maximizing their efficiency and overall effectiveness.

This project analyzes state-level wind energy production across the United States from 2001 to 2023 and explores regions with strong potential for future wind development. It integrates multiple datasets, including:Historical wind production data, Average wind speed by state, Potential wind energy capacity, and Tornado disaster frequency.

The objective is to:

- Identify past production trends  
- Evaluate the relationship between wind potential, average wind speed, and disaster risk  
- Apply clustering methods to group states with similar profiles  

These insights aim to support data-driven decision-making in renewable energy planning, infrastructure development, and climate risk mitigation.


## Data Sources

| No. | Dataset | Description | Source |
|-----|---------|-------------|--------|
| 1 | **Wind Power Production (2001–2023)** | Historical monthly wind energy production data across all U.S. states. Used to analyze state-level wind development trends and identify top producers. | [Kaggle – Wind Power Production US 2001–2023](https://www.kaggle.com/datasets/henriupton/wind-power-production-us-2001-2023) *(via Kaggle API)* |
| 2 | **Average Wind Speeds by State** | Provides each U.S. state's average wind speed (MPH). Useful for identifying optimal wind turbine placement zones. | [LandGate](https://www.landgate.com/news/average-wind-speeds-by-state) *(Web Scraped)* |
| 3 | **Tornado Events by State (1950–2022)** | Contains tornado occurrences, magnitudes, and locations across U.S. states. Used to assess disaster risks in wind development areas. | [Kaggle – Tornados Dataset](https://www.kaggle.com/datasets/sujaykapadnis/tornados) *(via Kaggle API)* |
| 4 | **Total Potential Wind Capacity (MW)** | Indicates each state’s wind energy development potential based on available land and conditions. Used for spatial suitability analysis. | [U.S. Department of Energy – WindExchange](https://windexchange.energy.gov/maps-data/321) *(Downloaded from government site; saved in Google Drive)* |


## Approach and Analysis

To achieve the project’s objectives, the analysis is structured into three main parts:

### 1. Historical Wind Production Analysis
- Identifies the top and bottom wind-producing states by total output.
- Analyzes state-level wind energy growth trends over time.
- Visualizes the contribution of top-producing states to national wind output.

### 2. Tornado Frequency and Magnitude Analysis
- Visualizes total tornado event counts per state.
- Breaks down tornado magnitudes in the most disaster-prone states (0 to 3 scale).

### 3. Correlation and Clustering of Wind Speed, Potential Yield, and Tornado Disaster Data
- Computes correlations between average wind speed, wind energy potential, and tornado frequency using a heatmap.
- Uses regression plots to explore key relationships.
- Applies the Elbow Method to determine the optimal number of clusters.
- Performs K-Means clustering to group states based on wind speed, wind capacity potential, and tornado risk.


## Summary of the results
- The top 10 states by total wind production are Texas, Iowa, California, Minnesota, Colorado, Oregon, Wyoming, Nebraska, New York, and South Dakota. The Top 5 states by energy production growth is Texas, Iowa, Oklahoma, Kansas, and Illinois.
- Texas is the national leader in both wind energy production growth rate and total output from 2001 to 2023.  
- Wind energy growth is accelerating, with Texas, Iowa, and Oklahoma showing the highest increases in production over time.  
- Tornado events are regionally concentrated, with Texas, Florida, and Kansas experiencing the highest number of tornadoes since 1950.  
- Most tornadoes are of lower magnitude in the top five tornado-prone states.  

### Correlation Insights
- A moderate positive relationship exists between average wind speed and wind energy potential.  
- A stronger correlation is observed between wind potential and tornado frequency, suggesting that high-potential wind areas often overlap with high-risk disaster zones.

### Clustering Results (K-Means)
- Elbow Method is used to determine the optimal number of clusters for K-Means clustering, and picked k = 3 for K-means clustering.
- Cluster 2 includes states have high wind protential, such as Texas, Kansas, and New Mexico, and some of the states show high wind potential but also high tornado risk.  
- Cluster 1 represents states with moderate wind potential and disaster risk.  
- Cluster 0 includes states with low wind potential and minimal disaster frequency.
- States in Cluster 2 are Arizona, Kansas, Montana, Nebraska, Nevada, New Mexico, Texas, Wyoming

## Discussion
These findings emphasize that wind energy is a rapidly growing sector in the United States. The analysis highlights a clear opportunity–risk tradeoff in wind energy development—states like Texas offer high renewable energy potential but also face higher natural hazard risks. As a result, the placement of wind turbines should not be driven by a single-factor perspective. Instead, development strategies must be region-specific and consider a combination of factors including local policies, renewable resource availability, and socio-economic conditions.


## How to run:
Follow these steps to reproduce the full pipeline, including data fetching, processing, and analysis:

### 1. Set Up Kaggle API

- Visit (https://www.kaggle.com/account)
- Click "Create New API Token" to download `kaggle.json`, check if it includes: username and key
- Save the file into same working directory as downloaded files

### 2. Download Required Files for data source 1 and 3

Download the following py from the `src/` folder into the **same working directory**:  `config.py`, `get_kaggle.py`,`get_data.py`, `data_analysis.py`

- Edit the following for `config.py` :

  - MY_API_KEY_PATH = "path/to/your/kaggle.json" to where you store the "kaggle.json"
  - BASE_DATA_DIR = os.path.expanduser("path/to/save/downloaded/data") to where you want the download file from kaggle to be.
  

- No edits required for get_data.py, get_kaggle.py and data_analysis.py


### 3. Download Required Files from google drive for data source 2 
 
- Open (https://drive.google.com/drive/folders/1D0Iy0MXt1ajLXR4I5TvIEBxyJEMxCK8E?usp=drive_link) download the total_wind_capacity_80m.csv to the same working directory

### 4. Check the requirements.txt and download all the required package before running the codes
  
### 5. Run the Analysis Notebook 

- Download results.ipynb from github final_project and save with all the downloaded files from previous steps
- Open results.ipynb in Jupyter Notebook or VSCode and run all cells to: fetch data from Kaggle, process and merge datasets, and generate figures with Markdown interpretations


