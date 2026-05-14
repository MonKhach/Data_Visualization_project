from pathlib import Path
import pandas as pd


BASE_DIR = Path(__file__).resolve().parent

DATA_PATHS = [
    BASE_DIR / "Placement_Data_Full_Class.csv",
    BASE_DIR / "data" / "Placement_Data_Full_Class.csv"
]


data_path = None

for path in DATA_PATHS:
    if path.exists():
        data_path = path
        break

if data_path is None:
    raise FileNotFoundError(
        "CSV file not found. Put Placement_Data_Full_Class.csv in the project folder "
        "or inside the data folder."
    )


df = pd.read_csv(data_path)

df["placed"] = df["status"].map({
    "Placed": 1,
    "Not Placed": 0
})

placed_df = df[df["status"] == "Placed"].copy()