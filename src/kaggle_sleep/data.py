import polars as pl

from pyarrow import Table
from pyarrow.parquet import read_table


def load_series(path: str) -> Table:

    data = read_table(path)

    return data


def load_data(path: str) -> pl.DataFrame:
    data = pl.read_parquet(path, use_pyarrow=True)

    return data
