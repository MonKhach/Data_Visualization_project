# Placement Data Dashboard

This project is an interactive dashboard built with Dash and Plotly for analyzing student placement outcomes.

The dashboard explores student placement status, academic performance, work experience, specialization, and salary patterns.

## Dashboard Pages

The dashboard contains three pages:

1. Overview
2. Placement Drivers
3. Salary Analysis

## Main Features

- Multi-page Dash dashboard
- KPI cards
- Interactive Plotly visualizations
- Dropdown filters
- Slider filter
- Input field
- Button-based filtering
- Dash callbacks

## Dataset

The project uses the Placement dataset.

The CSV file should be located in:

```text
data/Placement_Data_Full_Class.csv

## How to Run the Project

1. Clone or download this repository.

2. Make sure the dataset file is located in the project folder:

```text
Placement_Data_Full_Class.csv
or inside the data folder
data/Placement_Data_Full_Class.csv

3. Install the required python packages
pip install -r requirements.txt

4. Run Dash app
python app.py

5. Open dashboard in the browser
http://127.0.0.1:8050