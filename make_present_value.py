import pandas as pd
import duckdb
from dataclasses import asdict, dataclass
from decimal import *
from pydantic import BaseModel
import openpyxl
from collections import deque
import make_inputs_df, make_pl_waku, make_empty_pls, make_3pls_withZero

zero_pl_PSC_income, zero_pl_PSC_payments, zero_pl_LCC_income, zero_pl_LCC_payments, zero_pl_SPC_income, zero_pl_SPC_payments = make_3pls_withZero.output()
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

PSC_netpayments_top = pd.DataFrame({'periods': [0], 'net_payments': [Risk_adjust_gaku]})
LCC_netpayments_top = pd.DataFrame({'periods': [0], 'net_payments': [Decimal('0.000000')]})

PSC_netpayments_df = pd.concat(PSC_netpayments_top, PSC_netpayments_org, axis=1)
LCC_netpayments_df = pd.concat(LCC_netpayments_top, LCC_netpayments_org, axis=1)
print(PSC_netpayments_df)
print(LCC_netpayments_df)

#Risk_adjust_gaku_df = pd.DataFrame({'risk_adjust_gaku': [risk_adjust_gaku]})
#c.execute('CREATE OR REPLACE TABLE Risk_table AS SELECT * from Risk_adjust_gaku_df')
