import sys
sys.dont_write_bytecode = True
import os
import flet as ft
#import joblib
import pandas as pd
#import duckdb
import tinydb
from tinydb import TinyDB, Query
import VFM_calc as vc
import save_results as sr
from reactive_text import ReactiveText
from state import State, ReactiveState
#import sqlite3
# savedir = pathlib.Path(tempfile.mkdtemp(dir='.')) # 一時ディレクトリを作成
# filename = savedir / 'final_inputs.joblib' # 一時ディレクトリにファイルを作成
text = State("")
class Final_Inputs(ft.UserControl):
    def __init__(self):
        super().__init__()
        self.title = "最終入力"
        self.width = 500
        self.height = 1000
        self.resizable = True

        db = TinyDB("ii_db.json")
        self.initial_inputs = db.all()[0]

        self.tx1 = ReactiveText(self.initial_inputs["mgmt_type"])

    def build(self):
        self.tx1 = ft.Text(str(self.initial_inputs["mgmt_type"]))
        self.tx2 = ft.Text(str(self.initial_inputs["proj_ctgry"]))
        self.tx3 = ft.Text(str(self.initial_inputs["proj_type"]))
        self.tx4 = ft.Text(str(self.initial_inputs["proj_years"]))
        self.tx5 = ft.Text(str(self.initial_inputs["const_years"]))

        self.tx6 = ft.Text("施設整備費")
        self.sl3 = ft.Slider(
            value=float(self.initial_inputs["shisetsu_seibi"]),
            min=100,
            max=100000,
            divisions=10000,
            label="{value}百万円",
        )
        self.tx7 = ft.Text("維持管理運営費")
        self.sl4 = ft.Slider(
            value=float(self.initial_inputs["ijikanri_unnei"]),
            min=0,
            max=1000,
            divisions=1000,
            label="{value}百万円",
        )
        self.tx8 = ft.Text("施設整備費の削減率")
        self.sl5 = ft.Slider(
            value=float(self.initial_inputs["reduc_shisetsu"]),
            min=0,
            max=20,
            divisions=20,
            label="{value}%",
        )
        self.tx9 = ft.Text("維持管理運営費の削減率")
        self.sl6 = ft.Slider(
            value=float(self.initial_inputs["reduc_ijikanri"]),
            min=0,
            max=20,
            divisions=20,
            label="{value}%",
        )
        self.tx10 = ft.Text("起債充当率")
        self.sl7 = ft.Slider(
            value=float(self.initial_inputs["kisai_jutou"]),
            min=0,
            max=100,
            divisions=100,
            label="{value}%",
        )
        self.tx11 = ft.Text("起債への交付金カバー率")
        self.sl8 = ft.Slider(
            value=float(self.initial_inputs["kisai_koufu"]),
            min=0,
            max=50,
            divisions=50,
            label="{value}%",
        )
        self.tx12 = ft.Text("補助率")
        self.sl9 = ft.Slider(
            value=float(self.initial_inputs["hojo"]),
            min=0,
            max=60,
            divisions=50,
            label="{value}%",
        )
        self.tx13 = ft.Text("SPC経費年額")
        self.sl10 = ft.Slider(
            value=float(self.initial_inputs["SPC_keihi"]),
            min=0,
            max=15,
            divisions=15,
            label="{value}百万円",
        )
        self.b = ft.ElevatedButton(text="確認・計算", on_click=self.button_clicked)
        return ft.Column(
            [
                self.tx1,
                self.tx2,
                self.tx3,
                self.tx4,
                self.tx5,
                self.tx6,
                self.sl3,
                self.tx7,
                self.sl4,
                self.tx8,
                self.sl5,
                self.tx9,
                self.sl6,
                self.tx10,
                self.sl7,
                self.tx11,
                self.sl8,
                self.tx12,
                self.sl9,
                self.tx13,
                self.sl10,
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
        #joblib.dump(final_inputs, "final_inputs.joblib")
        
        res_PSC_LCC = vc.calc_PSC_LCC(final_inputs)
        results, results_2 = vc.calc_VFM(res_PSC_LCC)
        sr.save_ddb(results, results_2)
        self.page.go("/view_saved")
