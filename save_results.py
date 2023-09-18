import os
import pandas as pd
import joblib
import flet as ft
#from flet import client_storage, session_storage
from ulid import ULID
import timeflake
import datetime
import duckdb
import pyarrow as pa
import tinydb
from tinydb import TinyDB, Query

def save_ddb():
    fi_db = TinyDB("fi_db.json")
    final_inputs = fi_db.all()[0]
    res_PSC_LCC = joblib.load("results.joblib")['res_PSC_LCC']
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
    
    #vfm_results_psc = results["PSC"]
    #vfm_results_lcc = results["LCC"]
    #vfm_results_vfm = results["VFM"]
    #vfm_results_vfm_percent = results["VFM_percent"]
    vfm_results = {'PSC': results['PSC'], 'LCC': results['LCC'], 'VFM': results['VFM'], 'VFM_percent': results['VFM_percent']}
    vfm_results = pd.DataFrame(vfm_results, index=[0])
    #vfm_results['user_id'] = user_id
    #vfm_results['calc_id'] = str(calc_id)

    final_inputs = pd.DataFrame(final_inputs, index=[0])
    res_PSC_LCC = pd.DataFrame(res_PSC_LCC, index=[0])

#    final_inputs['user_id'] = user_id
#    final_inputs['calc_id'] = str(calc_id)
    final_inputs['datetime'] = dtime
 #   res_PSC_LCC['user_id'] = user_id
 #   res_PSC_LCC['calc_id'] = str(calc_id)
 #   res_PSC_LCC['datetime'] = dtime

    #if os.path.exists("dt_ci_db.json"):
    #    os.remove("dt_ci_db.json")
    #db = TinyDB("dt_ci_db.json")
    #db.insert({'calc_id': str(calc_id), 'datetime': dtime})
    
    save_results = {
        'final_inputs': final_inputs,
        'res_PSC_LCC': res_PSC_LCC,
        'vfm_results': vfm_results,
        'df_PV_cf_dc': df_PV_cf_dc
    }

    joblib.dump(save_results,'save_results_' + str(calc_id) + '.joblib')
    #con.sql('DROP TABLE IF EXISTS table_final_inputs')
    #con.sql("CREATE TABLE table_final_inputs AS SELECT * FROM final_inputs")
    #con.sql('DROP TABLE IF EXISTS table_res_PSC_LCC')
    #con.sql("CREATE TABLE table_res_PSC_LCC AS SELECT * FROM res_PSC_LCC")
    #con.sql('DROP TABLE IF EXISTS table_vfm_results')
    #con.sql("CREATE TABLE table_vfm_results AS SELECT * FROM vfm_results")

#   