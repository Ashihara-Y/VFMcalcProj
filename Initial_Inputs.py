import sys
sys.dont_write_bytecode = True
import os
import flet as ft
# from flet_core.session_storage import SessionStorage
import pandas as pd
import pyarrow as pa
import datetime
import tinydb
from tinydb import TinyDB, Query


class Initial_Inputs(ft.Column):
    def __init__(self):
        super().__init__()
        self.title = "初期入力"
        self.width = 500
        self.height = 370
        self.resizable = True

    def build(self):
        self.dd1 = ft.Dropdown(
            label="管理者の種別",
            hint_text="管理者の種別を選択してください",
            width=400,
            options=[
                ft.dropdown.Option("国"),
                ft.dropdown.Option("都道府県"),
                ft.dropdown.Option("市町村"),
            ],
        )
        self.dd2 = ft.Dropdown(
            label="事業の方式",
            hint_text="事業の方式を選択してください",
            width=400,
            options=[
                ft.dropdown.Option("サービス購入型"),
                # ft.dropdown.Option("独立採算型"),
                # ft.dropdown.Option("混合型"),
            ],
        )
        self.dd3 = ft.Dropdown(
            label="事業の類型",
            hint_text="事業の類型を選択してください",
            width=400,
            options=[
                ft.dropdown.Option("BTO/DBO/RO"),
                # ft.dropdown.Option("BOT"),
                ft.dropdown.Option("BT/DB"),
                ft.dropdown.Option("O"),
            ],
        )
        self.dd4 = ft.Dropdown(
            label="事業期間",
            hint_text="事業期間を選択してください(施設整備期間以上)",
            width=400,
            value="20",
            options=[
                ft.dropdown.Option("1"),
                ft.dropdown.Option("2"),
                ft.dropdown.Option("3"),
                ft.dropdown.Option("4"),
                ft.dropdown.Option("5"),
                ft.dropdown.Option("6"),
                ft.dropdown.Option("7"),
                ft.dropdown.Option("8"),
                ft.dropdown.Option("9"),
                ft.dropdown.Option("10"),
                ft.dropdown.Option("11"),
                ft.dropdown.Option("12"),
                ft.dropdown.Option("13"),
                ft.dropdown.Option("14"),
                ft.dropdown.Option("15"),
                ft.dropdown.Option("16"),
                ft.dropdown.Option("17"),
                ft.dropdown.Option("18"),
                ft.dropdown.Option("19"),
                ft.dropdown.Option("20"),
                ft.dropdown.Option("21"),
                ft.dropdown.Option("22"),
                ft.dropdown.Option("23"),
                ft.dropdown.Option("24"),
                ft.dropdown.Option("25"),
                ft.dropdown.Option("26"),
                ft.dropdown.Option("27"),
                ft.dropdown.Option("28"),
                ft.dropdown.Option("29"),
                ft.dropdown.Option("30"),
            ],
        )
        self.dd5 = ft.Dropdown(
            label="施設整備期間",
            hint_text="施設整備期間（O方式の場合のみゼロ）を選択してください",
            width=400,
            value="1",
            options=[
                ft.dropdown.Option("0"),
                ft.dropdown.Option("1"),
                ft.dropdown.Option("2"),
                ft.dropdown.Option("3"),
                ft.dropdown.Option("4"),
                ft.dropdown.Option("5"),
            ],
        )
        self.tx1 = ft.Text("施設整備費")
        self.sl1 = ft.Slider(
            value=float(self.initial_inputs["shisetsu_seibi"]),
            min=100,
            max=100000,
            divisions=10000,
            label="{value}百万円",
            #on_change=slider_changed,
        )

        self.tx2 = ft.Text("維持管理運営費(年額)")
        self.sl2 = ft.Slider(
            value=float(self.initial_inputs["ijikanri_unnei"]),
            min=0,
            max=1000,
            divisions=1000,
            label="{value}百万円",
        )
        self.tx3 = ft.Text("施設整備費の効率性")
        self.sl3 = ft.Slider(
            value=float(self.initial_inputs["reduc_shisetsu"]),
            min=0.0,
            max=0.20,
            divisions=200,
            label="{value}%",
        )
        self.tx4 = ft.Text("維持管理運営費の効率性")
        self.sl4 = ft.Slider(
            value=float(self.initial_inputs["reduc_ijikanri_1"]),
            min=0.0,
            max=0.20,
            divisions=200,
            label="{value}%",
        )
        self.tx5 = ft.Text("維持管理運営費の効率性2")
        self.sl5 = ft.Slider(
            value=float(self.initial_inputs["reduc_ijikanri_2"]),
            min=0.0,
            max=0.20,
            divisions=200,
            label="{value}%",
        )
        self.tx6 = ft.Text("維持管理運営費の効率性3")
        self.sl6 = ft.Slider(
            value=float(self.initial_inputs["reduc_ijikanri_3"]),
            min=0.0,
            max=0.20,
            divisions=20,
            label="{value}%",
        )
        self.tx7 = ft.Text("落札率(競争の効果反映)")
        self.sl7 = ft.Slider(
            value=float(self.initial_inputs["rakusatsu_ritsu"]),
            min=0.8,
            max=1.0,
            divisions=100,
            label="{value}%",
        )
        self.b = ft.ElevatedButton(text="初期値の入力", on_click=self.button_clicked)
        return ft.Column(
            [self.dd1, 
             self.dd2, 
             self.dd3, 
             self.dd4, 
             self.dd5, 
             self.tx1,
             self.sl1,
             self.tx2,
             self.sl2,
             self.tx3,
             self.sl3,
             self.tx4,
             self.sl4,
             self.tx5,
             self.sl5,
             self.tx6,
             self.sl6,
             self.tx7,
             self.sl7,
             self.b],
            scroll=ft.ScrollMode.ALWAYS,
        )

    def button_clicked(self, e):
        # jgb_rates.JGB_rates_conv()
        if self.dd3.value == "BT/DB":
            self.dd4.value = self.dd5.value
        
        if self.dd3.value == "O":
            self.dd5.value = "0"

        proj_years = int(self.dd4.value)
        const_years = int(self.dd5.value)
        ijikanri_unnei_years = proj_years - const_years

        if proj_years < const_years:
            ft.page.go("/")

        const_start_date = datetime.date.today()

        JGB_rates_df = pd.read_csv(
            "JGB_rates.csv",
            sep="\t",
            encoding="utf-8",
            header=None,
            names=["year", "rate"],
        ).set_index("year")

        JRB_rates_df = pd.read_csv(
            "JRB_rates.csv",
            encoding="utf-8",
            sep='\t', 
            names=[0,1,2,3,4,5], 
            index_col=0)

        y, d = divmod(int(self.dd4.value), 5)

        if d > 2:
            r_idx = str((y + 1) * 5) + "年"
        elif d <= 2:
            r_idx = str(y * 5) + "年"

        r1 = JGB_rates_df.loc[r_idx].iloc[0]

        r2 = JRB_rates_df.loc[proj_years][const_years]

        kitai_bukka_j = (
            pd.read_csv("BOJ_ExpInflRate_down.csv", encoding="shift-jis", skiprows=1)
            .dropna()
            .iloc[-1, 1]
        )
        gonensai_rimawari = JGB_rates_df.loc["5年"].iloc[0]
        # gonensai_rimawari = pd.read_csv('JGB_rates.csv', sep='\t', encoding='utf-8', header=None).iloc[0,-1]
        kitai_bukka = kitai_bukka_j - gonensai_rimawari

        if self.dd2.value == "サービス購入型":
            houjinzei_ritsu = 0.0
            houjinjuminzei_kintou = 0.18
            fudousanshutokuzei_hyoujun = 0.0
            fudousanshutokuzei_ritsu = 0.0
            koteishisanzei_hyoujun = 0.0
            koteishisanzei_ritsu = 0.0
            tourokumenkyozei_hyoujun = 0.0
            tourokumenkyozei_ritsu = 0.0
            houjinjuminzei_ritsu_todouhuken = 0.0
            houjinjuminzei_ritsu_shikuchoson = 0.0

        if self.dd1.value == "国":
            zei_modori = 27.8
            hojo = 0.0
            kisai_jutou = 0.0
            kisai_koufu = 0.0
        elif self.dd1.value == "都道府県":
            zei_modori = 5.78
            hojo = 50.0
            kisai_jutou = 75.0
            kisai_koufu = 30.0
        elif self.dd1.value == "市町村":
            zei_modori = 8.4
            hojo = 30.0
            kisai_jutou = 75.0
            kisai_koufu = 30.0
        else:
            pass

        initial_inputs = {
            "mgmt_type": self.dd1.value,
            "proj_ctgry": self.dd2.value,
            "proj_type": self.dd3.value,
            "proj_years": self.dd4.value,
            "const_years": self.dd5.value,
            "kijun_kinri": r1,
            "chisai_kinri": r2,
            "zei_modori": float(zei_modori),
            "lg_spread": 1.5,
            "zei_total": 41.98,
            "growth": 0.0,
            "kitai_bukka": float(kitai_bukka),
            "shisetsu_seibi": 2000.0,
            "ijikanri_unnei": 50.0,
            "reduc_shisetsu": 10.0,
            "reduc_ijikanri": 10.0,
            "pre_kyoukouka": False,
            "kisai_jutou": float(kisai_jutou),
            "kisai_koufu": float(kisai_koufu),
            "zeimae_rieki": 8.5,
            "SPC_keihi": 15.0,
            "hojo": float(hojo),
        }

        if os.path.exists("ii_db.json"):
            os.remove("ii_db.json")
        db = TinyDB('ii_db.json')
        db.insert(initial_inputs)
        db.close()
        self.page.go("/final_inputs")
