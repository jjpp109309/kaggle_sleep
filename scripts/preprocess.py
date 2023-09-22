import os

import pandas as pd

from kaggle_sleep.params import paths
from kaggle_sleep.preprocessing import preprocess

ts_path = os.path.join(paths['data'], '30_mins.parquet')

df = pd.read_parquet(ts_path, engine='pyarrow')

df_labels = pd.read_csv(paths['labels'])

preprocess(df_labels, df)
