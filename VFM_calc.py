#import os, sys, argparse, logging, time, datetime, re
#from pathlib import Path
import pandas as pd
import flet as ft
#import shelve as sv
import joblib
from Final_Inputs import Final_Inputs

class PSC:
    def __init__(self):
        self.final_inputs = joblib.load('final_inputs.pkl')
    
    def calc(self):
        shisetsu_seibi_total = float(self.final_inputs['shisetsu_seibi'])
        ijikanri_unnei_total = float(self.final_inputs['ijikanri_unnei']) * (int(self.final_inputs['proj_years']) - int(self.final_inputs['const_years']))
        hojokin_kan = shisetsu_seibi_total * (float(self.final_inputs['hojo'])/100)
        if self.final_inputs['mgmt_type'] == '国':
            hojokin_kan = 0 
        ribarai_kan = (shisetsu_seibi_total - hojokin_kan) * float(self.final_inputs['kisai_jutou'])/100 * (1 - float(self.final_inputs['kisai_koufu'])/100) * float(self.final_inputs['chisai_kinri'])
        if self.final_inputs['mgmt_type'] == '国':
            ribarai_kan = 0
        koufukin_kan = (shisetsu_seibi_total - hojokin_kan) * float(self.final_inputs['kisai_jutou'])/100 * float(self.final_inputs['kisai_koufu'])/100

        shisetsu_seibi_reduc_total = shisetsu_seibi_total * (float(self.final_inputs['reduc_shisetsu'])/100)
        ijikanri_unnei_reduc_total = ijikanri_unnei_total * (float(self.final_inputs['reduc_ijikanri'])/100)
        
        SPC_capital = (shisetsu_seibi_reduc_total + ijikanri_unnei_reduc_total) * 0.1
        SPC_yobihi = (shisetsu_seibi_reduc_total + ijikanri_unnei_reduc_total) * 0.1
        SPC_keihi_total = float(self.final_inputs['SPC_keihi']) * int(self.final_inputs['proj_years'])
        if SPC_keihi_total == 0:
            SPC_capital = SPC_yobihi = 0
        hojokin_min = (shisetsu_seibi_reduc_total) *  (float(self.final_inputs['hojo'])/100)
        ribarai_min = (((shisetsu_seibi_reduc_total - hojokin_min) * (1-float(self.final_inputs['kisai_jutou'])/100)) + (SPC_capital + SPC_yobihi)) * (float(self.final_inputs['kijun_kinri']) + float(self.final_inputs['lg_spread']))/100
        ribarai_min_chisai = (shisetsu_seibi_reduc_total - hojokin_min) * (float(self.final_inputs['kisai_jutou'])/100) * (1 - float(self.final_inputs['kisai_koufu'])/100) * float(self.final_inputs['chisai_kinri'])
        koufukin_min = (shisetsu_seibi_reduc_total - hojokin_min) * (float(self.final_inputs['kisai_jutou'])/100) * float(self.final_inputs['kisai_koufu'])/100
        
        ribarai_kanmin_sa = ribarai_min - ribarai_kan
        
        kappu_genka_s = (shisetsu_seibi_reduc_total + ijikanri_unnei_reduc_total + ribarai_min + SPC_capital + SPC_yobihi + SPC_keihi_total) / (1 - float(self.final_inputs['zeimae_rieki'])/100)
        zeimae_rieki_gaku = kappu_genka_s * float(self.final_inputs['zeimae_rieki'])/100
        nouzei_gaku = zeimae_rieki_gaku * float(self.final_inputs['zei_total'])/100
        zeigo_rieki_gaku = zeimae_rieki_gaku - nouzei_gaku
        
        zei_modori_gaku = zeimae_rieki_gaku * float(self.final_inputs['zei_modori'])/100
        
        
        PSC_income_total = float(hojokin_kan + koufukin_kan)
        PSC_expense_total = float(shisetsu_seibi_total + ijikanri_unnei_total + ribarai_kan + ribarai_kanmin_sa + SPC_capital + SPC_yobihi + SPC_keihi_total)
        PSC_net_expense = float(PSC_expense_total - PSC_income_total)
        
        LCC_income_total = float(hojokin_min + koufukin_min + zei_modori_gaku)
        LCC_expense_total = float(shisetsu_seibi_reduc_total + ijikanri_unnei_reduc_total + ribarai_min + ribarai_min_chisai + zeimae_rieki_gaku + SPC_capital + SPC_yobihi + SPC_keihi_total)
        LCC_net_expense = float(LCC_expense_total - LCC_income_total)

        discount_rate = float(self.final_inputs['kijun_kinri']) + float(self.final_inputs['kitai_bukka'])

        ijikanri_years = int(self.final_inputs['proj_years']) - int(self.final_inputs['const_years'])

        rakusatsu_ritsu = 0.95

        PSC_const_rate = shisetsu_seibi_total / (shisetsu_seibi_total + ijikanri_unnei_total)
        PSC_ijikanri_rate = ijikanri_unnei_total / (shisetsu_seibi_total + ijikanri_unnei_total)

        risk_adj_koufu = ribarai_kanmin_sa + SPC_capital + SPC_keihi_total + SPC_yobihi - koufukin_kan
        risk_adj_koufu_const = risk_adj_koufu * PSC_const_rate
        risk_adj_koufu_ijikanri = risk_adj_koufu * PSC_ijikanri_rate

        PSC_net_expense_const_kk = (risk_adj_koufu_const + shisetsu_seibi_total + ribarai_kan - hojokin_kan) * rakusatsu_ritsu
        PSC_net_expense_ijikanri_kk = (risk_adj_koufu_ijikanri + ijikanri_unnei_total) * rakusatsu_ritsu

        #NPV_PSC = PSC_net_expense / ((1 + discount_rate/100)**int(self.final_inputs['proj_years']))
    
class VFM:
    def __init__(self):
        pass
class Initial_inputs:
    def __init__(
            self, 
            mgmt_type, 
            proj_ctgry, 
            proj_type, 
            shisetsu_seibi_jurai, 
            ijikanri_unnei_jurai_nen,
            proj_years,
            const_years,
            reduc_shisetuseibi=0.9, 
            reduc_ijikannri=0.9, 
            pre_kyoukouka=False, 
            lg_spread=1.5, 
            kisai_jutou=0.0, 
            kisai_koufu=0.0, 
            zeimae_rieki=8.5, 
            zei_total=41.98, 
            SPC_keihi=1.0, 
            hojo=0.0, 
            growth=0.0):
        self.mgmt_type = mgmt_type
        self.proj_ctgry = proj_ctgry
        self.proj_type = proj_type
        self.shisetsu_seibi_jurai = shisetsu_seibi_jurai
        self.ijikanri_unnei_jurai_nen = ijikanri_unnei_jurai_nen
        self.reduc_shisetuseibi = reduc_shisetuseibi
        self.reduc_ijikannri = reduc_ijikannri
        self.pre_kyoukouka = pre_kyoukouka
        self.lg_spread = lg_spread
        self.kisai_jutou = kisai_jutou
        self.kisai_koufu = kisai_koufu
        self.zeimae_rieki = zeimae_rieki
        self.zei_total = zei_total
        self.SPC_keihi = SPC_keihi
        self.hojo = hojo
        self.growth = growth
        self.proj_years = proj_years
        self.const_years = const_years

class Inputs_from_DB:
    def __init__(self, JGB_rates, JRB_rates, kitai_bukka):
        self.JGB_rates = JGB_rates
        self.JRB_rates = JRB_rates
        self.kitai_bukka = kitai_bukka

#　Inputs＿from＿db には、SQLite３からの入力メソッドをつける。アプリ起動時にこのクラスを初期化して、DBからデータを得て、Shelveに書き出す。
# Initial_inputsには、Shelveへの書き出しメソッドをつける。
# PSCとLCCには、Shelveからの読み込みメソッドをつける。
# 入力の修正は、Shelveの保存内容を書き換える（WritebackをTrueにして書き換える）。まず既存の値があるかを確認して、あれば入力欄に表示、修正した入力をShelveに書き出す。

# s = shelve.open('test_shelf.db', writeback=True)
#try:
#    print s['key1']
#    s['key1']['new_value'] = 'this was not here before'
#    print s['key1']
#finally:
#    s.close()
#
#s = shelve.open('test_shelf.db', writeback=True)
#try:
#    print s['key1']
#finally:
#    s.close()