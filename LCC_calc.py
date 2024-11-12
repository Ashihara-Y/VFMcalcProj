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

LCC_shuushi_income = zero_pl_LCC_income
LCC_shuushi_payments = zero_pl_LCC_payments

shoukan_kaishi_jiki = inputs_supl_pdt.shoukan_kaishi_jiki
target_years = inputs_supl_pdt.target_years
Kappu_kinri = inputs_supl_pdt.Kappu_kinri
const_years = inputs_pdt.const_years
ijikanri_years = inputs_supl_pdt.ijikanri_years
proj_years = inputs_pdt.proj_years

# LCC_shuushi_payments 1
Shisetsu_seibihi_ikkatsu = inputs_pdt.shisetsu_seibi_org_LCC * inputs_pdt.shisetsu_seibi_paymentschedule_ikkatsu
LCC_shuushi_payments.loc[inputs_pdt.const_years, 'shisetsu_seibihi_ikkatsu'] = Shisetsu_seibihi_ikkatsu
Shisetsu_seibihi_kappu = inputs_pdt.shisetsu_seibi_org_LCC * inputs_pdt.shisetsu_seibi_paymentschedule_kappu

## LCC_income
Hojokin_LCC = (inputs_pdt.hojo) * (inputs_pdt.shisetsu_seibi_org_LCC)
LCC_shuushi_income.loc[inputs_pdt.const_years, 'hojokin'] = Hojokin_LCC
Kisai_gaku_LCC =  (inputs_pdt.kisai_jutou) * (Shisetsu_seibihi_ikkatsu - Hojokin_LCC) 
LCC_shuushi_income.loc[inputs_pdt.const_years, 'kisai_gaku'] = Kisai_gaku_LCC
Kouhukin_LCC = Kisai_gaku_LCC * (inputs_pdt.kisai_koufu)
LCC_shuushi_income.loc[inputs_pdt.const_years, 'kouhukin'] = Kouhukin_LCC
LCC_shuushi_income['income_total'] = (
    LCC_shuushi_income['hojokin'] + 
    LCC_shuushi_income['kouhukin'] + 
    LCC_shuushi_income['kisai_gaku'] + 
    LCC_shuushi_income['zeishu']
)

# LCC_shuushi_payments 2
# Pyxirrの仕様として、支払いは「マイナス値」で算出される（Excelと同じはず）
Shisetsu_seibihi_kappuganpon = [
    (
        pyxirr.ppmt(
            rate=Kappu_kinri, 
            per=i, 
            nper=ijikanri_years, 
            pv=Shisetsu_seibihi_kappu + inputs_pdt.SPC_shihon + (inputs_supl_pdt.SPC_hiyou_nen * inputs_pdt.const_years),
            pmt_at_beginning=False
        )
    ) for i in range(
        1-const_years,
        target_years-const_years+1
        )
]

Shisetsu_seibihi_kappukinri = [
    (
        pyxirr.ipmt(
            rate=Kappu_kinri, 
            per=i, 
            nper=ijikanri_years, 
            pv=Shisetsu_seibihi_kappu + inputs_pdt.SPC_shihon + (inputs_supl_pdt.SPC_hiyou_nen * inputs_pdt.const_years),
            pmt_at_beginning=False
        )
    ) for i in range(
        1-const_years,
        target_years-const_years+1
        )
]

kappugoukei = pyxirr.pmt(
            rate=Kappu_kinri, 
            nper=ijikanri_years, 
            pv=Shisetsu_seibihi_kappu + inputs_pdt.SPC_shihon + (inputs_supl_pdt.SPC_hiyou_nen * inputs_pdt.const_years),
            pmt_at_beginning=False
)

# ここでマイナス値が入ったリストを、Series化を通じて、プラス値のDecimalに変換することができるかを確認
periods= [i+1 for i in range(target_years)]
Shisetsu_seibihi_kappuganpon_sr = pd.Series(Shisetsu_seibihi_kappuganpon,index=periods).fillna(0)
Shisetsu_seibihi_kappuganpon_str = Shisetsu_seibihi_kappuganpon_sr.astype('str')
Shisetsu_seibihi_kappuganpon_dc_sr = Shisetsu_seibihi_kappuganpon_str.apply(Decimal)
Shisetsu_seibihi_kappuganpon_deci = Shisetsu_seibihi_kappuganpon_dc_sr * (-1)

Shisetsu_seibihi_kappukinri_sr = pd.Series(Shisetsu_seibihi_kappukinri,index=periods).fillna(0)
Shisetsu_seibihi_kappukinri_str = Shisetsu_seibihi_kappukinri_sr.astype('str')
Shisetsu_seibihi_kappukinri_dc_sr = Shisetsu_seibihi_kappukinri_str.apply(Decimal)
Shisetsu_seibihi_kappukinri_deci = Shisetsu_seibihi_kappukinri_dc_sr * (-1)

Shisetsu_seibihi_kappugoukei = [kappugoukei*(-1) for i in range(ijikanri_years)]
Shisetsu_seibihi_kappugoukei_sr = pd.Series(index=range(target_years))
Shisetsu_seibihi_kappugoukei_sr.loc[const_years+1:proj_years] = Shisetsu_seibihi_kappugoukei
Shisetsu_seibihi_kappugoukei_deci = Shisetsu_seibihi_kappugoukei_sr.fillna(Decimal(0.0000)).apply(Decimal)

LCC_shuushi_payments.loc[const_years+1:proj_years, 'shisetsu_seibihi_kappugoukei'] = Shisetsu_seibihi_kappugoukei_deci
LCC_shuushi_payments.loc[2:, 'shisetsu_seibihi_kappuganpon'] = Shisetsu_seibihi_kappuganpon_deci
LCC_shuushi_payments.loc[2:, 'shisetsu_seibihi_kappukinri'] = Shisetsu_seibihi_kappukinri_deci
Monitoring_costs_shoki = inputs_pdt.monitoring_costs_LCC + inputs_pdt.advisory_fee
Ijikanri_unnei_LCC = inputs_pdt.ijikanri_unnei_org_LCC

SPC_keihi_LCC = inputs_supl_pdt.SPC_keihi_LCC
LCC_shuushi_payments.loc[const_years+1:proj_years, 'ijikanri_unneihi'] = Ijikanri_unnei_LCC
LCC_shuushi_payments.loc[1, 'monitoring_costs'] = Monitoring_costs_shoki
LCC_shuushi_payments.loc[2:proj_years, 'monitoring_costs'] = inputs_pdt.monitoring_costs_LCC
LCC_shuushi_payments.loc[const_years+1:proj_years, 'SPC_keihi'] = SPC_keihi_LCC

#PFI-LCC shuushi payments:3
Kisai_ganpon_shoukan_gaku_LCC = Kisai_gaku_LCC / inputs_pdt.chisai_shoukan_kikan
#print(type(Kisai_ganpon_shoukan_gaku_LCC))

# kisai_shoukan_kikan以降は、償還額をゼロにする！
LCC_shuushi_payments.loc[shoukan_kaishi_jiki:shoukan_kaishi_jiki+inputs_pdt.chisai_shoukan_kikan-1, 'kisai_shoukan_gaku'] = Kisai_ganpon_shoukan_gaku_LCC
LCC_shuushi_payments.loc[shoukan_kaishi_jiki+inputs_pdt.chisai_shoukan_kikan:target_years, 'kisai_shoukan_gaku'] = Decimal('0.000000')
LCC_shuushi_payments.fillna({'kisai_shoukan_gaku':Decimal(0.0000)}, inplace=True)
LCC_shuushi_payments['kisai_shoukansumi_gaku'] = LCC_shuushi_payments['kisai_shoukan_gaku'].cumsum()

LCC_shuushi_payments.loc[
    const_years:target_years, 
    'chisai_zansai'
] = Kisai_gaku_LCC - LCC_shuushi_payments.loc[
    const_years:target_years, 
    'kisai_shoukansumi_gaku'
]

Chisai_zansai = LCC_shuushi_payments['chisai_zansai'].to_list()
Risoku_gaku = [Chisai_zansai[i]*inputs_pdt.chisai_kinri for i in range(target_years)]
R = deque(Risoku_gaku)
R.rotate(1)
Risoku_gaku = list(R)
LCC_shuushi_payments['kisai_risoku_gaku'] = Risoku_gaku
print(Chisai_zansai)
print(Risoku_gaku)
#LCC_shuushi_payments.loc[
#    const_years+1:target_years, 
#    'kisai_risoku_gaku'
#] = LCC_shuushi_payments.loc[
#    const_years+1:target_years, 
#    'chisai_zansai'] * (inputs_pdt.chisai_kinri)

LCC_shuushi_payments['payments_total'] = (
    LCC_shuushi_payments['shisetsu_seibihi_ikkatsu'] + 
    LCC_shuushi_payments['shisetsu_seibihi_kappuganpon'] + 
    LCC_shuushi_payments['shisetsu_seibihi_kappukinri'] + 
    LCC_shuushi_payments['ijikanri_unneihi'] +
    LCC_shuushi_payments['monitoring_costs'] + 
    LCC_shuushi_payments['SPC_keihi'] + 
    LCC_shuushi_payments['kisai_shoukan_gaku'] + 
    LCC_shuushi_payments['kisai_risoku_gaku']
)

#LCC_shuushi_income, LCC_shuushi_payments
LCC = LCC_shuushi_income.join(LCC_shuushi_payments.drop('year', axis=1))
LCC["net_payments"] = LCC_shuushi_income["income_total"] - LCC_shuushi_payments["payments_total"]
LCC['hojokin'] = LCC['hojokin'].map(lambda i: Decimal(i).quantize(Decimal('0.000001'), ROUND_HALF_UP))
LCC['kouhukin'] = LCC['kouhukin'].map(lambda i: Decimal(i).quantize(Decimal('0.000001'), ROUND_HALF_UP))
LCC['kisai_gaku'] = LCC['kisai_gaku'].map(lambda i: Decimal(i).quantize(Decimal('0.000001'), ROUND_HALF_UP))
LCC['zeishu'] = LCC['zeishu'].map(lambda i: Decimal(i).quantize(Decimal('0.000001'), ROUND_HALF_UP))
LCC['income_total'] = LCC['income_total'].map(lambda i: Decimal(i).quantize(Decimal('0.000001'), ROUND_HALF_UP))
LCC['shisetsu_seibihi_ikkatsu'] = LCC['shisetsu_seibihi_ikkatsu'].map(lambda i: Decimal(i).quantize(Decimal('0.000001'), ROUND_HALF_UP))
LCC['shisetsu_seibihi_kappugoukei'] = LCC['shisetsu_seibihi_kappugoukei'].map(lambda i: Decimal(i).quantize(Decimal('0.000001'), ROUND_HALF_UP))
LCC['shisetsu_seibihi_kappuganpon'] = LCC['shisetsu_seibihi_kappuganpon'].map(lambda i: Decimal(i).quantize(Decimal('0.000001'), ROUND_HALF_UP))
LCC['shisetsu_seibihi_kappukinri'] = LCC['shisetsu_seibihi_kappukinri'].map(lambda i: Decimal(i).quantize(Decimal('0.000001'), ROUND_HALF_UP))
LCC['ijikanri_unneihi'] = LCC['ijikanri_unneihi'].map(lambda i: Decimal(i).quantize(Decimal('0.000001'), ROUND_HALF_UP))
LCC['monitoring_costs'] = LCC['monitoring_costs'].map(lambda i: Decimal(i).quantize(Decimal('0.000001'), ROUND_HALF_UP))
LCC['SPC_keihi'] = LCC['SPC_keihi'].map(lambda i: Decimal(i).quantize(Decimal('0.000001'), ROUND_HALF_UP))
LCC['chisai_zansai'] = LCC['chisai_zansai'].map(lambda i: Decimal(i).quantize(Decimal('0.000001'), ROUND_HALF_UP))
LCC['kisai_shoukan_gaku'] = LCC['kisai_shoukan_gaku'].map(lambda i: Decimal(i).quantize(Decimal('0.000001'), ROUND_HALF_UP))
LCC['kisai_shoukansumi_gaku'] = LCC['kisai_shoukansumi_gaku'].map(lambda i: Decimal(i).quantize(Decimal('0.000001'), ROUND_HALF_UP))
LCC['kisai_risoku_gaku'] = LCC['kisai_risoku_gaku'].map(lambda i: Decimal(i).quantize(Decimal('0.000001'), ROUND_HALF_UP))
LCC['payments_total'] = LCC['payments_total'].map(lambda i: Decimal(i).quantize(Decimal('0.000001'), ROUND_HALF_UP))
LCC['net_payments'] = LCC['net_payments'].map(lambda i: Decimal(i).quantize(Decimal('0.000001'), ROUND_HALF_UP))
print(LCC)

# リスク調整
#    １）　施設整備費の割賦払い分総額　＋　サービス対価に含めるSPC経費（開業前分も含める）
#    2）　LCC収支表支出に計上している「施設整備費割賦元本」の累積和（リストkかSeries）
#    3）　官民利払い費用の差：　（　1）ー2）　）　＊　（（基準金利＋lg_spread）ー地方債）　の総和
#    ４） SPC関連のリスク対応費用：　SPC収支表のSPC設立費用　＋　SPC収支表のSPC経費総和　＋　SPC予備費
#  ⇒つまり、SPC収支表を先に作っておいた方が良さそうだ！    
#    shisetsu_seibihi_servicetaika_kappuganpon = [0 for i in range(proj_years)] 
#
#    SPC_hiyou = [0 for i in range(proj_years)]
#    SPC_yobihi = 
#    Kanmin_kinrisa = 

conn = duckdb.connect('VFM.duckdb')
c = conn.cursor()

LCC_r = LCC.reset_index(drop=False)
c.execute('CREATE OR REPLACE TABLE LCC_table AS SELECT * FROM LCC_r')

with pd.ExcelWriter('VFM_test.xlsx', engine='openpyxl', mode='a') as writer:
   LCC.to_excel(writer, sheet_name='LCC_sheet20241111_008')