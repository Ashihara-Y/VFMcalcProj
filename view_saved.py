import sys
sys.dont_write_bytecode = True
import os
import pandas as pd
import flet as ft
import simpledt
from simpledt import DataFrame
#import plotly.express as px
from flet.plotly_chart import PlotlyChart
#import glob
import Resultview
import duckdb
from tinydb import TinyDB


class View_saved(ft.Column):
    def __init__(self):
        super().__init__()
        self.title = "VFM算定結果リスト"
        self.width = 1800
        self.height = 3000
        self.resizable = True

        conn = duckdb.connect('VFM.duckdb')
        c = conn.cursor()
        
        res_summ_df = c.sql('select * from res_summ_df_res_table').df()
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
                index={0: "項目"},
            )

    # 以下のメソッドは、選択された日時を、次の画面に渡すためのメソッド。
    # ListViewのセルを選択したときに呼び出される。
    # 選択された日時を、selected_res.jsonに書き込む。次の画面に渡す。
    # session storageに書き込む形も併設しておいた。
    def send_mess(self, e):
        #ft.Page.pubsub.send_all(Message)
        if os.path.exists("selected_res.json"):
            os.remove("selected_res.json")
        con = TinyDB('selected_res.json')
        con.truncate()
        dtime = e.control.data
        dtime_dic = {'selected_datetime': str(dtime)}
        con.insert(dtime_dic)
        con.close()
        self.page.session.set(list(dtime_dic)[0], dtime)
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
            row = pd.DataFrame(row).drop(0, axis=0)
            df = DataFrame(row)
            dr = df.datarows
            dtime = dr[0].cells[0].content.value
            dr[0].data = dtime
            for i in dr:
                i.data = dtime                
                i.color=ft.Colors.AMBER_50
                i.selected=False
                i.on_long_press=self.send_mess
                i.on_select_changed=self.send_mess

            table = df.datatable
            # ここで、DTに修飾を追加する。チェックボックス、色、テキストスタイル
            table.width=1500
            table.show_checkbox_column=True
            table.checkbox_column_width=15
            table.checkbox_horizontal_margin=10
            table.on_select_all=True
            
            summ_lv.controls.append(table)
            summ_lv.controls.append(ft.Divider())

        return ft.Container(
                content=ft.Column(
                    controls=[
                        summ_lv,
                    ],
                    alignment=ft.MainAxisAlignment.START,
                    horizontal_alignment=ft.CrossAxisAlignment.END,
                ),
                width=1800,
                height=3000,
                padding=5,
        )
        

