from pyarrow import Table
from pyarrow.parquet import read_table


def load_series(path: str) -> Table:

    data = read_table(path)

    return data
