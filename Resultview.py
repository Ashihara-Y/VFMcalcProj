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
        self.width = 800
        self.height = 800
        self.resizable = True

    def build(self):

        self.b = ft.ElevatedButton(text="結果表示", on_click=self.button_clicked)
        return ft.Column([self.b ], scroll=ft.ScrollMode.ALWAYS)
    
#class VFM:
    def button_clicked(self,e):
        #to ft.datatable
        simpledt_df = DataFrame(self.results['df_PV_cf'])
        simpledt_dt = simpledt_df.datatable
        ft.page.add(simpledt_dt)

        #to Plotly_chart
        df_PV_cf = self.results['df_PV_cf']
        fig = px.bar(df_PV_cf, x=df_PV_cf.index, y=['PSC_present_value', 'LCC_present_value'], barmode='group')
        ft.page.add(PlotlyChart(fig, expand=True))
        
        