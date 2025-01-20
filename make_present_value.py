import pandas as pd
#import duckdb
from dataclasses import asdict, dataclass
from decimal import *
from pydantic import BaseModel
#import openpyxl
from collections import deque
import make_inputs_df
from sqlalchemy import create_engine, DECIMAL

engine = create_engine('sqlite:///VFM.db', echo=False)


#conn = duckdb.connect('VFM.duckdb')
#c = conn.cursor()
def make_pv():
    inputs_pdt = make_inputs_df.main()

    Risk_df = pd.read_sql_query("SELECT * FROM Risk_table", engine)
    Risk_adjust_gaku = Risk_df['risk_adjust_gaku'].loc[0]

    PSC_netpayments_df = pd.read_sql_query("SELECT periods, net_payments FROM PSC_table", engine)
    LCC_netpayments_df = pd.read_sql_query("SELECT periods, net_payments FROM LCC_table", engine)
    #PSC_netpayments_df = c.sql("SELECT periods, net_payments FROM LCC_table").df()

    PSC_netpayments_df['net_payments'] = PSC_netpayments_df['net_payments'].map(lambda i: Decimal(i).quantize(Decimal('0.000001'), ROUND_HALF_UP))
    LCC_netpayments_df['net_payments'] = LCC_netpayments_df['net_payments'].map(lambda i: Decimal(i).quantize(Decimal('0.000001'), ROUND_HALF_UP))
    PSC_netpayments_df = PSC_netpayments_df.set_index('periods')
    LCC_netpayments_df = LCC_netpayments_df.set_index('periods')

    PSC_netpayments_org = PSC_netpayments_df.reset_index(drop=False)
    LCC_netpayments_org = LCC_netpayments_df.reset_index(drop=False)

    # year列を入れるとすれば、「最初から1年前」の値を作って入れておくか、「ゼロ？」を入れておく必要あり！
    PSC_netpayments_top = pd.DataFrame({'periods': [0], 'net_payments': [Risk_adjust_gaku * -1]})
    LCC_netpayments_top = pd.DataFrame({'periods': [0], 'net_payments': [Decimal('0.000000')]})

    PSC_netpayments_df = pd.concat([PSC_netpayments_top, PSC_netpayments_org], axis=0)
    LCC_netpayments_df = pd.concat([LCC_netpayments_top, LCC_netpayments_org], axis=0)
    PSC_netpayments_df = PSC_netpayments_df.set_index('periods').map(lambda i: Decimal(i).quantize(Decimal('0.000001'), ROUND_HALF_UP))
    LCC_netpayments_df = LCC_netpayments_df.set_index('periods').map(lambda i: Decimal(i).quantize(Decimal('0.000001'), ROUND_HALF_UP))

    discount_rate = inputs_pdt.discount_rate
    discount_factor = Decimal(1 / (1 + discount_rate)).quantize(Decimal('0.000001'), ROUND_HALF_UP)
    PSC_netpayments_df['discount_factor'] = discount_factor ** PSC_netpayments_df.index
    LCC_netpayments_df['discount_factor'] = discount_factor ** LCC_netpayments_df.index

    PSC_netpayments_df['present_value'] = PSC_netpayments_df['net_payments'] * PSC_netpayments_df['discount_factor']
    LCC_netpayments_df['present_value'] = LCC_netpayments_df['net_payments'] * LCC_netpayments_df['discount_factor']
    PSC_netpayments_df['present_value'] = PSC_netpayments_df['present_value'].map(lambda i: Decimal(i).quantize(Decimal('0.000001'), ROUND_HALF_UP))
    LCC_netpayments_df['present_value'] = LCC_netpayments_df['present_value'].map(lambda i: Decimal(i).quantize(Decimal('0.000001'), ROUND_HALF_UP))
    #print(PSC_netpayments_df)
    #print(LCC_netpayments_df)

    PSC_present_value = PSC_netpayments_df['present_value'].sum()
    LCC_present_value = LCC_netpayments_df['present_value'].sum()
    VFM = PSC_present_value - LCC_present_value
    VFM_percent = (VFM / PSC_present_value) * 100
    #print(VFM, VFM_percent)

    VFM_df = pd.DataFrame({'VFM': [VFM], 'VFM_percent': [VFM_percent]})
    VFM_df.to_sql('VFM_table', engine, if_exists='replace', index=False, dtype={'VFM': DECIMAL, 'VFM_percent': DECIMAL})
    PSC_netpayments_df.to_sql('PSC_pv_table', engine, if_exists='replace', index=False, dtype={'present_value': DECIMAL, 'discount_factor': DECIMAL, 'net_payments': DECIMAL})
    LCC_netpayments_df.to_sql('LCC_pv_table', engine, if_exists='replace', index=False, dtype={'present_value': DECIMAL, 'discount_factor': DECIMAL, 'net_payments': DECIMAL})

