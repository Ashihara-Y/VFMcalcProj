from pydantic import BaseModel, Field, field_validator, model_validator
from typing import Optional, Literal
from decimal import Decimal
from datetime import datetime
from dataclasses import dataclass


class InitialInputs(BaseModel):

# 抽出メソッド(_extract_inputs)で生成された一時変数を受け取るためのフィールドを追加
    r1: Decimal = Field(default=0.0)
    r2: Decimal = Field(default=0.0)
    kitai_bukka_j: Decimal = Field(default=0.0)
    gonensai_rimawari: Decimal = Field(default=0.0)

# UIやCAVからの値の変換が不要な変数　Raw=Computed
    chisai_shoukan_kikan: int = Field(ge=10, le=30,default=10, description="地方債償還期間（年）")
    #chisai_sueoki_kikan: int = Field(ge=0, le=5,default=0, description="地方債元本返済据置期間（年）")
    const_years: int = Field(ge=0, le=5,default=1, description="施設整備期間（年）")
    mgmt_type: Literal["国", "都道府県", "市区町村"] = "市区町村"
    #pre_kyoukouka: bool = True
    proj_ctgry: Literal["サービス購入型", "コンセッション（スタジアム・アリーナタイプ）", "コンセッション（下水道タイプ）"] = "サービス購入型"
    proj_type: Literal["BTO", "DBO(SPCなし)", "BOT/BOO", "BT/DB(いずれもSPCなし)"] = "BTO"
    proj_years: int = Field(ge=10, le=30, default=10, description="事業期間（年）")

#　日付データ STR > datetime
    #const_start_date_str: str = Field(description="施設整備開始日(YYYY-MM-DD)")

    @property
    def const_start_date(self) -> datetime.date:
        try:
            return datetime.strptime(self.const_start_date_str, "%Y-%m-%d").date()
        except ValueError:
            raise ValueError("Invalid date format. Please use YYYY-MM-DD.")

#　金額（百万円単位）データ Decimal > Decimal（単位は百万円のまま）　Raw=Computed
    #hudousanshutokuzei_hyoujun: Decimal = Field(ge=0, default=0.0, description="不動産取得税標準（百万円）")
    #houjinjuminzei_kintou: Decimal = Field(ge=0, default=0.18, description="法人税住民税均等割（百万円）")
    #ijikanri_unnei_1: Decimal = Field(ge=0, default=0.0, description="維持管理運営費（百万円）") 
    #ijikanri_unnei_1_LCC: Decimal = Field(ge=0, default=0, description="維持管理運営費LCC（百万円）")
    #ijikanri_unnei_1_org: Decimal = Field(ge=0, default=0.0, description="維持管理運営費元（百万円）")
    ijikanri_unnei_1_org_Y: Decimal = Field(ge=0, default=0.0, description="維持管理運営費元Y（百万円）")
    ijikanri_unnei_1_org_R: Decimal = Field(ge=0, default=0.0, description="維持管理運営費元R（百万円）")
    #ijikanri_unnei_1_org_LCC: Decimal = Field(ge=0, default=0.0, description="維持管理運営費元LCC（百万円）")
    #ijikanri_unnei_2: Decimal = Field(ge=0, default=0.0, description="維持管理運営費2（百万円）")
    #ijikanri_unnei_2_LCC: Decimal = Field(ge=0, default=0.0, description="維持管理運営費2LCC（百万円）")
    #ijikanri_unnei_2_org: Decimal = Field(ge=0, default=0.0, description="維持管理運営費2元（百万円）")
    ijikanri_unnei_2_org_Y: Decimal = Field(ge=0, default=0.0, description="維持管理運営費2元Y（百万円）") 
    ijikanri_unnei_2_org_R: Decimal = Field(ge=0, default=0.0, description="維持管理運営費2元R（百万円）")
    #ijikanri_unnei_2_org_LCC: Decimal = Field(ge=0, default=0.0, description="維持管理運営費2元LCC（百万円）")
    #ijikanri_unnei_3: Decimal = Field(ge=0, default=0.0, description="維持管理運営費3（百万円）")
    #ijikanri_unnei_3_LCC: Decimal = Field(ge=0, default=0.0, description="維持管理運営費3LCC（百万円）")
    #ijikanri_unnei_3_org: Decimal = Field(ge=0, default=0.0, description="維持管理運営費3元（百万円）")
    ijikanri_unnei_3_org_Y: Decimal = Field(ge=0, default=0.0, description="維持管理運営費3元Y（百万円）")
    ijikanri_unnei_3_org_R: Decimal = Field(ge=0, default=0.0, description="維持管理運営費3元R（百万円）")
    #ijikanri_unnei_3_org_LCC: Decimal = Field(ge=0, default=0.0, description="維持管理運営費3元LCC（百万円）")
    ijikanri_unnei_years: int = Field(ge=0, default=10, description="維持管理運営期間（年）")
    #koteishisanzei_hyoujun: Decimal = Field(ge=0, default=0.0, description="固定資産税標準（百万円）")
    #riyouryoukin_shunyu: Decimal = Field(ge=0, default=0.0, description="利用料金収入（百万円）")
    #shisetsu_seibi: Decimal = Field(ge=0, default=0.0, description="施設整備費（百万円）")
    #shisetsu_seibi_LCC: Decimal = Field(ge=0, default=0.0, description="施設整備費LCC（百万円）")
    #shisetsu_seibi_org: Decimal = Field(ge=0, default=0.0, description="施設整備費元（百万円）")
    shisetsu_seibi_org_Y: Decimal = Field(ge=0, default=0.0, description="施設整備費元Y（百万円）")
    shisetsu_seibi_org_R: Decimal = Field(ge=0, default=0.0, description="施設整備費元R（百万円）")
    #shisetsu_seibi_org_LCC: Decimal = Field( ge=0, default=0.0, description="施設整備費元LCC（百万円）")
    #SPC_keihi: Decimal = Field(ge=0, default=20.0, description="SPC経費（百万円）")
    #SPC_fee: Decimal = Field(ge=0, default=20.0, description="SPC手数料（百万円）")
    #SPC_shihon: Decimal = Field(ge=0, default=100.0, description="SPC資本金（百万円）")
    #SPC_yobihi: Decimal = Field(ge=0, default=0.0, description="SPC予備費（百万円）")
    #tourokumenkyozei_hyoujun: Decimal = Field(ge=0, default=0.0, description="登録免許税標準（百万円）")
    #zei_total: Decimal = Field(ge=0, default=0.18, description="納税額合計（百万円）")
    #zei_modori: Decimal = Field(ge=0, default=0.0, description="発注側の収入となる税額（百万円）")
    #zeimae_rieki: Decimal = Field(ge=0, default=0.0, description="税前利益（百万円）")

#　パーセント・率データ Raw:% > Computed: Decimal(小数点)
    #chisai_kinri_pct: Decimal = Field(ge=0.0, le=100.0,description="地方債金利（%）")
    #hudousanshutokuzei_ritsu_pct: Decimal = Field(ge=0.0, le=100.0, description="不動産取得税率（%）")
    #growth_pct: Decimal = Field(ge=0.0, le=100.0, description="利用料金収入成長率（%）")
    #hojo_ritsu_pct: Decimal = Field(ge=0.0, le=100.0, description="補助率（%）")
    #houjinjuminzei_ritsu_todouhuken_pct: Decimal = Field(ge=0.0, le=100.0, description="法人税住民税均等割（%）")
    #houjinjuminzei_ritsu_shikuchoson_pct: Decimal = Field(ge=0.0, le=100.0, description="法人税住民税均等割（%）") 
    #houjinzei_ritsu_pct: Decimal = Field(ge=0.0, le=100.0, description="法人税税率（%）")
    #kijun_kinri_pct: Decimal = Field(ge=0.0, le=100.0, description="基準金利（%）")
    #kisai_jutou_pct: Decimal = Field(ge=0.0, le=100.0, description="規制受動率（%）")
    #kisai_koufu_pct: Decimal = Field(ge=0.0, le=100.0, description="規制補助率（%）")
    #kitai_bukka_pct: Decimal = Field(ge=0.0, le=100.0, description="契約部課率（%）")
    #koteishisanzei_ritsu_pct: Decimal = Field(ge=0.0, le=100.0, description="固定資産税率（%）")
    #lg_spread_pct: Decimal = Field(ge=0.0, le=100.0, description="LGスプレッド（%）")
    rakusatsu_ritsu_pct: Decimal = Field(ge=0.0, le=100.0, description="落札率（%）")
    reduc_shisetsu_pct: Decimal = Field(ge=0.0, le=100.0, description="施設削減率（%）")
    reduc_ijikanri_1_pct: Decimal = Field(ge=0.0, le=100.0, description="維持管理運営費削減率1（%）")
    reduc_ijikanri_2_pct: Decimal = Field(ge=0.0, le=100.0, description="維持管理運営費削減率2（%）")
    reduc_ijikanri_3_pct: Decimal = Field(ge=0.0, le=100.0, description="維持管理運営費削減率3（%）")
    #tourokumenkyozei_ritsu_pct: Decimal = Field(ge=0.0, le=100.0, description="登録免許税率（%）")
    #yosantanka_hiritsu_shisetsu_pct: Decimal = Field(ge=0.0, le=100.0, description="予算単価施設（%）")
    #yosantanka_hiritsu_ijikanri_1_pct: Decimal = Field(ge=0.0, le=100.0, description="予算単価維持管理運営費1（%）")
    #yosantanka_hiritsu_ijikanri_2_pct: Decimal = Field(ge=0.0, le=100.0, description="予算単価維持管理運営費2（%）")
    #yosantanka_hiritsu_ijikanri_3_pct: Decimal = Field(ge=0.0, le=100.0, description="予算単価維持管理運営費3（%）")

    @property
    def chisai_kinri(self) -> Decimal:
        return self.chisai_kinri_pct / Decimal(100)
    @property
    def hudousanshutokuzei_ritsu(self) -> Decimal:
        return self.hudousanshutokuzei_ritsu_pct / Decimal(100)
    @property
    def growth(self) -> Decimal:
        return self.growth_pct / Decimal(100)
    @property
    def hojo_ritsu(self) -> Decimal:
        return self.hojo_ritsu_pct / Decimal(100)
    @property
    def houjinjuminzei_ritsu_todouhuken(self) -> Decimal:
        return self.houjinjuminzei_ritsu_todouhuken_pct / Decimal(100)
    @property
    def houjinjuminzei_ritsu_shikuchoson(self) -> Decimal:
        return self.houjinjuminzei_ritsu_shikuchoson_pct / Decimal(100)
    @property
    def houjinzei_ritsu(self) -> Decimal:
        return self.houjinzei_ritsu_pct / Decimal(100)
    @property
    def kijun_kinri(self) -> Decimal:
        return self.kijun_kinri_pct / Decimal(100)
    @property
    def kisai_jutou(self) -> Decimal:
        return self.kisai_jutou_pct / Decimal(100)
    @property
    def kisai_koufu(self) -> Decimal:
        return self.kisai_koufu_pct / Decimal(100)
    @property
    def kitai_bukka(self) -> Decimal:
        return self.kitai_bukka_pct / Decimal(100)
    @property
    def koteishisanzei_ritsu(self) -> Decimal:
        return self.koteishisanzei_ritsu_pct / Decimal(100)
    @property
    def lg_spread(self) -> Decimal:
        return self.lg_spread_pct / Decimal(100)
    @property
    def rakusatsu_ritsu(self) -> Decimal:
        return self.rakusatsu_ritsu_pct / Decimal(100)
    @property
    def reduc_shisetsu(self) -> Decimal:
        return self.reduc_shisetsu_pct / Decimal(100)
    @property
    def reduc_ijikanri_1(self) -> Decimal:
        return self.reduc_ijikanri_1_pct / Decimal(100)
    @property
    def reduc_ijikanri_2(self) -> Decimal:
        return self.reduc_ijikanri_2_pct / Decimal(100)
    @property
    def reduc_ijikanri_3(self) -> Decimal:
        return self.reduc_ijikanri_3_pct / Decimal(100)
    @property
    def tourokumenkyozei_ritsu(self) -> Decimal:
        return self.tourokumenkyozei_ritsu_pct / Decimal(100)
    @property
    def yosantanka_hiritsu_shisetsu(self) -> Decimal:
        return self.yosantanka_hiritsu_shisetsu_pct / Decimal(100)
    @property
    def yosantanka_hiritsu_ijikanri_1(self) -> Decimal:
        return self.yosantanka_hiritsu_ijikanri_1_pct / Decimal(100)
    @property
    def yosantanka_hiritsu_ijikanri_2(self) -> Decimal:
        return self.yosantanka_hiritsu_ijikanri_2_pct / Decimal(100)
    @property
    def yosantanka_hiritsu_ijikanri_3(self) -> Decimal:
        return self.yosantanka_hiritsu_ijikanri_3_pct / Decimal(100)

    #@model_validator(mode="after")
    #def model_validator(self) -> InitialInputs:
    #    no_SPC_proj_types = ["BT/DB(いずれもSPCなし)", "DBO(SPCなし)"]
    #    if self.proj_type in no_SPC_proj_types:
    #        self.SPC_keihi = 0.0
    #        self.SPC_fee = 0.0
    #        self.SPC_shihon = 0.0
    #        self.SPC_yobihi = 0.0
    #    return self
    
    def to_sqlite_dict(self) -> dict:
        data = self.model_dump()
        for key, value in data.items():
            if isinstance(value, Decimal):
                data[key] = round(float(value), 6)
            elif isinstance(value, bool):
                data[key] = int(value)
            elif isinstance(value, datetime):
                data[key] = value.strftime("%Y-%m-%d")
        return data