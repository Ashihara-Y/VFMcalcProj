import pandas as pd
import tinydb
from tinydb import TinyDB, Query
import pyxirr
import duckdb
from dataclasses import asdict, dataclass
import datetime
from decimal import *
from pydantic import BaseModel
import pandera as pa
from pandera.typing import Series, DataFrame
from collections import deque
import make_inputs_df, make_pl_waku, make_empty_pls, make_3pls_withZero

zero_pl_PSC_income, zero_pl_PSC_payments, zero_pl_LCC_income, zero_pl_LCC_payments, zero_pl_SPC_income, zero_pl_SPC_payments = make_3pls_withZero.output()
inputs_pdt, inputs_supl_pdt = make_inputs_df.io()

# PSC
PSC_shuushi_income = zero_pl_PSC_income
PSC_shuushi_payments = zero_pl_PSC_payments

shoukan_kaishi_jiki = inputs_supl_pdt.shoukan_kaishi_jiki
target_years = inputs_supl_pdt.target_years

#print(inputs_pdt.shisetsu_seibi)
#print(inputs_pdt.hojo)
## PSC_income
Hojokin = Decimal(inputs_pdt.hojo_ritsu) * Decimal(inputs_pdt.shisetsu_seibi)
PSC_shuushi_income.loc[inputs_pdt.const_years, 'hojokin'] = Hojokin
Kisai_gaku =  (inputs_pdt.kisai_jutou) * (inputs_pdt.shisetsu_seibi - Hojokin) 
PSC_shuushi_income.loc[inputs_pdt.const_years, 'kisai_gaku'] = Kisai_gaku
Kouhukin = Kisai_gaku * (inputs_pdt.kisai_koufu)
PSC_shuushi_income.loc[inputs_pdt.const_years, 'kouhukin'] = Kouhukin

PSC_shuushi_income['hojokin']  = PSC_shuushi_income['hojokin'] .convert_dtypes('Decimal')
PSC_shuushi_income['kouhukin']  = PSC_shuushi_income['kouhukin'] .convert_dtypes('Decimal')
PSC_shuushi_income['kisai_gaku']  = PSC_shuushi_income['kisai_gaku'] .convert_dtypes('Decimal')
PSC_shuushi_income['riyou_ryoukin']  = PSC_shuushi_income['riyou_ryoukin'] .convert_dtypes('Decimal')

PSC_shuushi_income['income_total'] = (
    PSC_shuushi_income['hojokin'] + 
    PSC_shuushi_income['kouhukin'] + 
    PSC_shuushi_income['kisai_gaku'] + 
    PSC_shuushi_income['riyou_ryoukin']
)

## PSC_payments
PSC_shuushi_payments.loc[1:inputs_pdt.proj_years, 'monitoring_costs'] = inputs_pdt.monitoring_costs_PSC
kisai_ganpon_shoukan_gaku = Kisai_gaku / inputs_pdt.chisai_shoukan_kikan
PSC_shuushi_payments.loc[inputs_pdt.const_years, 'shisetsu_seibihi'] = inputs_pdt.shisetsu_seibi
PSC_shuushi_payments.loc[inputs_pdt.const_years+1:inputs_pdt.proj_years, 'ijikanri_unneihi'] = inputs_pdt.ijikanri_unnei
# chisai_shoukan_kikan:23, shoukan_kaishi_jiki:(3+3+1)=7 7期目を含めて23年後は、29期目。次の30期目からは償還額はゼロにする必要がある。
PSC_shuushi_payments.loc[shoukan_kaishi_jiki:shoukan_kaishi_jiki+inputs_pdt.chisai_shoukan_kikan-1, 'kisai_shoukan_gaku'] = kisai_ganpon_shoukan_gaku
PSC_shuushi_payments.loc[shoukan_kaishi_jiki+inputs_pdt.chisai_shoukan_kikan:target_years, 'kisai_shoukan_gaku'] = Decimal('0.000000')

PSC_shuushi_payments['kisai_shoukansumi_gaku'] = PSC_shuushi_payments['kisai_shoukan_gaku'].cumsum()
PSC_shuushi_payments.loc[
    inputs_pdt.const_years:target_years,
    'chisai_zansai'
] = Kisai_gaku - PSC_shuushi_payments.loc[
    inputs_pdt.const_years:target_years, 
    'kisai_shoukansumi_gaku'
]

Chisai_zansai = PSC_shuushi_payments['chisai_zansai'].to_list()
#print(Chisai_zansai[7]*inputs_pdt.chisai_kinri)
Risoku_gaku = [Chisai_zansai[i]*inputs_pdt.chisai_kinri for i in range(target_years)]
#print(Chisai_zansai)
#print(Risoku_gaku)
R = deque(Risoku_gaku)
R.rotate(1)
Risoku_gaku = list(R)

PSC_shuushi_payments['kisai_risoku_gaku'] = Risoku_gaku

PSC_shuushi_payments['payments_total'] = (
    PSC_shuushi_payments['shisetsu_seibihi'] + 
    PSC_shuushi_payments['ijikanri_unneihi'] + 
    PSC_shuushi_payments['monitoring_costs'] + 
    PSC_shuushi_payments['kisai_shoukan_gaku'] + 
    PSC_shuushi_payments['kisai_risoku_gaku']
)

#print(PSC_shuushi_payments)

PSC = PSC_shuushi_income.join(PSC_shuushi_payments.drop('year', axis=1))
PSC["net_payments"] = PSC_shuushi_income["income_total"] - PSC_shuushi_payments["payments_total"]
PSC['hojokin'] = PSC['hojokin'].map(lambda i: Decimal(i).quantize(Decimal('0.000001'), ROUND_HALF_UP))
PSC['kouhukin'] = PSC['kouhukin'].map(lambda i: Decimal(i).quantize(Decimal('0.000001'), ROUND_HALF_UP))
PSC['kisai_gaku'] = PSC['kisai_gaku'].map(lambda i: Decimal(i).quantize(Decimal('0.000001'), ROUND_HALF_UP))
PSC['riyou_ryoukin'] = PSC['riyou_ryoukin'].map(lambda i: Decimal(i).quantize(Decimal('0.000001'), ROUND_HALF_UP))
PSC['income_total'] = PSC['income_total'].map(lambda i: Decimal(i).quantize(Decimal('0.000001'), ROUND_HALF_UP))
PSC['shisetsu_seibihi'] = PSC['shisetsu_seibihi'].map(lambda i: Decimal(i).quantize(Decimal('0.000001'), ROUND_HALF_UP))
PSC['ijikanri_unneihi'] = PSC['ijikanri_unneihi'].map(lambda i: Decimal(i).quantize(Decimal('0.000001'), ROUND_HALF_UP))
PSC['monitoring_costs'] = PSC['monitoring_costs'].map(lambda i: Decimal(i).quantize(Decimal('0.000001'), ROUND_HALF_UP))
PSC['chisai_zansai'] = PSC['chisai_zansai'].map(lambda i: Decimal(i).quantize(Decimal('0.000001'), ROUND_HALF_UP))
PSC['kisai_shoukan_gaku'] = PSC['kisai_shoukan_gaku'].map(lambda i: Decimal(i).quantize(Decimal('0.000001'), ROUND_HALF_UP))
PSC['kisai_shoukansumi_gaku'] = PSC['kisai_shoukansumi_gaku'].map(lambda i: Decimal(i).quantize(Decimal('0.000001'), ROUND_HALF_UP))
PSC['kisai_risoku_gaku'] = PSC['kisai_risoku_gaku'].map(lambda i: Decimal(i).quantize(Decimal('0.000001'), ROUND_HALF_UP))
PSC['payments_total'] = PSC['payments_total'].map(lambda i: Decimal(i).quantize(Decimal('0.000001'), ROUND_HALF_UP))
PSC['net_payments'] = PSC['net_payments'].map(lambda i: Decimal(i).quantize(Decimal('0.000001'), ROUND_HALF_UP))
#print(PSC)

conn = duckdb.connect('VFM.duckdb')
c = conn.cursor()

PSC_r = PSC.reset_index(drop=False)
c.execute('CREATE OR REPLACE TABLE PSC_table AS SELECT * FROM PSC_r')
c.close()
#with pd.ExcelWriter('VFM_test.xlsx', engine='openpyxl', mode='a') as writer:
#   PSC.to_excel(writer, sheet_name='PSC_sheet20241111_007')
