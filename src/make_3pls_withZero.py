import os
import pandas as pd
import tinydb
from tinydb import TinyDB, Query
from pydantic import BaseModel
import make_empty_pls


cols_PSC_income = [
    'periods',
    'hojokin',
    'kouhukin',
    'kisai_gaku',
    'riyou_ryoukin'
]
cols_PSC_payments = [
    'periods',
    "shisetsu_seibihi", 
    "ijikanri_unneihi", 
    "monitoring_costs", 
    "chisai_zansai", 
    "kisai_shoukan_gaku", 
    "kisai_shoukansumi_gaku", 
    "kisai_risoku_gaku"
]
cols_LCC_income = [
    'periods', 
    "hojokin", 
    "kouhukin", 
    "kisai_gaku", 
    "zeishu"
]
cols_LCC_payments = [
    'periods', 
    "shisetsu_seibihi_ikkatsu", 
    "shisetsu_seibihi_kappugoukei", 
    "shisetsu_seibihi_kappuganpon", 
    "shisetsu_seibihi_kappukinri", 
    "ijikanri_unneihi", 
    "monitoring_costs", 
    "SPC_keihi", 
    "chisai_zansai", 
    "kisai_shoukan_gaku", 
    "kisai_shoukansumi_gaku", 
    "kisai_risoku_gaku",
]
cols_SPC_income = [
    'periods', 
    "shisetsu_seibihi_taika_ikkatsu", 
    "shisetsu_seibihi_taika_kappuganpon", 
    "shisetsu_seibihi_taika_kappukinri", 
    "ijikanri_unneihi_taika", 
    "SPC_hiyou_taika", 
    "riyou_ryoukin"
]
cols_SPC_payments = [
    'periods', 
    "shisetsu_seibihi", 
    "ijikanri_unneihi",
    "kariire_ganpon_hensai", 
    "shiharai_risoku", 
    "SPC_keihi",
    "SPC_setsuritsuhi",
    "houjinzei_etc"
]
zero_pl_PSC_income = make_empty_pls.make_empty_pl(cols_PSC_income)
zero_pl_PSC_payments = make_empty_pls.make_empty_pl(cols_PSC_payments)
zero_pl_LCC_income = make_empty_pls.make_empty_pl(cols_LCC_income)
zero_pl_LCC_payments = make_empty_pls.make_empty_pl(cols_LCC_payments)
zero_pl_SPC_income = make_empty_pls.make_empty_pl(cols_SPC_income)
zero_pl_SPC_payments = make_empty_pls.make_empty_pl(cols_SPC_payments)

def output():
    return zero_pl_PSC_income, zero_pl_PSC_payments, zero_pl_LCC_income, zero_pl_LCC_payments, zero_pl_SPC_income, zero_pl_SPC_payments
    