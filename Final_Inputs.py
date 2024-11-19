import sys
sys.dont_write_bytecode = True
import os
import flet as ft
import pandas as pd
import datetime
import tinydb
from tinydb import TinyDB, Query
import VFMcalc2 as vc
import save_results as sr
from decimal import *
import sqlite3

class Final_Inputs(ft.Column):
    def __init__(self):
        super().__init__()
        self.title = "最終入力"
        self.width = 500
        self.height = 1000
        self.resizable = True

        db = TinyDB("ii_db.json")
        self.initial_inputs = db.all()[0]
        
    def build(self):

        self.tx0 = ft.Text(str("＜＜初期データ＞＞"))
        self.tx1 = ft.Text(str("発注者区分： " + self.initial_inputs["mgmt_type"]))
        self.tx2 = ft.Text(str("事業タイプ： " + self.initial_inputs["proj_ctgry"]))
        self.tx3 = ft.Text(str("事業方式： " + self.initial_inputs["proj_type"]))
        self.tx4 = ft.Text(str("事業期間： " + self.initial_inputs["proj_years"] + "年"))
        self.tx5 = ft.Text(str("施設整備期間： " + self.initial_inputs["const_years"] + "年"))
        self.tx6 = ft.Text(str("地方債償還据置期間： " + self.initial_inputs["chisai_sueoki_years" + "年"]))
    
        self.dt1 = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("事業費項目")),
                ft.DataColumn(ft.Text("入力値"), numeic=True),
                ft.DataColumn(ft.Text("競争の効果反映(PSC)"), numeic=True),
                ft.DataColumn(ft.Text("効率性反映(PFI-LCC)"), numeic=True), 
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
        ),
        self.dt2 = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("税目")),
                ft.DataColumn(ft.Text("標準／均等"), numeic=True),
                ft.DataColumn(ft.Text("税率"), numeic=True),
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
                        ft.DataCell(ft.Text("法人住民税(都道府県、市区町村)")),
                        ft.DataCell(ft.Text(self.initial_inputs["houjinjuminzei_kintou"])),
                        ft.DataCell(ft.Text(self.initial_inputs["houjinjuminzei_ritsu_todouhuken"], self.initial_inputs["houjinjuminzei_ritsu_shikuchoson"])),
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
        ),

        self.tx7 = ft.Text("地方債償還期間")
        self.sl1 = ft.Slider(
            value=int(self.initial_inputs["chisai_shoukan_kikan"]),
            min=0,
            max=30,
            divisions=30,
            label="{value}%",
        )
        self.tx8 = ft.Text("施設整備費支払 一括払の比率")
        self.sl2 = ft.Slider(
            value=Decimal(self.initial_inputs["shisetsu_seibi_paymentschedule_ikkatsu"]),
            min=0.0,
            max=1.00,
            divisions=100,
            label="{value}%",
        )
        self.tx9 = ft.Text("モニタリング等費用(PSC)")
        self.sl3 = ft.Slider(
            value=Decimal(self.initial_inputs["monitoring_costs_PSC"]),
            min=0,
            max=100,
            divisions=100,
            label="{value}%",
        )
        self.tx10 = ft.Text("モニタリング等費用(PFI-LCC)")
        self.sl4 = ft.Slider(
            value=Decimal(self.initial_inputs["monitoring_costs_LCC"]),
            min=0,
            max=100,
            divisions=100,
            label="{value}%",
        )
        self.tx11 = ft.Text("起債充当率")
        self.sl5 = ft.Slider(
            value=Decimal(self.initial_inputs["kisai_jutou"]),
            min=0.0,
            max=1.00,
            divisions=100,
            label="{value}%",
        )
        self.tx12 = ft.Text("起債への交付金カバー率")
        self.sl6 = ft.Slider(
            value=Decimal(self.initial_inputs["kisai_koufu"]),
            min=0.0,
            max=0.50,
            divisions=50,
            label="{value}%",
        )
        self.tx13 = ft.Text("補助率")
        self.sl7 = ft.Slider(
            value=Decimal(self.initial_inputs["hojo_ritsu"]),
            min=0.0,
            max=0.60,
            divisions=60,
            label="{value}%",
        )
        self.tx14 = ft.Text("SPC経費年額")
        self.sl8 = ft.Slider(
            value=Decimal(self.initial_inputs["SPC_keihi"]),
            min=0,
            max=50,
            divisions=50,
            label="{value}百万円",
        )
        self.tx15 = ft.Text("SPCへの手数料")
        self.sl9 = ft.Slider(
            value=Decimal(self.initial_inputs["SPC_fee"]),
            min=0,
            max=50,
            divisions=50,
            label="{value}百万円",
        )
        self.tx16 = ft.Text("SPC資本金")
        self.sl10 = ft.Slider(
            value=Decimal(self.initial_inputs["SPC_shihon"]),
            min=0,
            max=100,
            divisions=100,
            label="{value}百万円",
        )
        self.tx17 = ft.Text("SPC予備費")
        self.sl11 = ft.Slider(
            value=Decimal(self.initial_inputs["SPC_yobihi"]),
            min=0,
            max=1000,
            divisions=1000,
            label="{value}百万円",
        )
        self.tx18 = ft.Text("SPC経費の扱い（デフォルト：割賦に含める）")
        self.sl12 = ft.Slider(
            value=self.initial_inputs["SPC_hiyou_atsukai"],
            min=0,
            max=1,
            divisions=1,
            label="{value}",
        )
        self.tx19 = ft.Text("アドバイザリー等経費")
        self.sl13 = ft.Slider(
            value=Decimal(self.initial_inputs["adovisory_fee"]),
            min=0,
            max=50,
            divisions=50,
            label="{value}百万円",
        )
        self.tx20 = ft.Text("利用料金収入")
        self.sl14 = ft.Slider(
            value=Decimal(self.initial_inputs["riyou_ryoukin"]),
            min=0,
            max=100,
            divisions=100,
            label="{value}百万円",
        )
        self.tx21 = ft.Text("割賦金利へのスプレッド")
        self.sl15 = ft.Slider(
            value=Decimal(self.initial_inputs["kappu_kinri_spread"]),
            min=0.0,
            max=2.0,
            divisions=20,
            label="{value*100}%",
        )
        self.tx22 = ft.Text("施設整備開始年月日")
        self.sl16 = ft.Slider(
            value=self.initial_inputs["const_start_date"],
            min=0,
            max=15,
            divisions=15,
            label="{value}",
        )
        self.b = ft.ElevatedButton(text="入力確認・計算", on_click=self.button_clicked)
        return ft.Column(
            [
                self.tx0,
                self.tx1,
                self.tx2,
                self.tx3,
                self.tx4,
                self.tx5,
                self.tx6,
                self.dt1,
                self.dt2,
                self.tx7,
                self.sl1,
                self.tx8,
                self.sl2,
                self.tx9,
                self.sl3,
                self.tx10,
                self.sl4,
                self.tx11,
                self.sl5,
                self.tx12,
                self.sl6,
                self.tx13,
                self.sl7,
                self.tx14,
                self.sl8,
                self.tx15,
                self.sl9,
                self.tx16,
                self.sl10,
                self.tx17,
                self.sl11,
                self.tx18,
                self.sl12,
                self.tx19,
                self.sl13,
                self.tx20,
                self.sl14,
                self.tx21,
                self.sl15,
                self.tx22,
                self.sl16,
                self.b,
            ],
            scroll=ft.ScrollMode.ALWAYS,
        )

    def button_clicked(self, e):

        shisetsu_seibi_paymentschedule_kappu = 1 - self.initial_inputs["shisetsu_seibi_paymentschedule_ikkatsu"]

        final_inputs = {
            "mgmt_type": self.initial_inputs["mgmt_type"],
            "proj_ctgry": self.initial_inputs["proj_ctgry"],
            "proj_type": self.initial_inputs["proj_type"],
            "proj_years": int(self.initial_inputs["proj_years"]),
            "const_years": int(self.initial_inputs["const_years"]),
            "kijun_kinri": float(self.initial_inputs["kijun_kinri"]),
            "chisai_kinri": float(self.initial_inputs["chisai_kinri"]),
            "zei_modori": float(self.initial_inputs["zei_modori"]),
            "lg_spread": float(self.initial_inputs["lg_spread"]),
            "zei_total": float(self.initial_inputs["zei_total"]),
            "growth": float(self.initial_inputs["growth"]),
            "kitai_bukka": float(self.initial_inputs["kitai_bukka"]),
            "shisetsu_seibi": float(self.sl3.value),
            "ijikanri_unnei": float(self.sl4.value),
            "reduc_shisetsu": float(self.sl5.value),
            "reduc_ijikanri": float(self.sl6.value),
            "pre_kyoukouka": bool(self.initial_inputs["pre_kyoukouka"]),
            "kisai_jutou": float(self.sl7.value),
            "kisai_koufu": float(self.sl8.value),
            "zeimae_rieki": float(self.initial_inputs["zeimae_rieki"]),
            "SPC_keihi": float(self.sl10.value),
            "hojo": float(self.sl9.value),
            "advisory_fee": Decimal,
            "chisai_kinri": Decimal,
            "chisai_shoukan_kikan": int,
            "chisai_sueoki_years": int,
            "const_years": int,
            "const_start_date": datetime.datetime,
            "growth": Decimal,
            "hojo_ritsu": Decimal,
            "ijikanri_unnei": Decimal,
            "ijikanri_unnei_LCC": Decimal,
            "ijikanri_unnei_org": Decimal,
            "ijikanri_unnei_org_LCC": Decimal,
            "ijikanri_unnei_years": int,
            "kappu_kinri_spread": Decimal,
            "kijun_kinri": Decimal,
            "kisai_jutou": Decimal,
            "kisai_koufu": Decimal,
            "kitai_bukka": Decimal,
            "kyoukouka_yosantanka_hiritsu": Decimal,
            "lg_spread": Decimal,
            "mgmt_type": str,
            "monitoring_costs_LCC": Decimal,
            "monitoring_costs_PSC": Decimal,
            "pre_kyoukouka": bool,
            "proj_ctgry": str,
            "proj_type": str,
            "rakusatsu_ritsu": Decimal,
            "reduc_shisetsu": Decimal,
            "reduc_ijikanri": Decimal,
            "riyouryoukin_shunyu": Decimal,
            "shisetsu_seibi": Decimal,
            "shisetsu_seibi_LCC": Decimal,
            "shisetsu_seibi_org": Decimal,
            "shisetsu_seibi_org_LCC": Decimal,
            "shisetsu_seibi_paymentschedule_ikkatsu": Decimal,
            "shisetsu_seibi_paymentschedule_kappu": Decimal,
            "SPC_hiyou_atsukai": int,
            "SPC_keihi": Decimal,
            "SPC_fee": Decimal,
            "SPC_shihon": Decimal,
            "SPC_yobihi": Decimal,
            "zei_modori": Decimal,
            "zei_total": Decimal,
            "zeimae_rieki": Decimal,
            "houjinzei_ritsu": Decimal,
            "houjinjuminzei_kintou": Decimal,
            "fudousanshutokuzei_hyoujun": Decimal,
            "fudousanshutokuzei_ritsu": Decimal,
            "koteishisanzei_hyoujun": Decimal,
            "koteishisanzei_ritsu": Decimal,
            "tourokumenkyozei_hyoujun": Decimal,
            "tourokumenkyozei_ritsu": Decimal,
            "houjinjuminzei_ritsu_todouhuken": Decimal,
            "houjinjuminzei_ritsu_shikuchoson": Decimal,
            "option_01": Decimal,
            "option_02": Decimal,
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
        
        res_PSC_LCC = vc.calc_PSC_LCC(final_inputs)
        results, results_2 = vc.calc_VFM(res_PSC_LCC)
        sr.save_ddb(results, results_2)
        self.page.go("/view_saved")
