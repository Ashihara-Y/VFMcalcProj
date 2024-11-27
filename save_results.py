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
import make_inputs_df


conn = duckdb.connect('VFM.duckdb')
c = conn.cursor()

# 各計算結果に、その計算の入力データを一緒に格納しておくか？
# inputs_pdt, inputs_supl_pdtを、DFに変換して、それぞれの計算結果のDFに追加するか？
inputs_pdt, inputs_supl_pdt = make_inputs_df.io()


PSC_df = c.sql('SELECT * FROM PSC_table').df()
PSC_pv_df = c.sql('SELECT * FROM PSC_pv_table').df()
LCC_df = c.sql('SELECT * FROM LCC_table').df()
LCC_pv_df = c.sql('SELECT * FROM LCC_pv_table').df()
SPC_df = c.sql('SELECT * FROM SPC_table').df()
SPC_check_df = c.sql('SELECT * FROM SPC_check_table').df()
Risk_df = c.sql('SELECT * FROM Risk_table').df()
VFM_df = c.sql('SELECT * FROM VFM_table').df()
PIRR_df = c.sql('SELECT * FROM PIRR_table').df()
# ここで、算定結果要約のDFを作成する
# 算定結果の要約は、それぞれの計算結果のDFから、必要な列を抽出して、新しいDFを作成する
# 必要な列として、PSCのキャッシュフロー現在価値合計額、LCCのキャッシュフロー現在価値合計額、SPCの融資返済チェック結果、リスクの調整額、VFM（金額と対PSC比率）、PIRRを抽出する
# それぞれのDFから、必要な列を抽出して、新しいDFを作成する
# それぞれのDFの列名は、それぞれの計算結果のDFの列名と同じにする

PSC_summary_df = PSC_df[['PSC_CashFlow_PV_total']]
LCC_summary_df = LCC_df[['LCC_CashFlow_PV_total']]
SPC_summary_df = SPC_check_df[['SPC_check']]
Risk_summary_df = Risk_df[['Risk_adjustment']]
VFM_summary_df = VFM_df[['VFM_amount','VFM_ratio']]
PIRR_summary_df = PIRR_df[['PIRR']]


# 算定結果要約も含めた、それぞれのDFに、user_id, calc_id, datetimeを追加する


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
        