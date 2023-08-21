import sys
sys.dont_write_bytecode = True
import flet as ft
import joblib
#from joblib import Memory
from tempfile import mkdtemp
import os
import pathlib

#savedir = pathlib.Path(mkdtemp(dir='.')) # 一時ディレクトリを作成
#filename = savedir / 'initial_inputs.joblib' # 一時ディレクトリにファイルを作成
#cachedir = savedir
#memory = Memory(cachedir, verbose=0)

#import sqlite3
import pandas as pd
import jgb_rates

class Initial_Inputs(ft.UserControl):
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
                #ft.dropdown.Option("独立採算型"),
                #ft.dropdown.Option("混合型"),
            ],
        )
        self.dd3 = ft.Dropdown(
            label="事業の類型",
            hint_text="事業の類型を選択してください", 
            width=400,
            options=[
                ft.dropdown.Option("BTO"),
                #ft.dropdown.Option("BOT"),
                #ft.dropdown.Option("BT"),
            ],
        )
        self.dd4 = ft.Dropdown(
            label="事業期間",
            hint_text="事業期間を選択してください", 
            width=400,
            value="20",
            options=[
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
                ft.dropdown.Option("30")
            ],
        )
        self.dd5 = ft.Dropdown(
            label="施設整備期間",
            hint_text="施設整備期間を選択してください", 
            width=400,
            value="1",
            options=[
                ft.dropdown.Option("1"),
                ft.dropdown.Option("2"),
                ft.dropdown.Option("3")
            ],
        )
        self.b = ft.ElevatedButton(text="選択", on_click=self.button_clicked)
        return ft.Column([self.dd1, self.dd2, self.dd3, self.dd4, self.dd5, self.b], scroll=ft.ScrollMode.ALWAYS)

#def main(page: ft.Page):
    #@Memory.cache
    def button_clicked(self, e):        
        #jgb_rates.JGB_rates_conv()
        JGB_rates_df = pd.read_csv('JGB_rates.csv', sep='\t', encoding='shift_jis', header=None, names=['year', 'rate'])
        #JRB_rates_df = pd.read_csv('JRB_rates.csv', sep='\t', encoding='shift_jis', header=None, names=['year', 'rate'])

        #year_select = ['10年', '10年', '10年', '15年', '15年', '15年', '15年', '15年', '20年', '20年', '20年', '20年', '20年', '25年', '25年', '25年', '25年', '25年', '30年', '30年', '30年']

        y,d = divmod(int(self.dd5.value), 5)

        if d > 2:
            r_idx = str((y+1) * 5) + '年'
        elif d <= 2:
            r_idx = str(y * 5) + '年'

        r1 = float(JGB_rates_df[JGB_rates_df['year']==r_idx]['rate'].iloc[0])
        #r2 = float(JRB_rates_df[JRB_rates_df['year']==r_idx]['rate'].iloc[0])
        r2 = 0.729
        
        if self.dd1.value == '国':
            zei_modori = 27.8
            hojo = 0.0
            kisai_jutou = 0.0
            kisai_koufu = 0.0
        elif self.dd1.value == '都道府県':
            zei_modori = 5.78
            hojo = 50.0
            kisai_jutou = 75.0
            kisai_koufu = 30.0
        elif self.dd1.value == '市町村':
            zei_modori = 8.4
            hojo = 30.0
            kisai_jutou = 75.0
            kisai_koufu = 30.0
        else:
            pass
        
        initail_inputs = {
            "mgmt_type":self.dd1.value, 
            "proj_ctgry":self.dd2.value, 
            "proj_type":self.dd3.value,
            "proj_years":self.dd4.value,
            "const_years":self.dd5.value,
            "kijun_kinri":float(r1),
            "chisai_kinri":float(r2),
            "zei_modori":float(zei_modori),
            "lg_spread":1.5,
            "zei_total":41.98,
            "growth":0.0,
            "kitai_bukka":2.0,
            "shisetsu_seibi":2000.0,
            "ijikanri_unnei":50.0,
            "reduc_shisetsu":90.0,
            "reduc_ijikanri":90.0,
            "pre_kyoukouka":False,
            "kisai_jutou":float(kisai_jutou),
            "kisai_koufu":float(kisai_koufu),
            "zeimae_rieki":8.5,
            "SPC_keihi":15.0,
            "hojo":float(hojo),
            }
        
        joblib.dump(initail_inputs, 'initial_inputs.joblib')
        #return initail_inputs#ft.page.ClientStorage.set("Initial_Inputs", initail_inputs)
        #ft.page.session.clear()
        #ft.page.session.set('initial_inputs', initail_inputs)
        #ft.page.save_state(initail_inputs)
