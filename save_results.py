import sys
sys.dont_write_bytecode = True
import os
import pandas as pd
#import joblib
import flet as ft
#from flet import client_storage, session_storage
from ulid import ULID
import timeflake
import datetime
import duckdb
import sqlite3
import tinydb
from tinydb import TinyDB, Query

def save_ddb(results, results_2):
    #fi_db = sqlite3.connect("final_inputs.db")
    fi_db = TinyDB('fi_db.json')
    fi_dic = fi_db.all()[0]
    fi_db.close()

    results_dic = {**results, **fi_dic}
    
    user_id = ULID.from_datetime(datetime.datetime.now())
    calc_id = timeflake.random()

    dtime = datetime.datetime.fromtimestamp(calc_id.timestamp // 1000)

    results_dic['datetime'] = str(dtime)
    results_dic['user_id'] = str(user_id)
    results_dic['calc_id'] = str(calc_id)

    results_2 = {**results_dic, **results_2}
    #results_2['datetime'] = str(dtime)
    #results_2['user_id'] = str(user_id)
    #results_2['calc_id'] = str(calc_id)

    res_df_db = TinyDB("res_01_db_" + str(calc_id) + ".json")
    res_df_db.insert(results_dic)
    res_df_db.close()

    df_PV_cf_db = TinyDB('res_02_db.json')
    df_PV_cf_db.insert(results_2)
    df_PV_cf_db.close()
        