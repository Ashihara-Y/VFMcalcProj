import sqlalchemy
import pandas as pd
import joblib
import flet as ft
#from flet import client_storage, session_storage
from ulid import ULID
import timeflake
import datetime
import duckdb
import pyarrow as pa
import pathlib

def save_ddb():
    final_inputs = joblib.load("final_inputs.joblib")
    res_PSC_LCC = joblib.load("res_PSC_LCC.joblib")
    results = joblib.load("results.joblib")
    user_id = ULID.from_datetime(datetime.datetime.now())
    calc_id = timeflake.random()

    df_PV_cf = results["df_PV_cf"].round(3)
    LCC_dc_fctr = pd.Series(results["LCC_discount_factor"])
    PSC_ct_dc_fctr = pd.Series(results["PSC_const_discount_factor"])
    PSC_iji_dc_fctr = pd.Series(results["PSC_iji_discount_factor"]) 

    PSC_dc_fctr = pd.concat([PSC_ct_dc_fctr, PSC_iji_dc_fctr], axis=0).reset_index(drop=True)
    PSC_LCC_dc_fctr = pd.concat([PSC_dc_fctr, LCC_dc_fctr], axis=1, ignore_index=True)
    df_PV_cf_dc = pd.concat([df_PV_cf, PSC_LCC_dc_fctr], axis=1, ignore_index=True)

    user_id_c = []
    calc_id_c = []

    for i in range(len(LCC_dc_fctr)):
        user_id_c.append(user_id)

    for i in range(len(LCC_dc_fctr)):
        calc_id_c.append(str(calc_id))

    df_PV_cf_dc['user_id'] = user_id_c
    df_PV_cf_dc['calc_id'] = calc_id_c

    #dt_PV_cf_dc = pa.Table.from_pandas(df_PV_cf_dc)
    
    final_inputs = pd.DataFrame(final_inputs, index=[0])
    res_PSC_LCC = pd.DataFrame(res_PSC_LCC, index=[0])

    final_inputs['user_id'] = user_id
    final_inputs['calc_id'] = str(calc_id)
    res_PSC_LCC['user_id'] = user_id
    res_PSC_LCC['calc_id'] = str(calc_id)

    #dt_final_inputs = pa.Table.from_pandas(final_inputs)
    #dt_res_PSC_LCC = pa.Table.from_pandas(res_PSC_LCC)

    con = duckdb.connect('file' + str(calc_id) + '.db')
    con.sql('DROP TABLE IF EXISTS table_dccf')
    con.sql("CREATE TABLE table_dccf AS SELECT * FROM df_PV_cf_dc")
    con.sql('DROP TABLE IF EXISTS table_final_inputs')
    con.sql("CREATE TABLE table_final_inputs AS SELECT * FROM final_inputs")
    con.sql('DROP TABLE IF EXISTS table_res_PSC_LCC')
    con.sql("CREATE TABLE table_res_PSC_LCC AS SELECT * FROM res_PSC_LCC")

#   