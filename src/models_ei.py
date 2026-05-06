from pydantic import BaseModel, Field, field_validator, model_validator
from typing import Optional, Literal
from decimal import Decimal
from datetime import datetime

class VFMInputs(BaseModel):

    advisory_fee: Decimal = Field(ge=0, le=50, default=0)
    chisai_kinri: Decimal = 0.0175
    chisai_shoukan_kikan: int = 23
    chisai_sueoki_years: int = 3
    const_start_date: datetime.date
    const_start_date_year: int = 2024
    const_start_date_month: int = 11
    const_start_date_day: int = 21
    const_years: int = Field(ge=0, le=5,default=1, description="施設整備期間（年）")
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
    mgmt_type: Literal["国", "都道府県", "市区町村"] = "市区町村"
    monitoring_costs_LCC: Decimal = 6.0
    monitoring_costs_PSC: Decimal = 10.0
    pre_kyoukouka: bool = True
    proj_ctgry: Literal["サービス購入型", "コンセッション（スタジアム・アリーナタイプ）", "コンセッション（下水道タイプ）"] = "サービス購入型"
    proj_type: Literal["BTO", "DBO(SPCなし)", "BOT/BOO", "BT/DB(いずれもSPCなし)"] = "BTO"
    proj_years: int = Field(ge=10, le=30, default=10, description="事業期間（年）")
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




#    advisory_fee": str(self.edit_inputs['advisory_fee']),
#    chisai_kinri": str(chisai_kinri), 
#            "chisai_shoukan_kikan": int(self.edit_inputs['chisai_shoukan_kikan']),
#            "chisai_sueoki_years": int(self.edit_inputs['chisai_sueoki_kikan']),
#            "const_start_date_year": const_start_date_year,
#           "const_start_date_month": const_start_date_month,
#            "const_start_date_day": const_start_date_day,
#            "const_start_date": const_start_date,
#            "const_years": int(self.target_inputs["const_years"]),
#            "discount_rate": str(discount_rate),

#            "first_end_fy": str(first_end_fy),
#            "fudousanshutokuzei_hyoujun": str(self.target_inputs["hudousanshutokuzei_hyoujun"]),
#            "fudousanshutokuzei_ritsu": str(self.target_inputs["hudousanshutokuzei_ritsu"]),
#            "growth": str(self.target_inputs["growth"]),
#            "hojo_ritsu": self.target_inputs["hojo_ritsu"],
#            "houjinzei_ritsu": str(self.target_inputs["houjinzei_ritsu"]),
#            "houjinjuminzei_kintou": str(self.target_inputs["houjinjuminzei_kintou"]),
#            "houjinjuminzei_ritsu_todouhuken": str(self.target_inputs["houjinjuminzei_ritsu_todouhuken"]),
#            "houjinjuminzei_ritsu_shikuchoson": str(self.target_inputs["houjinjuminzei_ritsu_shikuchoson"]),
#            "ijikanri_unnei": str(ijikanri_unnei),
#            "ijikanri_unnei_LCC": str(ijikanri_unnei_LCC),
#            "ijikanri_unnei_org": str(ijikanri_unnei_org),
#            "ijikanri_unnei_org_LCC": str(ijikanri_unnei_org_LCC),
#            "ijikanri_unnei_1": str(ijikanri_unnei_1),
#            "ijikanri_unnei_1_LCC": str(ijikanri_unnei_1_LCC),
#            "ijikanri_unnei_1_org": str(ijikanri_unnei_1_org),
#            "ijikanri_unnei_1_org_LCC": str(ijikanri_unnei_1_org_LCC),
#            "ijikanri_unnei_2": str(ijikanri_unnei_2),
#            "ijikanri_unnei_2_LCC": str(ijikanri_unnei_2_LCC),
#            "ijikanri_unnei_2_org": str(ijikanri_unnei_2_org),
#            "ijikanri_unnei_2_org_LCC": str(ijikanri_unnei_2_org_LCC),
#            "ijikanri_unnei_3": str(ijikanri_unnei_3),
#            "ijikanri_unnei_3_LCC": str(ijikanri_unnei_3_LCC),
#            "ijikanri_unnei_3_org": str(ijikanri_unnei_3_org),
#            "ijikanri_unnei_3_org_LCC": str(ijikanri_unnei_3_org_LCC),
#            "ijikanri_unnei_years": int(ijikanri_unnei_years),
#            "kappu_kinri_spread": str(kappu_kinri_spread),
#            "Kappu_kinri": str(Kappu_kinri),
#            "kijun_kinri": str(kijun_kinri),
#            "kisai_jutou": str(self.target_inputs["kisai_jutou"]),
#            "kisai_koufu": str(self.target_inputs["kisai_koufu"]),
#            "kitai_bukka": str(kitai_bukka), 
#            "koteishisanzei_hyoujun": str(self.target_inputs["koteishisanzei_hyoujun"]),
#            "koteishisanzei_ritsu": str(self.target_inputs["koteishisanzei_ritsu"]),

#            "lg_spread": str(self.target_inputs["lg_spread"]),
#            "mgmt_type": self.target_inputs["mgmt_type"],
#            "monitoring_costs_PSC": str(self.edit_inputs['monitoring_costs_PSC']),
#            "monitoring_costs_LCC": str(self.edit_inputs['monitoring_costs_LCC']),

#            "option_02": str(self.target_inputs['option_02']),
#            "pre_kyoukouka": bool(self.target_inputs["pre_kyoukouka"]),
#            "proj_ctgry": self.target_inputs["proj_ctgry"],
#            "proj_type": self.target_inputs["proj_type"],
#            "proj_years": int(self.target_inputs["proj_years"]),
#            "rakusatsu_ritsu": str(self.target_inputs["rakusatsu_ritsu"]),
#            "reduc_shisetsu": str(self.edit_inputs["reduc_shisetsu"]),
#            "reduc_ijikanri_1": str(self.edit_inputs["reduc_ijikanri_1"]),
#            "reduc_ijikanri_2": str(self.edit_inputs["reduc_ijikanri_2"]),
#            "reduc_ijikanri_3": str(self.edit_inputs["reduc_ijikanri_3"]),
#            "riyouryoukin_shunyu": str(self.target_inputs['riyouryoukin_shunyu']),

#            "shisetsu_seibi": str(shisetsu_seibi),
#            "shisetsu_seibi_LCC": str(shisetsu_seibi_LCC),
#            "shisetsu_seibi_org": str(shisetsu_seibi_org),
#            "shisetsu_seibi_org_LCC": str(shisetsu_seibi_org_LCC),
#            "shisetsu_seibi_paymentschedule_ikkatsu": str(shisetsu_seibi_paymentschedule_ikkatsu),
#            "shisetsu_seibi_paymentschedule_kappu": str(shisetsu_seibi_paymentschedule_kappu),
#            "shoukan_kaishi_jiki": int(shoukan_kaishi_jiki),
#            "SPC_keihi": str(SPC_keihi),
#            "SPC_fee": str(SPC_fee),
#            "SPC_shihon": str(SPC_shihon),
#            "SPC_yobihi": str(SPC_yobihi),
#            "SPC_hiyou_atsukai": int(1),
#            "SPC_hiyou_total": str(SPC_hiyou_total),
#            "SPC_hiyou_nen": str(SPC_hiyou_nen),
#            "SPC_keihi_LCC": str(SPC_keihi_LCC),

#            "target_years": int(self.target_inputs['target_years']),
#            "tourokumenkyozei_hyoujun": str(self.target_inputs["tourokumenkyozei_hyoujun"]),
#            "tourokumenkyozei_ritsu": str(self.target_inputs["tourokumenkyozei_ritsu"]),
#            "yosantanka_hiritsu_shisetsu": str(self.target_inputs["yosantanka_hiritsu_shisetsu"]),
#            "yosantanka_hiritsu_ijikanri_1": str(self.target_inputs["yosantanka_hiritsu_ijikanri_1"]),
#            "yosantanka_hiritsu_ijikanri_2": str(self.target_inputs["yosantanka_hiritsu_ijikanri_2"]),
#            "yosantanka_hiritsu_ijikanri_3": str(self.target_inputs["yosantanka_hiritsu_ijikanri_3"]),
#            "zei_total": str(self.target_inputs["zei_total"]),
