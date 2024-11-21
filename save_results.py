import sys
sys.dont_write_bytecode = True
import os
import pandas as pd
import duckdb
from ulid import ULID
import timeflake
import datetime
import tinydb
from tinydb import TinyDB, Query

# 各計算結果に、その計算の入力データを一緒に格納しておくか？
# だとすれば、FIの内容（辞書）をDFにしてDuckDBに「finalinputs_table」として入れておくか。

conn = duckdb.connect('VFM.duckdb')
c = conn.cursor()

# TinyDBから、fi_db.jsonを読み込む。

PSC_df = c.sql('SELECT * FROM PSC_table').df()
PSC_pv_df = c.sql('SELECT * FROM PSC_pv_table').df()
LCC_df = c.sql('SELECT * FROM LCC_table').df()
LCC_pv_df = c.sql('SELECT * FROM LCC_pv_table').df()
SPC_df = c.sql('SELECT * FROM SPC_table').df()
SPC_check_df = c.sql('SELECT * FROM SPC_check_table').df()
Risk_df = c.sql('SELECT * FROM Risk_table').df()
VFM_df = c.sql('SELECT * FROM VFM_table').df()
PIRR_df = c.sql('SELECT * FROM PIRR_table').df()
# ここで、FIのDFを作成しておく。

user_id = ULID.from_datetime(datetime.datetime.now())
calc_id = timeflake.random()
dtime = datetime.datetime.fromtimestamp(calc_id.timestamp // 1000)

df_list = [PSC_df,PSC_pv_df,LCC_df,LCC_pv_df,SPC_df,SPC_check_df,Risk_df,VFM_df,PIRR_df]
df_name_list = ['PSC_df','PSC_pv_df','LCC_df','LCC_pv_df','SPC_df','SPC_check_df','Risk_df','VFM_df','PIRR_df']

def addID(x_df):
    x_df['datetime'] = str(dtime)
    x_df['user_id'] = str(user_id)
    x_df['calc_id'] = str(calc_id)

    return x_df

for i in df_list:
    addID(i)

def save_ddb(x_df, name_x_df):
    c.sql('CREATE TABLE IF NOT EXISTS ' + name_x_df + '_results_table AS SELECT * FROM ' + name_x_df)
    new_df_name = name_x_df + '_added'
    new_df_name = c.sql("SELECT * FROM " + name_x_df + "_results_table").df()
    if new_df_name['datetime'].iloc[0] != x_df['datetime'].iloc[0]: 
        c.sql('INSERT INTO ' + name_x_df + '_results_table SELECT * FROM ' + name_x_df)   
    else:
        pass

for i in df_list:
    for j in df_name_list:
        save_ddb(i,j)    #ft.Page.go(self, route="/view_saved")
    #fi_db = sqlite3.connect("final_inputs.db")
        