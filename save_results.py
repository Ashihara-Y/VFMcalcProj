import os
import pandas as pd
#import joblib
import flet as ft
#from flet import client_storage, session_storage
from ulid import ULID
import timeflake
import datetime
#import duckdb
import sqlite3

def save_ddb(results):
    fi_db = sqlite3("final_inputs.db")
    final_inputs_df = pd.read_sql_query('SELECT * FROM final_inputs', fi_db)

    res_db = sqlite3("results.db")
    res_PSC_LCC_df = pd.read_sql_query('SELECT * FROM res_PSC_LCC', res_db)
    PSC_LCC_VFM_df = pd.read_sql_query('SELECT * FROM PSC_LCC_VFM', res_db)
    df_PV_cf_dc = pd.read_sql_query('SELECT * FROM df_PV_cf', res_db)

    #results = joblib.load("results.joblib")
    user_id = ULID.from_datetime(datetime.datetime.now())
    calc_id = timeflake.random()

    LCC_dc_fctr = df_PV_cf_dc["LCC_discount_factor"]

    user_id_c = []
    calc_id_c = []
    datetime_c = []

    dtime = datetime.datetime.fromtimestamp(calc_id.timestamp // 1000)

    for i in range(len(LCC_dc_fctr)):
        user_id_c.append(user_id)

    for i in range(len(LCC_dc_fctr)):
        calc_id_c.append(str(calc_id))

    for i in range(len(LCC_dc_fctr)):
        datetime_c.append(dtime)

    df_PV_cf_dc['user_id'] = user_id_c
    df_PV_cf_dc['calc_id'] = calc_id_c
    df_PV_cf_dc['datetime'] = datetime_c
    
    vfm_results = PSC_LCC_VFM_df

    final_inputs = final_inputs_df
    res_PSC_LCC = res_PSC_LCC_df

    final_inputs['datetime'] = dtime

    
    save_results = {
        'final_inputs': final_inputs,
        'res_PSC_LCC': res_PSC_LCC,
        'vfm_results': vfm_results,
        'df_PV_cf_dc': df_PV_cf_dc
    }

    s_res_db = sqlite3.connect('save_results_' + str(calc_id) + '.db')
    final_inputs.to_sql('final_inputs', s_res_db, if_exists='replace')
    res_PSC_LCC.to_sql('res_PSC_LCC', s_res_db, if_exists='replace')
    vfm_results.to_sql('vfm_results', s_res_db, if_exists='replace')
    df_PV_cf_dc.to_sql('df_PV_cf_dc', s_res_db, if_exists='replace')
    s_res_db.close()
    #con.sql('DROP TABLE IF EXISTS table_final_inputs')
    #con.sql("CREATE TABLE table_final_inputs AS SELECT * FROM final_inputs")
    #con.sql('DROP TABLE IF EXISTS table_res_PSC_LCC')
    #con.sql("CREATE TABLE table_res_PSC_LCC AS SELECT * FROM res_PSC_LCC")
    #con.sql('DROP TABLE IF EXISTS table_vfm_results')
    #con.sql("CREATE TABLE table_vfm_results AS SELECT * FROM vfm_results")

#   