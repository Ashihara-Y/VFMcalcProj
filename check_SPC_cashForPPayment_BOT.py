import pandas as pd
#from tinydb import TinyDB, Query
from pyxirr import xirr
#import duckdb
from dataclasses import asdict, dataclass
from decimal import *
from pydantic import BaseModel
#import openpyxl
import make_inputs_df
from sqlalchemy import create_engine, DECIMAL, BOOLEAN

engine = create_engine('sqlite:///VFM.db', echo=False)

#conn = duckdb.connect('VFM.duckdb')
#c = conn.cursor()
def check_cash():
    inputs_pdt = make_inputs_df.main()

    SPC_df = pd.read_sql_query("SELECT periods, year, income_total, kariire_ganpon_hensai, payments_total, payments_total_full, net_income FROM SPC_table", engine)
    #SPC_df = c.sql("SELECT  periods, year, income_total, kariire_ganpon_hensai, payments_total, payments_total_full, net_income FROM SPC_table").df()
    SPC_df['income_total'] = SPC_df['income_total'].map(lambda i: Decimal(i).quantize(Decimal('0.000001'), ROUND_HALF_UP))
    SPC_df['kariire_ganpon_hensai'] = SPC_df['kariire_ganpon_hensai'].map(lambda i: Decimal(i).quantize(Decimal('0.000001'), ROUND_HALF_UP))
    SPC_df['payments_total'] = SPC_df['payments_total'].map(lambda i: Decimal(i).quantize(Decimal('0.000001'), ROUND_HALF_UP))
    SPC_df['payments_total_full'] = SPC_df['payments_total_full'].map(lambda i: Decimal(i).quantize(Decimal('0.000001'), ROUND_HALF_UP))
    SPC_df['net_income'] = SPC_df['net_income'].map(lambda i: Decimal(i).quantize(Decimal('0.000001'), ROUND_HALF_UP))
    SPC_df['net_income_full'] = SPC_df['income_total'] - SPC_df['payments_total_full']

    SPC_df = SPC_df.set_index('periods')

    SPC_df['Cash_for_P_payment'] = SPC_df['income_total'] - (SPC_df['kariire_ganpon_hensai'] + SPC_df['payments_total'])

    SPC_df['P_payment_check'] = SPC_df['Cash_for_P_payment'] >= 0
    SPC_PPayment_check_ls = SPC_df.loc[inputs_pdt.const_years+1:inputs_pdt.proj_years, 'P_payment_check'].tolist()
    #print(SPC_df)

    year = SPC_df['year'].tolist()
    value = SPC_df['net_income'].tolist()

    if sum(value) == 0:
        PIRR = 0
    else:
        PIRR = xirr(year, value)

    PIRR_percent = PIRR * 100
    #print(PIRR, PIRR_percent)

    #print(SPC_df[['income_total','payments_total_full','net_income_full']])

    net_total_income_sum = float(SPC_df['net_income_full'].sum())
    SPC_shihon = float(inputs_pdt.SPC_shihon)
    year_factor = float(1 / inputs_pdt.proj_years)
    #print(net_total_income_sum, SPC_shihon, year_factor)


    value_EIRR = SPC_df['net_income_full'].to_list()

    #if SPC_shihon == 0:
    #    EIRR = 0
    #else:
    #    EIRR = xirr(year, value_EIRR)

    #EIRR_percent = EIRR * 100
    #print(EIRR, EIRR_percent)

    PIRR_df = pd.DataFrame({'PIRR': [PIRR], 'PIRR_percent': [PIRR_percent]})
    PIRR_df.to_sql('PIRR_table', engine, if_exists='replace', index=False, dtype={
        'PIRR': DECIMAL,
        'PIRR_percent': DECIMAL})
    SPC_df.to_sql('SPC_check_table', engine, if_exists='replace', index=False, dtype={
        'income_total': DECIMAL,
        'kariire_ganpon_hensai': DECIMAL,
        'payments_total': DECIMAL,
        'payments_total_full': DECIMAL,
        'net_income': DECIMAL,
        'net_income_full': DECIMAL,
        'Cash_for_P_payment': DECIMAL,
        'P_payment_check': BOOLEAN,
    })

    #c.execute('CREATE OR REPLACE TABLE PIRR_table AS SELECT * from PIRR_df')
    #c.execute('CREATE OR REPLACE TABLE SPC_check_table AS SELECT * from SPC_df')
    #PIRR_df = c.sql("SELECT * FROM PIRR_table").df()
