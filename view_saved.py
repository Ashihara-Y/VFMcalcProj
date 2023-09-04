import sys

sys.dont_write_bytecode = True
import pandas as pd
import flet as ft
import joblib
from simpledt import DataFrame
import plotly.express as px
from flet.plotly_chart import PlotlyChart
import duckdb
import glob


class View_saved(ft.UserControl):
    def __init__(self):
        super().__init__()
        self.title = "保存  結果"
        self.width = 1000
        self.height = 800
        self.resizable = True

        #PSC = round(float(self.results["PSC"]), 3)
        #LCC = round(float(self.results["LCC"]), 3)
        #VFM = round(float(self.results["VFM"]), 3)
        #VFM_percent = self.results["VFM_percent"]
        
        self.res_summ_list = []
        self.res_detail_list = []

        db_saved_list = glob.glob('file*.db')
        for file in db_saved_list:
            con = duckdb.connect(file)
            timestamp = con.sql('select datetime from table_final_inputs').df().iloc[0,0].timestamp()

            res_vfm = con.sql('select * from table_vfm_results').df().transpose()
            res_final_inputs = con.sql('select * from table_final_inputs').df().transpose()
            res_PSC_LCC = con.sql('select * from table_PSC_LCC').df()[['LCC_net_expense','PSC_net_expense_const_kk','PSC_net_expense_ijikanri_kk','discount_rate','rakusatsu_ritsu']].transpose()
            res_detail = pd.concat([res_final_inputs, res_PSC_LCC], axis=0)
            res_detail['PSC'] = res_vfm['PSC']
            res_detail['LCC'] = res_vfm['LCC']
            res_detail['VFM'] = res_vfm['VFM']
            res_detail['VFM_percent'] = res_vfm['VFM_percent']

            res_detail = res_detail.reindex(['datetime','user_id','calc_id','PSC','LCC','VFM','VFM_percent','mgmt_type','proj_ctgry','proj_type','proj_years','const_years','shisetsu_seibi','ijikanri_unnei','reduc_shisetsu','reduc_ijikanri','hojo','kisai_jutou','kisai_koufu','SPC_keihi','zeimae_rieki','zei_total','zei_modori','PSC_net_expense_const_kk','PSC_net_expense_ijikanri_kk','rakusatsu_ritsu','LCC_net_expense','discount_rate','kijun_kinri','kitai_bukka','lg_spread','chisai_kinri'])
            res_detail = res_detail.rename(index={
                'datetime':'作成日時',
                'user_id':'ユーザーID',
                'calc_id':'計算結果ID',
                'PSC':'PSC現在価値総額',
                'LCC':'LCC現在価値総額',
                'VFM':'VFM金額',
                'VFM_percent':'VFM(%)',
                'mgmt_type':'施設管理者種別',
                'proj_ctgry':'事業類型',
                'proj_type':'事業方式',
                'proj_years':'事業期間',
                'const_years':'施設整備期間',
                'shisetsu_seibi':'施設整備費',
                'ijikanri_unnei':'維持管理運営費（年額）',
                'reduc_shisetsu':'削減率（施設整備費）',
                'reduc_ijikanri':'削減率（維持管理運営費）',
                'hojo':'補助率',
                'kisai_jutou':'起債充当率',
                'kisai_koufu':'起債への交付金カバー率',
                'SPC_keihi':'SPC運営経費',
                'zeimae_rieki':'税引き前利益率',
                'zei_total':'実効税率',
                'zei_modori':'戻り税収の率（施設管理者への戻り）',
                'PSC_net_expense_const_kk':'PSC施設整備純支出（競争効果反映済）',
                'PSC_net_expense_ijikanri_kk':'PSC維持管理運営純支出（競争効果反映済）',
                'rakusatsu_ritsu':'落札率',
                'LCC_net_expense':'LCC純支出総額',
                'discount_rate':'割引率',
                'kijun_kinri':'基準金利',
                'kitai_bukka':'期待物価上昇率',
                'lg_spread':'基準金利からのスプレッド',
                'chisai_kinri':'地方債利回り'},
                columns={0:'値'}
            )

            simpledt_df_res_detail = DataFrame(res_detail)
            self.res_list.append(simpledt_df_res_detail)
            #リストから、各データフレームを取り出して、戦闘の日付を見出し用に読み込んで、順にDataTableに変換して表示していく。Datetimeを抽出して見出しにする。

        self.res_PSC_LCC = joblib.load('res_PSC_LCC.joblib')
        self.results = joblib.load("results.joblib")

    def build(self):
        df_PV_cf = self.results["df_PV_cf"].round(3)
        self.fig = px.bar(
            df_PV_cf,
            x=df_PV_cf.index,
            y=["PSC_present_value", "LCC_present_value"],
            barmode="group",
        )
        self.graph = PlotlyChart(self.fig, expand=True)

        # to ft.datatable
        self.table_list = []
        simpledt_df = DataFrame(self.res_list.pop())
        simpledt_dt = simpledt_df.datatable
        self.table_list.append(simpledt_dt)

        lv = ft.ListView(
            expand=1, spacing=10, padding=20, auto_scroll=True
        )
        lv.controls.append(self.table)

        PSC = round(float(self.results["PSC"]), 3)
        LCC = round(float(self.results["LCC"]), 3)
        VFM = round(float(self.results["VFM"]), 3)
        VFM_percent = self.results["VFM_percent"]

        return ft.Card(
            content=ft.Container(
                content=ft.Column(
                    controls=[
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
