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
        self.height = 2000
        self.resizable = True
        self.slider_value00 = ft.Text("0.00", size=30, weight=ft.FontWeight.W_200)
        self.slider_value01 = ft.Text("0.00", size=30, weight=ft.FontWeight.W_200)
        self.slider_value02 = ft.Text("0.00", size=30, weight=ft.FontWeight.W_200)
        self.slider_value03 = ft.Text("0.00", size=30, weight=ft.FontWeight.W_200)
        self.slider_value04 = ft.Text("0.00", size=30, weight=ft.FontWeight.W_200)
        self.slider_value05 = ft.Text("0.00", size=30, weight=ft.FontWeight.W_200)
        self.slider_value06 = ft.Text("0.00", size=30, weight=ft.FontWeight.W_200)
        self.slider_value07 = ft.Text("0.00", size=30, weight=ft.FontWeight.W_200)
        self.slider_value08 = ft.Text("0.00", size=30, weight=ft.FontWeight.W_200)
        self.slider_value09 = ft.Text("0.00", size=30, weight=ft.FontWeight.W_200)
        self.slider_value10 = ft.Text("0.00", size=30, weight=ft.FontWeight.W_200)
        self.slider_value11 = ft.Text("0.00", size=30, weight=ft.FontWeight.W_200)
        self.slider_value12 = ft.Text("0.00", size=30, weight=ft.FontWeight.W_200)
    
    def handle_change_00(self, e):
        sl_value = e.control.value
        self.slider_value00.value = str(sl_value)
        self.page.update()
    def handle_change_01(self, e):
        sl_value = e.control.value
        self.slider_value01.value = str(sl_value)
        self.page.update()
    def handle_change_02(self, e):
        sl_value = e.control.value
        self.slider_value02.value = str(sl_value)
        self.page.update()
    def handle_change_03(self, e):
        sl_value = e.control.value
        self.slider_value03.value = str(sl_value)
        self.page.update()
    def handle_change_04(self, e):
        sl_value = e.control.value
        self.slider_value04.value = str(sl_value)
        self.page.update()
    def handle_change_05(self, e):
        sl_value = e.control.value
        self.slider_value05.value = str(sl_value)
        self.page.update()
    def handle_change_06(self, e):
        sl_value = e.control.value
        self.slider_value06.value = str(sl_value)
        self.page.update()
    def handle_change_07(self, e):
        sl_value = e.control.value
        self.slider_value07.value = str(sl_value)
        self.page.update()
    def handle_change_08(self, e):
        sl_value = e.control.value
        self.slider_value08.value = str(sl_value)
        self.page.update()
    def handle_change_09(self, e):
        sl_value = e.control.value
        self.slider_value09.value = str(sl_value)
        self.page.update()
    def handle_change_10(self, e):
        sl_value = e.control.value
        self.slider_value10.value = str(sl_value)
        self.page.update()
    def handle_change_11(self, e):
        sl_value = e.control.value
        self.slider_value11.value = str(sl_value)
        self.page.update()
    def handle_change_12(self, e):
        sl_value = e.control.value
        self.slider_value12.value = str(sl_value)
        self.page.update()

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
                ft.dropdown.Option("BTO"),
                ft.dropdown.Option("DBO(SPCなし)"),
                ft.dropdown.Option("BOT/BOO"),
                ft.dropdown.Option("BT/DB(いずれもSPCなし)"),
            ],
        )
        self.dd4 = ft.Dropdown(
            label="事業期間",
            hint_text="事業期間を選択してください(施設整備期間以上)",
            width=400,
            value="20",
            options=[
                ft.dropdown.Option("1"),  ft.dropdown.Option("2"),  ft.dropdown.Option("3"),
                ft.dropdown.Option("4"),  ft.dropdown.Option("5"),  ft.dropdown.Option("6"),
                ft.dropdown.Option("7"),  ft.dropdown.Option("8"),  ft.dropdown.Option("9"),
                ft.dropdown.Option("10"), ft.dropdown.Option("11"), ft.dropdown.Option("12"),
                ft.dropdown.Option("13"), ft.dropdown.Option("14"), ft.dropdown.Option("15"),
                ft.dropdown.Option("16"), ft.dropdown.Option("17"), ft.dropdown.Option("18"),
                ft.dropdown.Option("19"), ft.dropdown.Option("20"), ft.dropdown.Option("21"),
                ft.dropdown.Option("22"), ft.dropdown.Option("23"), ft.dropdown.Option("24"),
                ft.dropdown.Option("25"), ft.dropdown.Option("26"), ft.dropdown.Option("27"),
                ft.dropdown.Option("28"), ft.dropdown.Option("29"), ft.dropdown.Option("30"),
            ],
        )
        self.dd5 = ft.Dropdown(
            label="地方債償還期間",
            hint_text="地方債償還期間を選択してください",
            width=400,
            value="20",
            options=[
                ft.dropdown.Option("1"),  ft.dropdown.Option("2"),  ft.dropdown.Option("3"),
                ft.dropdown.Option("4"),  ft.dropdown.Option("5"),  ft.dropdown.Option("6"),
                ft.dropdown.Option("7"),  ft.dropdown.Option("8"),  ft.dropdown.Option("9"),
                ft.dropdown.Option("10"), ft.dropdown.Option("11"), ft.dropdown.Option("12"),
                ft.dropdown.Option("13"), ft.dropdown.Option("14"), ft.dropdown.Option("15"),
                ft.dropdown.Option("16"), ft.dropdown.Option("17"), ft.dropdown.Option("18"),
                ft.dropdown.Option("19"), ft.dropdown.Option("20"), ft.dropdown.Option("21"),
                ft.dropdown.Option("22"), ft.dropdown.Option("23"), ft.dropdown.Option("24"),
                ft.dropdown.Option("25"), ft.dropdown.Option("26"),
            ],
        )
        self.dd6 = ft.Dropdown(
            label="施設整備期間",
            hint_text="施設整備期間（O方式ではゼロ）を選択してください",
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
        self.tx0 = ft.Text("施設整備費 落札価格ベース(百万円)")
        self.sl0 = ft.CupertinoSlider(
            value=0,
            min=0,
            max=100000,
            #divisions=10000,
            #label="{value}百万円",
            on_change=self.handle_change_00,
        )
        self.tx1 = ft.Text("施設整備費 予算単価ベース(百万円)")
        self.sl1 = ft.CupertinoSlider(
            value=0,
            min=0,
            max=100000,
            #divisions=10000,
            #label="{value}百万円",
            on_change=self.handle_change_01,
        )
        self.tx2 = ft.Text("維持管理運営費(年額)人件費 落札価格ベース(百万円)")
        self.sl2 = ft.CupertinoSlider(
            value=0,
            min=0,
            max=1000,
            #divisions=1000,
            #label="{value}百万円",
            on_change=self.handle_change_02,
        )
        self.tx3 = ft.Text("維持管理運営費(年額)人件費 予算単価ベース(百万円)")
        self.sl3 = ft.CupertinoSlider(
            value=0,
            min=0,
            max=1000,
            #divisions=1000,
            on_change=self.handle_change_03,
            #label="{value}百万円",
        )
        self.tx4 = ft.Text("維持管理運営費(年額)修繕費 落札価格ベース(百万円)")
        self.sl4 = ft.CupertinoSlider(
            value=0,
            min=0,
            max=100,
            #divisions=100,
            #label="{value}百万円",
            on_change=self.handle_change_04,
        )
        self.tx5 = ft.Text("維持管理運営費(年額)修繕費 予算単価ベース(百万円)")
        self.sl5 = ft.CupertinoSlider(
            value=0,
            min=0,
            max=100,
            #divisions=100,
            #label="{value}百万円",
            on_change=self.handle_change_05,
        )
        self.tx6 = ft.Text("維持管理運営費(年額)動力費 落札価格ベース(百万円)")
        self.sl6 = ft.CupertinoSlider(
            value=0,
            min=0,
            max=100,
            #divisions=100,
            #label="{value}百万円",
            on_change=self.handle_change_06,
        )
        self.tx7 = ft.Text("維持管理運営費(年額)動力費 予算単価ベース(百万円)")
        self.sl7 = ft.CupertinoSlider(
            value=0,
            min=0,
            max=100,
            #divisions=100,
            #label="{value}百万円",
            on_change=self.handle_change_07,
        )
        self.tx8 = ft.Text("施設整備費の効率性(%)(推奨:5%")
        self.sl8 = ft.CupertinoSlider(
            value=0,
            min=0.0,
            max=20,
            #divisions=20,
            #label="{value}%",
            on_change=self.handle_change_08,
        )
        self.tx9 = ft.Text("維持管理運営費の効率性(人件費,%)(推奨:5%)")
        self.sl9 = ft.CupertinoSlider(
            value=0,
            min=0.0,
            max=20,
            #divisions=20,
            #label="{value}%",
            on_change=self.handle_change_09,
        )
        self.tx10 = ft.Text("維持管理運営費の効率性(修繕費,%)(推奨:5%)")
        self.sl10 = ft.CupertinoSlider(
            value=0,
            min=0.0,
            max=20,
            #divisions=20,
            #label="{value}%",
            on_change=self.handle_change_10,
        )
        self.tx11 = ft.Text("維持管理運営費の効率性(動力費,%)(推奨:5%)")
        self.sl11 = ft.CupertinoSlider(
            value=0,
            min=0.0,
            max=20,
            #divisions=20,
            #label="{value}%",
            on_change=self.handle_change_11,
        )
        self.tx12 = ft.Text("落札率(競争の効果反映,%)(推奨:95%)")
        self.sl12 = ft.CupertinoSlider(
            value=0,
            min=0,
            max=100,
            #divisions=20,
            #label="{value}%",
            on_change=self.handle_change_12,
        )
        self.b = ft.ElevatedButton(text="初期値の入力", on_click=self.button_clicked)
        return ft.Column(
            [
                self.dd1,  self.dd2, self.dd3,  self.dd4,  self.dd5,  self.dd6, 
                self.tx0,  self.slider_value, self.sl0, self.tx1,  self.slider_value, self.sl1,  
                self.tx2,  self.slider_value, self.sl2, self.tx3,  self.slider_value, self.sl3, 
                self.tx4,  self.slider_value, self.sl4,  self.tx5,  self.slider_value, self.sl5,
                self.tx6,  self.slider_value, self.sl6, self.tx7,  self.slider_value, self.sl7,  
                self.tx8,  self.slider_value, self.sl8, self.tx9,  self.slider_value, self.sl9, 
                self.tx10, self.slider_value, self.sl10, self.tx11, self.slider_value, self.sl11,
                self.tx12, self.slider_value, self.sl12,
                self.b
            ],
            scroll=ft.ScrollMode.ALWAYS,
        )

    def button_clicked(self, e):
        # jgb_rates.JGB_rates_conv()
        if self.dd3.value == "BT/DB":
            self.dd4.value = self.dd5.value
        
        if self.dd3.value == "O":
            self.dd5.value = "0"

        proj_years = int(self.dd4.value)
        const_years = int(self.dd6.value)
        ijikanri_unnei_years = proj_years - const_years

        if proj_years < const_years:
            ft.page.go("/")

        const_start_date = datetime.date.today().strftime('%Y-%m-%d')
        

        shisetsu_seibi_org_R = Decimal(self.sl0.value).quantize(Decimal('0.000001'), ROUND_HALF_UP)
        shisetsu_seibi_org_Y = Decimal(self.sl1.value).quantize(Decimal('0.000001'), ROUND_HALF_UP)
        shisetsu_seibi_org = Decimal(shisetsu_seibi_org_R + shisetsu_seibi_org_Y).quantize(Decimal('0.000001'), ROUND_HALF_UP)
        ijikanri_unnei_1_org_R = Decimal(self.sl2.value).quantize(Decimal('0.000001'), ROUND_HALF_UP)
        ijikanri_unnei_1_org_Y = Decimal(self.sl3.value).quantize(Decimal('0.000001'), ROUND_HALF_UP)
        ijikanri_unnei_1_org = Decimal(ijikanri_unnei_1_org_R + ijikanri_unnei_1_org_Y).quantize(Decimal('0.000001'), ROUND_HALF_UP)
        ijikanri_unnei_2_org_R= Decimal(self.sl4.value).quantize(Decimal('0.000001'), ROUND_HALF_UP)
        ijikanri_unnei_2_org_Y = Decimal(self.sl5.value).quantize(Decimal('0.000001'), ROUND_HALF_UP)
        ijikanri_unnei_2_org = Decimal(ijikanri_unnei_2_org_R + ijikanri_unnei_2_org_Y).quantize(Decimal('0.000001'), ROUND_HALF_UP)
        ijikanri_unnei_3_org_R = Decimal(self.sl6.value).quantize(Decimal('0.000001'), ROUND_HALF_UP)
        ijikanri_unnei_3_org_Y = Decimal(self.sl7.value).quantize(Decimal('0.000001'), ROUND_HALF_UP)
        ijikanri_unnei_3_org = Decimal(ijikanri_unnei_3_org_R + ijikanri_unnei_3_org_Y).quantize(Decimal('0.000001'), ROUND_HALF_UP)
        reduc_shisetsu = Decimal(self.sl8.value / 100).quantize(Decimal('0.000001'), ROUND_HALF_UP)
        reduc_ijikanri_1 = Decimal(self.sl9.value / 100).quantize(Decimal('0.000001'), ROUND_HALF_UP)
        reduc_ijikanri_2 = Decimal(self.sl10.value / 100).quantize(Decimal('0.000001'), ROUND_HALF_UP)
        reduc_ijikanri_3 = Decimal(self.sl11.value / 100).quantize(Decimal('0.000001'), ROUND_HALF_UP)
        rakusatsu_ritsu = Decimal(self.sl12.value / 100).quantize(Decimal('0.000001'), ROUND_HALF_UP)

        shisetsu_seibi_org_LCC = Decimal(shisetsu_seibi_org * (1- reduc_shisetsu)).quantize(Decimal('0.000001'), ROUND_HALF_UP)
        shisetsu_seibi = Decimal(shisetsu_seibi_org_R + (shisetsu_seibi_org_Y * rakusatsu_ritsu)).quantize(Decimal('0.000001'), ROUND_HALF_UP)
        shisetsu_seibi_LCC = Decimal(shisetsu_seibi * (1- reduc_shisetsu)).quantize(Decimal('0.000001'), ROUND_HALF_UP)
        ijikanri_unnei_1_org_LCC = Decimal(ijikanri_unnei_1_org * (1-reduc_ijikanri_1)).quantize(Decimal('0.000001'), ROUND_HALF_UP)
        ijikanri_unnei_1 = Decimal(ijikanri_unnei_1_org_R + (ijikanri_unnei_1_org_Y * rakusatsu_ritsu)).quantize(Decimal('0.000001'), ROUND_HALF_UP)
        ijikanri_unnei_1_LCC = Decimal(ijikanri_unnei_1 * (1-reduc_ijikanri_1)).quantize(Decimal('0.000001'), ROUND_HALF_UP)
        ijikanri_unnei_2_org_LCC = Decimal(ijikanri_unnei_2_org * (1-reduc_ijikanri_2)).quantize(Decimal('0.000001'), ROUND_HALF_UP)
        ijikanri_unnei_2 = Decimal(ijikanri_unnei_2_org_R + (ijikanri_unnei_2_org_Y * rakusatsu_ritsu)).quantize(Decimal('0.000001'), ROUND_HALF_UP)
        ijikanri_unnei_2_LCC = Decimal(ijikanri_unnei_2 * (1-reduc_ijikanri_2)).quantize(Decimal('0.000001'), ROUND_HALF_UP)
        ijikanri_unnei_3_org_LCC = Decimal(ijikanri_unnei_3_org * (1-reduc_ijikanri_3)).quantize(Decimal('0.000001'), ROUND_HALF_UP)
        ijikanri_unnei_3 = Decimal(ijikanri_unnei_3_org_R + (ijikanri_unnei_3_org_Y * rakusatsu_ritsu)).quantize(Decimal('0.000001'), ROUND_HALF_UP)
        ijikanri_unnei_3_LCC = Decimal(ijikanri_unnei_3 * (1-reduc_ijikanri_3)).quantize(Decimal('0.000001'), ROUND_HALF_UP)

        yosantanka_hiritsu_shisetsu = Decimal(shisetsu_seibi_org_Y/shisetsu_seibi_org).quantize(Decimal('0.000001'), ROUND_HALF_UP)
        yosantanka_hiritsu_ijikanri_1 = Decimal(ijikanri_unnei_1_org_Y/ijikanri_unnei_1_org).quantize(Decimal('0.000001'), ROUND_HALF_UP)
        yosantanka_hiritsu_ijikanri_2 = Decimal(ijikanri_unnei_2_org_Y/ijikanri_unnei_2_org).quantize(Decimal('0.000001'), ROUND_HALF_UP)
        yosantanka_hiritsu_ijikanri_3 = Decimal(ijikanri_unnei_3_org_Y/ijikanri_unnei_3_org).quantize(Decimal('0.000001'), ROUND_HALF_UP)

        chisai_shoukan_kikan = int(self.dd5.value)

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

        r2 = JRB_rates_df.loc[chisai_shoukan_kikan][const_years]

        chisai_sueoki_kikan = const_years

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
            hudousanshutokuzei_hyoujun = 0.0
            hudousanshutokuzei_ritsu = 0.0
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

        SPC_fee = Decimal(20).quantize(Decimal('0.000001'), ROUND_HALF_UP)
        SPC_shihon = Decimal(100).quantize(Decimal('0.000001'), ROUND_HALF_UP)
        SPC_yobihi = Decimal(456).quantize(Decimal('0.000001'), ROUND_HALF_UP)
        SPC_hiyou_atsukai = int(1)

        initial_inputs = {
            "mgmt_type": self.dd1.value,
            "proj_ctgry": self.dd2.value,
            "proj_type": self.dd3.value,
            "proj_years": self.dd4.value,
            "const_years": self.dd6.value,
            "ijikanri_unnei_years": int(ijikanri_unnei_years),
            "const_start_date": const_start_date,
            "kijun_kinri": str(Decimal(r1).quantize(Decimal('0.000001'), ROUND_HALF_UP)),
            "chisai_kinri": str(Decimal(r2).quantize(Decimal('0.000001'), ROUND_HALF_UP)),
            "chisai_sueoki_kikan": int(chisai_sueoki_kikan),
            "chisai_shoukan_kikan": int(chisai_shoukan_kikan),
            "zei_modori": str(Decimal(zei_modori)),
            "lg_spread": str(Decimal(0.01).quantize(Decimal('0.000001'), ROUND_HALF_UP)),
            "zei_total": str(Decimal(0.18).quantize(Decimal('0.000001'), ROUND_HALF_UP)),
            "riyou_ryoukin": riyou_ryoukin,
            "growth": str(Decimal(0.0).quantize(Decimal('0.000001'), ROUND_HALF_UP)),
            "kitai_bukka": str(Decimal(kitai_bukka)),
            "shisetsu_seibi": str(shisetsu_seibi),
            "shisetsu_seibi_org": str(shisetsu_seibi_org),
            "shisetsu_seibi_org_LCC": str(shisetsu_seibi_org_LCC),
            "shisetsu_seibi_LCC": str(shisetsu_seibi_LCC),
            "ijikanri_unnei_1": str(ijikanri_unnei_1),
            "ijikanri_unnei_1_org": str(ijikanri_unnei_1_org),
            "ijikanri_unnei_1_org_LCC": str(ijikanri_unnei_1_org_LCC),
            "ijikanri_unnei_1_LCC": str(ijikanri_unnei_1_LCC),
            "ijikanri_unnei_2": str(ijikanri_unnei_2),
            "ijikanri_unnei_2_org": str(ijikanri_unnei_2_org),
            "ijikanri_unnei_2_org_LCC": str(ijikanri_unnei_2_org_LCC),
            "ijikanri_unnei_2_LCC": str(ijikanri_unnei_2_LCC),
            "ijikanri_unnei_3": str(ijikanri_unnei_3),
            "ijikanri_unnei_3_org": str(ijikanri_unnei_3_org),
            "ijikanri_unnei_3_org_LCC": str(ijikanri_unnei_3_org_LCC),
            "ijikanri_unnei_3_LCC": str(ijikanri_unnei_3_LCC),
            "yosantanka_hiritsu_shisetsu": str(yosantanka_hiritsu_shisetsu),
            "yosantanka_hiritsu_ijikanri_1": str(yosantanka_hiritsu_ijikanri_1),
            "yosantanka_hiritsu_ijikanri_2": str(yosantanka_hiritsu_ijikanri_2),
            "yosantanka_hiritsu_ijikanri_3": str(yosantanka_hiritsu_ijikanri_3),
            "rakusatsu_ritsu": str(rakusatsu_ritsu),
            "reduc_shisetsu": str(reduc_shisetsu),
            "reduc_ijikanri_1": str(reduc_ijikanri_1),
            "reduc_ijikanri_2": str(reduc_ijikanri_2),
            "reduc_ijikanri_3": str(reduc_ijikanri_3),
            "pre_kyoukouka": True,
            "kisai_jutou": str(Decimal(kisai_jutou)),
            "kisai_koufu": str(Decimal(kisai_koufu)),
            "hojo_ritsu": str(Decimal(hojo)),
            "zeimae_rieki": str(Decimal(0.0).quantize(Decimal('0.000001'), ROUND_HALF_UP)),
            "SPC_keihi": str(Decimal(20.0).quantize(Decimal('0.000001'), ROUND_HALF_UP)),
            "SPC_fee": str(SPC_fee),
            "SPC_shihon": str(SPC_shihon),
            "SPC_yobihi": str(SPC_yobihi),
            "SPC_hiyou_atsukai": SPC_hiyou_atsukai,
            "houjinzei_ritsu": houjinzei_ritsu,
            "houjinjuminzei_kintou": houjinjuminzei_kintou,
            "hudousanshutokuzei_hyoujun": hudousanshutokuzei_hyoujun,
            "hudousanshutokuzei_ritsu": hudousanshutokuzei_ritsu,
            "koteishisanzei_hyoujun": koteishisanzei_hyoujun,
            "koteishisanzei_ritsu": koteishisanzei_ritsu,
            "tourokumenkyozei_hyoujun": tourokumenkyozei_hyoujun,
            "tourokumenkyozei_ritsu": tourokumenkyozei_ritsu,
            "houjinjuminzei_ritsu_todouhuken": houjinjuminzei_ritsu_todouhuken,
            "houjinjuminzei_ritsu_shikuchoson": houjinjuminzei_ritsu_shikuchoson,
        }

        #for item in list(initial_inputs.values()):
        #    if not item:
        #        ft.page.go("/")
        #    else:
        #        pass


        if os.path.exists("ii_db.json"):
            os.remove("ii_db.json")
        db = TinyDB('ii_db.json')
        db.insert(initial_inputs)
        db.close()
        self.page.go("/final_inputs")
