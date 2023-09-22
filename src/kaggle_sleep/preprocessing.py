import os

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib

from .params import paths

from pyarrow.compute import field
from pyarrow import Table
from tqdm import tqdm
from pyts.image import GramianAngularField


def get_time_series(time_series: Table, df_labels: pd.DataFrame,
                    n_steps: int, path: str) -> pd.DataFrame:

    date_format = '%Y-%m-%dT%H:%M:%S%z'

    df_records = []
    for series_id, df in df_labels.groupby('series_id'):

        series_flt = field('series_id') == series_id
        series = time_series.filter(series_flt).to_pandas()

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


def time_series_to_image(X: np.ndarray) -> np.ndarray:

    mapping = GramianAngularField()
    X_transformed = mapping.fit_transform([X])

    return X_transformed


def preprocess(labels: pd.DataFrame, time_series: pd.DataFrame) -> None:

    matplotlib.use('Agg')

    cols_all = ['series_id', 'id', 'event']
    df_all = labels.merge(time_series[['series_id', 'step', 'id']],
                          on=['series_id', 'step'])[cols_all]

    grouper = time_series.groupby(['series_id', 'id'], observed=True)
    records = []
    for (series_id, id), df_ in tqdm(grouper):

        flt = (df_all['series_id'] == series_id) & (df_all['id'] == id)
        label = list(df_all[flt].T.to_dict().values())[0]['event']

        anglez = time_series_to_image(df_['anglez'].to_numpy())
        enmo = time_series_to_image(df_['enmo'].to_numpy())

        fig, ax = plt.subplots()
        ax.imshow(anglez[0])
        ax.axis('off')
        image_file_name = os.path.join(paths['data'], 'dataset', 'images',
                                       f'{series_id}_{id}_anglez.jpg')
        fig.savefig(image_file_name, bbox_inches='tight', pad_inches=0)

        fig, ax = plt.subplots()
        ax.imshow(enmo[0])
        ax.axis('off')
        image_file_name = os.path.join(paths['data'], 'dataset', 'images',
                                       f'{series_id}_{id}_enmo.jpg')
        fig.savefig(image_file_name, bbox_inches='tight', pad_inches=0)

        records.append((f'{series_id}_{id}', label))
        plt.close('all')

    df = pd.DataFrame(records, columns=['image_id', 'label'])
    labels_path = os.path.join(paths['data'], 'dataset', 'labels.csv')
    df.to_csv(labels_path, index=False)
