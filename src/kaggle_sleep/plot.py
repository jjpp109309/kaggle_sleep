import pyarrow.compute as pc
import plotly.express as px
import pandas as pd

from pyarrow import Table
from toolz import curry


@curry
def _convert_date(df: pd.DataFrame, col: str,  date_fmt: str) -> pd.DataFrame:
    return pd.to_datetime(df[col], format=date_fmt)


@curry
def plot_series(data_series: Table, df_events: pd.DataFrame, series_id: str,
                variable: str) -> None:

    flt_series = pc.field('series_id') == series_id
    df = data_series.filter(flt_series).to_pandas()
    df_events = df_events[df_events['series_id'] == series_id]

    date_format = '%Y-%m-%dT%H:%M:%S%z'
    assign_conf = {
        'timestamp': _convert_date(col='timestamp', date_fmt=date_format)
    }
    df = df.assign(**assign_conf)
    df_events = df_events.assign(**assign_conf)

    fig = px.line(data_frame=df, x='timestamp', y=variable)

    # for _, event in df_events[['event', 'timestamp']].T.to_dict().items():
    #     if event['timestamp']:
    #         fig.add_vline(x=event['timestamp'])

    fig.show()


plot_anglez = plot_series(variable='anglez')
plot_enmo = plot_series(variable='enmo')
