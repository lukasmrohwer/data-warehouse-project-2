#find the set difference between two csvs

import pandas as pd

data1 = pd.read_csv("routes_edges.csv")
data2 = pd.read_csv("message.csv")


# find the rows in data1 that are not in data2
data_diff = pd.concat([data1, data2]).drop_duplicates(keep=False)

print(data_diff.to_string())