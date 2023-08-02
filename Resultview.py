import sys
sys.dont_write_bytecode = True
import pandas as pd
import flet as ft
#import shelve as sv
import joblib
#from Final_Inputs import Final_Inputs
from simpledt import DataFrame
import plotly.express as px
from flet.plotly_chart import PlotlyChart

class Results(ft.UserControl):

    results = joblib.load('results.pkl')

    def __init__(self):
        super().__init__()
        self.title = "結果"
        self.width = 1000
        self.height = 800
        self.resizable = True

    def build(self):

        #self.b = ft.ElevatedButton(text="結果表示", on_click=self.button_clicked)
        #self.b2 = ft.ElevatedButton(text="結果表示2", on_click=self.view_make)
        df_PV_cf = self.results['df_PV_cf']
        self.fig = px.bar(df_PV_cf, x=df_PV_cf.index, y=['PSC_present_value', 'LCC_present_value'], barmode='group')
        self.graph = PlotlyChart(self.fig, expand=True)

        #to ft.datatable
        simpledt_df = DataFrame(df_PV_cf.transpose())
        simpledt_dt = simpledt_df.datatable
        self.table = simpledt_dt

        PSC = self.results['PSC']
        LCC = self.results['LCC']
        VFM = self.results['VFM']
        VFM_percent = self.results['VFM_percent']
        self.tx_PSC = ft.Text(PSC)
        self.tx_LCC = ft.Text(LCC)
        self.tx_VFM = ft.Text(VFM)
        self.tx_VFM_percent = ft.Text(VFM_percent)


        return ft.Card(
            content=ft.Container(
                content=ft.Column(
                    controls=[
                        self.tx_PSC, self.tx_LCC, self.tx_VFM, self.tx_VFM_percent,
                        self.graph,
                        self.table,
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_AROUND,
                ),
                width=1000,
                padding=16,
            )
        ) 
    
    

        