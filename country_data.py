import pandas as pd


file = "data/population_1960.csv"
max_objects = 25

df = pd.read_csv(file, sep=",")
df["Population"] = df["Population"].fillna(0).astype(int)

last_page = df.shape[0] / max_objects
last_page = int(last_page) + 1 if isinstance(last_page, float) else last_page

df.columns = ['name','code','population']
