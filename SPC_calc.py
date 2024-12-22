import pandas as pd
import tinydb
from tinydb import TinyDB, Query
import pyxirr
import duckdb
from dataclasses import asdict, dataclass
import datetime
from decimal import *
from pydantic import BaseModel
import openpyxl
import make_inputs_df, make_pl_waku, make_empty_pls, make_3pls_withZero

conn = duckdb.connect('VFM.duckdb')
c = conn.cursor()

LCC_df = c.sql("SELECT * FROM LCC_table").df()
LCC_df['hojokin'] = LCC_df['hojokin'].map(lambda i: Decimal(i).quantize(Decimal('0.000001'), ROUND_HALF_UP))
LCC_df['kouhukin'] = LCC_df['kouhukin'].map(lambda i: Decimal(i).quantize(Decimal('0.000001'), ROUND_HALF_UP))
LCC_df['kisai_gaku'] = LCC_df['kisai_gaku'].map(lambda i: Decimal(i).quantize(Decimal('0.000001'), ROUND_HALF_UP))
LCC_df['zeishu'] = LCC_df['zeishu'].map(lambda i: Decimal(i).quantize(Decimal('0.000001'), ROUND_HALF_UP))
LCC_df['income_total'] = LCC_df['income_total'].map(lambda i: Decimal(i).quantize(Decimal('0.000001'), ROUND_HALF_UP))
LCC_df['shisetsu_seibihi_ikkatsu'] = LCC_df['shisetsu_seibihi_ikkatsu'].map(lambda i: Decimal(i).quantize(Decimal('0.000001'), ROUND_HALF_UP))
LCC_df['shisetsu_seibihi_kappugoukei'] = LCC_df['shisetsu_seibihi_kappugoukei'].map(lambda i: Decimal(i).quantize(Decimal('0.000001'), ROUND_HALF_UP))
LCC_df['shisetsu_seibihi_kappuganpon'] = LCC_df['shisetsu_seibihi_kappuganpon'].map(lambda i: Decimal(i).quantize(Decimal('0.000001'), ROUND_HALF_UP))
LCC_df['shisetsu_seibihi_kappukinri'] = LCC_df['shisetsu_seibihi_kappukinri'].map(lambda i: Decimal(i).quantize(Decimal('0.000001'), ROUND_HALF_UP))
LCC_df['ijikanri_unneihi'] = LCC_df['ijikanri_unneihi'].map(lambda i: Decimal(i).quantize(Decimal('0.000001'), ROUND_HALF_UP))
LCC_df['monitoring_costs'] = LCC_df['monitoring_costs'].map(lambda i: Decimal(i).quantize(Decimal('0.000001'), ROUND_HALF_UP))
LCC_df['SPC_keihi'] = LCC_df['SPC_keihi'].map(lambda i: Decimal(i).quantize(Decimal('0.000001'), ROUND_HALF_UP))
LCC_df['chisai_zansai'] = LCC_df['chisai_zansai'].map(lambda i: Decimal(i).quantize(Decimal('0.000001'), ROUND_HALF_UP))
LCC_df['kisai_shoukan_gaku'] = LCC_df['kisai_shoukan_gaku'].map(lambda i: Decimal(i).quantize(Decimal('0.000001'), ROUND_HALF_UP))
LCC_df['kisai_shoukansumi_gaku'] = LCC_df['kisai_shoukansumi_gaku'].map(lambda i: Decimal(i).quantize(Decimal('0.000001'), ROUND_HALF_UP))
LCC_df['kisai_risoku_gaku'] = LCC_df['kisai_risoku_gaku'].map(lambda i: Decimal(i).quantize(Decimal('0.000001'), ROUND_HALF_UP))
LCC_df['payments_total'] = LCC_df['payments_total'].map(lambda i: Decimal(i).quantize(Decimal('0.000001'), ROUND_HALF_UP))
LCC_df['net_payments'] = LCC_df['net_payments'].map(lambda i: Decimal(i).quantize(Decimal('0.000001'), ROUND_HALF_UP))

LCC = LCC_df.set_index('periods')

#print(LCC.info())

zero_pl_PSC_income, zero_pl_PSC_payments, zero_pl_LCC_income, zero_pl_LCC_payments, zero_pl_SPC_income, zero_pl_SPC_payments = make_3pls_withZero.output()
inputs_pdt = make_inputs_df.io()

#periods= [i+1 for i in range(inputs_supl_pdt.target_years.iloc[0])]
#LCC.set_index(periods, inplace=True)
#print(LCC)

SPC_shuushi_income = zero_pl_SPC_income
SPC_shuushi_payments = zero_pl_SPC_payments

shoukan_kaishi_jiki = inputs_pdt.shoukan_kaishi_jiki
target_years = inputs_pdt.target_years
Kappu_kinri = inputs_pdt.Kappu_kinri
const_years = inputs_pdt.const_years
ijikanri_years = inputs_pdt.ijikanri_unnei_years
proj_years = inputs_pdt.proj_years

## SPC_income
SPC_shuushi_income[[
    "shisetsu_seibihi_taika_ikkatsu", 
    "shisetsu_seibihi_taika_kappuganpon", 
    "shisetsu_seibihi_taika_kappukinri", 
    "ijikanri_unneihi_taika", 
    "SPC_hiyou_taika", 
]] = LCC[[
    "shisetsu_seibihi_ikkatsu", 
    "shisetsu_seibihi_kappuganpon", 
    "shisetsu_seibihi_kappukinri", 
    "ijikanri_unneihi", 
    "SPC_keihi", 
]]

SPC_shuushi_income['income_total'] = (
    SPC_shuushi_income['shisetsu_seibihi_taika_ikkatsu'] + 
    SPC_shuushi_income['shisetsu_seibihi_taika_kappuganpon'] + 
    SPC_shuushi_income['shisetsu_seibihi_taika_kappukinri'] + 
    SPC_shuushi_income["ijikanri_unneihi_taika"] + 
    SPC_shuushi_income["SPC_hiyou_taika"]
)

#print(SPC_shuushi_income)

#SPC_payments
Shisetsu_seibihi_kappu = inputs_pdt.shisetsu_seibi_org_LCC * inputs_pdt.shisetsu_seibi_paymentschedule_ikkatsu

Kariire_hensai_ganpon = [
    (
        pyxirr.ppmt(
            rate=inputs_pdt.kijun_kinri + inputs_pdt.lg_spread, 
            per=i, 
            nper=ijikanri_years, 
            pv=Shisetsu_seibihi_kappu + inputs_pdt.SPC_shihon + (inputs_pdt.SPC_hiyou_nen * inputs_pdt.const_years),
            pmt_at_beginning=False
        )
    ) for i in range(
        1-const_years,
        target_years-const_years+1
        )
]

Kariire_hensai_kinri = [
    (
        pyxirr.ipmt(
            rate=inputs_pdt.kijun_kinri + inputs_pdt.lg_spread, 
            per=i, 
            nper=ijikanri_years, 
            pv=Shisetsu_seibihi_kappu + inputs_pdt.SPC_shihon + (inputs_pdt.SPC_hiyou_nen * inputs_pdt.const_years),
            pmt_at_beginning=False
        )
    ) for i in range(
        1-const_years,
        target_years-const_years+1
        )
]

# ここでマイナス値が入ったリストを、Series化を通じて、プラス値のDecimalに変換することができるかを確認
periods= [i+1 for i in range(target_years)]
Kariire_hensai_ganpon_sr = pd.Series(Kariire_hensai_ganpon,index=periods).fillna(0)
Kariire_hensai_ganpon_str = Kariire_hensai_ganpon_sr.astype('str')
Kariire_hensai_ganpon_dc_sr = Kariire_hensai_ganpon_str.apply(Decimal)
Kariire_hensai_ganpon_deci = Kariire_hensai_ganpon_dc_sr * (-1)

#print(inputs_pdt.SPC_fee)
Kariire_hensai_kinri_sr = pd.Series(Kariire_hensai_kinri,index=periods).fillna(0)
Kariire_hensai_kinri_str = Kariire_hensai_kinri_sr.astype('str')
Kariire_hensai_kinri_dc_sr = Kariire_hensai_kinri_str.apply(Decimal)
Kariire_hensai_kinri_deci = Kariire_hensai_kinri_dc_sr * (-1)

Shisetsu_seibihi = inputs_pdt.shisetsu_seibi_org_LCC
SPC_shuushi_payments.loc[inputs_pdt.const_years, 'shisetsu_seibihi'] = Shisetsu_seibihi
Ijikanri_unnei_SPC = Decimal(str(inputs_pdt.ijikanri_unnei_org_LCC))
SPC_shuushi_payments.loc[inputs_pdt.const_years+1:inputs_pdt.proj_years, 'ijikanri_unneihi'] = Ijikanri_unnei_SPC

SPC_keihi = inputs_pdt.SPC_keihi
SPC_shuushi_payments.loc[1:inputs_pdt.proj_years, 'SPC_keihi'] = SPC_keihi
SPC_setsuritsuhi = inputs_pdt.SPC_shihon + inputs_pdt.SPC_yobihi
SPC_shuushi_payments.loc[1, 'SPC_setsuritsuhi'] = SPC_setsuritsuhi
Houjinzei_etc = inputs_pdt.houjinjuminzei_kintou
SPC_shuushi_payments.loc[1:inputs_pdt.proj_years, 'houjinzei_etc'] = Houjinzei_etc

#SPC_shuushi_payments.loc[const_years+1:proj_years, 'kariire_hensai_goukei'] = Kariire_hensai_goukei_deci
SPC_shuushi_payments.loc[2:, 'kariire_ganpon_hensai'] = Kariire_hensai_ganpon_deci
SPC_shuushi_payments.loc[2:, 'shiharai_risoku'] = Kariire_hensai_kinri_deci

SPC_shuushi_payments['payments_total_full'] = (
    SPC_shuushi_payments['shisetsu_seibihi'] + 
    SPC_shuushi_payments['ijikanri_unneihi'] +
    SPC_shuushi_payments['kariire_ganpon_hensai'] +   
    SPC_shuushi_payments['shiharai_risoku'] + 
    SPC_shuushi_payments['SPC_keihi'] + 
    SPC_shuushi_payments['SPC_setsuritsuhi'] + 
    SPC_shuushi_payments['houjinzei_etc']
)
SPC_shuushi_payments['payments_total'] = (
    SPC_shuushi_payments['shisetsu_seibihi'] + 
    SPC_shuushi_payments['ijikanri_unneihi'] +
    SPC_shuushi_payments['SPC_keihi'] + 
    SPC_shuushi_payments['SPC_setsuritsuhi'] + 
    SPC_shuushi_payments['houjinzei_etc']
)

#print(SPC_shuushi_payments)

SPC = SPC_shuushi_income.join(SPC_shuushi_payments.drop('year', axis=1))
SPC["net_income"] = SPC_shuushi_income["income_total"] - SPC_shuushi_payments["payments_total"]
SPC['shisetsu_seibihi_taika_ikkatsu'] = SPC['shisetsu_seibihi_taika_ikkatsu'].map(lambda i: Decimal(i).quantize(Decimal('0.000001'), ROUND_HALF_UP))
SPC['shisetsu_seibihi_taika_kappuganpon'] = SPC['shisetsu_seibihi_taika_kappuganpon'].map(lambda i: Decimal(i).quantize(Decimal('0.000001'), ROUND_HALF_UP))
SPC['shisetsu_seibihi_taika_kappukinri'] = SPC['shisetsu_seibihi_taika_kappukinri'].map(lambda i: Decimal(i).quantize(Decimal('0.000001'), ROUND_HALF_UP))
SPC['ijikanri_unneihi_taika'] = SPC['ijikanri_unneihi_taika'].map(lambda i: Decimal(i).quantize(Decimal('0.000001'), ROUND_HALF_UP))
SPC['riyou_ryoukin'] = SPC['riyou_ryoukin'].map(lambda i: Decimal(i).quantize(Decimal('0.000001'), ROUND_HALF_UP))
SPC['SPC_hiyou_taika'] = SPC['SPC_hiyou_taika'].map(lambda i: Decimal(i).quantize(Decimal('0.000001'), ROUND_HALF_UP))
SPC['income_total'] = SPC['income_total'].map(lambda i: Decimal(i).quantize(Decimal('0.000001'), ROUND_HALF_UP))
SPC['shisetsu_seibihi'] = SPC['shisetsu_seibihi'].map(lambda i: Decimal(i).quantize(Decimal('0.000001'), ROUND_HALF_UP))
SPC['ijikanri_unneihi'] = SPC['ijikanri_unneihi'].map(lambda i: Decimal(i).quantize(Decimal('0.000001'), ROUND_HALF_UP))
SPC['kariire_ganpon_hensai'] = SPC['kariire_ganpon_hensai'].map(lambda i: Decimal(i).quantize(Decimal('0.000001'), ROUND_HALF_UP))
SPC['shiharai_risoku'] = SPC['shiharai_risoku'].map(lambda i: Decimal(i).quantize(Decimal('0.000001'), ROUND_HALF_UP))
SPC['SPC_keihi'] = SPC['SPC_keihi'].map(lambda i: Decimal(i).quantize(Decimal('0.000001'), ROUND_HALF_UP))
SPC['SPC_setsuritsuhi'] = SPC['SPC_setsuritsuhi'].map(lambda i: Decimal(i).quantize(Decimal('0.000001'), ROUND_HALF_UP))
SPC['houjinzei_etc'] = SPC['houjinzei_etc'].map(lambda i: Decimal(i).quantize(Decimal('0.000001'), ROUND_HALF_UP))
SPC['payments_total'] = SPC['payments_total'].map(lambda i: Decimal(i).quantize(Decimal('0.000001'), ROUND_HALF_UP))
SPC['payments_total_full'] = SPC['payments_total_full'].map(lambda i: Decimal(i).quantize(Decimal('0.000001'), ROUND_HALF_UP))
SPC['net_income'] = SPC['net_income'].map(lambda i: Decimal(i).quantize(Decimal('0.000001'), ROUND_HALF_UP))
#print(SPC)

SPC_r = SPC.reset_index(drop=False)
c.execute('CREATE OR REPLACE TABLE SPC_table AS SELECT * FROM SPC_r')
c.close()
#with pd.ExcelWriter('VFM_test.xlsx', engine='openpyxl', mode='a') as writer:
#   SPC.to_excel(writer, sheet_name='SPC_sheet20241111_005')
