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
#import adbc_driver_sqlite.dbapi
import make_inputs_df, make_pl_waku, make_empty_pls, make_3pls_withZero, inputs_pandera_validate

conn = duckdb.connect('VFM.duckdb')
c = conn.cursor()

LCC_df = c.sql("SELECT * FROM LCC_table").df()
LCC_pdr_df = inputs_pandera_validate.validate_LCC(LCC_df)
LCC = LCC_pdr_df


zero_pl_PSC_income, zero_pl_PSC_payments, zero_pl_LCC_income, zero_pl_LCC_payments, zero_pl_SPC_income, zero_pl_SPC_payments = make_3pls_withZero.output()
inputs_pdt, inputs_supl_pdt = make_inputs_df.io()

periods= [i+1 for i in range(inputs_supl_pdt.target_years.iloc[0])]
LCC.set_index(periods, inplace=True)
print(LCC)

SPC_shuushi_income = zero_pl_SPC_income
SPC_shuushi_payments = zero_pl_SPC_payments

shoukan_kaishi_jiki = inputs_supl_pdt.shoukan_kaishi_jiki.iloc[0]
target_years = inputs_supl_pdt.target_years.iloc[0]
Kappu_kinri = inputs_supl_pdt.Kappu_kinri.iloc[0]
const_years = inputs_pdt.const_years
ijikanri_years = inputs_supl_pdt.ijikanri_years.iloc[0]
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
            pv=Shisetsu_seibihi_kappu + inputs_pdt.SPC_shihon,
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
            pv=Shisetsu_seibihi_kappu + inputs_pdt.SPC_shihon,
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

print(inputs_pdt.SPC_fee)
Kariire_hensai_kinri_sr = pd.Series(Kariire_hensai_kinri,index=periods).fillna(0)
Kariire_hensai_kinri_str = Kariire_hensai_kinri_sr.astype('str')
Kariire_hensai_kinri_dc_sr = Kariire_hensai_kinri_str.apply(Decimal)
Kariire_hensai_kinri_deci = Kariire_hensai_kinri_dc_sr * (-1)

Shisetsu_seibihi = inputs_pdt.shisetsu_seibi_org_LCC
SPC_shuushi_payments.loc[inputs_pdt.const_years, 'shisetsu_seibihi'] = Shisetsu_seibihi
Ijikanri_unnei_SPC = inputs_pdt.ijikanri_unnei_org_LCC
SPC_shuushi_payments.loc[inputs_pdt.const_years+1:inputs_pdt.proj_years, 'ijikanri_unneihi'] = Ijikanri_unnei_SPC

SPC_keihi = inputs_pdt.SPC_keihi
SPC_shuushi_payments.loc[1:inputs_pdt.proj_years, 'SPC_keihi'] = SPC_keihi
SPC_setsuritsuhi = inputs_pdt.SPC_shihon + inputs_pdt.SPC_yobihi
SPC_shuushi_payments.loc[1, 'SPC_setsuritsuhi'] = SPC_setsuritsuhi
Houjinzei_etc = inputs_pdt.houjinjuminzei_kintou
SPC_shuushi_payments.loc[inputs_pdt.const_years+1:inputs_pdt.proj_years, 'houjinzei_etc'] = Houjinzei_etc

#SPC_shuushi_payments.loc[const_years+1:proj_years, 'kariire_hensai_goukei'] = Kariire_hensai_goukei_deci
SPC_shuushi_payments.loc[2:, 'kariire_ganpon_hensai'] = Kariire_hensai_ganpon_deci
SPC_shuushi_payments.loc[2:, 'shiharai_risoku'] = Kariire_hensai_kinri_deci

SPC_shuushi_payments['payments_total'] = (
    SPC_shuushi_payments['shisetsu_seibihi'] + 
    SPC_shuushi_payments['ijikanri_unneihi'] +
    SPC_shuushi_payments['kariire_ganpon_hensai'] +   
    SPC_shuushi_payments['shiharai_risoku'] + 
    SPC_shuushi_payments['SPC_keihi'] + 
    SPC_shuushi_payments['SPC_setsuritsuhi'] + 
    SPC_shuushi_payments['houjinzei_etc']
)

#print(SPC_shuushi_payments)

SPC = SPC_shuushi_income.join(SPC_shuushi_payments.drop('year', axis=1))
SPC["net_income"] = SPC_shuushi_income["income_total"] - SPC_shuushi_payments["payments_total"]
print(SPC)

c.execute('CREATE OR REPLACE TABLE SPC_table AS SELECT * FROM SPC')

