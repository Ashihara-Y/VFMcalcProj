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
        self.b2 = ft.ElevatedButton(text="結果表示2", on_click=self.view_make)
        return ft.Column([self.b, self.b2], scroll=ft.ScrollMode.ALWAYS)
    
    
#class VFM:
    def button_clicked(self,e):
        #to Plotly_chart
        df_PV_cf = self.results['df_PV_cf']
        fig = px.bar(df_PV_cf, x=df_PV_cf.index, y=['PSC_present_value', 'LCC_present_value'], barmode='group')
        #ft.Page.page.add(PlotlyChart(self.fig, expand=True)) 
        return fig
    
    def view_make(self, e, page: ft.Page):
        self.self.fig = self.button_clicked(self)
        #page.add(self.simpledt_dt)
        page.add(PlotlyChart(self.fig, expand=True))
        page.update()
        