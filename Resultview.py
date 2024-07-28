import sys
sys.dont_write_bytecode = True
import kaleido
import pandas as pd
import flet as ft
from simpledt import DataFrame
import plotly.express as px
from flet.plotly_chart import PlotlyChart
import tinydb
from tinydb import TinyDB, Query
import glob
import openpyxl


# savedir = pathlib.Path(mkdtemp(prefix=None, suffix=None, dir='.')) # 一時ディレクトリを作成
class Results(ft.Stack):
    def __init__(self):
        super().__init__()
        self.title = "結果 要約"
        self.width = 1800
        self.height = 1000
        self.resizable = True

        con = TinyDB("selected_res.json")
        self.dtime = con.all()[0]['selected_datetime']
        con.close()
        con2 = TinyDB("res_02_db.json")
        items = Query()
        self.selected_results_dict = con2.search(items.datetime == self.dtime)[0]
        con2.close()
        #self.res_PSC_LCC = pd.read_sql_query("SELECT * FROM res_PSC_LCC", con)
        #self.final_inputs = pd.read_sql_query("SELECT * FROM final_inputs", con)


    def build(self):
        PSC_PV_dict = self.selected_results_dict['PSC_present_value']
        LCC_PV_dict = self.selected_results_dict['LCC_present_value']
        PSC_LCC_PV_df = pd.DataFrame([PSC_PV_dict, LCC_PV_dict], index=['PSC現在価値','LCC現在価値'])
        PSC_LCC_PV_df_t = PSC_LCC_PV_df.transpose()
        df_col = PSC_LCC_PV_df.columns.to_list()
        #period = [int(f)+1 for f in df_col]
        self.fig = px.bar(
            PSC_LCC_PV_df_t,
            x=PSC_LCC_PV_df.columns,
            y=PSC_LCC_PV_df.index,
            #color=PSC_LCC_PV_df.columns,
            barmode="group",
        )    
        self.graph = PlotlyChart(self.fig, expand=True)

        # to ft.datatable
        simpledt_df = DataFrame(PSC_LCC_PV_df)
        simpledt_dt = simpledt_df.datatable
        self.table = simpledt_dt

        lv = ft.ListView(
            expand=True, spacing=10, padding=10, auto_scroll=True, horizontal=True
        )
        lv.controls.append(self.table)

        #PSC = round(float(self.results["PSC"]), 3)
        #LCC = round(float(self.results["LCC"]), 3)
        #VFM = round(float(self.results["VFM"]), 3)
        #VFM_percent = self.results["VFM_percent"]
        #self.tx_PSC = ft.Text("PSC(百万円): ", style=ft.TextThemeStyle.HEADLINE_SMALL)
        #self.v_PSC = ft.Text(PSC, style=ft.TextThemeStyle.HEADLINE_SMALL)
        #self.tx_LCC = ft.Text("LCC(百万円): ", style=ft.TextThemeStyle.HEADLINE_SMALL)
        #self.v_LCC = ft.Text(LCC, style=ft.TextThemeStyle.HEADLINE_SMALL)
        #self.tx_VFM = ft.Text("VFM(百万円): ", style=ft.TextThemeStyle.HEADLINE_SMALL)
        #self.v_VFM = ft.Text(VFM, style=ft.TextThemeStyle.HEADLINE_SMALL)
        #self.tx_VFM_percent = ft.Text(
        #    "VFM(%): ", style=ft.TextThemeStyle.HEADLINE_SMALL
        #)
        #self.v_VFM_percent = ft.Text(
        #    VFM_percent, style=ft.TextThemeStyle.HEADLINE_SMALL
        #)

        return ft.Card(
            content=ft.Container(
                content=ft.Column(
                    controls=[
                        #ft.Column(
                        #    [
                        #        ft.Row(
                        #            [self.tx_PSC, self.v_PSC],
                        #            alignment=ft.MainAxisAlignment.START,
                        #        ),
                        #        ft.Row(
                        #            [self.tx_LCC, self.v_LCC],
                        #            alignment=ft.MainAxisAlignment.START,
                        #        ),
                        #        ft.Row(
                        #            [self.tx_VFM, self.v_VFM],
                        #            alignment=ft.MainAxisAlignment.START,
                        #        ),
                        #        ft.Row(
                        #            [self.tx_VFM_percent, self.v_VFM_percent],
                        #            alignment=ft.MainAxisAlignment.START,
                        #        ),
                        #    ]
                        #),
                        self.graph,
                        lv,
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_AROUND,
                ),
                # content=lv,
                width=1800,
                padding=10,
            )
        )
    def export_to_excel():
        wb = openpyxl.load_workbook('VFM_result_sheet.xlsx')
        ws = wb.active
        ws.append(['PSC', 'LCC', 'VFM', 'VFM_percent'])

