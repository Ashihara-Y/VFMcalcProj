import sys

sys.dont_write_bytecode = True
import pandas as pd
import flet as ft
import joblib
from simpledt import DataFrame
import plotly.express as px
from flet.plotly_chart import PlotlyChart
import sqlite3
import glob
import Resultview
import tinydb
from tinydb import TinyDB, Query


class View_saved(ft.UserControl):
    def __init__(self):
        super().__init__()
        self.title = "結果リスト"
        self.width = 1000
        self.height = 800
        self.resizable = True

        save_res_01_list = glob.glob("res_01_db_*.json")
        save_res_01_list.sort(reverse=True)
        
        #save_res_02_list = glob.glob("res_02_db_*.json")
        #save_res_02_list.sort(reverse=True)

        self.res_summ_list = []
        # self.res_detail_list = []

        for file in save_res_01_list:
            con = TinyDB(file)
            res_detail = con.all()[0]
            res_detail = pd.DataFrame(data=res_detail, index=[0])
            #res_vfm = pd.read_sql_query('SELECT * FROM vfm_results', con)
            #res_final_inputs = pd.read_sql_query('SELECT * FROM final_inputs', con)
            #res_PSC_LCC = pd.read_sql_query("SELECT LCC_net_expense, PSC_net_expense_const_kk, PSC_net_expense_ijikanri_kk, discount_rate, rakusatsu_ritsu FROM res_PSC_LCC", con)
            
            #res_detail = pd.concat([res_final_inputs, res_PSC_LCC], axis=1)
            #res_detail = pd.concat([res_detail, res_vfm], axis=1)

            res_detail = res_detail.reindex(
                columns=[
                    "datetime",
                    "user_id",
                    "calc_id",
                    "PSC",
                    "LCC",
                    "VFM",
                    "VFM_percent",
                    "mgmt_type",
                    "proj_ctgry",
                    "proj_type",
                    "proj_years",
                    "const_years",
                    "shisetsu_seibi",
                    "ijikanri_unnei",
                    "reduc_shisetsu",
                    "reduc_ijikanri",
                    "hojo",
                    "kisai_jutou",
                    "kisai_koufu",
                    "SPC_keihi",
                    "zeimae_rieki",
                    "zei_total",
                    "zei_modori",
                    "PSC_net_expense_const_kk",
                    "PSC_net_expense_ijikanri_kk",
                    "rakusatsu_ritsu",
                    "LCC_net_expense",
                    "discount_rate",
                    "kijun_kinri",
                    "kitai_bukka",
                    "lg_spread",
                    "chisai_kinri",
                ]
            )
            res_detail = res_detail.rename(
                columns={
                    "datetime": "作成日時",
                    "user_id": "ユーザーID",
                    "calc_id": "計算結果ID",
                    "PSC": "PSC現在価値総額",
                    "LCC": "LCC現在価値総額",
                    "VFM": "VFM金額",
                    "VFM_percent": "VFM(%)",
                    "mgmt_type": "施設管理者種別",
                    "proj_ctgry": "事業類型",
                    "proj_type": "事業方式",
                    "proj_years": "事業期間",
                    "const_years": "施設整備期間",
                    "shisetsu_seibi": "施設整備費",
                    "ijikanri_unnei": "維持管理運営費（年額）",
                    "reduc_shisetsu": "削減率（施設整備費）",
                    "reduc_ijikanri": "削減率（維持管理運営費）",
                    "hojo": "補助率",
                    "kisai_jutou": "起債充当率",
                    "kisai_koufu": "起債への交付金カバー率",
                    "SPC_keihi": "SPC運営経費",
                    "zeimae_rieki": "税引き前利益率",
                    "zei_total": "実効税率",
                    "zei_modori": "戻り税収の率（施設管理者への戻り）",
                    "PSC_net_expense_const_kk": "PSC施設整備純支出（競争効果反映済）",
                    "PSC_net_expense_ijikanri_kk": "PSC維持管理運営純支出（競争効果反映済）",
                    "rakusatsu_ritsu": "落札率",
                    "LCC_net_expense": "LCC純支出総額",
                    "discount_rate": "割引率",
                    "kijun_kinri": "基準金利",
                    "kitai_bukka": "期待物価上昇率",
                    "lg_spread": "基準金利からのスプレッド",
                    "chisai_kinri": "地方債利回り",
                },
                index={0: "項目"},
            )
            res_summary = res_detail.reindex(
                columns=[
                    "作成日時",
                    "VFM(%)",
                    "PSC現在価値総額",
                    "LCC現在価値総額",
                    "施設管理者種別",
                    "事業類型",
                    "事業方式",
                    "事業期間",
                    "施設整備期間",
                    "割引率",
                ]
            )

            # simpledt_df_res_detail = DataFrame(res_detail)
            simpledt_df_res_summary = DataFrame(res_summary)
            # self.res_detail_list.append(simpledt_df_res_detail)
            self.res_summ_list.append(simpledt_df_res_summary)
            # リストから、各データフレームを取り出して、戦闘の日付を見出し用に読み込んで、順にDataTableに変換して表示していく。Datetimeを抽出して見出しにする。

        # self.res_PSC_LCC = joblib.load('res_PSC_LCC.joblib')
        # self.results = joblib.load("results.joblib")

    def build(self):
        # Smmary table
        # self.summ_table_list = []
        summ_lv = ft.ListView(
            expand=1,
            spacing=10,
            padding=20,
            auto_scroll=False,
            first_item_prototype=True,
            horizontal=False,
        )
        for df in self.res_summ_list:
            table = df.datatable
            # ここで、DTに修飾を追加する。チェックボックス、色、テキストスタイル
            #summ_lv.controls.append(
            #    ft.Text(Value=self.datetime, visible=False)
            #)
            summ_lv.controls.append(table)
            summ_lv.controls.append(ft.Divider())

        return ft.Card(
            content=ft.Container(
                content=ft.Column(
                    controls=[
                        summ_lv,
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_AROUND,
                ),
                # content=lv,
                width=1800,
                height=1800,
                padding=16,
            )
        )

    def button_clicked(self, e):
        Resultview.Results_detail()
