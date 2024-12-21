import sys
sys.dont_write_bytecode = True
import os
import flet as ft
import pandas as pd
import datetime
import tinydb
from tinydb import TinyDB, Query
#import VFMcalc2 as vc
from VFMcalc2 import VFM_calc
import save_results as sr
from decimal import *
import dateutil

class Final_Inputs(ft.Column):
    def __init__(self):
        super().__init__()
        self.title = "最終入力・確認"
        self.width = 500
        self.height = 3000
        self.resizable = True

        db = TinyDB("ii_db.json")
        self.initial_inputs = db.all()[0]
        
    def build(self):

        date_format = '%Y-%m-%d'
        date_dt = datetime.datetime.strptime(self.initial_inputs["const_start_date"], date_format)
        const_start_year = date_dt.year
        const_start_month = date_dt.month
        const_start_day = date_dt.day

        self.tx0 = ft.Text(str("＜＜初期データ＞＞"))
        self.tx1 = ft.Text(str("発注者区分： " + str(self.initial_inputs["mgmt_type"])))
        self.tx2 = ft.Text(str("事業タイプ： " + str(self.initial_inputs["proj_ctgry"])))
        self.tx3 = ft.Text(str("事業方式： " + str(self.initial_inputs["proj_type"])))
        self.tx4 = ft.Text(str("事業期間： " + str(self.initial_inputs["proj_years"]) + "年"))
        self.tx5 = ft.Text(str("施設整備期間： " + str(self.initial_inputs["const_years"]) + "年"))
        self.tx6 = ft.Text(str("地方債償還据置期間： " + str(self.initial_inputs["chisai_sueoki_kikan"]) + "年"))
    
        self.dt1 = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("事業費項目")),
                ft.DataColumn(ft.Text("入力値"), numeric=True),
                ft.DataColumn(ft.Text("競争の効果反映(PSC)"), numeric=True),
                ft.DataColumn(ft.Text("効率性反映(PFI-LCC)"), numeric=True), 
            ],         
            rows=[
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("施設整備費")),
                        ft.DataCell(ft.Text(self.initial_inputs["shisetsu_seibi_org"])),
                        ft.DataCell(ft.Text(self.initial_inputs["shisetsu_seibi"])),
                        ft.DataCell(ft.Text(self.initial_inputs["shisetsu_seibi_org_LCC"])),                
                        ],
                ),
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("維持管理運営費(人件費)")),
                        ft.DataCell(ft.Text(self.initial_inputs["ijikanri_unnei_1_org"])),
                        ft.DataCell(ft.Text(self.initial_inputs["ijikanri_unnei_1"])),
                        ft.DataCell(ft.Text(self.initial_inputs["ijikanri_unnei_1_org_LCC"])),                
                        ],
                ),
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("維持管理運営費(修繕費)")),
                        ft.DataCell(ft.Text(self.initial_inputs["ijikanri_unnei_2_org"])),
                        ft.DataCell(ft.Text(self.initial_inputs["ijikanri_unnei_2"])),
                        ft.DataCell(ft.Text(self.initial_inputs["ijikanri_unnei_2_org_LCC"])),                
                        ],
                ),
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("維持管理運営費(動力費)")),
                        ft.DataCell(ft.Text(self.initial_inputs["ijikanri_unnei_3_org"])),
                        ft.DataCell(ft.Text(self.initial_inputs["ijikanri_unnei_3"])),
                        ft.DataCell(ft.Text(self.initial_inputs["ijikanri_unnei_3_org_LCC"])),                
                        ],
                ),
            ],
        )
        self.dt2 = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("税目")),
                ft.DataColumn(ft.Text("標準／均等割"), numeric=True),
                ft.DataColumn(ft.Text("税率"), numeric=True),
            ],         
            rows=[
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("法人税")),
                        ft.DataCell(ft.Text("-")),
                        ft.DataCell(ft.Text(self.initial_inputs["houjinzei_ritsu"])),
                        ],
                ),
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("法人住民税(都道府県)")),
                        ft.DataCell(ft.Text(self.initial_inputs["houjinjuminzei_kintou"])),
                        ft.DataCell(ft.Text(self.initial_inputs["houjinjuminzei_ritsu_todouhuken"])),
                        ],
                ),
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("法人住民税(市区町村)")),
                        ft.DataCell(ft.Text(self.initial_inputs["houjinjuminzei_kintou"])),
                        ft.DataCell(ft.Text(self.initial_inputs["houjinjuminzei_ritsu_shikuchoson"])),
                        ],
                ),
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("不動産取得税")),
                        ft.DataCell(ft.Text(self.initial_inputs["hudousanshutokuzei_hyoujun"])),
                        ft.DataCell(ft.Text(self.initial_inputs["hudousanshutokuzei_ritsu"])),
                        ],
                ),
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("固定資産税")),
                        ft.DataCell(ft.Text(self.initial_inputs["koteishisanzei_hyoujun"])),
                        ft.DataCell(ft.Text(self.initial_inputs["koteishisanzei_ritsu"])),
                        ],
                ),
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("登録免許税")),
                        ft.DataCell(ft.Text(self.initial_inputs["tourokumenkyozei_hyoujun"])),
                        ft.DataCell(ft.Text(self.initial_inputs["tourokumenkyozei_ritsu"])),
                        ],
                ),
            ],
        )

        self.tx7 = ft.Text("地方債償還期間")
        self.sl1 = ft.Slider(
            value=int(self.initial_inputs["chisai_shoukan_kikan"]),
            min=0,
            max=30,
            divisions=30,
            label="{value}年",
#            badge=self.sl1.value,
        )
        self.tx8 = ft.Text("施設整備費支払 一括払の比率")
        self.sl2 = ft.Slider(
            value=50,
            min=0.0,
            max=100,
            divisions=100,
            label="{value}%",
#            badge=self.sl2.value,
        )
        self.tx9 = ft.Text("モニタリング等費用(PSC)")
        self.sl3 = ft.Slider(
            value=10,
            min=0,
            max=100,
            divisions=100,
            label="{value}百万円",
#            badge=self.sl3.value,
        )
        self.tx10 = ft.Text("モニタリング等費用(PFI-LCC)")
        self.sl4 = ft.Slider(
            value=6,
            min=0,
            max=100,
            divisions=100,
            label="{value}百万円",
#            badge=self.sl4.value,
        )
        self.tx11 = ft.Text("起債充当率")
        self.sl5 = ft.Slider(
            value=Decimal(self.initial_inputs["kisai_jutou"]),
            min=0.0,
            max=100.0,
            divisions=100,
            label="{value}%",
#            badge=self.sl5.value,
        )
        self.tx12 = ft.Text("起債への交付金カバー率")
        self.sl6 = ft.Slider(
            value=Decimal(self.initial_inputs["kisai_koufu"]),
            min=0.0,
            max=50.0,
            divisions=50,
            label="{value}%",
#            badge=self.sl6.value,
        )
        self.tx13 = ft.Text("補助率")
        self.sl7 = ft.Slider(
            value=Decimal(self.initial_inputs["hojo_ritsu"]),
            min=0.0,
            max=70.0,
            divisions=70,
            label="{value}%",
#            badge=self.sl7.value,
        )
        self.tx14 = ft.Text("SPC経費年額")
        self.sl8 = ft.Slider(
            value=Decimal(self.initial_inputs["SPC_keihi"]),
            min=0,
            max=50,
            divisions=50,
            label="{value}百万円",
#            badge=self.sl8.value,
        )
        self.tx15 = ft.Text("SPCへの手数料")
        self.sl9 = ft.Slider(
            value=Decimal(self.initial_inputs["SPC_fee"]),
            min=0,
            max=50,
            divisions=50,
            label="{value}百万円",
#            badge=self.sl9.value,
        )
        self.tx16 = ft.Text("SPC資本金")
        self.sl10 = ft.Slider(
            value=Decimal(self.initial_inputs["SPC_shihon"]),
            min=0,
            max=100,
            divisions=100,
            label="{value}百万円",
#            badge=self.sl10.value,
        )
        self.tx17 = ft.Text("SPC予備費")
        self.sl11 = ft.Slider(
            value=Decimal(self.initial_inputs["SPC_yobihi"]),
            min=0,
            max=1000,
            divisions=1000,
            label="{value}百万円",
#            badge=self.sl11.value,
        )
        self.tx18 = ft.Text("SPC経費の扱い（デフォルト：割賦に含める）")
        self.sl12 = ft.Slider(
            value=self.initial_inputs["SPC_hiyou_atsukai"],
            min=0,
            max=1,
            divisions=1,
            label="{value}",
#            badge=self.sl12.value,
        )
        self.tx19 = ft.Text("アドバイザリー等経費")
        self.sl13 = ft.Slider(
            value=25,
            min=0,
            max=50,
            divisions=50,
            label="{value}百万円",
#            badge=self.sl13.value,
        )
        self.tx20 = ft.Text("利用料金収入")
        self.sl14 = ft.Slider(
            value=self.initial_inputs["riyou_ryoukin"],
            min=0,
            max=100,
            divisions=100,
            label="{value}百万円",
#            badge=self.sl14.value,
        )
        self.tx21 = ft.Text("割賦金利へのスプレッド")
        self.sl15 = ft.Slider(
            value=1.00,
            min=0.00,
            max=2.00,
            divisions=200,
            label="{value}％",
#            badge=self.sl15.value,
        )
        self.tx22 = ft.Text("施設整備開始年")
        self.sl16 = ft.Slider(
            value=const_start_year,
            min=const_start_year,
            max=(const_start_year + 10),
            divisions=10,
            label="{value}年",
#            badge=self.sl16.value,
        )
        self.tx23 = ft.Text("施設整備開始月")
        self.sl17 = ft.Slider(
            value=const_start_month,
            min=1,
            max=12,
            divisions=12,
            label="{value}月",
#            badge=self.sl17.value,
        )
        self.tx24 = ft.Text("施設整備開始日")
        self.sl18 = ft.Slider(
            value=const_start_day,
            min=1,
            max=31,
            divisions=31,
            label="{value}日",
#            badge=self.sl18.value,
        )
        self.tx25 = ft.Text("予備入力（１）")
        self.sl19 = ft.Slider(
            value=0,
            min=0,
            max=0,
            divisions=31,
            label="{value}",
        )
        self.tx26 = ft.Text("予備入力（２）")
        self.sl20 = ft.Slider(
            value=0,
            min=0,
            max=0,
            divisions=31,
            label="{value}",
        )
        self.b = ft.ElevatedButton(text="入力確認・計算", on_click=self.button_clicked)
        return ft.Column(
            [
                self.tx0,self.tx1,self.tx2,
                self.tx3,self.tx4,self.tx5,self.tx6,
                self.dt1,self.dt2,
                self.tx7,self.sl1,self.tx8,self.sl2,
                self.tx9,self.sl3,self.tx10,self.sl4,
                self.tx11,self.sl5,self.tx12,self.sl6,
                self.tx13,self.sl7,self.tx14,self.sl8,
                self.tx15,self.sl9,self.tx16,self.sl10,
                self.tx17,self.sl11,self.tx18,self.sl12,
                self.tx19,self.sl13,self.tx20,self.sl14,
                self.tx21,self.sl15,self.tx22,self.sl16,
                self.tx23,self.sl17,self.tx24,self.sl18,
                self.tx25,self.sl19,self.tx26,self.sl20,
                self.b,
            ],
            scroll=ft.ScrollMode.ALWAYS,
        )

    def button_clicked(self, e):

        shisetsu_seibi_paymentschedule_ikkatsu = Decimal(self.sl2.value/100)
        shisetsu_seibi_paymentschedule_kappu = Decimal(1 - shisetsu_seibi_paymentschedule_ikkatsu).quantize(Decimal('0.000001'), ROUND_HALF_UP)
        kisai_jutou = Decimal((self.sl5.value/100)).quantize(Decimal('0.000001'), ROUND_HALF_UP),
        kisai_koufu = Decimal(self.sl6.value/100).quantize(Decimal('0.000001'), ROUND_HALF_UP),
        hojo_ritsu = Decimal(self.sl7.value/100).quantize(Decimal('0.000001'), ROUND_HALF_UP),
        kappu_kinri_spread = Decimal(self.sl15.value/100).quantize(Decimal('0.000001'), ROUND_HALF_UP),

        # ここで、補足の入力値を算定して、辞書（final_inputs）に
        # 含めて、TinyDBに格納、それをMake_inputsで呼び出して、
        # pydanticで検証する。
        #const_start_date_year = self.inputs['const_start_date_year']
        #const_start_date_month = self.inputs['const_start_date_month']
        #const_start_date_day = self.inputs['const_start_date_day']
        const_start_date = datetime.date(const_start_date_year, const_start_date_month, const_start_date_day)
        start_year = datetime.datetime.strptime(str(const_start_date), '%Y-%m-%d').year
        start_month = datetime.datetime.strptime(str(const_start_date), '%Y-%m-%d').month

        if start_month < 4:
            first_end_fy = datetime.date(start_year, 3, 31)
        else:
            first_end_fy = datetime.date(start_year + 1, 3, 31)
    
        discount_rate = self.inputs['kijun_kinri'] + self.inputs['kitai_bukka']
        discount_rate = Decimal(str(discount_rate)).quantize(Decimal('0.000001'), ROUND_HALF_UP)

        target_years = 45
        proj_years = self.inputs['proj_years']
        const_years = self.inputs['const_years']
        ijikanri_years = proj_years - const_years
        shoukan_kaishi_jiki = const_years + self.inputs['chisai_sueoki_kikan']  + 1

        Kappu_kinri = self.inputs['kijun_kinri'] + self.inputs['lg_spread'] + self.inputs['kappu_kinri_spread']
        Kappu_kinri = Decimal(str(Kappu_kinri)).quantize(Decimal('0.000001'), ROUND_HALF_UP)

        first_end_fy, first_end_fy + dateutil.relativedelta.relativedelta(year=1)

        SPC_hiyou_total = self.inputs['SPC_keihi'] * self.inputs['ijikanri_unnei_years'] + self.inputs['SPC_shihon']
        SPC_hiyou_nen = self.inputs['SPC_fee'] + self.inputs['SPC_keihi']
        SPC_keihi_LCC = self.inputs['SPC_keihi'] + Decimal(str(self.inputs['SPC_fee'])) + self.inputs['houjinjuminzei_kintou']
        #d_format = '%Y-%m-%d'

        final_inputs = {
            "advisory_fee": str(self.sl13.value),
            "chisai_kinri": str(Decimal(self.initial_inputs["chisai_kinri"]/100).quantize(Decimal('0.000001'), ROUND_HALF_UP)),# CSVに％単位されているため、実数表記に切り替える。 
            "chisai_shoukan_kikan": int(self.sl1.value),
            "chisai_sueoki_kikan": int(self.initial_inputs["chisai_sueoki_kikan"]),
            "const_start_date_year": int(self.sl16.value),
            "const_start_date_month": int(self.sl17.value),
            "const_start_date_day": int(self.sl18.value),
            "const_start_date": str(const_start_date), 
            "const_years": int(self.initial_inputs["const_years"]),
            "discount_rate": str(discount_rate),

            "first_end_fy": first_end_fy,
            "growth": str(self.initial_inputs["growth"]),
            "hojo_ritsu": str(hojo_ritsu),
            "houjinzei_ritsu": str(self.initial_inputs["houjinzei_ritsu"]),
            "houjinjuminzei_kintou": str(self.initial_inputs["houjinjuminzei_kintou"]),
            "houjinjuminzei_ritsu_todouhuken": str(self.initial_inputs["houjinjuminzei_ritsu_todouhuken"]),
            "houjinjuminzei_ritsu_shikuchoson": str(self.initial_inputs["houjinjuminzei_ritsu_shikuchoson"]),
            "hudousanshutokuzei_hyoujun": str(self.initial_inputs["hudousanshutokuzei_hyoujun"]),
            "hudousanshutokuzei_ritsu": str(self.initial_inputs["hudousanshutokuzei_ritsu"]),
            "ijikanri_unnei_1": str(self.initial_inputs["ijikanri_unnei_1"]),
            "ijikanri_unnei_1_LCC": str(self.initial_inputs["ijikanri_unnei_1_LCC"]),
            "ijikanri_unnei_1_org": str(self.initial_inputs["ijikanri_unnei_1_org"]),
            "ijikanri_unnei_1_org_LCC": str(self.initial_inputs["ijikanri_unnei_1_org_LCC"]),
            "ijikanri_unnei_2": str(self.initial_inputs["ijikanri_unnei_2"]),
            "ijikanri_unnei_2_LCC": str(self.initial_inputs["ijikanri_unnei_2_LCC"]),
            "ijikanri_unnei_2_org": str(self.initial_inputs["ijikanri_unnei_2_org"]),
            "ijikanri_unnei_2_org_LCC": str(self.initial_inputs["ijikanri_unnei_2_org_LCC"]),
            "ijikanri_unnei_3": str(self.initial_inputs["ijikanri_unnei_3"]),
            "ijikanri_unnei_3_LCC": str(self.initial_inputs["ijikanri_unnei_3_LCC"]),
            "ijikanri_unnei_3_org": str(self.initial_inputs["ijikanri_unnei_3_org"]),
            "ijikanri_unnei_3_org_LCC": str(self.initial_inputs["ijikanri_unnei_3_org_LCC"]),
            "ijikanri_unnei_years": int(self.initial_inputs["ijikanri_unnei_years"]),
            "ijikanri_years": ijikanri_years,
            "kappu_kinri_spread": str(kappu_kinri_spread),
            "Kappu_kinri": str(Kappu_kinri),
            "kijun_kinri": str(Decimal(self.initial_inputs["kijun_kinri"]/100).quantize(Decimal('0.000001'), ROUND_HALF_UP)),# CSVに％単位されているため、実数表記に切り替える。
            "kisai_jutou": str(kisai_jutou),
            "kisai_koufu": str(kisai_koufu),
            "kitai_bukka": str(Decimal(self.initial_inputs["kitai_bukka"]/100).quantize(Decimal('0.000001'), ROUND_HALF_UP)), # CSVに％単位されているため、実数表記に切り替える。
            "koteishisanzei_hyoujun": str(self.initial_inputs["koteishisanzei_hyoujun"]),
            "koteishisanzei_ritsu": str(self.initial_inputs["koteishisanzei_ritsu"]),

            "lg_spread": str(self.initial_inputs["lg_spread"]),
            "mgmt_type": self.initial_inputs["mgmt_type"],
            "monitoring_costs_PSC": str(self.sl3.value),
            "monitoring_costs_LCC": str(self.sl4.value),

            "option_01": str(self.sl19.value),
            "option_02": str(self.sl20.value),
            "pre_kyoukouka": bool(self.initial_inputs["pre_kyoukouka"]),
            "proj_ctgry": self.initial_inputs["proj_ctgry"],
            "proj_type": self.initial_inputs["proj_type"],
            "proj_years": int(self.initial_inputs["proj_years"]),
            "rakusatsu_ritsu": str(self.initial_inputs["rakusatsu_ritsu"]),
            "reduc_shisetsu": str(self.initial_inputs["reduc_shisetsu"]),
            "reduc_ijikanri_1": str(self.initial_inputs["reduc_ijikanri_1"]),
            "reduc_ijikanri_2": str(self.initial_inputs["reduc_ijikanri_2"]),
            "reduc_ijikanri_3": str(self.initial_inputs["reduc_ijikanri_3"]),
            "riyouryoukin_shunyu": str(self.sl14.value),

            "shisetsu_seibi": str(self.initial_inputs["shisetsu_seibi"]),
            "shisetsu_seibi_LCC": str(self.initial_inputs["shisetsu_seibi_LCC"]),
            "shisetsu_seibi_org": str(self.initial_inputs["shisetsu_seibi_org"]),
            "shisetsu_seibi_org_LCC": str(self.initial_inputs["shisetsu_seibi_org_LCC"]),
            "shisetsu_seibi_paymentschedule_ikkatsu": str(shisetsu_seibi_paymentschedule_ikkatsu),
            "shisetsu_seibi_paymentschedule_kappu": str(shisetsu_seibi_paymentschedule_kappu),
            "shoukan_kaishi_jiki": shoukan_kaishi_jiki,
            "SPC_keihi": str(self.sl8.value),
            "SPC_fee": str(self.sl9.value),
            "SPC_shihon": str(self.sl10.value),
            "SPC_yobihi": str(self.sl11.value),
            "SPC_hiyou_atsukai": int(self.sl12.value),
            "SPC_hiyou_total": SPC_hiyou_total,
            "SPC_hiyou_nen": SPC_hiyou_nen,
            "SPC_keihi_LCC": SPC_keihi_LCC,

            "target_years": target_years,
            "tourokumenkyozei_hyoujun": str(self.initial_inputs["tourokumenkyozei_hyoujun"]),
            "tourokumenkyozei_ritsu": str(self.initial_inputs["tourokumenkyozei_ritsu"]),
            "yosantanka_hiritsu_shisetsu": str(self.initial_inputs["yosantanka_hiritsu_shisetsu"]),
            "yosantanka_hiritsu_ijikanri_1": str(self.initial_inputs["yosantanka_hiritsu_ijikanri_1"]),
            "yosantanka_hiritsu_ijikanri_2": str(self.initial_inputs["yosantanka_hiritsu_ijikanri_2"]),
            "yosantanka_hiritsu_ijikanri_3": str(self.initial_inputs["yosantanka_hiritsu_ijikanri_3"]),
            "zei_modori": str(self.initial_inputs["zei_modori"]),
            "zei_total": str(self.initial_inputs["zei_total"]),
            "zeimae_rieki": str(self.initial_inputs["zeimae_rieki"]),
            "zei_modori": str(self.initial_inputs["zei_modori"]),
            "zei_total": str(self.initial_inputs["zei_total"]),

        }

        if os.path.exists("fi_db.json"):
            os.remove("fi_db.json")
        db = TinyDB('fi_db.json')
        db.insert(final_inputs)
        db.close()
        #if os.path.exists("final_inputs.db"):
        #    os.remove("final_inputs.db")
        #con = sqlite3.connect('final_inputs.db')
        #con.close()
        
        VFM_calc()
        self.page.go("/view_saved")
