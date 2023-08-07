import sys
sys.dont_write_bytecode = True
import flet as ft
import joblib
import pandas as pd
#import tempfile
#import pathlib
import VFM_calc as vc
#savedir = pathlib.Path(tempfile.mkdtemp(dir='.')) # 一時ディレクトリを作成
#filename = savedir / 'final_inputs.joblib' # 一時ディレクトリにファイルを作成

class Final_Inputs(ft.UserControl):

    def __init__(self):
        super().__init__()
        self.title = "最終入力"
        self.width = 500
        self.height = 800
        self.resizable = True

        self.initial_inputs = joblib.load('initial_inputs.joblib') #Paheを指定する必要がある！Pathlibを使うか？

    def build(self):
        self.tx1 = ft.Text(str(self.initial_inputs['mgmt_type']))
        self.tx2 = ft.Text(str(self.initial_inputs['proj_ctgry']))
        self.tx3 = ft.Text(str(self.initial_inputs['proj_type']))
        self.tx4 = ft.Text(str(self.initial_inputs['proj_years']))
        self.tx5 = ft.Text(str(self.initial_inputs['const_years']))

        self.tx6 = ft.Text('施設整備費')
        self.sl3 = ft.Slider(
            value=float(self.initial_inputs['shisetsu_seibi']),
            min=100, max=100000, divisions=10000, label="{value}百万円"
        )
        self.tx7 = ft.Text('維持管理運営費')
        self.sl4 = ft.Slider(
            value=float(self.initial_inputs['ijikanri_unnei']),
            min=0, max=1000, divisions=1000, label="{value}百万円"
        )
        self.tx8 = ft.Text('施設整備費の削減率')
        self.sl5 = ft.Slider(
            value=float(self.initial_inputs['reduc_shisetsu']),
            min=85, max=95, divisions=10, label="{value}%"
        )
        self.tx9 = ft.Text('維持管理運営費の削減率')
        self.sl6 = ft.Slider(
            value=float(self.initial_inputs['reduc_ijikanri']),
            min=85, max=95, divisions=10, label="{value}%"
        )
        self.tx10 = ft.Text('起債充当率')
        self.sl7 = ft.Slider(
            value=float(self.initial_inputs['kisai_jutou']),
            min=0, max=100, divisions=100, label="{value}%"
        )
        self.tx11 = ft.Text('起債への交付金カバー率')
        self.sl8 = ft.Slider(
            value=float(self.initial_inputs['kisai_koufu']),
            min=0, max=50, divisions=50, label="{value}%"
        )
        self.tx12 = ft.Text('補助率')
        self.sl9 = ft.Slider(
            value=float(self.initial_inputs['hojo']),
            min=0, max=60, divisions=50, label="{value}%"
        )
        self.tx13 = ft.Text('SPC経費年額')
        self.sl10 = ft.Slider(
            value=float(self.initial_inputs['SPC_keihi']),
            min=0, max=15, divisions=15, label="{value}百万円"
        )
        self.b = ft.ElevatedButton(text="確認", on_click=self.button_clicked)
        return ft.Column([self.tx1, self.tx2, self.tx3, 
                          self.tx4,  
                          self.tx5, 
                          self.tx6, self.sl3, 
                          self.tx7, self.sl4, 
                          self.tx8, self.sl5, 
                          self.tx9, self.sl6, 
                          self.tx10, self.sl7, 
                          self.tx11, self.sl8, 
                          self.tx12, self.sl9, 
                          self.tx13, self.sl10,
                          self.b 
                        ], scroll=ft.ScrollMode.ALWAYS)

#def main(page: ft.Page):
    
    def button_clicked(self, e):        

        final_inputs = {
            "mgmt_type":self.initial_inputs['mgmt_type'], 
            "proj_ctgry":self.initial_inputs['proj_ctgry'],
            "proj_type":self.initial_inputs['proj_type'],
            "proj_years":int(self.initial_inputs['proj_years']),
            "const_years":int(self.initial_inputs['const_years']),
            "kijun_kinri":float(self.initial_inputs['kijun_kinri']),
            "chisai_kinri":float(self.initial_inputs['chisai_kinri']),
            "zei_modori":float(self.initial_inputs['zei_modori']),
            "lg_spread":float(self.initial_inputs['lg_spread']),
            "zei_total":float(self.initial_inputs['zei_total']),
            "growth":float(self.initial_inputs['growth']),
            "kitai_bukka":float(self.initial_inputs['kitai_bukka']),
            "shisetsu_seibi":float(self.sl3.value),
            "ijikanri_unnei":float(self.sl4.value),
            "reduc_shisetsu":float(self.sl5.value),
            "reduc_ijikanri":float(self.sl6.value),
            "pre_kyoukouka":bool(self.initial_inputs['pre_kyoukouka']),
            "kisai_jutou":float(self.sl7.value),
            "kisai_koufu":float(self.sl8.value),
            "zeimae_rieki":float(self.initial_inputs['zeimae_rieki']),
            "SPC_keihi":float(self.sl10.value),
            "hojo":float(self.sl9.value)
            }
        
        joblib.dump(final_inputs, 'final_inputs.joblib')
        #ft.page.client_storage.set("final_inputs", final_inputs)
        #ft.page.save_state(final_inputs)

        vc.calc_PSC_LCC()
        #shisetsu_seibi_total = float(final_inputs['shisetsu_seibi'])
        #ijikanri_unnei_total = float(final_inputs['ijikanri_unnei']) * (int(final_inputs['proj_years']) - int(final_inputs['const_years']))
        #hojokin_kan = shisetsu_seibi_total * (float(final_inputs['hojo'])/100)
        #if final_inputs['mgmt_type'] == '国':
        #    hojokin_kan = 0 
        #ribarai_kan = (shisetsu_seibi_total - hojokin_kan) * float(final_inputs['kisai_jutou'])/100 * (1 - float(final_inputs['kisai_koufu'])/100) * float(final_inputs['chisai_kinri'])
        #if final_inputs['mgmt_type'] == '国':
        #    ribarai_kan = 0
        #koufukin_kan = (shisetsu_seibi_total - hojokin_kan) * float(final_inputs['kisai_jutou'])/100 * float(final_inputs['kisai_koufu'])/100

        #shisetsu_seibi_reduc_total = shisetsu_seibi_total * (float(final_inputs['reduc_shisetsu'])/100)
        #ijikanri_unnei_reduc_total = ijikanri_unnei_total * (float(final_inputs['reduc_ijikanri'])/100)
        
        #SPC_capital = (shisetsu_seibi_reduc_total + ijikanri_unnei_reduc_total) * 0.1
        #SPC_yobihi = (shisetsu_seibi_reduc_total + ijikanri_unnei_reduc_total) * 0.1
        #SPC_keihi_total = float(final_inputs['SPC_keihi']) * int(final_inputs['proj_years'])
        #if SPC_keihi_total == 0:
        #    SPC_capital = SPC_yobihi = 0
        #hojokin_min = (shisetsu_seibi_reduc_total) *  (float(final_inputs['hojo'])/100)
        #ribarai_min = (((shisetsu_seibi_reduc_total - hojokin_min) * (1-float(final_inputs['kisai_jutou'])/100)) + (SPC_capital + SPC_yobihi)) * (float(final_inputs['kijun_kinri']) + float(final_inputs['lg_spread']))/100
        #ribarai_min_chisai = (shisetsu_seibi_reduc_total - hojokin_min) * (float(final_inputs['kisai_jutou'])/100) * (1 - float(final_inputs['kisai_koufu'])/100) * float(final_inputs['chisai_kinri'])
        #koufukin_min = (shisetsu_seibi_reduc_total - hojokin_min) * (float(final_inputs['kisai_jutou'])/100) * float(final_inputs['kisai_koufu'])/100
        
        #ribarai_kanmin_sa = ribarai_min - ribarai_kan
        
        #kappu_genka_s = (shisetsu_seibi_reduc_total + ijikanri_unnei_reduc_total + ribarai_min + SPC_capital + SPC_yobihi + SPC_keihi_total) / (1 - float(final_inputs['zeimae_rieki'])/100)
        #zeimae_rieki_gaku = kappu_genka_s * float(final_inputs['zeimae_rieki'])/100
        #nouzei_gaku = zeimae_rieki_gaku * float(final_inputs['zei_total'])/100
        #zeigo_rieki_gaku = zeimae_rieki_gaku - nouzei_gaku
        
        #zei_modori_gaku = zeimae_rieki_gaku * float(final_inputs['zei_modori'])/100
        
        #PSC_income_total = float(hojokin_kan + koufukin_kan)
        #PSC_expense_total = float(shisetsu_seibi_total + ijikanri_unnei_total + ribarai_kan + ribarai_kanmin_sa + SPC_capital + SPC_yobihi + SPC_keihi_total)
        #PSC_net_expense = float(PSC_expense_total - PSC_income_total)
        
        #LCC_income_total = float(hojokin_min + koufukin_min + zei_modori_gaku)
        #LCC_expense_total = float(shisetsu_seibi_reduc_total + ijikanri_unnei_reduc_total + ribarai_min + ribarai_min_chisai + zeimae_rieki_gaku + SPC_capital + SPC_yobihi + SPC_keihi_total)
        #LCC_net_expense = float(LCC_expense_total - LCC_income_total)

        #discount_rate = float(final_inputs['kijun_kinri']) + float(final_inputs['kitai_bukka'])

        #ijikanri_years = int(final_inputs['proj_years']) - int(final_inputs['const_years'])

        #rakusatsu_ritsu = 0.95

        #PSC_const_rate = shisetsu_seibi_total / (shisetsu_seibi_total + ijikanri_unnei_total)
        #PSC_ijikanri_rate = ijikanri_unnei_total / (shisetsu_seibi_total + ijikanri_unnei_total)

        #risk_adj_koufu = ribarai_kanmin_sa + SPC_capital + SPC_keihi_total + SPC_yobihi - koufukin_kan
        #risk_adj_koufu_const = risk_adj_koufu * PSC_const_rate
        #risk_adj_koufu_ijikanri = risk_adj_koufu * PSC_ijikanri_rate

        #PSC_net_expense_const_kk = (risk_adj_koufu_const + shisetsu_seibi_total + ribarai_kan - hojokin_kan) * rakusatsu_ritsu
        #PSC_net_expense_ijikanri_kk = (risk_adj_koufu_ijikanri + ijikanri_unnei_total) * rakusatsu_ritsu

        #res_PSC_LCC = {
        #    "LCC_net_expense": LCC_net_expense, 
        #    "PSC_net_expense_const_kk": PSC_net_expense_const_kk,
        #    "PSC_net_expense_ijikanri_kk": PSC_net_expense_ijikanri_kk,
        #    "proj_years":int(final_inputs['proj_years']),
        #    "const_years":int(final_inputs['const_years']),
        #    "ijikanri_years":ijikanri_years,
        #    "discount_rate":discount_rate
        #}

        #joblib.dump(res_PSC_LCC, 'res_PSC_LCC.joblib') 

        #res_PSC_LCC = joblib.load('res_PSC_LCC.joblib')

        vc.calc_VFM()
        #LCC_net_expense = float(res_PSC_LCC['LCC_net_expense'])
        #PSC_net_expense_const_kk = float(res_PSC_LCC['PSC_net_expense_const_kk'])
        #PSC_net_expense_ijikanri_kk = float(res_PSC_LCC['PSC_net_expense_ijikanri_kk'])
        #proj_years = int(res_PSC_LCC['proj_years'])
        #const_years = int(res_PSC_LCC['const_years'])
        #ijikanri_years = int(res_PSC_LCC['ijikanri_years'])
        #discount_rate = float(res_PSC_LCC['discount_rate'])/100
        
        #PSC_const = []
        #PSC_ijikanri = []
        #LCC = []
        
        #for i in range(proj_years):
        #    LCC.append(LCC_net_expense/proj_years)

        #for i in range(const_years):
        #    PSC_const.append(PSC_net_expense_const_kk/const_years)

        #for i in range(ijikanri_years):
        #    PSC_ijikanri.append(PSC_net_expense_ijikanri_kk/ijikanri_years)

        #df_LCC = pd.DataFrame(LCC, columns=['LCC_net_expense'])

        #df_PSC_const = pd.DataFrame(PSC_const, columns=['PSC_net_expense_const'])
        #df_PSC_ijikanri = pd.DataFrame(PSC_ijikanri, columns=['PSC_net_expense_iji'])
        
        #LCC
        #LCC_discount_factor = [(1/(1+discount_rate))** i for i in range(1, proj_years+1)]
        #df_LCC['LCC_discount_factor'] = LCC_discount_factor
        # calculate the present value of each cash flow
        #df_LCC['LCC_present_value'] = df_LCC['LCC_net_expense'] * df_LCC['LCC_discount_factor']
        
        #PSC
        #PSC_const_discount_factor = [(1/(1-discount_rate))** i for i in reversed(range(const_years))]
        #PSC_iji_discount_factor = [(1/(1+discount_rate))** i for i in range(1, ijikanri_years+1)]
        #df_PSC_const['PSC_const_discount_factor'] = PSC_const_discount_factor
        #df_PSC_ijikanri['PSC_iji_discount_factor'] = PSC_iji_discount_factor
        #df_PSC_const['PSC_const_present_value'] = df_PSC_const['PSC_net_expense_const'] * df_PSC_const['PSC_const_discount_factor']
        #df_PSC_ijikanri['PSC_iji_present_value'] = df_PSC_ijikanri['PSC_net_expense_iji'] * df_PSC_ijikanri['PSC_iji_discount_factor']
        
        #df_PSC = pd.concat([df_PSC_const['PSC_const_present_value'], df_PSC_ijikanri['PSC_iji_present_value']]).reset_index(drop=True)
        #df_PSC.columns = ['PSC_present_value']

        #df_PV_cf = pd.concat([df_PSC, df_LCC['LCC_present_value']], axis=1)
        #df_PV_cf = df_PV_cf.set_axis(['PSC_present_value', 'LCC_present_value'], axis=1)

        #PSC = df_PV_cf['PSC_present_value'].sum()
        #LCC = df_PV_cf['LCC_present_value'].sum()
        #VFM = PSC - LCC
        #VFM_percent = VFM/PSC*100
        
        #results = {
        #    'df_PV_cf': df_PV_cf,
        #    'LCC_discount_factor': LCC_discount_factor,
        #    'PSC_const_discount_factor': PSC_const_discount_factor,
        #    'PSC_iji_discount_factor': PSC_iji_discount_factor,
        #    'PSC': PSC,
        #    'LCC': LCC,
        #    'VFM': VFM,
        #    'VFM_percent': VFM_percent
        #}

        #joblib.dump(results, 'results.joblib')