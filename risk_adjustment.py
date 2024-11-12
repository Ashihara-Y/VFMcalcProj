import pandas as pd
import duckdb
from dataclasses import asdict, dataclass
import datetime
from decimal import *
from pydantic import BaseModel
import openpyxl
import make_inputs_df, make_pl_waku, make_empty_pls, make_3pls_withZero

conn = duckdb.connect('VFM.duckdb')
c = conn.cursor()

LCC_kappuganpon_df = c.sql("SELECT periods, shisetsu_seibihi_kappuganpon FROM LCC_table").df()
LCC_kappuganpon_df['shisetsu_seibihi_kappuganpon'] = LCC_kappuganpon_df['shisetsu_seibihi_kappuganpon'].map(lambda i: Decimal(i).quantize(Decimal('0.000001'), ROUND_HALF_UP))
LCC_kappuganpon_df = LCC_kappuganpon_df.set_index('periods')
#print(LCC.info())
LCC_kappuganpon_cumsum = LCC_kappuganpon_df.cumsum()
print(LCC_kappuganpon_cumsum)

zero_pl_PSC_income, zero_pl_PSC_payments, zero_pl_LCC_income, zero_pl_LCC_payments, zero_pl_SPC_income, zero_pl_SPC_payments = make_3pls_withZero.output()
inputs_pdt, inputs_supl_pdt = make_inputs_df.io()

SPC_SPCkeihi_SPCsetsuritsuhi_df = c.sql("SELECT periods, SPC_keihi, SPC_setsuritsuhi FROM SPC_table").df()#periods= [i+1 for i in range(inputs_supl_pdt.target_years.iloc[0])]
SPC_SPCkeihi_SPCsetsuritsuhi_df['SPC_keihi'] = SPC_SPCkeihi_SPCsetsuritsuhi_df['SPC_keihi'].map(lambda i: Decimal(i).quantize(Decimal('0.000001'), ROUND_HALF_UP))
SPC_SPCkeihi_SPCsetsuritsuhi_df['SPC_setsuritsuhi'] = SPC_SPCkeihi_SPCsetsuritsuhi_df['SPC_setsuritsuhi'].map(lambda i: Decimal(i).quantize(Decimal('0.000001'), ROUND_HALF_UP))
SPC_SPCkeihi_SPCtoushokeihi_df = SPC_SPCkeihi_SPCsetsuritsuhi_df.set_index('periods')

