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
import decimal
from decimal import Decimal

def init():
    if not os.path.exists('fi_db.json'):
        db = TinyDB("fi_db.json")
        db.insert({'mgmt_type': '','proj_ctgry': '','proj_type': '','const_years': '','proj_years': '','kijun_kinri': '','kitai_bukka': '','lg_spread': ''})
    elif os.path.exists('fi_db.json') and os.path.getsize('fi_db.json') == 0:
        db = TinyDB("fi_db.json")
        db.insert({'mgmt_type': '','proj_ctgry': '','proj_type': '','const_years': '','proj_years': '','kijun_kinri': '','kitai_bukka': '','lg_spread': ''})
    else:
        pass
init()

conn = duckdb.connect('VFM.duckdb')
c = conn.cursor()

db = TinyDB("fi_db.json")
final_inputs = db.all()[0]
# 将来的には、inputs_pdtの検証済の入力データを使うように修正する必要あり！
inputs_pdt = make_inputs_df.io()


PSC_df = c.sql('SELECT * FROM PSC_table').df()
PSC_pv_df = c.sql('SELECT * FROM PSC_pv_table').df()
LCC_df = c.sql('SELECT * FROM LCC_table').df()
LCC_pv_df = c.sql('SELECT * FROM LCC_pv_table').df()
SPC_df = c.sql('SELECT * FROM SPC_table').df()
SPC_check_df = c.sql('SELECT * FROM SPC_check_table').df()
Risk_df = c.sql('SELECT * FROM Risk_table').df()
VFM_df = c.sql('SELECT * FROM VFM_table').df()
PIRR_df = c.sql('SELECT * FROM PIRR_table').df()

# make summary
PSC_pv_summary_org = PSC_pv_df[['present_value']].sum()
LCC_pv_summary_org = LCC_pv_df[['present_value']].sum()
SPC_check_summary_org = SPC_check_df.loc[int(inputs_pdt.const_years)+1:int(inputs_pdt.proj_years), 'P_payment_check'].to_list()
VFM_summary_df = VFM_df[['VFM','VFM_percent']]
PIRR_summary_df = PIRR_df[['PIRR_percent']]

def payment_check(bool):
    if bool == 'True':
        return "返済資金は十分"
    elif bool == 'False':
        return "返済資金が不足"

SPC_check_mod = str('False' not in SPC_check_summary_org)
SPC_check_res = payment_check(SPC_check_mod)

VFM_calc_summary_df = pd.DataFrame(columns=['VFM_percent','PSC_present_value','LCC_present_value','PIRR','SPC_payment_cash'], index=['0'])

#VFM_calc_summary_df['VFM'] = VFM_summary_df['VFM'].iloc[0]
VFM_calc_summary_df['VFM_percent'] = VFM_summary_df['VFM_percent'].iloc[0]
VFM_calc_summary_df['PSC_present_value'] = PSC_pv_summary_org.iloc[0]
VFM_calc_summary_df['LCC_present_value'] = LCC_pv_summary_org.iloc[0]
VFM_calc_summary_df['PIRR'] = PIRR_summary_df['PIRR_percent'].iloc[0]
VFM_calc_summary_df['SPC_payment_cash'] = SPC_check_res

kijun_kinri = Decimal(str(inputs_pdt.kijun_kinri)).quantize(Decimal('0.001'), 'ROUND_HALF_UP')
kitai_bukka = Decimal(str(inputs_pdt.kitai_bukka)).quantize(Decimal('0.001'), 'ROUND_HALF_UP')
lg_spread = Decimal(str(inputs_pdt.lg_spread)).quantize(Decimal('0.001'), 'ROUND_HALF_UP')

#discount_rate = Decimal((kijun_kinri + kitai_bukka)*100).quantize(Decimal('0.001'), 'ROUND_HALF_UP')
kariire_kinri = Decimal((kijun_kinri + lg_spread)*100).quantize(Decimal('0.001'), 'ROUND_HALF_UP')

final_inputs_dic = {
    'mgmt_type': inputs_pdt.mgmt_type,
    'proj_ctgry': inputs_pdt.proj_ctgry,
    'proj_type': inputs_pdt.proj_type,
    'const_years': inputs_pdt.const_years,
    'proj_years': inputs_pdt.proj_years,
    'discount_rate': inputs_pdt.discount_rate,
    'kariire_kinri': inputs_pdt.kariire_kinri,
}

final_inputs_df = pd.DataFrame(final_inputs_dic, index=['0'])
#print(inputs_pdt.kijun_kinri, inputs_pdt.lg_spread)
res_summ_df = VFM_calc_summary_df.join(final_inputs_df)


user_id = ULID.from_datetime(datetime.datetime.now())
calc_id = timeflake.random()
dtime = datetime.datetime.fromtimestamp(calc_id.timestamp // 1000)

df_list = [
    PSC_df,
    PSC_pv_df,
    LCC_df,
    LCC_pv_df,
    SPC_df,
    SPC_check_df,
    Risk_df,
    VFM_df,
    PIRR_df, 
    res_summ_df
    ]
#df_name_list = ['PSC_df','PSC_pv_df','LCC_df','LCC_pv_df','SPC_df','SPC_check_df','Risk_df','VFM_df','PIRR_df','result_summary_df']
df_name_list = [
    (PSC_df,'PSC_df'),
    (PSC_pv_df,'PSC_pv_df'),
    (LCC_df,'LCC_df'),
    (LCC_pv_df,'LCC_pv_df'),
    (SPC_df,'SPC_df'),
    (SPC_check_df,'SPC_check_df'),
    (Risk_df,'Risk_df'),
    (VFM_df,'VFM_df'),
    (PIRR_df,'PIRR_df'),
    (res_summ_df,'res_summ_df')
    ]

def addID(x_df):
    x_df['datetime'] = str(dtime)
    x_df['user_id'] = str(user_id)
    x_df['calc_id'] = str(calc_id)

    return x_df

for i in df_list:
    addID(i)

#def save_ddb(x_df, name_x_df):
#    c.sql('CREATE TABLE IF NOT EXISTS ' + name_x_df + '_results_table AS SELECT * FROM ' + name_x_df)
#    new_df_name = name_x_df + '_added'
#    new_df_name = c.sql("SELECT * FROM " + name_x_df + "_results_table").df()
#    if new_df_name['datetime'].iloc[0] != x_df['datetime'].iloc[0]: 
#        c.sql('INSERT INTO ' + name_x_df + '_results_table SELECT * FROM ' + name_x_df)   
#    else:
#        pass

def save_ddb(x_df):
    c.sql('CREATE TABLE IF NOT EXISTS ' + x_df[1] + '_res_table AS SELECT * FROM ' + x_df[1])
    new_df_name = x_df[1] + '_added'
    new_df_name = c.sql("SELECT * FROM " + x_df[1] + "_res_table").df()
    if new_df_name['datetime'].iloc[0] != x_df[0]['datetime'].iloc[0]: 
        c.sql('INSERT INTO ' + x_df[1] + '_res_table SELECT * FROM ' + x_df[1])   
    else:
        pass

#for i in df_list:
#    for j in df_name_list:
#        save_ddb(i,j)    #ft.Page.go(self, route="/view_saved")
for j in df_name_list:
    save_ddb(j)
        