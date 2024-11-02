import pydantic
import os
import pandas as pd
import tinydb
from tinydb import TinyDB, Query
import pyxirr

from dataclasses import asdict, dataclass
import datetime
from decimal import *
from pydantic import BaseModel
import pandera as pa
from pandera.typing import Series, DataFrame
import duckdb
import make_inputs_df, make_pl_waku

inputs_pdt, inputs_supl_pdt = make_inputs_df.io()

cols_waku = ['year','periods']

target_years = inputs_supl_pdt.target_years.iloc[0]
first_end_fy = inputs_supl_pdt.first_end_fy.iloc[0]

waku = make_pl_waku.make_waku_df(first_end_fy, target_years, cols_waku)
print(waku.info())

cols_PSC_income = ['periods','hojokin','kouhukin','kisai_gaku','riyou_ryoukin']
added_cols = make_pl_waku.add_cols_df(target_years, waku, cols_PSC_income)
print(added_cols.info())

empty_pl_PSC_income = make_pl_waku.join_cols2waku(added_cols, waku)

print(empty_pl_PSC_income.info())