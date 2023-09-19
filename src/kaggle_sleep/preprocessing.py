import os
import shutil

import pandas as pd
import numpy as np

from pyarrow.compute import field
from pyarrow import Table


def get_time_series(time_series: Table, df_labels: pd.DataFrame,
                    n_steps: int, path: str) -> pd.DataFrame:

    date_format = '%Y-%m-%dT%H:%M:%S%z'

    df_records = []
    for series_id, df in df_labels.groupby('series_id'):

        series_flt = field('series_id') == series_id
        series = time_series.filter(series_flt).to_pandas()

        # pdb.set_trace()
        series['timestamp'] = pd.to_datetime(series['timestamp'],
                                             format=date_format, utc=True)

        labels = df.T.to_dict().values()

        for idx, label in enumerate(labels):
            if ~np.isnan(label['step']):

                flt = series['timestamp'] <= label['timestamp']
                df_record = series[flt].tail(n_steps).copy()

                df_record.insert(1, 'id', idx)
                df_records.append(df_record)

        if df_records:
            df_records = pd.concat(df_records, ignore_index=True)
            df_records.to_parquet(path, engine='pyarrow',
                                  partition_cols=['series_id'])
            df_records = []
