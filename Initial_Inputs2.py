import sys
sys.dont_write_bytecode = True
import os
import flet as ft
# from flet_core.session_storage import SessionStorage
import pandas as pd
import datetime
import timeflake
from tinydb import TinyDB, Query
from decimal import *
from zoneinfo import ZoneInfo

class Initial_Inputs(ft.Column):

    def __init__(self):
        super().__init__()
        self.title = "初期入力"
        self.width = 500
        self.height = 2000
        self.resizable = True

        def get_options(op_list):
            options=[]
            for i in op_list:
                options.append(
                    ft.DropdownOption(
                        i, 
                        #content = ft.Text(i)
                    )
                )
            return options

        options_1 = [
            "国",
            "都道府県",
            "市町村",
            ]
        options_2 = [
                "サービス購入型",
                #{key:"コンセッション（スタジアム・アリーナタイプ）"},
                #{key: "コンセッション（下水道タイプ）"},
            ]
        options_3 = [
                "BTO",
                "DBO(SPCなし)",
                "BOT/BOO",
                "BT/DB(いずれもSPCなし)",
            ]
        options_4 = [
                "1", "2", "3", "4", "5",
                "6", "7", "8", "9", "10",
                "11","12","13","14","15",
                "16","17","18","19","20",
                "21","22","23","24","25",
                "26","27","28","29","30",
            ]
        options_5 = [
                "1", "2", "3", "4", "5",
                "6", "7", "8", "9", "10",
                "11","12","13","14","15",
                "16","17","18","19","20",
                "21","22","23","24","25",
                "26",
            ]
        options_6 = [
                "1", "2", "3", "4", "5",
            ]

        self.dd1 = ft.Dropdown(
            label="管理者の種別",
            #hint_text="管理者の種別を選択してください",
            #width=400,
            options=get_options(options_1),
        )
        self.dd2 = ft.Dropdown(
            label="事業の方式",
            #hint_text="事業の方式を選択してください",
            #width=400,
            options=get_options(options_2),
        )
        self.dd3 = ft.Dropdown(
            label="事業の類型",
            #hint_text="事業の類型を選択してください",
            #width=400,
            options=get_options(options_3),
        )
        self.dd4 = ft.Dropdown(
            label="事業期間",
            #hint_text="事業期間を選択してください(施設整備期間以上)",
            #width=400,
            #value="20",
            options=get_options(options_4),
        )
        self.dd5 = ft.Dropdown(
            label="地方債償還期間",
            #hint_text="地方債償還期間を選択してください",
            #width=400,
            #value="20",
            options=get_options(options_5),
        )
        self.dd6 = ft.Dropdown(
            label="施設整備期間",
            #hint_text="施設整備期間を選択してください",
            #width=400,
            #value="1",
            options=get_options(options_6),
        )
        self.b = ft.ElevatedButton(text="初期値の入力", on_click=self.button_clicked)

        self.controls = [
            self.dd1,
            self.dd2,
            self.dd3,
            self.dd4,
            self.dd5,
            self.dd6,
            self.b,
        ]

        
    def button_clicked(self, e):
        # jgb_rates.JGB_rates_conv()
        if self.dd3.value == "BT/DB(いずれもSPCなし)":
            self.dd4.value = self.dd6.value
        
        proj_years = int(self.dd4.value)
        const_years = int(self.dd6.value)
        ijikanri_unnei_years = proj_years - const_years

        if proj_years < const_years:
            ft.page.go("/")

        calc_id = timeflake.random()
        dtime = datetime.datetime.fromtimestamp(calc_id.timestamp // 1000, tz=ZoneInfo("Asia/Tokyo"))
        const_start_date = datetime.date(dtime.year, dtime.month, dtime.day).strftime('%Y-%m-%d')
        
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

        if y >= 1:

            if d > 2:
                r_idx = str((y + 1) * 5) + "年"
            elif d <= 2:
                r_idx = str(y * 5) + "年"
        else:
            r_idx = str(d) + "年"

        r1 = JGB_rates_df.loc[r_idx].iloc[0]

        r2 = JRB_rates_df.loc[chisai_shoukan_kikan][const_years]

        chisai_sueoki_kikan = const_years

        kitai_bukka_j = (
            pd.read_csv("BOJ_ExpInflRate_down.csv", encoding="shift-jis", skiprows=1)
            .dropna()
            .iloc[-1, 1]
        )
        gonensai_rimawari = JGB_rates_df.loc["5年"].iloc[0]
        kitai_bukka = kitai_bukka_j - gonensai_rimawari

        if self.dd2.value == "サービス購入型" and self.dd3.value == "BTO":
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
        else:
            houjinzei_ritsu = 0.0
            houjinjuminzei_kintou = 0.0
            hudousanshutokuzei_hyoujun = 0.0
            hudousanshutokuzei_ritsu = 0.0
            koteishisanzei_hyoujun = 0.0
            koteishisanzei_ritsu = 0.0
            tourokumenkyozei_hyoujun = 0.0
            tourokumenkyozei_ritsu = 0.0
            houjinjuminzei_ritsu_todouhuken = 0.0
            houjinjuminzei_ritsu_shikuchoson = 0.0

        if self.dd1.value == "国":
            hojo = 0.0
            kisai_jutou = 0.0
            kisai_koufu = 0.0
        elif self.dd1.value == "都道府県":
            hojo = 0.5
            kisai_jutou = 0.75
            kisai_koufu = 0.30
        elif self.dd1.value == "市町村":
            hojo = 0.300
            kisai_jutou = 0.750
            kisai_koufu = 0.300
        else:
            pass

        if self.dd3.value == "DBO(SPCなし)" or self.dd3.value == "BT/DB(いずれもSPCなし)":
            SPC_fee = Decimal(0).quantize(Decimal('0.000001'), ROUND_HALF_UP)
            SPC_shihon = Decimal(0).quantize(Decimal('0.000001'), ROUND_HALF_UP)
            SPC_yobihi = Decimal(0).quantize(Decimal('0.000001'), ROUND_HALF_UP)
            SPC_hiyou_atsukai = int(1)
        else:
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
            "lg_spread": str(Decimal(0.01).quantize(Decimal('0.000001'), ROUND_HALF_UP)),
            "kitai_bukka": str(Decimal(kitai_bukka)),
            "pre_kyoukouka": True,
            "kisai_jutou": str(Decimal(kisai_jutou)),
            "kisai_koufu": str(Decimal(kisai_koufu)),
            "hojo_ritsu": str(Decimal(hojo)),
            "SPC_keihi": str(Decimal(20.0).quantize(Decimal('0.000001'), ROUND_HALF_UP)),
            "SPC_fee": str(SPC_fee),
            "SPC_shihon": str(SPC_shihon),
            "SPC_yobihi": str(SPC_yobihi),
            "SPC_hiyou_atsukai": SPC_hiyou_atsukai,
            "houjinzei_ritsu": str(houjinzei_ritsu),
            "houjinjuminzei_kintou": str(houjinjuminzei_kintou),
            "hudousanshutokuzei_hyoujun": str(hudousanshutokuzei_hyoujun),
            "hudousanshutokuzei_ritsu": str(hudousanshutokuzei_ritsu),
            "koteishisanzei_hyoujun": str(koteishisanzei_hyoujun),
            "koteishisanzei_ritsu": str(koteishisanzei_ritsu),
            "tourokumenkyozei_hyoujun": str(tourokumenkyozei_hyoujun),
            "tourokumenkyozei_ritsu": str(tourokumenkyozei_ritsu),
            "houjinjuminzei_ritsu_todouhuken": str(houjinjuminzei_ritsu_todouhuken),
            "houjinjuminzei_ritsu_shikuchoson": str(houjinjuminzei_ritsu_shikuchoson),
        }

        if os.path.exists("ii_db2.json"):
            os.remove("ii_db2.json")
        db = TinyDB('ii_db2.json')
        db.insert(initial_inputs)
        db.close()
        self.page.go("/final_inputs")

def main(page: ft.Page):
    page.add(
            Initial_Inputs()
    )


#ft.app(target=main, view=ft.AppView.WEB_BROWSER)
ft.app(target=main)