import pandas as pd
import duckdb
from dataclasses import asdict, dataclass
import datetime
from decimal import *
from pydantic import BaseModel
import openpyxl
from collections import deque
import make_inputs_df, make_pl_waku, make_empty_pls, make_3pls_withZero

zero_pl_PSC_income, zero_pl_PSC_payments, zero_pl_LCC_income, zero_pl_LCC_payments, zero_pl_SPC_income, zero_pl_SPC_payments = make_3pls_withZero.output()
inputs_pdt, inputs_supl_pdt = make_inputs_df.io()

conn = duckdb.connect('VFM.duckdb')
c = conn.cursor()

LCC_kappuganpon_df = c.sql("SELECT periods, shisetsu_seibihi_kappuganpon FROM LCC_table").df()
LCC_kappuganpon_df['shisetsu_seibihi_kappuganpon'] = LCC_kappuganpon_df['shisetsu_seibihi_kappuganpon'].map(lambda i: Decimal(i).quantize(Decimal('0.000001'), ROUND_HALF_UP))
LCC_kappuganpon_df = LCC_kappuganpon_df.set_index('periods')
#print(LCC.info())
LCC_kappuganpon_cumsum = LCC_kappuganpon_df.cumsum()
LCC_kappuganpon_cumsum.loc[inputs_pdt.proj_years+1:, 'shisetsu_seibihi_kappuganpon'] = Decimal('0.000000')
#print(LCC_kappuganpon_cumsum)
#print(LCC_kappuganpon_cumsum.loc[inputs_pdt.proj_years+1:])

SPC_SPCkeihi_SPCsetsuritsuhi_df = c.sql("SELECT periods, SPC_keihi, SPC_setsuritsuhi FROM SPC_table").df()#periods= [i+1 for i in range(inputs_supl_pdt.target_years.iloc[0])]
periods = SPC_SPCkeihi_SPCsetsuritsuhi_df['periods'].to_list()
SPC_SPCkeihi_SPCsetsuritsuhi_df['SPC_keihi'] = SPC_SPCkeihi_SPCsetsuritsuhi_df['SPC_keihi'].map(lambda i: Decimal(i).quantize(Decimal('0.000001'), ROUND_HALF_UP))
SPC_SPCkeihi_SPCsetsuritsuhi_df['SPC_setsuritsuhi'] = SPC_SPCkeihi_SPCsetsuritsuhi_df['SPC_setsuritsuhi'].map(lambda i: Decimal(i).quantize(Decimal('0.000001'), ROUND_HALF_UP))
SPC_SPCkeihi_SPCsetsuritduhi_df = SPC_SPCkeihi_SPCsetsuritsuhi_df.set_index('periods')

SPC_keihi_sum = SPC_SPCkeihi_SPCsetsuritsuhi_df['SPC_keihi'].sum()
SPC_seturitsuhi_sum = SPC_SPCkeihi_SPCsetsuritsuhi_df['SPC_setsuritsuhi'].sum()

Shisetsu_seibihi_kappu = inputs_pdt.shisetsu_seibi_org_LCC * inputs_pdt.shisetsu_seibi_paymentschedule_kappu

PSC_kappu_etc = Shisetsu_seibihi_kappu + inputs_pdt.SPC_shihon + (inputs_supl_pdt.SPC_hiyou_nen * inputs_pdt.const_years)

kanmin_kinrisa = (inputs_pdt.kijun_kinri + inputs_pdt.lg_spread) - inputs_pdt.chisai_kinri

LCC_kappuganpon_cumsum_ls = LCC_kappuganpon_cumsum['shisetsu_seibihi_kappuganpon'].to_list()
R = deque(LCC_kappuganpon_cumsum_ls)
R.rotate(1)
#R[0] = Decimal('0.000000')
LCC_kappuganpon_cumsum_ls = list(R)
#print(len(LCC_kappuganpon_cumsum_ls))
kanmin_ribaraihiyou_sa = pd.DataFrame(index=periods,columns=['LCC_kappuganpon_cumsum', 'ribaraihiyou_sa']).fillna(Decimal('0.000001'))
kanmin_ribaraihiyou_sa['LCC_kappuganpon_cumsum'] = LCC_kappuganpon_cumsum_ls
print(kanmin_ribaraihiyou_sa)

Chisai_zansai = LCC_shuushi_payments['chisai_zansai'].to_list()
Risoku_gaku = [Chisai_zansai[i]*inputs_pdt.chisai_kinri for i in range(3,target_years)]
R = deque(Risoku_gaku)
R.rotate(1)
Risoku_gaku = list(R)
