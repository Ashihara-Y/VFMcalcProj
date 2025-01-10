import sys
sys.dont_write_bytecode = True
#import os
import pandas as pd
#import duckdb
from ulid import ULID
import timeflake
import datetime
#import tinydb
from tinydb import TinyDB, Query
import make_inputs_df
#import decimal
from decimal import Decimal
from sqlalchemy import create_engine
import sqlite3

class Save_results():
    def __init__(self):   
        self.engine = create_engine('sqlite:///VFM.db', echo=False)
        self.conn = sqlite3.connect('VFM.db')
        self.c = self.conn.cursor()

        self.user_id = ULID.from_datetime(datetime.datetime.now())
        self.calc_id = timeflake.random()
        self.dtime = datetime.datetime.fromtimestamp(self.calc_id.timestamp // 1000)

        self.inputs_pdt = make_inputs_df.io()

    def make_df(self):
        self.PSC_df = pd.read_sql_query("SELECT * FROM PSC_table", self.engine)
        self.PSC_pv_df = pd.read_sql_query("SELECT * FROM PSC_pv_table", self.engine)
        self.LCC_df = pd.read_sql_query("SELECT * FROM LCC_table", self.engine)
        self.LCC_pv_df = pd.read_sql_query("SELECT * FROM LCC_pv_table", self.engine)
        self.SPC_df = pd.read_sql_query("SELECT * FROM SPC_table", self.engine)
        self.SPC_check_df = pd.read_sql_query("SELECT * FROM SPC_check_table", self.engine)
        self.Risk_df = pd.read_sql_query("SELECT * FROM Risk_table", self.engine)
        self.VFM_df = pd.read_sql_query("SELECT * FROM VFM_table", self.engine)
        self.PIRR_df = pd.read_sql_query("SELECT * FROM PIRR_table", self.engine)

        # make summary
        self.PSC_pv_summary_org = self.PSC_pv_df[['present_value']].sum()
        self.LCC_pv_summary_org = self.LCC_pv_df[['present_value']].sum()
        self.SPC_check_summary_org = self.SPC_check_df.loc[int(self.inputs_pdt.const_years)+1:int(self.inputs_pdt.proj_years), 'P_payment_check'].to_list()
        self.VFM_summary_df = self.VFM_df[['VFM','VFM_percent']]
        self.PIRR_summary_df = self.PIRR_df[['PIRR_percent']]

        def payment_check(bool):
            if bool == 'True':
                return "返済資金は十分"
            elif bool == 'False':
                return "返済資金が不足"

        SPC_check_mod = str('False' not in self.SPC_check_summary_org)
        self.SPC_check_res = payment_check(SPC_check_mod)

    def make_summary_add_ids(self):
        VFM_calc_summary_df = pd.DataFrame(columns=['VFM_percent','PSC_present_value','LCC_present_value','PIRR','SPC_payment_cash'], index=['0'])

        #VFM_calc_summary_df['VFM'] = VFM_summary_df['VFM'].iloc[0]
        VFM_calc_summary_df['VFM_percent'] = self.VFM_summary_df['VFM_percent'].iloc[0]
        VFM_calc_summary_df['PSC_present_value'] = self.PSC_pv_summary_org.iloc[0]
        VFM_calc_summary_df['LCC_present_value'] = self.LCC_pv_summary_org.iloc[0]
        VFM_calc_summary_df['PIRR'] = self.PIRR_summary_df['PIRR_percent'].iloc[0]
        VFM_calc_summary_df['SPC_payment_cash'] = self.SPC_check_res

        kijun_kinri = Decimal(str(self.inputs_pdt.kijun_kinri)).quantize(Decimal('0.001'), 'ROUND_HALF_UP')
        kitai_bukka = Decimal(str(self.inputs_pdt.kitai_bukka)).quantize(Decimal('0.001'), 'ROUND_HALF_UP')
        lg_spread = Decimal(str(self.inputs_pdt.lg_spread)).quantize(Decimal('0.001'), 'ROUND_HALF_UP')

        #discount_rate = Decimal((kijun_kinri + kitai_bukka)*100).quantize(Decimal('0.001'), 'ROUND_HALF_UP')
        kariire_kinri = Decimal((kijun_kinri + lg_spread)*100).quantize(Decimal('0.001'), 'ROUND_HALF_UP')

        final_inputs_dic = {
            'mgmt_type': self.inputs_pdt.mgmt_type,
            'proj_ctgry': self.inputs_pdt.proj_ctgry,
            'proj_type': self.inputs_pdt.proj_type,
            'const_years': self.inputs_pdt.const_years,
            'proj_years': self.inputs_pdt.proj_years,
            'discount_rate': self.inputs_pdt.discount_rate,
            'kariire_kinri': kariire_kinri,
        }

        final_inputs_df = pd.DataFrame(final_inputs_dic, index=['0'])
        #print(inputs_pdt.kijun_kinri, inputs_pdt.lg_spread)
        self.res_summ_df = VFM_calc_summary_df.join(final_inputs_df)

        def addID(self,x_df):
            x_df['datetime'] = str(self.dtime)
            x_df['user_id'] = str(self.user_id)
            x_df['calc_id'] = str(self.calc_id)

            return x_df

        df_list = [
            self.PSC_df,
            self.PSC_pv_df,
            self.LCC_df,
            self.LCC_pv_df,
            self.SPC_df,
            self.SPC_check_df,
            self.Risk_df,
            self.VFM_df,
            self.PIRR_df, 
            self.res_summ_df
        ]
        self.df_name_list = [
            (self.PSC_df,'self.PSC_df'),
            (self.PSC_pv_df,'self.PSC_pv_df'),
            (self.LCC_df,'self.LCC_df'),
            (self.LCC_pv_df,'self.LCC_pv_df'),
            (self.SPC_df,'self.SPC_df'),
            (self.SPC_check_df,'self.SPC_check_df'),
            (self.Risk_df,'self.Risk_df'),
            (self.VFM_df,'self.VFM_df'),
            (self.PIRR_df,'self.PIRR_df'),
            (self.res_summ_df,'self.res_summ_df')
        ]

        for i in df_list:
            addID(i)

# df_listの要素であるDFそれぞれに、２つのIDEAと日時が追加されている。
# 上記のDFを、「結果蓄積用テーブル」に追加していく。その最に、「既に追加済の結果」を再度追加することは避ける必要がある。
# 他方で、『「既に追加済の結果」を再度追加する』事態は、どこで発生するのか？
# 「PSC等の直近の計算結果テーブル」には、それぞれの直近の計算結果１つだけが保存されている。
# したがって、「PSC等の直近の計算結果テーブル」から保存されている結果を抽出して、「結果蓄積用テーブル」への書き込みが
# 1回だけ実施されるなら、上記の問題は発生しないのでは？
# 結果蓄積に保存したら、直近の計算結果は消去してしまうか？これが残っていないと、どこで問題が生じるか？
# 丁寧にやるなら、結果蓄積テーブルのDatetime列をリストに抽出して、その中に、これから書き込みDFのDatetimeが
# 含まれていたら、書き込みを中止するか？
# まず存在しなかれば当該の結果蓄積テーブルを空で作成する。存在すればスルーのはず。
# 空ならばDatetimeは要素なしになるが、存在していればDatetimeには１つ以上の要素がある。
# Datetimeリストに要素がないか、要素はあっても直近結果のDatetimeと同じ要素がなければ、直近結果を結果蓄積に書き込む。
# Datetimeリストに、直近結果のDatetimeと同じ要素があれば、（直近結果は保存済なので）書き込みはしない。

    def save_db(self):
        for x_df in self.df_name_list:
            self.c.execute('CREATE TABLE IF NOT EXISTS ' + x_df[1].replace('_df','') + '_res_table')
            df_dtime = pd.read_sql_table(x_df[1].replace('_df','') + '_res_table', self.engine, columns=['datetime'])
            list_dtime = df_dtime['datetime'].to_list()
            if len(list_dtime)==0 or x_df[0]['datetime'].iloc[0] not in list_dtime: 
                x_df[0].to_sql(x_df[1].replace('_df','') + '_res_table', self.engine, if_exists='append', index=False)
            else:
                pass
        