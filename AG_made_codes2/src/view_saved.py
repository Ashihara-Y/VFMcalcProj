import sys
sys.dont_write_bytecode = True
import os
import pandas as pd
import flet as ft
#import simpledt
from simpledt import DataFrame
#import plotly.express as px
#from flet.plotly_chart import PlotlyChart
#import glob
#import Resultview2
import sqlite3
from tinydb import TinyDB
from sqlalchemy import create_engine

class View_saved(ft.Column):
    def __init__(self):
        super().__init__()
        self.title = "VFM算定結果リスト(結果要約を長めにクリックすると詳細に遷移します)"
        self.width = 1800
        self.height = 3000
        self.resizable = True

        engine = create_engine('sqlite:///VFM.db', echo=False, connect_args={'check_same_thread': False})
        self.engine_m = create_engine('sqlite:///sel_res.db', echo=False, connect_args={'check_same_thread': False})
        #conn = sqlite3.connect("":memory:")
        #c = conn.cursor()
        
        res_summ_df = pd.read_sql_table('res_summ_res_table', engine)
        #res_summ_df = c.sql('select * from res_summ_df_res_table').df()
        grd_df_exp = res_summ_df.groupby('datetime').apply(lambda x: x.head(1), include_groups=False)
        grd_df_exp_ri = grd_df_exp.reset_index().drop('level_1', axis=1)
        grd_df_exp_ri_r = grd_df_exp_ri.sort_values('datetime', ascending=False)
        grd_df_exp_ri2 = grd_df_exp_ri_r[[
            'datetime',
            'VFM_percent',
            'PSC_present_value',
            'LCC_present_value',
            'PIRR',
            'kariire_kinri',
            'discount_rate',
            'SPC_payment_cash',
            'mgmt_type',
            'proj_ctgry',
            'proj_type',
            'proj_years',
            'const_years'
            ]]
        
        self.res_summ_list = grd_df_exp_ri2.rename(
                index={0: 0},
            )

    # 以下のメソッドは、選択された日時を、次の画面に渡すためのメソッド。
    # ListViewのセルを選択したときに呼び出される。
    # 選択された日時を、SQLiteのテーブルsel_resに書き込んで、次の画面に渡す。
    def send_mess(self, e):
        dtime = e.control.data
        #print(dtime)
        dtime_dic = {'selected_datetime': str(dtime)}
        dtime_df = pd.DataFrame(dtime_dic, index=[0])
        dtime_df.to_sql('sel_res', self.engine_m, if_exists='replace', index=False)
        #page.session.set("selected_datetime", str(dtime))
        self.page.go("/results_detail")

    def build(self):
        summ_lv = ft.ListView(
            expand=True,
            spacing=10,
            #padding=5,
            auto_scroll=True,
            item_extent=1500,
            first_item_prototype=False,
            horizontal=False,
        )

        for row in self.res_summ_list.itertuples():
            row_dic = row._asdict()
            row = pd.DataFrame(row_dic, index=[0])
            dtime = row['datetime'].iloc[0]
            row['discount_rate'] = row['discount_rate'] * 100
            row = row.rename(
                columns={
                    "datetime": "算定日時",
                    "VFM_percent": "VFM(%)",
                    "PSC_present_value": "PSC現在価値総額",
                    "LCC_present_value": "LCC現在価値総額",
                    "PIRR": "プロジェクトの内部収益率(%)",
                    "kariire_kinri": "借入コスト(%)",
                    "discount_rate": "割引率(%)",
                    "SPC_payment_cash":"SPCのキャッシュ水準",
                    "mgmt_type": "施設管理者種別",
                    "proj_ctgry": "事業類型",
                    "proj_type": "事業方式",
                    "proj_years": "事業期間",
                    "const_years": "施設整備期間",
                },
            )
            row = row.T.reset_index()
            row = row.rename(columns={"index":"項目名", 0:"値"}).drop(0, axis=0)
            df = DataFrame(row)
            dr = df.datarows
            for i in dr:
                i.data = dtime                
                #i.color=ft.Colors.AMBER_50
                i.selected=False
                #page = ft.Page
                i.on_long_press=self.send_mess
                i.on_select_changed=self.send_mess

            #df_t  = df.tranpose().reset_index()
            table = df.datatable
            # ここで、DTに修飾を追加する。チェックボックス、色、テキストスタイル
            table.width=500
            table.show_checkbox_column=False
            #table.checkbox_column_width=15
            #table.checkbox_horizontal_margin=10
            table.on_select_all=True
            
            summ_lv.controls.append(table)
            summ_lv.controls.append(ft.Divider())

        return ft.Container(
                content=ft.Column(
                    controls=[
                        summ_lv,
                    ],
                    alignment=ft.MainAxisAlignment.START,
                    horizontal_alignment=ft.CrossAxisAlignment.START,
                ),
                width=800,
                height=3000,
                padding=5,
        )
        

