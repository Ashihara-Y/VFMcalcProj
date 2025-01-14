import sys
sys.dont_write_bytecode = True
import pandas as pd
import flet as ft
from simpledt import DataFrame
import plotly.express as px
from flet.plotly_chart import PlotlyChart
import duckdb
from tinydb import TinyDB, Query
#import glob
import openpyxl
#from openpyxl import Workbook, load_workbook
import sqlite3
from sqlalchemy import create_engine


# savedir = pathlib.Path(mkdtemp(prefix=None, suffix=None, dir='.')) # 一時ディレクトリを作成
class Results(ft.Stack):
    def __init__(self):
        super().__init__()
        self.title = "結果 詳細"
        self.width = 2100
        self.height = 1000
        self.resizable = True

        con = TinyDB("selected_res.json")
        #self.dtime = page.session.get('selected_datetime')
        self.dtime = con.all()[0]['selected_datetime']
        con.close()

        #conn = sqlite3.connect('VFM.duckdb')
        #c = conn.cursor()

        engine = create_engine('sqlite:///VFM.db', echo=False, connect_args={'check_same_thread': False})
        
        table_names = [
            'PSC_res_table', 
            'PSC_pv_res_table', 
            'LCC_res_table', 
            'LCC_pv_res_table', 
            'SPC_res_table', 
            'SPC_check_res_table',
            'Risk_res_table',
            'VFM_res_table',
            'PIRR_res_table',
            'res_summ_res_table',
        ]
        self.selected_res_list = []
        for table_name in table_names:
            query = 'select * from ' + table_name + ' where datetime = ' + '"' + self.dtime + '"'
            table_name = pd.read_sql_query(query, engine)
            self.selected_res_list.append(table_name)

    def build(self):
        # ここで、各結果・IDを格納したテーブルから、該当Datetimeのものを抽出して、DFに格納する。
        PSC_res_df = self.selected_res_list[0]
        PSC_pv_df = self.selected_res_list[1]
        LCC_res_df = self.selected_res_list[2]
        LCC_pv_df = self.selected_res_list[3]
        SPC_res_df = self.selected_res_list[4]
        SPC_check_df = self.selected_res_list[5]
        Risk_res_df = self.selected_res_list[6]
        VFM_res_df = self.selected_res_list[7]
        PIRR_res_df = self.selected_res_list[8]
        res_summ_df = self.selected_res_list[9]

        # 総括表をここに追加する。PSC,LCC、SPCの表も作成して、別個定義しておく。
        simpledt_PSC_df = DataFrame(PSC_res_df)
        simpledt_PSC_dt = simpledt_PSC_df.datatable
        self.table_PSC = simpledt_PSC_dt
        simpledt_PSC_pv_df = DataFrame(PSC_pv_df)
        simpledt_PSC_pv_dt = simpledt_PSC_pv_df.datatable
        self.table_PSC_pv = simpledt_PSC_pv_dt

        simpledt_LCC_df = DataFrame(LCC_res_df)
        simpledt_LCC_dt = simpledt_LCC_df.datatable
        self.table_LCC = simpledt_LCC_dt
        simpledt_LCC_pv_df = DataFrame(LCC_pv_df)
        simpledt_LCC_pv_dt = simpledt_LCC_pv_df.datatable
        self.table_LCC_pv = simpledt_LCC_pv_dt

        simpledt_SPC_df = DataFrame(SPC_res_df)
        simpledt_SPC_dt = simpledt_SPC_df.datatable
        self.table_SPC = simpledt_SPC_dt
        simpledt_SPC_check_df = DataFrame(SPC_check_df)
        simpledt_SPC_check_dt = simpledt_SPC_check_df.datatable
        self.table_SPC_check = simpledt_SPC_check_dt

        simpledt_Risk_df = DataFrame(Risk_res_df)
        simpledt_Risk_dt = simpledt_Risk_df.datatable
        self.table_Risk = simpledt_Risk_dt

        simpledt_VFM_df = DataFrame(VFM_res_df)
        simpledt_VFM_dt = simpledt_VFM_df.datatable
        self.table_VFM = simpledt_VFM_dt
        simpledt_PIRR_df = DataFrame(PIRR_res_df)
        simpledt_PIRR_dt = simpledt_PIRR_df.datatable
        self.table_PIRR = simpledt_PIRR_dt

        res_summ_df_t = res_summ_df.transpose().reset_index()
        simpledt_res_summ_df = DataFrame(res_summ_df_t)
        simpledt_res_summ_dt = simpledt_res_summ_df.datatable
        self.table_res_summ = simpledt_res_summ_dt

        lv_01 = ft.ListView(
            expand=True, spacing=10, padding=10, auto_scroll=True, horizontal=False
        )
        lv_01.controls.append(ft.Text('算定結果要約'))
        lv_01.controls.append(self.table_res_summ)
        lv_01.controls.append(ft.Divider())
        lv_01.controls.append(ft.Text('VFM結果'))
        lv_01.controls.append(self.table_VFM)
        lv_01.controls.append(ft.Divider())
        lv_01.controls.append(ft.Text('PIRR結果'))
        lv_01.controls.append(self.table_PIRR)

        lv_02 = ft.ListView(
            expand=True, spacing=10, padding=10, auto_scroll=True, horizontal=False
        )
        lv_02.controls.append(ft.Text('PSCでの公共側収支'))
        lv_02.controls.append(self.table_PSC)
        lv_02.controls.append(ft.Divider())
        lv_02.controls.append(ft.Text('PSCでの公共側キャッシュ・フローとその現在価値'))
        lv_02.controls.append(self.table_PSC_pv)
        lv_02.controls.append(ft.Divider())
        lv_02.controls.append(ft.Text('PFI-LCCでの公共側収支'))
        lv_02.controls.append(self.table_LCC)
        lv_02.controls.append(ft.Divider())
        lv_02.controls.append(ft.Text('PFI-LCCでの公共側キャッシュ・フローとその現在価値'))
        lv_02.controls.append(self.table_LCC_pv)
        lv_02.controls.append(ft.Divider())
        lv_02.controls.append(ft.Text('PSCへのリスク調整'))
        lv_02.controls.append(self.table_Risk)

        lv_03 = ft.ListView(
            expand=True, spacing=10, padding=10, auto_scroll=True, horizontal=False
        )
        lv_03.controls.append(ft.Text('PFI-LCCでのSPC側収支'))
        lv_03.controls.append(self.table_SPC)
        lv_03.controls.append(ft.Divider())
        lv_03.controls.append(ft.Text('PFI-LCCでのSPCの返済資金確認結果'))
        lv_03.controls.append(self.table_SPC_check)


        return ft.Tabs(
                selected_index=1,
                animation_duration=300,
                tabs=[
                    ft.Tab(
                        text="結果・入力の要約",
                        content=ft.Card(
                            content=ft.Container(
                                content=ft.Column(
                                    controls=[
                                        #self.graph,
                                        lv_01,
                                    ],
                                    alignment=ft.MainAxisAlignment.SPACE_AROUND,
                                ),
                                width=2100,
                                padding=10,
                            )
                        ),
                    ),
                    ft.Tab(
                        text="PSC,LCCでの公共側収支等",
                        content=ft.Card(
                            content=ft.Container(
                                content=ft.Column(
                                    controls=[
                                        #self.graph,
                                        lv_02,
                                    ],
                                    alignment=ft.MainAxisAlignment.SPACE_AROUND,
                                ),
                                width=2100,
                                padding=10,
                            )
                        )
                    ),
                    ft.Tab(
                        text="SPC収支等",
                        content=ft.Card(
                            content=ft.Container(
                                content=ft.Column(
                                    controls=[
                                        #self.graph,
                                        lv_03,
                                    ],
                                    alignment=ft.MainAxisAlignment.SPACE_AROUND,
                                ),
                                width=2100,
                                padding=10,
                            )
                        )
                    ),
                ],
            )
 
