import sys
sys.dont_write_bytecode = True
import os
import flet as ft
import pandas as pd
#import duckdb
import tinydb
from tinydb import TinyDB, Query
import VFMcalc2 as vc
import save_results as sr
from decimal import *
import sqlite3
# savedir = pathlib.Path(tempfile.mkdtemp(dir='.')) # 一時ディレクトリを作成
# filename = savedir / 'final_inputs.joblib' # 一時ディレクトリにファイルを作成

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

        self.tx1 = ft.Text(str("管理者種別： " + self.initial_inputs["mgmt_type"]))
        self.tx2 = ft.Text(str(self.initial_inputs["proj_ctgry"]))
        self.tx3 = ft.Text(str(self.initial_inputs["proj_type"]))
        self.tx4 = ft.Text(str(self.initial_inputs["proj_years"]))
        self.tx5 = ft.Text(str(self.initial_inputs["const_years"]))
        self.tx6 = ft.Text(str(self.initial_inputs["chisai_sueoki_years"]))
        self.tx7 = ft.Text(str(self.initial_inputs["houjinzei_ritsu"]))
        self.tx8 = ft.Text(str(self.initial_inputs["houjinjuminzei_kintou"]))
        self.tx8 = ft.Text(str(self.initial_inputs["hudousanshutokuzei_hyoujun"]))
        self.tx9 = ft.Text(str(self.initial_inputs["hudousanshutokuzei_ritsu"]))
        self.tx10 = ft.Text(str(self.initial_inputs["koteishisanzei_hyoujun"]))
        self.tx11 = ft.Text(str(self.initial_inputs["koteishisanzei_ritsu"]))
        self.tx12 = ft.Text(str(self.initial_inputs["tourokumenkyozei_hyoujun"]))
        self.tx13 = ft.Text(str(self.initial_inputs["tourokumenkyozei_ritsu"]))
        self.tx14 = ft.Text(str(self.initial_inputs["houjinjuminzei_ritsu_todouhuken"]))
        self.tx15 = ft.Text(str(self.initial_inputs["houjinjuminzei_ritsu_shikuchoson"]))

        #self.tx6 = ft.Row(ft.Text("施設整備費："), t_sl)
        self.tx16 = ft.Text("地方債償還期間")
        self.sl1 = ft.Slider(
            value=int(self.initial_inputs["chisai_shoukan_kikan"]),
            min=0,
            max=30,
            divisions=30,
            label="{value}%",
        )
        self.tx17 = ft.Text("施設整備費支払 一括払の比率")
        self.sl2 = ft.Slider(
            value=Decimal(self.initial_inputs["shisetsu_seibi_paymentschedule_ikkatsu"]),
            min=0.0,
            max=1.00,
            divisions=100,
            label="{value}%",
        )
        self.tx18 = ft.Text("モニタリング等費用(PSC)")
        self.sl3 = ft.Slider(
            value=Decimal(self.initial_inputs["monitoring_costs_PSC"]),
            min=0,
            max=100,
            divisions=100,
            label="{value}%",
        )
        self.tx19 = ft.Text("モニタリング等費用(PFI-LCC)")
        self.sl4 = ft.Slider(
            value=Decimal(self.initial_inputs["monitoring_costs_LCC"]),
            min=0,
            max=100,
            divisions=100,
            label="{value}%",
        )
        self.tx20 = ft.Text("起債充当率")
        self.sl5 = ft.Slider(
            value=Decimal(self.initial_inputs["kisai_jutou"]),
            min=0.0,
            max=1.00,
            divisions=100,
            label="{value}%",
        )
        self.tx21 = ft.Text("起債への交付金カバー率")
        self.sl6 = ft.Slider(
            value=Decimal(self.initial_inputs["kisai_koufu"]),
            min=0.0,
            max=0.50,
            divisions=50,
            label="{value}%",
        )
        self.tx22 = ft.Text("補助率")
        self.sl7 = ft.Slider(
            value=Decimal(self.initial_inputs["hojo_ritsu"]),
            min=0.0,
            max=0.60,
            divisions=60,
            label="{value}%",
        )
        self.tx23 = ft.Text("SPC経費年額")
        self.sl8 = ft.Slider(
            value=Decimal(self.initial_inputs["SPC_keihi"]),
            min=0,
            max=50,
            divisions=50,
            label="{value}百万円",
        )
        self.tx24 = ft.Text("SPCへの手数料")
        self.sl9 = ft.Slider(
            value=Decimal(self.initial_inputs["SPC_fee"]),
            min=0,
            max=50,
            divisions=50,
            label="{value}百万円",
        )
        self.tx25 = ft.Text("SPC資本金")
        self.sl10 = ft.Slider(
            value=Decimal(self.initial_inputs["SPC_shihon"]),
            min=0,
            max=100,
            divisions=100,
            label="{value}百万円",
        )
        self.tx26 = ft.Text("SPC予備費")
        self.sl11 = ft.Slider(
            value=Decimal(self.initial_inputs["SPC_yobihi"]),
            min=0,
            max=1000,
            divisions=1000,
            label="{value}百万円",
        )
        self.tx27 = ft.Text("SPC経費の扱い（デフォルト：割賦に含める）")
        self.sl12 = ft.Slider(
            value=self.initial_inputs["SPC_hiyou_atsukai"],
            min=0,
            max=1,
            divisions=1,
            label="{value}",
        )
        self.tx28 = ft.Text("アドバイザリー等経費")
        self.sl13 = ft.Slider(
            value=Decimal(self.initial_inputs["adovisory_fee"]),
            min=0,
            max=50,
            divisions=50,
            label="{value}百万円",
        )
        self.tx29 = ft.Text("利用料金収入")
        self.sl14 = ft.Slider(
            value=Decimal(self.initial_inputs["riyou_ryoukin"]),
            min=0,
            max=100,
            divisions=100,
            label="{value}百万円",
        )
        self.tx30 = ft.Text("割賦金利へのスプレッド")
        self.sl15 = ft.Slider(
            value=Decimal(self.initial_inputs["kappu_kinri_spread"]),
            min=0.0,
            max=2.0,
            divisions=20,
            label="{value*100}%",
        )
        self.tx31 = ft.Text("施設整備開始年月日")
        self.sl16 = ft.Slider(
            value=self.initial_inputs["const_start_date"],
            min=0,
            max=15,
            divisions=15,
            label="{value}",
        )
        self.tx32 = ft.Text("SPC経費年額")
        self.sl17 = ft.Slider(
            value=float(self.initial_inputs["SPC_keihi"]),
            min=0,
            max=15,
            divisions=15,
            label="{value}百万円",
        )
        self.tx33 = ft.Text("SPC経費年額")
        self.sl18 = ft.Slider(
            value=float(self.initial_inputs["SPC_keihi"]),
            min=0,
            max=15,
            divisions=15,
            label="{value}百万円",
        )
        self.tx34 = ft.Text("SPC経費年額")
        self.sl19 = ft.Slider(
            value=float(self.initial_inputs["SPC_keihi"]),
            min=0,
            max=15,
            divisions=15,
            label="{value}百万円",
        )
        self.tx35 = ft.Text("SPC経費年額")
        self.sl20 = ft.Slider(
            value=float(self.initial_inputs["SPC_keihi"]),
            min=0,
            max=15,
            divisions=15,
            label="{value}百万円",
        )
        self.b = ft.ElevatedButton(text="入力確認・計算", on_click=self.button_clicked)
        return ft.Column(
            [
                self.tx1,
                self.tx2,
                self.tx3,
                self.tx4,
                self.tx5,
                self.tx6,
                self.tx7,
                self.tx8,
                self.tx9,
                self.tx10,
                self.tx11,
                self.tx12,
                self.tx13,
                self.tx14,
                self.tx15,
                self.tx16,
                self.sl1,
                self.tx17,
                self.sl2,
                self.tx18,
                self.sl3,
                self.tx19,
                self.sl4,
                self.tx20,
                self.sl5,
                self.tx21,
                self.sl6,
                self.tx22,
                self.sl7,
                self.tx23,
                self.sl8,
                self.tx24,
                self.sl9,
                self.tx25,
                self.sl10,
                self.tx26,
                self.sl11,
                self.tx27,
                self.sl12,
                self.tx28,
                self.sl13,
                self.tx29,
                self.sl14,
                self.tx30,
                self.sl15,
                self.tx31,
                self.sl16,
                self.tx32,
                self.sl17,
                self.tx33,
                self.sl18,
                self.tx34,
                self.sl19,
                self.tx35,
                self.sl20,
                self.b,
            ],
            scroll=ft.ScrollMode.ALWAYS,
        )

    def button_clicked(self, e):
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
        }

        if os.path.exists("fi_db.json"):
            os.remove("fi_db.json")
        db = TinyDB('fi_db.json')
        db.insert(final_inputs)
        db.close()
        #if os.path.exists("final_inputs.db"):
        #    os.remove("final_inputs.db")
        #con = sqlite3.connect('final_inputs.db')
        #con = duckdb.connect('final_inputs.db')
        #df_fi = pd.DataFrame(data=final_inputs, index=[1])
        #con.sql('create table final_inputs as select * from df_fi')
        #con.close()
        
        res_PSC_LCC = vc.calc_PSC_LCC(final_inputs)
        results, results_2 = vc.calc_VFM(res_PSC_LCC)
        sr.save_ddb(results, results_2)
        self.page.go("/view_saved")
