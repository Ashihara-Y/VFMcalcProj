import sys
sys.dont_write_bytecode = True
#import os
import pandas as pd
#import duckdb
from ulid import ULID
import timeflake
import datetime
#import tinydb
from tinydb import TinyDB, Query
import make_inputs_df
#import decimal
import decimal
from sqlalchemy import create_engine
import sqlite3

engine = create_engine('sqlite:///VFM.db', echo=False, connect_args={'check_same_thread': False})
conn = sqlite3.connect('VFM.db')
c = conn.cursor()

user_id = ULID.from_datetime(datetime.datetime.now())
calc_id = timeflake.random()
dtime = datetime.datetime.fromtimestamp(calc_id.timestamp // 1000)

df_name_list=[]

def make_df_addID_saveDB():
    inputs_pdt = make_inputs_df.main()

    PSC_df = pd.read_sql_query("SELECT * FROM PSC_table", engine)
    PSC_pv_df = pd.read_sql_query("SELECT * FROM PSC_pv_table", engine)
    LCC_df = pd.read_sql_query("SELECT * FROM LCC_table", engine)
    LCC_pv_df = pd.read_sql_query("SELECT * FROM LCC_pv_table", engine)
    SPC_df = pd.read_sql_query("SELECT * FROM SPC_table", engine)
    SPC_check_df = pd.read_sql_query("SELECT * FROM SPC_check_table", engine)
    Risk_df = pd.read_sql_query("SELECT * FROM Risk_table", engine)
    VFM_df = pd.read_sql_query("SELECT * FROM VFM_table", engine)
    PIRR_df = pd.read_sql_query("SELECT * FROM PIRR_table", engine)

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

    kijun_kinri = decimal.Decimal(str(inputs_pdt.kijun_kinri)).quantize(decimal.Decimal('0.001'), 'ROUND_HALF_UP')
    #kitai_bukka = Decimal(str(inputs_pdt.kitai_bukka)).quantize(Decimal('0.001'), 'ROUND_HALF_UP')
    lg_spread = decimal.Decimal(str(inputs_pdt.lg_spread)).quantize(decimal.Decimal('0.001'), 'ROUND_HALF_UP')

    #discount_rate = Decimal((kijun_kinri + kitai_bukka)*100).quantize(Decimal('0.001'), 'ROUND_HALF_UP')
    kariire_kinri = decimal.Decimal((kijun_kinri + lg_spread)*100).quantize(decimal.Decimal('0.001'), 'ROUND_HALF_UP')

    final_inputs_dic = {
        'mgmt_type': inputs_pdt.mgmt_type,
        'proj_ctgry': inputs_pdt.proj_ctgry,
        'proj_type': inputs_pdt.proj_type,
        'const_years': inputs_pdt.const_years,
        'proj_years': inputs_pdt.proj_years,
        'discount_rate': round(float(inputs_pdt.discount_rate),6),
        'kariire_kinri': round(float(kariire_kinri),6),
        'Kappu_kinri': round(float(inputs_pdt.Kappu_kinri),6),
        'kappu_kinri_spread': round(float(inputs_pdt.kappu_kinri_spread),6),
        'SPC_fee': inputs_pdt.SPC_fee,
    }

    final_inputs_df = pd.DataFrame(final_inputs_dic, index=['0'])
    #print(inputs_pdt.kijun_kinri, inputs_pdt.lg_spread)
    res_summ_df = VFM_calc_summary_df.join(final_inputs_df)

    def addID(x_df):
        x_df['datetime'] = str(dtime)
        x_df['user_id'] = str(user_id)
        x_df['calc_id'] = str(calc_id)

        return x_df

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

    for i in df_list:
            addID(i)

    for x_df in df_name_list:
        x_df[0].applymap(lambda x: float(x) if isinstance(x, decimal.Decimal) else x)
        x_df[0].to_sql(x_df[1].replace('_df','') + '_res_table', engine, if_exists='append', index=False)
    


if __name__ == "__main__":
    make_df_addID_saveDB()
