import pandas as pd
import duckdb
from dataclasses import asdict, dataclass
from decimal import *
from pydantic import BaseModel
import openpyxl
from collections import deque
import make_inputs_df, make_pl_waku, make_empty_pls, make_3pls_withZero

inputs_pdt, inputs_supl_pdt = make_inputs_df.io()

conn = duckdb.connect('VFM.duckdb')
c = conn.cursor()

Risk_df = c.sql("SELECT * FROM Risk_table").df()
Risk_adjust_gaku = Risk_df['risk_adjust_gaku'].loc[0]

PSC_netpayments_df = c.sql("SELECT periods, net_payments FROM PSC_table").df()
LCC_netpayments_df = c.sql("SELECT periods, net_payments FROM LCC_table").df()

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

discount_rate = inputs_supl_pdt.discount_rate
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
c.execute('CREATE OR REPLACE TABLE VFM_table AS SELECT * from VFM_df')
c.execute('CREATE OR REPLACE TABLE PSC_pv_table AS SELECT * from PSC_netpayments_df')
c.execute('CREATE OR REPLACE TABLE LCC_pv_table AS SELECT * from LCC_netpayments_df')
c.close()
