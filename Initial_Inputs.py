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
from decimal import *

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
            value=Decimal(3000),
            min=100,
            max=100000,
            divisions=10000,
            label="{value}百万円",
            #on_change=slider_changed,
        )
        self.tx2 = ft.Text("維持管理運営費(年額)人件費")
        self.sl2 = ft.Slider(
            value=Decimal(30),
            min=0,
            max=1000,
            divisions=1000,
            label="{value}百万円",
        )
        self.tx3 = ft.Text("維持管理運営費(年額)修繕費")
        self.sl3 = ft.Slider(
            value=Decimal(15),
            min=0,
            max=1000,
            divisions=1000,
            label="{value}百万円",
        )
        self.tx4 = ft.Text("維持管理運営費(年額)動力費")
        self.sl4 = ft.Slider(
            value=Decimal(5),
            min=0,
            max=1000,
            divisions=1000,
            label="{value}百万円",
        )
        self.tx5 = ft.Text("施設整備費の効率性")
        self.sl5 = ft.Slider(
            value=Decimal(0.05),
            min=0.0,
            max=0.20,
            divisions=200,
            label="{value}%",
        )
        self.tx6 = ft.Text("維持管理運営費の効率性(人件費)")
        self.sl6 = ft.Slider(
            value=Decimal(0.05),
            min=0.0,
            max=0.20,
            divisions=200,
            label="{value}%",
        )
        self.tx7 = ft.Text("維持管理運営費の効率性(修繕費)")
        self.sl7 = ft.Slider(
            value=Decimal(0.05),
            min=0.0,
            max=0.20,
            divisions=200,
            label="{value}%",
        )
        self.tx8 = ft.Text("維持管理運営費の効率性(動力費)")
        self.sl8 = ft.Slider(
            value=Decimal(0.05),
            min=0.0,
            max=0.20,
            divisions=20,
            label="{value}%",
        )
        self.tx9 = ft.Text("落札率(競争の効果反映)")
        self.sl9 = ft.Slider(
            value=Decimal(0.95),
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
        
        shisetsu_seibi_org = Decimal(self.sl1.value)
        ijikanri_unnei_1_org = Decimal(self.sl2.value)
        ijikanri_unnei_2_org = Decimal(self.sl3.value)
        ijikanri_unnei_3_org = Decimal(self.sl4.value)
        reduc_shisetsu = Decimal(self.sl4.value)
        reduc_ijikanri_1 = Decimal(self.sl6.value)
        reduc_ijikanri_2 = Decimal(self.sl7.value)
        reduc_ijikanri_3 = Decimal(self.sl8.value)
        rakusatsu_ritsu = Decimal(self.sl9.value)

        shisetsu_seibi_org_LCC = shisetsu_seibi_org * reduc_shisetsu
        shisetsu_seibi = shisetsu_seibi_org * rakusatsu_ritsu
        shisetsu_seibi_LCC = shisetsu_seibi * reduc_shisetsu
        ijikanri_unnei_1_org_LCC = ijikanri_unnei_1_org * reduc_ijikanri_1
        ijikanri_unnei_1 = ijikanri_unnei_1_org * rakusatsu_ritsu
        ijikanri_unnei_1_LCC = ijikanri_unnei_1 * reduc_ijikanri_1
        ijikanri_unnei_2_org_LCC = ijikanri_unnei_2_org * reduc_ijikanri_2
        ijikanri_unnei_2 = ijikanri_unnei_2_org * rakusatsu_ritsu
        ijikanri_unnei_2_LCC = ijikanri_unnei_2 * reduc_ijikanri_2
        ijikanri_unnei_3_org_LCC = ijikanri_unnei_3_org * reduc_ijikanri_3
        ijikanri_unnei_3 = ijikanri_unnei_3_org * rakusatsu_ritsu
        ijikanri_unnei_3_LCC = ijikanri_unnei_3 * reduc_ijikanri_3

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
            riyou_ryoukin = 0.0

        if self.dd1.value == "国":
            zei_modori = 0.278
            hojo = 0.0
            kisai_jutou = 0.0
            kisai_koufu = 0.0
        elif self.dd1.value == "都道府県":
            zei_modori = 0.0578
            hojo = 0.5
            kisai_jutou = 0.75
            kisai_koufu = 0.30
        elif self.dd1.value == "市町村":
            zei_modori = 0.084
            hojo = 0.300
            kisai_jutou = 0.750
            kisai_koufu = 0.300
        else:
            pass

        SPC_fee = Decimal(20)
        SPC_shihon = Decimal(100)
        SPC_yobihi = Decimal(456)
        SPC_hiyou_atsukai = int(1)

        initial_inputs = {
            "mgmt_type": self.dd1.value,
            "proj_ctgry": self.dd2.value,
            "proj_type": self.dd3.value,
            "proj_years": self.dd4.value,
            "const_years": self.dd5.value,
            "ijikanri_unnei_years": int(ijikanri_unnei_years),
            "const_start_date": const_start_date,
            "kijun_kinri": Decimal(r1),
            "chisai_kinri": Decimal(r2),
            "zei_modori": Decimal(zei_modori),
            "lg_spread": Decimal(0.01),
            "zei_total": Decimal(0.18),
            "riyou_ryoukin": riyou_ryoukin,
            "growth": Decimal(0.0),
            "kitai_bukka": Decimal(kitai_bukka),
            "shisetsu_seibi": shisetsu_seibi,
            "shisetsu_seibi_org": shisetsu_seibi_org,
            "shisetsu_seibi_org_LCC": shisetsu_seibi_org_LCC,
            "shisetsu_seibi_LCC": shisetsu_seibi_LCC,
            "ijikanri_unnei_1": ijikanri_unnei_1,
            "ijikanri_unnei_1_org": ijikanri_unnei_1_org,
            "ijikanri_unnei_1_org_LCC": ijikanri_unnei_1_org_LCC,
            "ijikanri_unnei_1_LCC": ijikanri_unnei_1_LCC,
            "ijikanri_unnei_2": ijikanri_unnei_2,
            "ijikanri_unnei_2_org": ijikanri_unnei_2_org,
            "ijikanri_unnei_2_org_LCC": ijikanri_unnei_2_org_LCC,
            "ijikanri_unnei_2_LCC": ijikanri_unnei_2_LCC,
            "ijikanri_unnei_3": ijikanri_unnei_3,
            "ijikanri_unnei_3_org": ijikanri_unnei_3_org,
            "ijikanri_unnei_3_org_LCC": ijikanri_unnei_3_org_LCC,
            "ijikanri_unnei_3_LCC": ijikanri_unnei_3_LCC,
            "reduc_shisetsu": reduc_shisetsu,
            "reduc_ijikanri_1": reduc_ijikanri_1,
            "reduc_ijikanri_2": reduc_ijikanri_2,
            "reduc_ijikanri_3": reduc_ijikanri_3,
            "pre_kyoukouka": True,
            "kisai_jutou": Decimal(kisai_jutou),
            "kisai_koufu": Decimal(kisai_koufu),
            "hojo_ritsu": Decimal(hojo),
            "zeimae_rieki": Decimal(0.0),
            "SPC_keihi": Decimal(20.0),
            "SPC_fee": SPC_fee,
            "SPC_shihon": SPC_shihon,
            "SPC_yobihi": SPC_yobihi,
            "SPC_hiyou_atsukai": SPC_hiyou_atsukai,
            "houjinzei_ritsu": houjinzei_ritsu,
            "houjinjuminzei_kintou": houjinjuminzei_kintou,
            "fudousanshutokuzei_hyoujun": fudousanshutokuzei_hyoujun,
            "fudousanshutokuzei_ritsu": fudousanshutokuzei_ritsu,
            "koteishisanzei_hyoujun": koteishisanzei_hyoujun,
            "koteishisanzei_ritsu": koteishisanzei_ritsu,
            "tourokumenkyozei_hyoujun": tourokumenkyozei_hyoujun,
            "tourokumenkyozei_ritsu": tourokumenkyozei_ritsu,
            "houjinjuminzei_ritsu_todouhuken": houjinjuminzei_ritsu_todouhuken,
            "houjinjuminzei_ritsu_shikuchoson": houjinjuminzei_ritsu_shikuchoson,
        }

        if os.path.exists("ii_db.json"):
            os.remove("ii_db.json")
        db = TinyDB('ii_db.json')
        db.insert(initial_inputs)
        db.close()
        self.page.go("/final_inputs")
