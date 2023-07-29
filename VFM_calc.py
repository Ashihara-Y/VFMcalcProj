import os, sys, argparse, logging, time, datetime, re
from pathlib import Path
import pandas as pd
#import flet as ft
import shelve as sv
import joblib as jl

class PSC:
    def __init__(self, inputs_path, inputs_name):
        self.inputs_path = Path(inputs_path)
        self.inputs_name = inputs_name
        self.inputs_file = inputs_path / inputs_name
        self.psc = sv.open(self.inputs_file, writeback=True)
        #tmp_dir = Path('temp')
        #tmp_sub1_file = tmp_dir / 'sub1' / 'file1.txt'

class LCC:
    def __init__(self, inputs_path,inputs_name):
        self.lcc_path = lcc_path
        self.lcc_name = lcc_name
        self.lcc_file = os.path.join(self.lcc_path, self.lcc_name)
        self.lcc = sv.open(self.lcc_file, writeback=True)

class VFM:
    def __init__(self, vfm_path, vfm_name, vfm_version):
        self.vfm_path = vfm_path
        self.vfm_name = vfm_name
        self.vfm_version = vfm_version
        self.vfm_file = os.path.join(self.vfm_path, self.vfm_name)
        self.vfm = pd.read_csv(self.vfm_file, sep='\t', dtype=str)
        self.vfm = self.vfm[self.vfm['version'] == self.vfm_version]
        self.vfm = self.vfm[self.vfm['status'] == 'active']

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