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

def validate(df):
    pdr_df = inputs_schema.validate(df)
    return pdr_df
