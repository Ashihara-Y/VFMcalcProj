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


# savedir = pathlib.Path(mkdtemp(prefix=None, suffix=None, dir='.')) # 一時ディレクトリを作成
class Results(ft.Stack):
    def __init__(self):
        super().__init__()
        self.title = "結果 詳細"
        self.width = 1800
        self.height = 1000
        self.resizable = True

        con = TinyDB("selected_res.json")
        self.dtime = con.all()[0]['selected_datetime']
        con.close()

        conn = duckdb.connect('VFM.duckdb')
        c = conn.cursor()
        
        # DuckDbの各「算定結果テーブル」から、上記のself.dtimeと同じdatetimeを持つレコードを抽出する。
        # 
        # 
        # 
        # 
        # 
        # 


    def build(self):
        # ここで、各結果・IDを格納したテーブルから、該当Datetimeのものを抽出して、DFに格納する。
        PSC_PV_dict = self.selected_results_dict['PSC_present_value']
        LCC_PV_dict = self.selected_results_dict['LCC_present_value']
        PSC_LCC_PV_df = pd.DataFrame([PSC_PV_dict, LCC_PV_dict], index=['PSC現在価値','LCC現在価値'])
        PSC_LCC_PV_df_t = PSC_LCC_PV_df.transpose()
        df_col = PSC_LCC_PV_df.columns.to_list()
        #period = [int(f)+1 for f in df_col]

        # 以下は、「総括表」にする。
        self.fig = px.bar(
            PSC_LCC_PV_df_t,
            x=PSC_LCC_PV_df.columns,
            y=PSC_LCC_PV_df.index,
            #color=PSC_LCC_PV_df.columns,
            barmode="group",
        )    

        # Plotlyを使わないグラフに切り替える。
        self.graph = PlotlyChart(self.fig, expand=True)

        # 総括表をここに追加する。PSC,LCC、SPCの表も作成して、別個定義しておく。
        simpledt_df = DataFrame(PSC_LCC_PV_df)
        simpledt_dt = simpledt_df.datatable
        self.table = simpledt_dt

        lv = ft.ListView(
            expand=True, spacing=10, padding=10, auto_scroll=True, horizontal=True
        )
        lv.controls.append(self.table)

        # ここでタブを定義できないか？各タブに、各Cardを配置する形で実装できないか？

        return ft.tabs(
                selected_index=1,
                animation_duration=300,
                tabs=[
                    ft.Tab(
                        text="結果・入力の要約",
                        content=ft.Card(
                            content=ft.Container(
                                content=ft.Column(
                                    controls=[
                                        self.graph,
                                        lv,
                                    ],
                                    alignment=ft.MainAxisAlignment.SPACE_AROUND,
                                ),
                                width=1800,
                                padding=10,
                            )
                        ),
                    ),
                    ft.Tab(
                        text="Tab 2",
                        icon=ft.Icons.BOOK,
                        content=ft.Text("This is Tab 2"),
                    ),
                    ft.Tab(
                        text="Tab 3",
                        icon=ft.Icons.SETTINGS,
                        content=ft.Text("This is Tab 3"),
                    ),
                ],
            )
 
    def export_to_excel():
        wb = openpyxl.load_workbook('VFM_result_sheet.xlsx')
        ws = wb.active
        ws.append(['PSC', 'LCC', 'VFM', 'VFM_percent'])

