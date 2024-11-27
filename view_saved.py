import sys
sys.dont_write_bytecode = True
import os
import pandas as pd
import flet as ft
import simpledt
from simpledt import DataFrame
import plotly.express as px
from flet.plotly_chart import PlotlyChart
import glob
import Resultview
import tinydb
from tinydb import TinyDB, Query



class View_saved(ft.Column):
    def __init__(self):
        super().__init__()
        self.title = "VFM算定結果リスト"
        self.width = 1800
        self.height = 1800
        self.resizable = True

        # 以下を、DBからの読み込みに切り替えるとして、どのテーブルを読み込むか？
        # ここでは、「全結果のリスト」を作成している。
        save_res_01_list = glob.glob("res_01_db_*.json")
        save_res_01_list.sort(reverse=True)
        
        self.res_summ_list = []

        # 詳細結果は、ファイル読み込みではなく、DB各テーブルの内容そのものに切り替える必要。
        # なので、Datetimeで必要なテーブルから各結果を抽出して、要約用のDFを作成する必要。
        # それとも、「aave_results.py」の最後で、要約用DFを作成して、DuckDBに入れておいた
        # 方が早いのでは？ 少なくともDatetime、UserID、CalcIDを挿入する段階なら、作成
        # できるはず。
        for file in save_res_01_list:        
            con = TinyDB(file)
            res_detail = con.all()[0]
            con.close()
            res_detail_df = pd.DataFrame(data=res_detail, index=[0])
            
            # DBの各テーブルからの読み込み結果から、以下のカラムのDFを作成する。
            res_summary = res_detail_df.reindex(
                columns=[
                    "datetime",
                    "VFM_percent",
                    "PSC_pv",
                    "LCC_pv",
                    "P-IRR",
                    "mgmt_type",
                    "proj_ctgry",
                    "proj_type",
                    "proj_years",
                    "const_years",
                    "discount_rate",
                ]
            )
            res_summary = res_summary.rename(
                columns={
                    "datetime": "作成日時",
                    "VFM_percent": "VFM(%)",
                    "PSC_pv": "PSC現在価値総額",
                    "LCC_pv": "LCC現在価値総額",
                    "P-IRR": "プロジェクトの内部収益率"
                    "mgmt_type": "施設管理者種別",
                    "proj_ctgry": "事業類型",
                    "proj_type": "事業方式",
                    "proj_years": "事業期間",
                    "const_years": "施設整備期間",
                    "discount_rate": "割引率",
                },
                index={0: "項目"},
            )
            self.res_summ_list.append(res_summary)

    def send_mess(self, e):
        #ft.Page.pubsub.send_all(Message)
        if os.path.exists("selected_res.json"):
            os.remove("selected_res.json")
        con = TinyDB('selected_res.json')
        con.truncate()
        #dtime = e.control.cells[0].content.value
        dtime = e.control.data
        #print(dtime)
        dtime_dic = {'selected_datetime': str(dtime)}
        con.insert(dtime_dic)
        con.close()
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

        for df in self.res_summ_list:
            #self.dtime = str(df['作成日時'].iloc[0])
            df = DataFrame(df)
            dr = df.datarows
            for i in dr:
                dtime = i.cells[0].content.value
                i.data = dtime
                i.color=ft.colors.AMBER_50
                i.selected=False
                #message = {'selected_datetime': dtime}
                i.on_long_press=self.send_mess
                i.on_selectd_changed=self.send_mess
            table = df.datatable
            # ここで、DTに修飾を追加する。チェックボックス、色、テキストスタイル
            table.width=1500
            #table.bg_color=ft.colors.AMBER_50
            table.show_checkbox_column=True
            table.checkbox_column_width=100
            table.checkbox_horizontal_margin=10
            table.on_select_all=True
            
            summ_lv.controls.append(table)
            summ_lv.controls.append(ft.Divider())

        return ft.Container(
                #content=sum_col,
                content=ft.Column(
                    controls=[
                        summ_lv,
                    ],
                    alignment=ft.MainAxisAlignment.START,
                    horizontal_alignment=ft.CrossAxisAlignment.END,
                ),
                width=1800,
                height=1800,
                padding=5,
        )
        

