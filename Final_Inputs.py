import flet as ft
import joblib
import pandas as pd

class Final_Inputs(ft.UserControl):

    initial_inputs = joblib.load('Initial_Inputs.pkl')

    def __init__(self):
        super().__init__()
        self.title = "最終入力"
        self.width = 500
        self.height = 500
        self.resizable = False

    def build(self):
        #self.tx1 = ft.Text(f'管理者の種別：{self.initial_inputs['mgmt_type']}')
        #self.tx2 = ft.Text(f'事業の方式：{self.initial_inputs['proj_ctgry']}')
        #self.tx3 = ft.Text(f'事業の類型：{self.initial_inputs['proj_type']}')

        self.tx4 = ft.Text('事業期間') 
        self.sl1 = ft.Slider(
            value=int(self.initial_inputs['proj_years']),
            min=10, max=30, divisions=1, label="{value}年"
        )
        self.tx5 = ft.Text('施設整備期間')
        self.sl2 = ft.Slider(
            value=int(self.initial_inputs['const_years']),
            min=1, max=3, divisions=1, label="{value}年"
        )
        self.tx6 = ft.Text('施設整備費')
        self.sl3 = ft.Slider(
            value=float(self.initial_inputs['shisetsu_seibi']),
            min=100, max=99999, divisions=10, label="{value}百万円"
        )
        self.tx7 = ft.Text('維持管理運営費')
        self.sl4 = ft.Slider(
            value=float(self.initial_inputs['ijikanri_unnei']),
            min=0, max=999, divisions=5, label="{value}百万円",
        )
        self.tx8 = ft.Text('施設整備費の削減率')
        self.sl5 = ft.Slider(
            value=float(self.initial_inputs['reduc_shisetsu']),
            min=85, max=95, divisions=5, label="{value}%"
        )
        self.tx9 = ft.Text('維持管理運営費の削減率')
        self.sl6 = ft.Slider(
            value=float(self.initial_inputs['reduc_ijikanri']),
            min=85, max=95, divisions=5, label="{value}%"
        )
        self.tx10 = ft.Text('起債充当率')
        self.sl7 = ft.Slider(
            value=float(self.initial_inputs['kisai_jutou']),
            min=0, max=100, divisions=5, label="{value}%"
        )
        self.tx11 = ft.Text('起債への交付金カバー率')
        self.sl8 = ft.Slider(
            value=float(self.initial_inputs['kisai_koufu']),
            min=0, max=50, divisions=10, label="{value}%"
        )
        self.tx12 = ft.Text('補助率')
        self.sl9 = ft.Slider(
            value=float(self.initial_inputs['hojo']),
            min=0, max=60, divisions=1, label="{value}%"
        )
        self.tx13 = ft.Text('SPC経費年額')
        self.sl10 = ft.Slider(
            value=float(self.initial_inputs['SPC_keihi']),
            min=0, max=15, divisions=1, label="{value}百万円"
        )
        self.b = ft.ElevatedButton(text="確認", on_click=self.button_clicked)
        return ft.Column([#self.tx1, self.tx2, self.tx3, 
                          self.tx4, self.sl1, 
                          self.tx5, self.sl2, 
                          self.tx6, self.sl3, 
                          self.tx7, self.sl4, 
                          self.tx8, self.sl5, 
                          self.tx9, self.sl6, 
                          self.tx10, self.sl7, 
                          self.tx11, self.sl8, 
                          self.tx12, self.sl9, 
                          self.tx13, self.sl10,
                          self.b], scroll=ft.ScrollMode.ALWAYS)

#def main(page: ft.Page):
    
    def button_clicked(self, e):        

        final_inputs = {
            "mgmt_type":self.initial_inputs['mgmt_type'], 
            "proj_ctgry":self.initial_inputs['proj_ctgry'],
            "proj_type":self.initial_inputs['proj_type'],
            "proj_years":self.sl1.value,
            "const_years":self.sl2.value,
            "kijun_kinri":self.initial_inputs['kijun_kinri'],
            "chisai_kinri":self.initial_inputs['chisai_kinri'],
            "zei_modori":self.initial_inputs['zei_modori'],
            "lg_spread":self.initial_inputs['lg_spread'],
            "zei_total":self.initial_inputs['zei_total'],
            "growth":self.initial_inputs['growth'],
            "kitai_bukka":self.initial_inputs['kitai_bukka'],
            "shisetsu_seibi":self.sl3.value,
            "ijikanri_unnei":self.sl4.value,
            "reduc_shisetsu":self.sl5.value,
            "reduc_ijikanri":self.sl6.value,
            "pre_kyoukouka":self.initial_inputs['pre_kyoukouka'],
            "kisai_jutou":self.sl7.value,
            "kisai_koufu":self.sl8.value,
            "zeimae_rieki":self.initial_inputs['zeimae_rieki'],
            "SPC_keihi":self.sl10.value,
            "hojo":self.sl9.value
            }
        
        joblib.dump(final_inputs, 'Final_Inputs.pkl')
        #ft.page.client_storage.set("Final_Inputs", final_inputs)
        #ft.page.save_state(final_inputs)