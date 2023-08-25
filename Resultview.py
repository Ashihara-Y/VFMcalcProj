import sys

sys.dont_write_bytecode = True
import pandas as pd
import flet as ft
import joblib
from simpledt import DataFrame
import plotly.express as px
from flet.plotly_chart import PlotlyChart


# savedir = pathlib.Path(mkdtemp(prefix=None, suffix=None, dir='.')) # 一時ディレクトリを作成
class Results(ft.UserControl):
    def __init__(self):
        super().__init__()
        self.title = "結果"
        self.width = 1000
        self.height = 800
        self.resizable = True

        # self.final=inputs = joblib.load('final_inputs.joblib')
        self.results = joblib.load("results.joblib")

    def build(self):
        # self.b = ft.ElevatedButton(text="結果表示", on_click=self.button_clicked)
        # self.b2 = ft.ElevatedButton(text="結果表示2", on_click=self.view_make)
        df_PV_cf = self.results["df_PV_cf"].round(3)
        self.fig = px.bar(
            df_PV_cf,
            x=df_PV_cf.index,
            y=["PSC_present_value", "LCC_present_value"],
            barmode="group",
        )
        self.graph = PlotlyChart(self.fig, expand=True)

        # to ft.datatable
        simpledt_df = DataFrame(df_PV_cf.transpose())
        simpledt_dt = simpledt_df.datatable
        self.table = simpledt_dt

        lv = ft.ListView(
            expand=1, spacing=10, padding=20, auto_scroll=True, horizontal=True
        )
        lv.controls.append(self.table)

        PSC = round(float(self.results["PSC"]), 3)
        LCC = round(float(self.results["LCC"]), 3)
        VFM = round(float(self.results["VFM"]), 3)
        VFM_percent = self.results["VFM_percent"]
        self.tx_PSC = ft.Text("PSC(百万円): ", style=ft.TextThemeStyle.HEADLINE_SMALL)
        self.v_PSC = ft.Text(PSC, style=ft.TextThemeStyle.HEADLINE_SMALL)
        self.tx_LCC = ft.Text("LCC(百万円): ", style=ft.TextThemeStyle.HEADLINE_SMALL)
        self.v_LCC = ft.Text(LCC, style=ft.TextThemeStyle.HEADLINE_SMALL)
        self.tx_VFM = ft.Text("VFM(百万円): ", style=ft.TextThemeStyle.HEADLINE_SMALL)
        self.v_VFM = ft.Text(VFM, style=ft.TextThemeStyle.HEADLINE_SMALL)
        self.tx_VFM_percent = ft.Text(
            "VFM(%): ", style=ft.TextThemeStyle.HEADLINE_SMALL
        )
        self.v_VFM_percent = ft.Text(
            VFM_percent, style=ft.TextThemeStyle.HEADLINE_SMALL
        )

        return ft.Card(
            content=ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Column(
                            [
                                ft.Row(
                                    [self.tx_PSC, self.v_PSC],
                                    alignment=ft.MainAxisAlignment.START,
                                ),
                                ft.Row(
                                    [self.tx_LCC, self.v_LCC],
                                    alignment=ft.MainAxisAlignment.START,
                                ),
                                ft.Row(
                                    [self.tx_VFM, self.v_VFM],
                                    alignment=ft.MainAxisAlignment.START,
                                ),
                                ft.Row(
                                    [self.tx_VFM_percent, self.v_VFM_percent],
                                    alignment=ft.MainAxisAlignment.START,
                                ),
                            ]
                        ),
                        self.graph,
                        lv,
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_AROUND,
                ),
                # content=lv,
                width=1000,
                padding=16,
            )
        )
