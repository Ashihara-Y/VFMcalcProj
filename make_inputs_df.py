import pydantic
import pandas as pd
import tinydb
from tinydb import TinyDB, Query
import pyxirr

from dataclasses import asdict, dataclass
import datetime
from decimal import *
from pydantic import BaseModel
import pandera as pa
from pandera.typing import Series, DataFrame
import dateutil
from pandera import Column, DataFrameSchema


db = TinyDB("test_inputs_db.json")
inputs = db.all()[0]

# schema for validation
@dataclass
class Inputs(BaseModel):
    advisory_fee: Decimal = 25.0
    chisai_kinri: Decimal = 0.0175
    chisai_shoukan_kikan: int = 23
    chisai_sueoki_years: int = 3
    const_years: int = 3
    const_start_date: datetime.datetime = '2024-11-01'
    growth: Decimal = 0.0
    hojo: Decimal = 0.4
    ijikanri_unnei: Decimal = 47.5
    ijikanri_unnei_LCC: Decimal = 45.125
    ijikanri_unnei_org: Decimal = 50.0
    ijikanri_unnei_org_LCC: Decimal = 47.5
    ijikanri_unnei_years: int = 20
    kappu_kinri_spread: Decimal = 0.01
    kijun_kinri: Decimal = 0.0163
    kisai_jutou: Decimal = 0.75
    kisai_koufu: Decimal = 0.30
    kitai_bukka: Decimal = 0.2
    kyoukouka_yosantanka_hiritsu: Decimal = 0.010
    lg_spread: Decimal = 0.010
    mgmt_type: str = '市区町村'
    monitoring_costs_LCC: Decimal = 6.0
    monitoring_costs_PSC: Decimal = 10.0
    pre_kyoukouka: bool = True
    proj_ctgry: str = 'サービス購入型'
    proj_type: str = 'BTO'
    proj_years: int = 23
    rakusatsu_ritsu: Decimal = 0.95
    reduc_shisetsu: Decimal = 0.05
    reduc_ijikanri: Decimal = 0.05
    riyouryoukin_shunyu: Decimal = 0.0
    shisetsu_seibi: Decimal = 2850.0
    shisetsu_seibi_LCC: Decimal = 2707.5
    shisetsu_seibi_org: Decimal = 3000.0
    shisetsu_seibi_org_LCC: Decimal = 2850.0
    shisetsu_seibi_paymentschedule_ikkatsu: Decimal = 0.5
    shisetsu_seibi_paymentschedule_kappu: Decimal = 0.5
    SPC_hiyou_atsukai: int = 1
    SPC_keihi: Decimal = 20.0
    SPC_fee: Decimal = 20.0
    SPC_shihon: Decimal = 100.0
    SPC_yobihi: Decimal = 456.0
    zei_modori: Decimal = 0.084
    zei_total: Decimal = 0.4197
    zeimae_rieki: Decimal = 0.05
    houjinzei_ritsu: Decimal = 0.0
    houjinjuminzei_kintou: Decimal = 0.18
    fudousanshutokuzei_hyoujun: Decimal = 0.0
    fudousanshutokuzei_ritsu: Decimal = 0.0
    koteishisanzei_hyoujun: Decimal = 0.0
    koteishisanzei_ritsu: Decimal = 0.0
    tourokumenkyozei_hyoujun: Decimal = 0.0
    tourokumenkyozei_ritsu: Decimal = 0.0
    houjinjuminzei_ritsu_todouhuken: Decimal = 0.0
    houjinjuminzei_ritsu_shikuchoson: Decimal = 0.0
    option_01: Decimal = 0.0
    option_02: Decimal = 0.0

# validate inputs
inputs_pdt = Inputs.model_validate(inputs)

# making inputs supplementary
start_year = datetime.datetime.strptime(str(inputs_pdt.const_start_date), '%Y-%m-%d %H:%M:%S').year
start_month = datetime.datetime.strptime(str(inputs_pdt.const_start_date), '%Y-%m-%d %H:%M:%S').month

if start_month < 4:
    first_end_fy = datetime.date(start_year, 3, 31)
else:
    first_end_fy = datetime.date(start_year + 1, 3, 31)
    
discount_rate = inputs_pdt.kijun_kinri + inputs_pdt.kitai_bukka
discount_rate = Decimal(str(discount_rate))

target_years = 45
proj_years = inputs_pdt.proj_years
const_years = inputs_pdt.const_years
ijikanri_years = proj_years - const_years
shoukan_kaishi_jiki = const_years + inputs_pdt.chisai_sueoki_years + 1

Kappu_kinri = inputs_pdt.kijun_kinri + inputs_pdt.lg_spread + inputs_pdt.kappu_kinri_spread

first_end_fy, first_end_fy + dateutil.relativedelta.relativedelta(year=1)

SPC_hiyou_total = inputs_pdt.SPC_keihi * inputs_pdt.ijikanri_unnei_years + inputs_pdt.SPC_shihon
SPC_hiyou_nen = SPC_hiyou_total / proj_years
SPC_keihi_LCC = inputs_pdt.SPC_keihi + Decimal(str(inputs_pdt.SPC_fee)) + inputs_pdt.houjinjuminzei_kintou

inputs_supl = {
    'first_end_fy': first_end_fy,
    'discount_rate': discount_rate,
    'ijikanri_years': ijikanri_years,
    'shoukan_kaishi_jiki': shoukan_kaishi_jiki,
    'target_years': target_years,
    'Kappu_kinri': Kappu_kinri,
    'SPC_hiyou_total': SPC_hiyou_total,
    'SPC_hiyou_nen': SPC_hiyou_nen,    
    'SPC_keihi_LCC': SPC_keihi_LCC,    
}

# to DataFrame
#inputs_supl_df = pd.DataFrame(inputs_supl, index=['val'])

# schema for validation
@dataclass
class Inputs_supl(BaseModel):
    first_end_fy: datetime.date
    discount_rate: Decimal
    ijikanri_years: int
    shoukan_kaishi_jiki: int
    target_years: int
    Kappu_kinri: Decimal
    SPC_hiyou_total: Decimal
    SPC_hiyou_nen: Decimal
    SPC_keihi_LCC: Decimal

# validate inputs supplementary
inputs_supl_pdt = Inputs_supl.model_validate(inputs_supl)

def io():
    return inputs_pdt, inputs_supl_pdt