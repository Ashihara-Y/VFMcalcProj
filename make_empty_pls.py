import pydantic
import os
import pandas as pd
import tinydb
from tinydb import TinyDB, Query

from dataclasses import asdict, dataclass
from decimal import *
from pydantic import BaseModel
import make_inputs_df, make_pl_waku
import datetime
import timeflake
from zoneinfo import ZoneInfo


def make_empty_pl(cols):
    #inputs_pdt = make_inputs_df.main()

    cols_waku = ['year','periods']

    if os.path.exists("fi_db.json"):
        db = TinyDB("fi_db.json")
        final_inputs = db.all()[0]
        target_years = final_inputs['target_years']
        first_end_fy = final_inputs['first_end_fy']
    else:
        target_years = 45
        calc_id = timeflake.random()
        dtime = datetime.datetime.fromtimestamp(calc_id.timestamp // 1000, tz=ZoneInfo("Asia/Tokyo"))
        const_start_date = datetime.date(dtime.year, dtime.month, dtime.day).strftime('%Y-%m-%d')
        start_year = datetime.datetime.strptime(str(const_start_date), '%Y-%m-%d').year
        start_month = datetime.datetime.strptime(str(const_start_date), '%Y-%m-%d').month

        if start_month < 4:
            first_end_fy = datetime.date(start_year, 3, 31)
        else:
            first_end_fy = datetime.date(start_year + 1, 3, 31)

    waku = make_pl_waku.make_waku_df(first_end_fy, target_years, cols_waku)

    added_cols = make_pl_waku.add_cols_df(target_years, waku, cols)
    empty_pl = make_pl_waku.join_cols2waku(added_cols, waku)

    return empty_pl


