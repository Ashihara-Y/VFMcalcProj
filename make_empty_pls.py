import pydantic
import os
import pandas as pd
import tinydb
from tinydb import TinyDB, Query

from dataclasses import asdict, dataclass
from decimal import *
from pydantic import BaseModel
import make_inputs_df, make_pl_waku

db = TinyDB("fi_db.json")
final_inputs = db.all()[0]


def make_empty_pl(cols):
    #inputs_pdt = make_inputs_df.main()

    cols_waku = ['year','periods']

    target_years = final_inputs.target_years
    first_end_fy = final_inputs.first_end_fy

    waku = make_pl_waku.make_waku_df(first_end_fy, target_years, cols_waku)

    added_cols = make_pl_waku.add_cols_df(target_years, waku, cols)
    empty_pl = make_pl_waku.join_cols2waku(added_cols, waku)

    return empty_pl


