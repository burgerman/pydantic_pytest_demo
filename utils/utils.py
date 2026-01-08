import pandas as pd
from typing import Any

def get_statistics_df(df: pd.DataFrame, group_by: list[str], val_col: str, agg_func: list[str]) -> Any:
    try:
        stats = df.groupby(by=group_by)[val_col].agg(agg_func)
        return stats
    except ValueError as val_error:
        print("The given values not supported", val_error)
        return None

def to_dict_from_dataframe(df: pd.DataFrame) -> dict:
    return df.to_dict(orient='records')