#import pydantic
import pandas as pd
#import tinydb
from tinydb import TinyDB, Query
#import pyxirr
import flet as ft
from dataclasses import asdict, dataclass
import datetime
from decimal import *
from pydantic import BaseModel
from pathlib import Path
#import dateutil

def main(inputs):
    #if Path("ei_db.json").exists():
    #    db = TinyDB("ei_db.json")
    #    inputs = db.all()[0]
    if Path("fi_db.json").exists():
        db = TinyDB("fi_db.json")
        inputs = db.all()[0]
    #else:
    #    inputs = {
    #        "advisory_fee": 25.0,
    #        "chisai_kinri": 0.0175,
    #        "chisai_shoukan_kikan": 23,
    #        "chisai_sueoki_years": 3,
    #        "const_start_date": datetime.date(2024, 11, 21),
    #        "const_start_date_year": 2024,
    #        "const_start_date_month": 11,
    #        "const_start_date_day": 21,
    #        "const_years": 3,
    #        "discount_rate": None,
    #        "first_end_fy": None,
    #        "fudousanshutokuzei_hyoujun": 0.0,
    #        "fudousanshutokuzei_ritsu": 0.0,
    #        "growth": 0.0,
    #        "hojo_ritsu": 0.4,
    #        "houjinjuminzei_kintou": 0.18,
    #        "houjinjuminzei_ritsu_todouhuken": 0.0,
    #         "houjinjuminzei_ritsu_shikuchoson": 0.0,
    #        "houjinzei_ritsu": 0.0,
    #        "ijikanri_unnei": 47.5,
    #        "ijikanri_unnei_LCC": 45.125,
    #        "ijikanri_unnei_org": 50.0,
    #        "ijikanri_unnei_org_LCC": 47.5,
    #        "ijikanri_unnei_1": 47.5,
    #        "ijikanri_unnei_1_LCC": 45.125,
    #        "ijikanri_unnei_1_org": 50.0,
    #        "ijikanri_unnei_1_org_LCC": 47.5,
    #        "ijikanri_unnei_2": 47.5,
    #        "ijikanri_unnei_2_LCC": 45.125,
    #        "ijikanri_unnei_2_org": 50.0,
    #        "ijikanri_unnei_2_org_LCC": 47.5,
    #        "ijikanri_unnei_3": 47.5,
    #        "ijikanri_unnei_3_LCC": 45.125,
    #        "ijikanri_unnei_3_org": 50.0,
    #        "ijikanri_unnei_3_org_LCC": 47.5,
    #        "ijikanri_unnei_years": 20,
    #        "Kappu_kinri": 0.0163,
    #        "kappu_kinri_spread": 0.01,
    #        "kijun_kinri": 0.0163,
    #        "kisai_jutou": 0.75,
    #        "kisai_koufu": 0.30, 
    #        "kitai_bukka": 0.2,
    #        "koteishisanzei_hyoujun": 0.0,
    #        "koteishisanzei_ritsu": 0.0,
    #        "lg_spread": 0.010,
    #        "mgmt_type": '市区町村',
    #        "monitoring_costs_LCC": 6.0,
    #        "monitoring_costs_PSC": 10.0,
    #        "pre_kyoukouka": True,
    #        "proj_ctgry": 'サービス購入型',
    #        "proj_type": 'BTO',
    #        "proj_years": 23,
    #        "rakusatsu_ritsu": 0.95,
    #        "reduc_shisetsu": 0.05,
    #        "reduc_ijikanri_1": 0.05,
    #        "reduc_ijikanri_2": 0.05,
    #        "reduc_ijikanri_3": 0.05,
    #        "riyouryoukin_shunyu": 0.0,
    #        "shisetsu_seibi": 2850.0,
    #        "shisetsu_seibi_LCC": 2707.5,
    #        "shisetsu_seibi_org": 3000.0,
    #        "shisetsu_seibi_org_LCC": 2850.0,
    #        "shisetsu_seibi_paymentschedule_ikkatsu": 0.5,
            #"shisetsu_seibi_paymentschedule_kappu": 0.5,
            #"shoukan_kaishi_jiki": 1,
            #"SPC_hiyou_atsukai": 1,
            #"SPC_keihi": 20.0,
            #"SPC_fee": 20.0,
            #"SPC_hiyou_total": 0.0,
            #"SPC_hiyou_nen": 0.0,
            #"SPC_keihi_LCC": 0.0,
            #"SPC_shihon": 100.0,
            #"SPC_yobihi": 456.0,
            #"target_years": 45,
            #"tourokumenkyozei_hyoujun": 0.0,
            #"tourokumenkyozei_ritsu": 0.0,
            #"yosantanka_hiritsu_shisetsu": 0.010,
            #"yosantanka_hiritsu_ijikanri_1": 0.010,
            #"yosantanka_hiritsu_ijikanri_2": 0.010,
            #"yosantanka_hiritsu_ijikanri_3": 0.010,
            #"zei_total": 0.4197
        #}


    # schema for validation
    @dataclass
    class Inputs(BaseModel):
        advisory_fee: Decimal = 25.0
        chisai_kinri: Decimal = 0.0175
        chisai_shoukan_kikan: int = 23
        chisai_sueoki_years: int = 3
        const_start_date: datetime.date
        const_start_date_year: int = 2024
        const_start_date_month: int = 11
        const_start_date_day: int = 21
        const_years: int = 3
        discount_rate: Decimal
        first_end_fy: datetime.date
        fudousanshutokuzei_hyoujun: Decimal = 0.0
        fudousanshutokuzei_ritsu: Decimal = 0.0
        growth: Decimal = 0.0
        hojo_ritsu: Decimal = 0.4
        houjinjuminzei_kintou: Decimal = 0.18
        houjinjuminzei_ritsu_todouhuken: Decimal = 0.0
        houjinjuminzei_ritsu_shikuchoson: Decimal = 0.0
        houjinzei_ritsu: Decimal = 0.0
        ijikanri_unnei: Decimal = 47.5
        ijikanri_unnei_LCC: Decimal = 45.125
        ijikanri_unnei_org: Decimal = 50.0
        ijikanri_unnei_org_LCC: Decimal = 47.5
        ijikanri_unnei_1: Decimal = 47.5
        ijikanri_unnei_1_LCC: Decimal = 45.125
        ijikanri_unnei_1_org: Decimal = 50.0
        ijikanri_unnei_1_org_LCC: Decimal = 47.5
        ijikanri_unnei_2: Decimal = 47.5
        ijikanri_unnei_2_LCC: Decimal = 45.125
        ijikanri_unnei_2_org: Decimal = 50.0
        ijikanri_unnei_2_org_LCC: Decimal = 47.5
        ijikanri_unnei_3: Decimal = 47.5
        ijikanri_unnei_3_LCC: Decimal = 45.125
        ijikanri_unnei_3_org: Decimal = 50.0
        ijikanri_unnei_3_org_LCC: Decimal = 47.5
        ijikanri_unnei_years: int = 20
        Kappu_kinri: Decimal = 0.0163
        kappu_kinri_spread: Decimal = 0.01
        kijun_kinri: Decimal = 0.0163
        kisai_jutou: Decimal = 0.75
        kisai_koufu: Decimal = 0.30
        kitai_bukka: Decimal = 0.2
        koteishisanzei_hyoujun: Decimal = 0.0
        koteishisanzei_ritsu: Decimal = 0.0
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
        reduc_ijikanri_1: Decimal = 0.05
        reduc_ijikanri_2: Decimal = 0.05
        reduc_ijikanri_3: Decimal = 0.05
        riyouryoukin_shunyu: Decimal = 0.0
        shisetsu_seibi: Decimal = 2850.0
        shisetsu_seibi_LCC: Decimal = 2707.5
        shisetsu_seibi_org: Decimal = 3000.0
        shisetsu_seibi_org_LCC: Decimal = 2850.0
        shisetsu_seibi_paymentschedule_ikkatsu: Decimal = 0.5
        shisetsu_seibi_paymentschedule_kappu: Decimal = 0.5
        shoukan_kaishi_jiki: int = 1
        SPC_hiyou_atsukai: int = 1
        SPC_keihi: Decimal = 20.0
        SPC_fee: Decimal = 20.0
        SPC_hiyou_total: Decimal
        SPC_hiyou_nen: Decimal
        SPC_keihi_LCC: Decimal
        SPC_shihon: Decimal = 100.0
        SPC_yobihi: Decimal = 456.0
        target_years: int = 45
        tourokumenkyozei_hyoujun: Decimal = 0.0
        tourokumenkyozei_ritsu: Decimal = 0.0
        yosantanka_hiritsu_shisetsu: Decimal = 0.010
        yosantanka_hiritsu_ijikanri_1: Decimal = 0.010
        yosantanka_hiritsu_ijikanri_2: Decimal = 0.010
        yosantanka_hiritsu_ijikanri_3: Decimal = 0.010
        zei_total: Decimal = 0.4197


    # validate inputs
    inputs_pdt = Inputs.model_validate(inputs)

    return inputs_pdt