import pandera
from pandera import Column, DataFrameSchema
import pandas as pd
import decimal
from decimal import *
import datetime

inputs_schema = DataFrameSchema({
    'advisory_fee': Column(Decimal.quantize(Decimal('0.000001'), ROUND_HALF_UP), coerce=True),
    'chisai_kinri': Column(Decimal.quantize(Decimal('0.000001'), ROUND_HALF_UP), coerce=True),
    'chisai_shoukan_kikan': Column(int, coerce=True),
    'chisai_sueoki_years': Column(int, coerce=True),
    'const_years': Column(int, coerce=True),
    'const_start_date': Column(datetime.datetime, coerce=True),
    'growth': Column(Decimal.quantize(Decimal('0.000001'), ROUND_HALF_UP), coerce=True),
    'hojo': Column(Decimal.quantize(Decimal('0.000001'), ROUND_HALF_UP), coerce=True),
    'ijikanri_unnei': Column(Decimal.quantize(Decimal('0.000001'), ROUND_HALF_UP), coerce=True),
    'ijikanri_unnei_LCC': Column(Decimal.quantize(Decimal('0.000001'), ROUND_HALF_UP), coerce=True),
    'ijikanri_unnei_org': Column(Decimal.quantize(Decimal('0.000001'), ROUND_HALF_UP), coerce=True),
    'ijikanri_unnei_org_LCC': Column(Decimal.quantize(Decimal('0.000001'), ROUND_HALF_UP), coerce=True),
    'ijikanri_unnei_years': Column(int, coerce=True),
    'kappu_kinri_spread': Column(Decimal.quantize(Decimal('0.000001'), ROUND_HALF_UP), coerce=True),
    'kijun_kinri': Column(Decimal.quantize(Decimal('0.000001'), ROUND_HALF_UP), coerce=True),
    'kisai_jutou': Column(Decimal.quantize(Decimal('0.000001'), ROUND_HALF_UP), coerce=True),
    'kisai_koufu': Column(Decimal.quantize(Decimal('0.000001'), ROUND_HALF_UP), coerce=True),
    'kitai_bukka': Column(Decimal.quantize(Decimal('0.000001'), ROUND_HALF_UP), coerce=True),
    'kyoukouka_yosantanka_hiritsu': Column(Decimal.quantize(Decimal('0.000001'), ROUND_HALF_UP), coerce=True),
    'lg_spread': Column(Decimal.quantize(Decimal('0.000001'), ROUND_HALF_UP), coerce=True),
    'mgmt_type': Column(str, coerce=True),
    'monitoring_costs_LCC': Column(Decimal.quantize(Decimal('0.000001'), ROUND_HALF_UP), coerce=True),
    'monitoring_costs_PSC': Column(Decimal.quantize(Decimal('0.000001'), ROUND_HALF_UP), coerce=True),
    'pre_kyoukouka': Column(bool, coerce=True),
    'proj_ctgry': Column(str, coerce=True),
    'proj_type': Column(str, coerce=True),
    'proj_years': Column(int, coerce=True),
    'rakusatsu_ritsu': Column(Decimal.quantize(Decimal('0.000001'), ROUND_HALF_UP), coerce=True),
    'reduc_shisetsu': Column(Decimal.quantize(Decimal('0.000001'), ROUND_HALF_UP), coerce=True),
    'reduc_ijikanri': Column(Decimal.quantize(Decimal('0.000001'), ROUND_HALF_UP), coerce=True),
    'riyouryoukin_shunyu': Column(Decimal.quantize(Decimal('0.000001'), ROUND_HALF_UP), coerce=True),
    'shisetsu_seibi': Column(Decimal.quantize(Decimal('0.000001'), ROUND_HALF_UP), coerce=True),
    'shisetsu_seibi_LCC': Column(Decimal.quantize(Decimal('0.000001'), ROUND_HALF_UP), coerce=True),
    'shisetsu_seibi_org': Column(Decimal.quantize(Decimal('0.000001'), ROUND_HALF_UP), coerce=True),
    'shisetsu_seibi_org_LCC': Column(Decimal.quantize(Decimal('0.000001'), ROUND_HALF_UP), coerce=True),
    'shisetsu_seibi_paymentschedule_ikkatsu': Column(Decimal.quantize(Decimal('0.000001'), ROUND_HALF_UP), coerce=True),
    'shisetsu_seibi_paymentschedule_kappu': Column(Decimal.quantize(Decimal('0.000001'), ROUND_HALF_UP), coerce=True),
    'SPC_hiyou_atsukai': Column(int, coerce=True),
    'SPC_keihi': Column(Decimal.quantize(Decimal('0.000001'), ROUND_HALF_UP), coerce=True),
    'SPC_fee': Column(Decimal.quantize(Decimal('0.000001'), ROUND_HALF_UP), coerce=True),
    'SPC_shihon': Column(Decimal.quantize(Decimal('0.000001'), ROUND_HALF_UP), coerce=True),
    'SPC_yobihi': Column(Decimal.quantize(Decimal('0.000001'), ROUND_HALF_UP), coerce=True),
    'zei_modori': Column(Decimal.quantize(Decimal('0.000001'), ROUND_HALF_UP), coerce=True),
    'zei_total': Column(Decimal.quantize(Decimal('0.000001'), ROUND_HALF_UP), coerce=True),
    'zeimae_rieki': Column(Decimal.quantize(Decimal('0.000001'), ROUND_HALF_UP), coerce=True),
    'houjinzei_ritsu': Column(Decimal.quantize(Decimal('0.000001'), ROUND_HALF_UP), coerce=True),
    'houjinjuminzei_kintou': Column(Decimal.quantize(Decimal('0.000001'), ROUND_HALF_UP), coerce=True),
    'fudousanshutokuzei_hyoujun': Column(Decimal.quantize(Decimal('0.000001'), ROUND_HALF_UP), coerce=True),
    'fudousanshutokuzei_ritsu': Column(Decimal.quantize(Decimal('0.000001'), ROUND_HALF_UP), coerce=True),
    'koteishisanzei_hyoujun': Column(Decimal.quantize(Decimal('0.000001'), ROUND_HALF_UP), coerce=True),
    'koteishisanzei_ritsu': Column(Decimal.quantize(Decimal('0.000001'), ROUND_HALF_UP), coerce=True),
    'tourokumenkyozei_hyoujun': Column(Decimal.quantize(Decimal('0.000001'), ROUND_HALF_UP), coerce=True),
    'tourokumenkyozei_ritsu': Column(Decimal.quantize(Decimal('0.000001'), ROUND_HALF_UP), coerce=True),
    'houjinjuminzei_ritsu_todouhuken': Column(Decimal.quantize(Decimal('0.000001'), ROUND_HALF_UP), coerce=True),
    'houjinjuminzei_ritsu_shikuchoson': Column(Decimal.quantize(Decimal('0.000001'), ROUND_HALF_UP), coerce=True),
    'option_01': Column(Decimal.quantize(Decimal('0.000001'), ROUND_HALF_UP), coerce=True),
})

inputs_supl_schema = DataFrameSchema({
    'first_end_fy': Column(datetime.date),
    'discount_rate': Column(Decimal.quantize(Decimal('0.000001'), ROUND_HALF_UP), coerce=True),
    'ijikanri_years': Column(int, coerce=True),
    'shoukan_kaishi_jiki': Column(int, coerce=True),
    'target_years': Column(int, coerce=True),
    'Kappu_kinri': Column(Decimal.quantize(Decimal('0.000001'), ROUND_HALF_UP), coerce=True),
    'SPC_hiyou_total': Column(Decimal.quantize(Decimal('0.000001'), ROUND_HALF_UP), coerce=True),
    'SPC_hiyou_nen': Column(Decimal.quantize(Decimal('0.000001'), ROUND_HALF_UP), coerce=True),
    'SPC_keihi_LCC': Column(Decimal.quantize(Decimal('0.000001'), ROUND_HALF_UP), coerce=True),
})

PSC_schema = DataFrameSchema({
    'year': Column(datetime.datetime, coerce=True),
    'hojokin': Column(Decimal.quantize(Decimal('0.000001'), ROUND_HALF_UP), coerce=True),
    'kouhukin': Column(Decimal.quantize(Decimal('0.000001'), ROUND_HALF_UP), coerce=True),
    'kisai_gaku': Column(Decimal.quantize(Decimal('0.000001'), ROUND_HALF_UP), coerce=True),
    'riyou_ryoukin': Column(Decimal.quantize(Decimal('0.000001'), ROUND_HALF_UP), coerce=True),
    'income_total': Column(Decimal.quantize(Decimal('0.000001'), ROUND_HALF_UP), coerce=True),
    'shisetsu_seibihi': Column(Decimal.quantize(Decimal('0.000001'), ROUND_HALF_UP), coerce=True),
    'ijikanri_unneihi': Column(Decimal.quantize(Decimal('0.000001'), ROUND_HALF_UP), coerce=True),
    'monitoring_costs': Column(Decimal.quantize(Decimal('0.000001'), ROUND_HALF_UP), coerce=True),
    'chisai_zansai': Column(Decimal.quantize(Decimal('0.000001'), ROUND_HALF_UP), coerce=True),
    'kisai_shoukan_gaku': Column(Decimal.quantize(Decimal('0.000001'), ROUND_HALF_UP), coerce=True),
    'kisai_shoukansumi_gaku': Column(Decimal.quantize(Decimal('0.000001'), ROUND_HALF_UP), coerce=True),
    'kisai_risoku_gaku': Column(Decimal.quantize(Decimal('0.000001'), ROUND_HALF_UP), coerce=True),
    'lpayments_total': Column(Decimal.quantize(Decimal('0.000001'), ROUND_HALF_UP), coerce=True),
    'net_payments': Column(Decimal.quantize(Decimal('0.000001'), ROUND_HALF_UP), coerce=True),
})
PSC_r_schema = DataFrameSchema({
    'periods': Column(int, coerce=True), 
    'year': Column(datetime.datetime, coerce=True),
    'hojokin': Column(Decimal.quantize(Decimal('0.000001'), ROUND_HALF_UP), coerce=True),
    'kouhukin': Column(Decimal.quantize(Decimal('0.000001'), ROUND_HALF_UP), coerce=True),
    'kisai_gaku': Column(Decimal.quantize(Decimal('0.000001'), ROUND_HALF_UP), coerce=True),
    'riyou_ryoukin': Column(Decimal.quantize(Decimal('0.000001'), ROUND_HALF_UP), coerce=True),
    'income_total': Column(Decimal.quantize(Decimal('0.000001'), ROUND_HALF_UP), coerce=True),
    'shisetsu_seibihi': Column(Decimal.quantize(Decimal('0.000001'), ROUND_HALF_UP), coerce=True),
    'ijikanri_unneihi': Column(Decimal.quantize(Decimal('0.000001'), ROUND_HALF_UP), coerce=True),
    'monitoring_costs': Column(Decimal.quantize(Decimal('0.000001'), ROUND_HALF_UP), coerce=True),
    'chisai_zansai': Column(Decimal.quantize(Decimal('0.000001'), ROUND_HALF_UP), coerce=True),
    'kisai_shoukan_gaku': Column(Decimal.quantize(Decimal('0.000001'), ROUND_HALF_UP), coerce=True),
    'kisai_shoukansumi_gaku': Column(Decimal.quantize(Decimal('0.000001'), ROUND_HALF_UP), coerce=True),
    'kisai_risoku_gaku': Column(Decimal.quantize(Decimal('0.000001'), ROUND_HALF_UP), coerce=True),
    'lpayments_total': Column(Decimal.quantize(Decimal('0.000001'), ROUND_HALF_UP), coerce=True),
    'net_payments': Column(Decimal.quantize(Decimal('0.000001'), ROUND_HALF_UP), coerce=True),
})
LCC_schema = DataFrameSchema({
    'year': Column(datetime.datetime, coerce=True),
    'hojokin': Column(Decimal.quantize(Decimal('0.000001'), ROUND_HALF_UP), coerce=True),
    'kouhukin': Column(Decimal.quantize(Decimal('0.000001'), ROUND_HALF_UP), coerce=True),
    'kisai_gaku': Column(Decimal.quantize(Decimal('0.000001'), ROUND_HALF_UP), coerce=True),
    'zeishu': Column(Decimal.quantize(Decimal('0.000001'), ROUND_HALF_UP), coerce=True),
    'income_total': Column(Decimal.quantize(Decimal('0.000001'), ROUND_HALF_UP), coerce=True),
    'shisetsu_seibihi_ikkatsu': Column(Decimal.quantize(Decimal('0.000001'), ROUND_HALF_UP), coerce=True),
    'shisetsu_seibihi_kappugoukei': Column(Decimal.quantize(Decimal('0.000001'), ROUND_HALF_UP), coerce=True),
    'shisetsu_seibihi_kappuganpon': Column(Decimal.quantize(Decimal('0.000001'), ROUND_HALF_UP), coerce=True),
    'shisetsu_seibihi_kappukinri': Column(Decimal.quantize(Decimal('0.000001'), ROUND_HALF_UP), coerce=True),
    'ijikanri_unneihi': Column(Decimal.quantize(Decimal('0.000001'), ROUND_HALF_UP), coerce=True),
    'monitoring_costs': Column(Decimal.quantize(Decimal('0.000001'), ROUND_HALF_UP), coerce=True),
    'SPC_keihi': Column(Decimal.quantize(Decimal('0.000001'), ROUND_HALF_UP), coerce=True),
    'chisai_zansai': Column(Decimal.quantize(Decimal('0.000001'), ROUND_HALF_UP), coerce=True),
    'kisai_shoukan_gaku': Column(Decimal.quantize(Decimal('0.000001'), ROUND_HALF_UP), coerce=True),
    'kisai_shoukansumi_gaku': Column(Decimal.quantize(Decimal('0.000001'), ROUND_HALF_UP), coerce=True),
    'kisai_risoku_gaku': Column(Decimal.quantize(Decimal('0.000001'), ROUND_HALF_UP), coerce=True),
    'payments_total': Column(Decimal.quantize(Decimal('0.000001'), ROUND_HALF_UP), coerce=True),
    'net_payments': Column(Decimal.quantize(Decimal('0.000001'), ROUND_HALF_UP), coerce=True),
})
LCC_r_schema = DataFrameSchema({
    'periods': Column(int, coerce=True), 
    'year': Column(datetime.datetime, coerce=True),
    'hojokin': Column(Decimal.quantize(Decimal('0.000001'), ROUND_HALF_UP), coerce=True),
    'kouhukin': Column(Decimal.quantize(Decimal('0.000001'), ROUND_HALF_UP), coerce=True),
    'kisai_gaku': Column(Decimal.quantize(Decimal('0.000001'), ROUND_HALF_UP), coerce=True),
    'zeishu': Column(Decimal.quantize(Decimal('0.000001'), ROUND_HALF_UP), coerce=True),
    'income_total': Column(Decimal.quantize(Decimal('0.000001'), ROUND_HALF_UP), coerce=True),
    'shisetsu_seibihi_ikkatsu': Column(Decimal.quantize(Decimal('0.000001'), ROUND_HALF_UP), coerce=True),
    'shisetsu_seibihi_kappugoukei': Column(Decimal.quantize(Decimal('0.000001'), ROUND_HALF_UP), coerce=True),
    'shisetsu_seibihi_kappuganpon': Column(Decimal.quantize(Decimal('0.000001'), ROUND_HALF_UP), coerce=True),
    'shisetsu_seibihi_kappukinri': Column(Decimal.quantize(Decimal('0.000001'), ROUND_HALF_UP), coerce=True),
    'ijikanri_unneihi': Column(Decimal.quantize(Decimal('0.000001'), ROUND_HALF_UP), coerce=True),
    'monitoring_costs': Column(Decimal.quantize(Decimal('0.000001'), ROUND_HALF_UP), coerce=True),
    'SPC_keihi': Column(Decimal.quantize(Decimal('0.000001'), ROUND_HALF_UP), coerce=True),
    'chisai_zansai': Column(Decimal.quantize(Decimal('0.000001'), ROUND_HALF_UP), coerce=True),
    'kisai_shoukan_gaku': Column(Decimal.quantize(Decimal('0.000001'), ROUND_HALF_UP), coerce=True),
    'kisai_shoukansumi_gaku': Column(Decimal.quantize(Decimal('0.000001'), ROUND_HALF_UP), coerce=True),
    'kisai_risoku_gaku': Column(Decimal.quantize(Decimal('0.000001'), ROUND_HALF_UP), coerce=True),
    'payments_total': Column(Decimal.quantize(Decimal('0.000001'), ROUND_HALF_UP), coerce=True),
    'net_payments': Column(Decimal.quantize(Decimal('0.000001'), ROUND_HALF_UP), coerce=True),
})

SPC_schema = DataFrameSchema({
    'year': Column(datetime.datetime, coerce=True),
    'shisetsu_seibihi_taika_ikkatsu': Column(Decimal.quantize(Decimal('0.000001'), ROUND_HALF_UP), coerce=True),
    'shisetsu_seibihi_taika_kappuganpon': Column(Decimal.quantize(Decimal('0.000001'), ROUND_HALF_UP), coerce=True),
    'shisetsu_seibihi_taika_kappukinri': Column(Decimal.quantize(Decimal('0.000001'), ROUND_HALF_UP), coerce=True),
    'ijikanri_unneihi_taika': Column(Decimal.quantize(Decimal('0.000001'), ROUND_HALF_UP), coerce=True),
    'SPC_hiyou_taika': Column(Decimal.quantize(Decimal('0.000001'), ROUND_HALF_UP), coerce=True),
    'riyou_ryoukin': Column(Decimal.quantize(Decimal('0.000001'), ROUND_HALF_UP), coerce=True),
    'income_total': Column(Decimal.quantize(Decimal('0.000001'), ROUND_HALF_UP), coerce=True),
    'shisetsu_seibihi': Column(Decimal.quantize(Decimal('0.000001'), ROUND_HALF_UP), coerce=True),
    'ijikanri_unneihi': Column(Decimal.quantize(Decimal('0.000001'), ROUND_HALF_UP), coerce=True),
    'kariire_ganpon_hensai': Column(Decimal.quantize(Decimal('0.000001'), ROUND_HALF_UP), coerce=True),
    'shiharai_risoku': Column(Decimal.quantize(Decimal('0.000001'), ROUND_HALF_UP), coerce=True),
    'SPC_keihi': Column(Decimal.quantize(Decimal('0.000001'), ROUND_HALF_UP), coerce=True),
    'SPC_setsuritsuhi': Column(Decimal.quantize(Decimal('0.000001'), ROUND_HALF_UP), coerce=True),
    'houjinzei_etc': Column(Decimal.quantize(Decimal('0.000001'), ROUND_HALF_UP), coerce=True),
    'payments_total': Column(Decimal.quantize(Decimal('0.000001'), ROUND_HALF_UP), coerce=True),
    'net_income': Column(Decimal.quantize(Decimal('0.000001'), ROUND_HALF_UP), coerce=True),
})
SPC_r_schema = DataFrameSchema({
    'periods': Column(int, coerce=True), 
    'year': Column(datetime.datetime, coerce=True),
    'shisetsu_seibihi_taika_ikkatsu': Column(Decimal.quantize(Decimal('0.000001'), ROUND_HALF_UP), coerce=True),
    'shisetsu_seibihi_taika_kappuganpon': Column(Decimal.quantize(Decimal('0.000001'), ROUND_HALF_UP), coerce=True),
    'shisetsu_seibihi_taika_kappukinri': Column(Decimal.quantize(Decimal('0.000001'), ROUND_HALF_UP), coerce=True),
    'ijikanri_unneihi_taika': Column(Decimal.quantize(Decimal('0.000001'), ROUND_HALF_UP), coerce=True),
    'SPC_hiyou_taika': Column(Decimal.quantize(Decimal('0.000001'), ROUND_HALF_UP), coerce=True),
    'riyou_ryoukin': Column(Decimal.quantize(Decimal('0.000001'), ROUND_HALF_UP), coerce=True),
    'income_total': Column(Decimal.quantize(Decimal('0.000001'), ROUND_HALF_UP), coerce=True),
    'shisetsu_seibihi': Column(Decimal.quantize(Decimal('0.000001'), ROUND_HALF_UP), coerce=True),
    'ijikanri_unneihi': Column(Decimal.quantize(Decimal('0.000001'), ROUND_HALF_UP), coerce=True),
    'kariire_ganpon_hensai': Column(Decimal.quantize(Decimal('0.000001'), ROUND_HALF_UP), coerce=True),
    'shiharai_risoku': Column(Decimal.quantize(Decimal('0.000001'), ROUND_HALF_UP), coerce=True),
    'SPC_keihi': Column(Decimal.quantize(Decimal('0.000001'), ROUND_HALF_UP), coerce=True),
    'SPC_setsuritsuhi': Column(Decimal.quantize(Decimal('0.000001'), ROUND_HALF_UP), coerce=True),
    'houjinzei_etc': Column(Decimal.quantize(Decimal('0.000001'), ROUND_HALF_UP), coerce=True),
    'payments_total': Column(Decimal.quantize(Decimal('0.000001'), ROUND_HALF_UP), coerce=True),
    'net_income': Column(Decimal.quantize(Decimal('0.000001'), ROUND_HALF_UP), coerce=True),
})

def validate_inputs(df):
    pdr_df = inputs_schema.validate(df)
    return pdr_df

def validate_inputs_supl(df):
    pdr_df = inputs_supl_schema.validate(df)
    return pdr_df

def validate_PSC(df):
    pdr_df = PSC_schema.validate(df)
    return pdr_df

def validate_PSC_r(df):
    pdr_df = PSC_r_schema.validate(df)
    return pdr_df

def validate_LCC(df):
    pdr_df = LCC_schema.validate(df)
    return pdr_df

def validate_LCC_r(df):
    pdr_df = LCC_r_schema.validate(df)
    return pdr_df

def validate_SPC(df):
    pdr_df = SPC_schema.validate(df)
    return pdr_df

def validate_SPC_r(df):
    pdr_df = SPC_r_schema.validate(df)
    return pdr_df
