import pandas as pd
from functools import lru_cache
from pathlib import Path


@lru_cache(maxsize=1)
def get_dataframe() -> pd.DataFrame:
    base_path = Path(__file__).resolve().parent.parent
    file_path = base_path / "data" / "titanic.csv"

    df = pd.read_csv(file_path)
    return df