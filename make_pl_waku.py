import pandas as pd
from tinydb import TinyDB, Query

from dataclasses import asdict, dataclass
from decimal import *
import make_inputs_df

def make_waku_df(first_end_fy, target_years, cols):
    waku = pd.DataFrame(
        index=range(target_years),
        columns=cols
    ).convert_dtypes(dtype_backend='pyarrow')

    waku[cols[0]] = pd.date_range(
        start=first_end_fy, 
        periods=target_years, 
        freq="12ME")
    
    waku[cols[1]] = [i+1 for i in range(target_years)]
    #waku.set_index(cols[0], inplace=True)

    return waku

def add_cols_df(first_end_fy, target_years, waku, cols):
    added_cols = pd.DataFrame(
        index=range(target_years),
        columns=cols[1:]
    ).fillna(Decimal('0.0000')).convert_dtypes('Decimal', dtype_backend='pyarrow')
    
    added_cols[cols[0]] = pd.date_range(
        start=first_end_fy, 
        periods=target_years, 
        freq="12ME")
    
    added_cols.set_index(cols[0], inplace=True)

    #duckdb.sql("CREATE OR REPLACE TABLE add_cols AS SELECT * FROM add_cols")
    #print(add_cols.dtypes)
    return added_cols

def join_cols2waku(added_cols, waku):
    result = waku.join(added_cols)

    #duckdb.sql("CREATE OR REPLACE TABLE result AS SELECT * FROM result")

    return result






