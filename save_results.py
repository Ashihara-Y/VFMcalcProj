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

def save_ddb(results):
    #fi_db = sqlite3.connect("final_inputs.db")
    fi_db = TinyDB('fi_db.json')
    fi_dic = fi_db.all()[0]
    #final_inputs_df = pd.DataFrame(data=fi_dic, index=[1])

    #res_db = sqlite3.connect("results.db")
    #res_db = duckdb.connect('results.db')
    #res_PSC_LCC_df = results['res_PSC_LCC']
    #PSC_LCC_VFM_df = results['PSC_LCC_VFM_df']
    #df_PV_cf_dc = results['df_PV_cf']
    #results = joblib.load("results.joblib")
    results_dic = {**results, **fi_dic}
    
    user_id = ULID.from_datetime(datetime.datetime.now())
    calc_id = timeflake.random()

    #LCC_dc_fctr = df_PV_cf_dc["LCC_discount_factor"]

    #user_id_c = []
    #calc_id_c = []
    #datetime_c = []

    dtime = datetime.datetime.fromtimestamp(calc_id.timestamp // 1000)

    #for i in range(len(LCC_dc_fctr)):
    #    user_id_c.append(str(user_id))

    #for i in range(len(LCC_dc_fctr)):
    #    calc_id_c.append(str(calc_id))

    #for i in range(len(LCC_dc_fctr)):
    #    datetime_c.append(str(dtime))

    #df_PV_cf_dc['user_id'] = user_id_c
    #df_PV_cf_dc['calc_id'] = calc_id_c
    #df_PV_cf_dc['datetime'] = datetime_c
    
    #vfm_results = PSC_LCC_VFM_df

    #final_inputs = final_inputs_df
    #res_PSC_LCC = res_PSC_LCC_df

    #final_inputs['datetime'] = str(dtime)

    #res_df = pd.concat([final_inputs, res_PSC_LCC], axis=1)
    #res_df = pd.concat([res_df, vfm_results], axis=1)

    results_dic['datetime'] = str(dtime)
    results_dic['user_id'] = str(user_id)
    results_dic['calc_id'] = str(calc_id)

    #save_results = {
    #    'final_inputs': final_inputs,
    #    'res_PSC_LCC': res_PSC_LCC,
    #    'vfm_results': vfm_results,
    #    'df_PV_cf_dc': df_PV_cf_dc
    #}

    #s_res_db = sqlite3.connect('save_results_' + str(calc_id) + '.db')
    #final_inputs.to_sql('final_inputs', s_res_db, if_exists='replace')
    #res_PSC_LCC.to_sql('res_PSC_LCC', s_res_db, if_exists='replace')
    #vfm_results.to_sql('vfm_results', s_res_db, if_exists='replace')
    #df_PV_cf_dc.to_sql('df_PV_cf_dc', s_res_db, if_exists='replace')
    #s_res_db.close()
    
    res_df_db = TinyDB("res_01_db_" + str(calc_id) + ".json")
    res_df_db.insert(results_dic)

    #df_PV_cf_db = TinyDB('res_02_db_' + str(calc_id) + '.json')
    #df_PV_cf_db.insert(df_PV_cf_dc.to_dict())
        
    #con.sql('DROP TABLE IF EXISTS table_final_inputs')
    #con.sql("CREATE TABLE table_final_inputs AS SELECT * FROM final_inputs")
    #con.sql('DROP TABLE IF EXISTS table_res_PSC_LCC')
    #con.sql("CREATE TABLE table_res_PSC_LCC AS SELECT * FROM res_PSC_LCC")
    #con.sql('DROP TABLE IF EXISTS table_vfm_results')
    #con.sql("CREATE TABLE table_vfm_results AS SELECT * FROM vfm_results")

#   