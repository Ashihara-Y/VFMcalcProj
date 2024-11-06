import pandera
from pandera import Column, DataFrameSchema
import pandas as pd
import decimal
from decimal import *
import datetime

inputs_schema = DataFrameSchema({
    'advisory_fee': Column(Decimal, coerce=True),
    'chisai_kinri': Column(Decimal, coerce=True),
    'chisai_shoukan_kikan': Column(int, coerce=True),
    'chisai_sueoki_years': Column(int, coerce=True),
    'const_years': Column(int, coerce=True),
    'const_start_date': Column(datetime.datetime, coerce=True),
    'growth': Column(Decimal, coerce=True),
    'hojo': Column(Decimal, coerce=True),
    'ijikanri_unnei': Column(Decimal, coerce=True),
    'ijikanri_unnei_LCC': Column(Decimal, coerce=True),
    'ijikanri_unnei_org': Column(Decimal, coerce=True),
    'ijikanri_unnei_org_LCC': Column(Decimal, coerce=True),
    'ijikanri_unnei_years': Column(int, coerce=True),
    'kappu_kinri_spread': Column(Decimal, coerce=True),
    'kijun_kinri': Column(Decimal, coerce=True),
    'kisai_jutou': Column(Decimal, coerce=True),
    'kisai_koufu': Column(Decimal, coerce=True),
    'kitai_bukka': Column(Decimal, coerce=True),
    'kyoukouka_yosantanka_hiritsu': Column(Decimal, coerce=True),
    'lg_spread': Column(Decimal, coerce=True),
    'mgmt_type': Column(str, coerce=True),
    'monitoring_costs_LCC': Column(Decimal, coerce=True),
    'monitoring_costs_PSC': Column(Decimal, coerce=True),
    'pre_kyoukouka': Column(bool, coerce=True),
    'proj_ctgry': Column(str, coerce=True),
    'proj_type': Column(str, coerce=True),
    'proj_years': Column(int, coerce=True),
    'rakusatsu_ritsu': Column(Decimal, coerce=True),
    'reduc_shisetsu': Column(Decimal, coerce=True),
    'reduc_ijikanri': Column(Decimal, coerce=True),
    'riyouryoukin_shunyu': Column(Decimal, coerce=True),
    'shisetsu_seibi': Column(Decimal, coerce=True),
    'shisetsu_seibi_LCC': Column(Decimal, coerce=True),
    'shisetsu_seibi_org': Column(Decimal, coerce=True),
    'shisetsu_seibi_org_LCC': Column(Decimal, coerce=True),
    'shisetsu_seibi_paymentschedule_ikkatsu': Column(Decimal, coerce=True),
    'shisetsu_seibi_paymentschedule_kappu': Column(Decimal, coerce=True),
    'SPC_hiyou_atsukai': Column(int, coerce=True),
    'SPC_keihi': Column(Decimal, coerce=True),
    'SPC_fee': Column(Decimal, coerce=True),
    'SPC_shihon': Column(Decimal, coerce=True),
    'SPC_yobihi': Column(Decimal, coerce=True),
    'zei_modori': Column(Decimal, coerce=True),
    'zei_total': Column(Decimal, coerce=True),
    'zeimae_rieki': Column(Decimal, coerce=True),
    'houjinzei_ritsu': Column(Decimal, coerce=True),
    'houjinjuminzei_kintou': Column(Decimal, coerce=True),
    'fudousanshutokuzei_hyoujun': Column(Decimal, coerce=True),
    'fudousanshutokuzei_ritsu': Column(Decimal, coerce=True),
    'koteishisanzei_hyoujun': Column(Decimal, coerce=True),
    'koteishisanzei_ritsu': Column(Decimal, coerce=True),
    'tourokumenkyozei_hyoujun': Column(Decimal, coerce=True),
    'tourokumenkyozei_ritsu': Column(Decimal, coerce=True),
    'houjinjuminzei_ritsu_todouhuken': Column(Decimal, coerce=True),
    'houjinjuminzei_ritsu_shikuchoson': Column(Decimal, coerce=True),
    'option_01': Column(Decimal, coerce=True),
})

inputs_supl_schema_ = DataFrameSchema({
    'first_end_fy': Column(datetime.date),
    'discount_rate': Column(Decimal, coerce=True),
    'ijikanri_years': Column(int, coerce=True),
    'shoukan_kaishi_jiki': Column(int, coerce=True),
    'target_years': Column(int, coerce=True),
    'Kappu_kinri': Column(Decimal, coerce=True),
    'SPC_hiyou_total': Column(Decimal, coerce=True),
    'SPC_hiyou_nen': Column(Decimal, coerce=True),
    'SPC_keihi_LCC': Column(Decimal, coerce=True),
})

PSC_schema = DataFrameSchema({
    'year': Column(datetime.datetime, coerce=True),
    'hojokin': Column(Decimal, coerce=True),
    'kouhukin': Column(Decimal, coerce=True),
    'kisai_gaku': Column(Decimal, coerce=True),
    'riyou_ryoukin': Column(Decimal, coerce=True),
    'income_total': Column(Decimal, coerce=True),
    'shisetsu_seibihi': Column(Decimal, coerce=True),
    'ijikanri_unneihi': Column(Decimal, coerce=True),
    'monitoring_costs': Column(Decimal, coerce=True),
    'chisai_zansai': Column(Decimal, coerce=True),
    'kisai_shoukan_gaku': Column(Decimal, coerce=True),
    'kisai_shoukansumi_gaku': Column(Decimal, coerce=True),
    'kisai_risoku_gaku': Column(Decimal, coerce=True),
    'lpayments_total': Column(Decimal, coerce=True),
    'net_payments': Column(Decimal, coerce=True),
})
LCC_schema = DataFrameSchema({
    'year': Column(datetime.datetime, coerce=True),
    'hojokin': Column(Decimal, coerce=True),
    'kouhukin': Column(Decimal, coerce=True),
    'kisai_gaku': Column(Decimal, coerce=True),
    'zeishu': Column(Decimal, coerce=True),
    'income_total': Column(Decimal, coerce=True),
    'shisetsu_seibihi_ikkatsu': Column(Decimal, coerce=True),
    'shisetsu_seibihi_kappuganpon': Column(Decimal, coerce=True),
    'shisetsu_seibihi_kappukinri': Column(Decimal, coerce=True),
    'ijikanri_unneihi': Column(Decimal, coerce=True),
    'monitoring_costs': Column(Decimal, coerce=True),
    'SPC_keihi': Column(Decimal, coerce=True),
    'chisai_zansai': Column(Decimal, coerce=True),
    'kisai_shoukan_gaku': Column(Decimal, coerce=True),
    'kisai_shoukansumi_gaku': Column(Decimal, coerce=True),
    'kisai_risoku_gaku': Column(Decimal, coerce=True),
    'payments_total': Column(Decimal, coerce=True),
    'net_payments': Column(Decimal, coerce=True),
})

SPC_schema = DataFrameSchema({
    'year': Column(datetime.datetime, coerce=True),
    'shisetsu_seibihi_taika_ikkatsu': Column(Decimal, coerce=True),
    'shisetsu_seibihi_taika_kappuganpon': Column(Decimal, coerce=True),
    'shisetsu_seibihi_taika_kappukinri': Column(Decimal, coerce=True),
    'ijikanri_unneihi_taika': Column(Decimal, coerce=True),
    'SPC_hiyou_taika': Column(Decimal, coerce=True),
    'riyou_ryoukin': Column(Decimal, coerce=True),
    'income_total': Column(Decimal, coerce=True),
    'shisetsu_seibihi': Column(Decimal, coerce=True),
    'ijikanri_unneihi': Column(Decimal, coerce=True),
    'kariire_ganpon_hensai': Column(Decimal, coerce=True),
    'shiharai_risoku': Column(Decimal, coerce=True),
    'SPC_keihi': Column(Decimal, coerce=True),
    'SPC_setsuritsuhi': Column(Decimal, coerce=True),
    'houjinzei_etc': Column(Decimal, coerce=True),
    'payments_total': Column(Decimal, coerce=True),
    'net_income': Column(Decimal, coerce=True),
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

def validate_LCC(df):
    pdr_df = LCC_schema.validate(df)
    return pdr_df

def validate_SPC(df):
    pdr_df = SPC_schema.validate(df)
    return pdr_df
