import pandas as pd
import pickle
import os
import base64

df = pd.read_csv(os.path.join(os.path.dirname(__file__), "../data/file.csv"))
print(df.head())
serialized_data = pickle.dumps(df)# bytes
print(serialized_data[0:50])
print(base64.b64encode(serialized_data).decode("ascii")[0:50])