import sys
sys.dont_write_bytecode = True
import os
import pandas as pd
import flet as ft
from simpledt import DataFrame
from tinydb import TinyDB, Query
#import openpyxl
from sqlalchemy import create_engine
#import make_inputs_df
#import decimal
from decimal import Decimal, ROUND_HALF_UP
#import timeflake
#import datetime
#from zoneinfo import ZoneInfo
from VFMcalc2 import VFM_calc

@ft.control
class Edit_result(ft.Stack):
    def __init__(self, selected_datetime):
        super().__init__()
        #self.title = "結果 詳細"
        self.width = 2100
        self.height = 1000
        #self.resizable = True

        self.dtime = selected_datetime # コンストラクタでselected_datetimeを受け取るように変更
        engine = create_engine('sqlite:///VFM.db', echo=False, connect_args={'check_same_thread': False})

        table_names = [
            'res_summ_res_table',
            'final_inputs_res_table',
        ]
        self.selected_res_list = []
        for table_name in table_names:
            query = 'select * from ' + table_name + ' where datetime = ' + '"' + self.dtime + '"'
            table_name = pd.read_sql_query(query, engine)
            self.selected_res_list.append(table_name)
# この２つのテーブルからDFを作成して表示。
# final_inputs_res_tableの方は、編集前後の入力値等を算定過程も通じて作成するための材料
# res_summ_res_tableの方は、結果要約の表を作るための材料。
        target_summ_df = self.selected_res_list[0]
        target_inputs_df = self.selected_res_list[1]
        self.target_inputs = target_inputs_df.rename(columns={
                'datetime':'datetime',
                '施設管理者区分':'mgmt_type',
                '事業形態':'proj_ctgry',
                '事業方式':'proj_type',
                '事業期間':'proj_years',
                '施設整備期間':'const_years',
                '施設整備開始日':'const_start_date',
                '維持管理運営費期間':'ijikanri_unnei_years',
                '落札率(%)':'rakusatsu_ritsu',
                '施設整備削減率(%)':'reduc_shisetsu',
                '維持管理運営費（人件費）削減率(%)':'reduc_ijikanri_1',
                '維持管理運営費（修繕費）削減率(%)':'reduc_ijikanri_2',
                '維持管理運営費（動力費）削減率(%)':'reduc_ijikanri_3',
                '施設整備費(競争効果反映後)(百万円)':'shisetsu_seibi',
                '施設整備費原額(百万円)':'shisetsu_seibi_org',
                'LCC施設整備費（削減率適用）(百万円)':'shisetsu_seibi_org_LCC',
                '維持管理運営費総額(競争効果反映後)(百万円)':'ijikanri_unnei',
                '維持管理運営費総額原額(百万円)':'ijikanri_unnei_org',
                'LCC維持管理運営費総額（削減率適用）(百万円)':'ijikanri_unnei_org_LCC',
                '維持管理運営費(人件費)(競争効果反映後)(百万円)':'ijikanri_unnei_1',
                '維持管理運営費(人件費)原額(百万円)':'ijikanri_unnei_1_org',
                'LCC維持管理運営費(人件費)（削減率適用）(百万円)':'ijikanri_unnei_1_org_LCC',
                '維持管理運営費(修繕費)(競争効果反映後)(百万円)':'ijikanri_unnei_2',
                '維持管理運営費(修繕費)原額(百万円)':'ijikanri_unnei_2_org',
                'LCC維持管理運営費(修繕費)（削減率適用）(百万円)':'ijikanri_unnei_2_org_LCC',
                '維持管理運営費(動力費)(競争効果反映後)(百万円)':'ijikanri_unnei_3',
                '維持管理運営費(動力費)原額(百万円)':'ijikanri_unnei_3_org',
                'LCC維持管理運営費(動力費)（削減率適用）(百万円)':'ijikanri_unnei_3_org_LCC',
                '補助率(%)':'hojo_ritsu',
                '起債充当率(%)':'kisai_jutou',
                '起債交付金カバー率(%)':'kisai_koufu',
                'アドバイザリー手数料(百万円)':'advisory_fee',
                'PFI-LCCでのモニタリング等費用(百万円)':'monitoring_costs_LCC',
                'PSCでのモニタリング等費用(百万円)':'monitoring_costs_PSC',
                'SPC費用の処理（デフォルト：サービス対価に含める）':'SPC_hiyou_atsukai',
                'SPC手数料(百万円)':'SPC_fee',
                'SPC経費(百万円)':'SPC_keihi',
                'SPC設立費用(百万円)':'SPC_setsuritsuhi',
                'SPC費用総額(百万円)':'SPC_hiyou_total',
                'SPC費用年額(百万円)':'SPC_hiyou_nen',
                'LCCでのSPC経費(百万円)':'SPC_keihi_LCC',
                'SPC資本金(百万円)':'SPC_shihon',
                'SPC予備費(百万円)':'SPC_yobihi',
                '利用料金収入(百万円)':'riyouryoukin_shunyu',
                '施設整備対価一括払比率(%)':'shisetsu_seibi_paymentschedule_ikkatsu',
                '施設整備対価割賦払比率(%)':'shisetsu_seibi_paymentschedule_kappu',
                '基準金利(%)':'kijun_kinri',
                '官民スプレッド(%)':'lg_spread',
                '期待物価上昇率(%)':'kitai_bukka',
                '割引率(%)':'discount_rate',
                '割賦金利(%)':'Kappu_kinri',
                '割賦スプレッド(%)':'kappu_kinri_spread',
                '地方債金利(%)':'chisai_kinri',
                '地方債償還期間':'chisai_shoukan_kikan',
                '地方債償還据置期間':'chisai_sueoki_years',
                '法人税率(%)':'houjinzei_ritsu',
                '法人住民税均等割(百万円)':'houjinjuminzei_kintou',
                '不動産取得税課税標準(百万円)':'fudousanshutokuzei_hyoujun',
                '不動産取得税率(%)':'fudousanshutokuzei_ritsu',
                '固定資産税課税標準(百万円)':'koteishisanzei_hyoujun',
                '固定資産税率(%)':'koteishisanzei_ritsu',
                '登録免許税課税標準(百万円)':'tourokumenkyozei_hyoujun',
                '登録免許税率(%)':'tourokumenkyozei_ritsu',
                }
        ).set_index('項目名')['値'].to_dict()

        target_summ_df['discount_rate'] = target_summ_df['discount_rate'] * 100

        target_summ_df = target_summ_df.drop(['datetime', 'user_id', 'calc_id'], axis=1)
        target_inputs_df = target_inputs_df.drop(['datetime'], axis=1)

        target_summ_df_J = target_summ_df.rename(
            columns={
                'VFM_percent':'VFM(％)', 
                'PSC_present_value':'PSCでの公共キャッシュ・フロー現在価値', 
                'LCC_present_value':'PFI-LCCでの公共キャッシュ・フロー現在価値', 
                'PIRR':'プロジェクト内部収益率(％)',
                'SPC_payment_cash':'SPCの元本返済可否', 
                'mgmt_type':'発注者区分', 
                'proj_ctgry':'事業形態', 
                'proj_type':'事業方式',
                'const_years':'施設整備期間', 
                'proj_years':'事業期間', 
                'discount_rate':'割引率(％)', 
                'kariire_kinri':'借入コスト(％)',
                'Kappu_kinri':'割賦金利(％)',
                'kappu_kinri_spread':'割賦スプレッド(％)',
                'SPC_fee':'SPCへの手数料(百万円)',
            }
        )
        # 最終入力・パラメータの表を作成
        self.target_inputs_df = target_inputs_df.transpose().reset_index().rename(columns={"index":"項目名", 0:"値"})
        simpledt_targetinputs_df = DataFrame(self.target_inputs_df)
        simpledt_targetinputs_dt = simpledt_targetinputs_df.datatable
        self.table_targetinputs = simpledt_targetinputs_dt

        # 編集対象算定結果要約の表を作成
        target_summ_df_t = target_summ_df.transpose().reset_index()
        target_summ_df_t = target_summ_df_t.rename(columns={"index":"項目名", 0:"値"})
        simpledt_target_summ_df = DataFrame(target_summ_df_t)
        simpledt_target_summ_dt = simpledt_target_summ_df.datatable
        self.table_target_summ = simpledt_target_summ_dt

        lv_01 = ft.ListView(
            expand=True, spacing=10, padding=10, auto_scroll=True, horizontal=False
        )
        lv_01.controls.append(ft.Text('編集対象算定結果の要約'))
        lv_01.controls.append(self.table_target_summ)

        lv_04 = ft.ListView(
            expand=True, spacing=10, padding=10, auto_scroll=True, horizontal=False
        )
        lv_04.controls.append(ft.Text('編集対象入力値・パラメータ等一覧'))
        lv_04.controls.append(self.table_targetinputs)

        if self.target_inputs["proj_type"] == "DBO(SPCなし)" or self.target_inputs["proj_type"] == "BT/DB(いずれもSPCなし)":
            self.controls = [
                ft.Tabs(
                    selected_index=0,
                    length=4,
                    animation_duration=300,
                    content = ft.Column(
                        expand=True,    
                        controls=[
                            ft.TabBar(
                                tabs=[
                                    ft.Tab(
                                        label="編集対象結果・入力の要約",
                                    ),
                                    ft.Tab(
                                        label="編集対象入力値等一覧",
                                    ),
                                    ft.Tab(
                                        label="入力値の修正と再計算",
                                    ),
                                ],
                            ),
                        ft.TabBarView(
                            expand=True,
                            controls=[
                                ft.Container(
                                    content=ft.Column(
                                        controls=[
                                            lv_01,
                                        ],
                                    alignment=ft.MainAxisAlignment.SPACE_AROUND,
                                    ),
                                    width=2100,
                                    padding=10,
                                    margin=10,
                                    height=1000,
                                ),
                                ft.Container(
                                    content=ft.Column(
                                        controls=[
                                            lv_04,
                                        ],
                                    alignment=ft.MainAxisAlignment.SPACE_AROUND,
                                    ),
                                    width=2100,
                                    padding=10,
                                    height=3000,
                                    margin=10,
                                ),
                                ft.Container(
                                    content=ft.Column(
                                        controls = [
                                            fi_lv2,
                                        ],
                                    alignment=ft.MainAxisAlignment.SPACE_AROUND,
                                    ),
                                    width=2100,
                                    padding=10,
                                    height=3000,
                                    margin=10,
                                ),
                            ],
                        )
                    ],
                ),
            )
        ]
        else:
           self.controls = [
                ft.Tabs(
                    selected_index=0,
                    length=4,
                    animation_duration=300,
                    content = ft.Column(
                        expand=True,    
                        controls=[
                            ft.TabBar(
                                tabs=[
                                    ft.Tab(
                                        label="編集対象結果・入力の要約",
                                    ),
                                    ft.Tab(
                                        label="編集対象入力値等一覧",
                                    ),
                                    ft.Tab(
                                        label="入力値の修正と再計算",
                                    ),
                                ],
                            ),
                        ft.TabBarView(
                            expand=True,
                            controls=[
                                ft.Container(
                                    content=ft.Column(
                                        controls=[
                                            lv_01,
                                        ],
                                    alignment=ft.MainAxisAlignment.SPACE_AROUND,
                                    ),
                                    width=2100,
                                    padding=10,
                                    margin=10,
                                    height=1000,
                                ),
                                ft.Container(
                                    content=ft.Column(
                                        controls=[
                                            lv_04,
                                        ],
                                    alignment=ft.MainAxisAlignment.SPACE_AROUND,
                                    ),
                                    width=2100,
                                    padding=10,
                                    height=3000,
                                    margin=10,
                                ),
                                ft.Container(
                                    content=ft.Column(
                                        controls = [
                                            fi_lv1,
                                        ],   
                                    alignment=ft.MainAxisAlignment.SPACE_AROUND,
                                    ),
                                    width=2100,
                                    padding=10,
                                    height=3000,
                                    margin=10,
                                ),
                            ],       
                        )
                    ],
                ),
            )
        ]

#FIからのUIの材料⇒主にスライダと、上記表、そしてそれらのレイアウトの材料
        slider_value01 = ft.Text("", size=30, weight=ft.FontWeight.W_200)
        slider_value02 = ft.Text("", size=30, weight=ft.FontWeight.W_200)
        slider_value03 = ft.Text("", size=30, weight=ft.FontWeight.W_200)
        slider_value04 = ft.Text("", size=30, weight=ft.FontWeight.W_200)
        slider_value05 = ft.Text("", size=30, weight=ft.FontWeight.W_200)
        slider_value06 = ft.Text("", size=30, weight=ft.FontWeight.W_200)
        slider_value07 = ft.Text("", size=30, weight=ft.FontWeight.W_200)
        slider_value08 = ft.Text("", size=30, weight=ft.FontWeight.W_200)
        slider_value09 = ft.Text("", size=30, weight=ft.FontWeight.W_200)
        slider_value10 = ft.Text("", size=30, weight=ft.FontWeight.W_200)
        slider_value11 = ft.Text("", size=30, weight=ft.FontWeight.W_200)
        slider_value12 = ft.Text("", size=30, weight=ft.FontWeight.W_200)
        slider_value13 = ft.Text("", size=30, weight=ft.FontWeight.W_200)
        slider_value14 = ft.Text("", size=30, weight=ft.FontWeight.W_200)
        slider_value15 = ft.Text("", size=30, weight=ft.FontWeight.W_200)
        slider_value16 = ft.Text("", size=30, weight=ft.FontWeight.W_200)
            
        def handle_slider_change(e):
            sl_value = e.control.value
            target_text_control = e.control.data
            target_text_control.value = str(sl_value)
            target_text_control.update()

        tx1 = ft.Text("地方債償還期間(年)")
        self.sl1 = ft.Slider(
            value=int(self.target_inputs["chisai_shoukan_kikan"]),
            min=-2+int(self.target_inputs["chisai_shoukan_kikan"]),
            max=2+int(self.target_inputs["chisai_shoukan_kikan"]),
            divisions=5,
            label="{value}年",
            round=0,
            width=100,
            on_change=handle_slider_change,
            data=slider_value01,
        )
        tx2 = ft.Text("地方債元本返済据置期間(年)")
        self.sl2 = ft.Slider(
            value=float(self.target_inputs["chisai_sueoki_kikan"]),
            min=-2+float(self.target_inputs["chisai_sueoki_kikan"]),
            max=2+float(self.target_inputs["chisai_sueoki_kikan"]),
            divisions=5,
            label="{value}年",
            round=0,
            width=100,
            on_change=handle_slider_change,
            data=slider_value02,
        )
        tx3 = ft.Text("施設整備費支払 一括払の比率(%)")
        self.sl3 = ft.Slider(
            value=float(self.target_inputs["shisetsu_seibi_ikkatsu_hiritsu"])*100,
            min=0.975*float(self.target_inputs["shisetsu_seibi_ikkatsu_hiritsu"])*100,
            max=100.00,
            divisions=1000,
            label="{value}%",
            round=2,
            width=100,
            on_change=handle_slider_change,
            data=slider_value03,
        )
        tx4 = ft.Text("施設整備費の削減率(%)")
        self.sl4 = ft.Slider(
            value=float(self.target_inputs["reduc_shisetsu"])*100,
            min=0.0,
            max=5.0,
            divisions=50,
            label="{value}%",
            round=1,
            width=100,
            on_change=handle_slider_change,
            data=slider_value04,
        )
        tx5 = ft.Text("維持管理運営費（人件費）の削減率(%)")
        self.sl5 = ft.Slider(
            value=float(self.target_inputs["reduc_ijikanri_1"])*100,
            min=0.0,
            max=5.0,
            divisions=50,
            label="{value}%",
            round=1,
            width=100,
            on_change=handle_slider_change,
            data=slider_value05,
        ) 
        tx6 = ft.Text("維持管理運営費（修繕費）の削減率(%)")
        self.sl6 = ft.Slider(
            value=float(self.target_inputs["reduc_ijikanri_2"])*100,
            min=0.0,
            max=5.0,
            divisions=50,
            label="{value}%",
            round=1,
            width=100,
            on_change=handle_slider_change,
            data=slider_value06,
        )
        tx7 = ft.Text("維持管理運営費(動力費)の削減率(%)")
        self.sl7 = ft.Slider(
            value=float(self.target_inputs["reduc_ijikanri_3"])*100,
            min=0.0,
            max=5.0,
            divisions=50,
            label="{value}%",
            round=1,
            width=100,
            on_change=handle_slider_change,
            data=slider_value07,
        )
        tx8 = ft.Text("モニタリング等費用(PSC)(百万円、BT/DB:5程度、その他:10程度)")
        self.sl8 = ft.Slider(
            value=float(self.target_inputs["monitoring_costs_PSC"]),
            min=0.975*float(self.target_inputs["monitoring_costs_PSC"]),
            max=1.025*float(self.target_inputs["monitoring_costs_PSC"]),
            divisions=500,
            label="{value}百万円",
            round=1,
            width=100,
            on_change=handle_slider_change,
            data=slider_value08,
        )
        tx9 = ft.Text("モニタリング等費用(PFI-LCC)(百万円、BT/DB:3程度、その他:6程度)")
        self.sl9 = ft.Slider(
            value=float(self.target_inputs["monitoring_costs_PFI_LCC"]),
            min=0.975*float(self.target_inputs["monitoring_costs_PFI_LCC"]),
            max=1.025*float(self.target_inputs["monitoring_costs_PFI_LCC"]),
            divisions=500,
            label="{value}百万円",
            round=1,
            width=100,
            on_change=handle_slider_change,
            data=slider_value09,
        )
        tx10 = ft.Text("SPC経費年額(百万円)")
        self.sl10 = ft.Slider(
            value=float(self.target_inputs["SPC_keihi"]),
            min=0.95*float(self.target_inputs["SPC_keihi"]),
            max=1.05*float(self.target_inputs["SPC_keihi"]),
            divisions=1000,
            label="{value}百万円",
            round=1,
            width=100,
            on_change=handle_slider_change,
            data=slider_value10,
        )
        tx11 = ft.Text("SPCへの手数料(百万円)")
        self.sl11 = ft.Slider(
            value=float(self.target_inputs["SPC_fee"]),
            min=0,
            max=50,
            divisions=50,
            label="{value}百万円",
            round=1,
            width=100,
            on_change=handle_slider_change,
            data=slider_value11,
        )
        tx12 = ft.Text("SPC資本金(百万円)")
        self.sl12 = ft.Slider(
            value=float(self.target_inputs["SPC_shihon"]),
            min=0.95*float(self.target_inputs["SPC_shihon"]),
            max=1.05*float(self.target_inputs["SPC_shihon"]),
            divisions=1000,
            label="{value}百万円",
            round=1,
            width=100,
            on_change=handle_slider_change,
            data=slider_value12,
        )
        tx13 = ft.Text("SPC予備費(百万円)")
        self.sl13 = ft.Slider(
            value=float(self.target_inputs["SPC_yobihi"]),
            min=0.95*float(self.target_inputs["SPC_yobihi"]),
            max=1.05*float(self.target_inputs["SPC_yobihi"]),
            divisions=100,
            label="{value}百万円",
            round=1,
            width=100,
            on_change=handle_slider_change,
            data=slider_value13,
        )
        tx14 = ft.Text("アドバイザリー等経費(百万円)")
        self.sl14 = ft.Slider(
            value=float(self.target_inputs["advisory_fee"]),
            min=0.95*float(self.target_inputs["advisory_fee"]),
            max=1.05*float(self.target_inputs["advisory_fee"]),
            divisions=10,
            label="{value}百万円",
            round=1,
            width=100,
            on_change=handle_slider_change,
            data=slider_value14,
        )
        tx15 = ft.Text("割賦金利へのスプレッド(%)")
        self.sl15 = ft.Slider(
            value=float(self.target_inputs["kappu_kinri_spread"])*100,
            min=0.95*float(self.target_inputs["kappu_kinri_spread"])*100,
            max=1.05*float(self.target_inputs["kappu_kinri_spread"])*100,
            divisions=100,
            label="{value}%",
            round=2,
            width=100,
            on_change=handle_slider_change,
            data=slider_value15,
        )
        b = ft.Button(content="修正再計算", on_click=self.button_clicked)

        fi_lv1 = ft.ListView(
            expand=True,
            spacing=10,
            padding=5,
            #auto_scroll=True,
            item_extent=500,
            first_item_prototype=False,
            horizontal=False,
        )
        fi_lv2 = ft.ListView(
            expand=True,
            spacing=10,
            padding=5,
            #auto_scroll=True,
            item_extent=500,
            first_item_prototype=False,
            horizontal=False,
        )
        fi_lv1.controls= [
                    tx1, slider_value01, self.sl1,  ft.Divider(height=1, color="amber"), 
                    tx2, slider_value02, self.sl2,  ft.Divider(height=1, color="amber"),
                    tx3, slider_value03, self.sl3,  ft.Divider(height=1, color="amber"),
                    tx4, slider_value04, self.sl4,  ft.Divider(height=1, color="amber"),
                    tx5, slider_value05, self.sl5,  ft.Divider(height=1, color="amber"),
                    tx6, slider_value06, self.sl6,  ft.Divider(height=1, color="amber"),
                    tx7, slider_value07, self.sl7,  ft.Divider(height=1, color="amber"),
                    tx8, slider_value08, self.sl8,  ft.Divider(height=1, color="amber"),
                    tx9, slider_value09, self.sl9,  ft.Divider(height=1, color="amber"),
                    tx10,slider_value10, self.sl10, ft.Divider(height=1, color="amber"),
                    tx11,slider_value11, self.sl11, ft.Divider(height=1, color="amber"),
                    tx12,slider_value12, self.sl12, ft.Divider(height=1, color="amber"),
                    tx13,slider_value13, self.sl13, ft.Divider(height=1, color="amber"),
                    tx14,slider_value14, self.sl14, ft.Divider(height=1, color="amber"),
                    tx15,slider_value15, self.sl15, ft.Divider(height=1, color="amber"),
                    b,
        ]        
        fi_lv2.controls= [
                    tx1, slider_value01, self.sl1,  ft.Divider(height=1, color="amber"), 
                    tx2, slider_value02, self.sl2,  ft.Divider(height=1, color="amber"),
                    tx4, slider_value04, self.sl4,  ft.Divider(height=1, color="amber"),
                    tx5, slider_value05, self.sl5,  ft.Divider(height=1, color="amber"),
                    tx6, slider_value06, self.sl6,  ft.Divider(height=1, color="amber"),
                    tx7, slider_value07, self.sl7,  ft.Divider(height=1, color="amber"),
                    tx9, slider_value08, self.sl8,  ft.Divider(height=1, color="amber"),
                    tx14,slider_value13, self.sl13, ft.Divider(height=1, color="amber"),
                    b,
        ]        

# button_clicked
    async def button_clicked(self, e):
        self._extract_inputs()

        edit_results = self._calculate_financials()
        
        self._save_to_db(edit_results)
        VFM_calc()
        await self.page.push_route("/view_saved")
        
# 編集画面からの_extract_inputs
    def to_dec(val):
            return Decimal(val).quantize(Decimal('0.000001'), ROUND_HALF_UP)

    def _extract_inputs(self):

        proj_years = int(self.target_inputs["proj_years"])

        chisai_shoukan_kikan = int(self.sl1.value)
        chisai_sueoki_kikan = int(self.sl2.value)
        shisetsu_seibi_ikkatsu_hiritsu = self.to_dec(self.sl3.value)/self.to_dec(100)
        reduc_shisetsu = self.to_dec(self.sl4.value) / self.to_dec(100)
        reduc_ijikanri_1 = self.to_dec(self.sl5.value) / self.to_dec(100)
        reduc_ijikanri_2 = self.to_dec(self.sl6.value) / self.to_dec(100)
        reduc_ijikanri_3 = self.to_dec(self.sl7.value) / self.to_dec(100)
        monitoring_costs_PSC = self.to_dec(self.sl8.value)
        monitoring_costs_LCC = self.to_dec(self.sl9.value)
        SPC_keihi = self.to_dec(self.sl10.value)
        SPC_fee = self.to_dec(self.sl11.value)
        SPC_shihon = self.to_dec(self.sl12.value)
        SPC_yobihi = self.to_dec(self.sl13.value)    
        advisory_fee = self.to_dec(self.sl14.value)
        kappu_kinri_spread = self.to_dec(self.sl15.value)/self.to_dec(100)

        JGB_rates_df = pd.read_csv("src/JGB_rates.csv", sep="\t", encoding="utf-8", header=None, names=["year", "rate"],).set_index("year")
        JRB_rates_df = pd.read_csv("src/JRB_rates.csv", sep="\t", encoding="utf-8", names=[0,1,2,3,4,5], index_col=0)

        y, d = divmod(proj_years, 5)
        if y >= 1:
            r_idx = str((y + 1) * 5) + "年" if d > 2 else str(y * 5) + "年"
        else:
            r_idx = str(d) + "年"

        kijun_kinri = Decimal(JGB_rates_df.loc[r_idx].iloc[0])
        chisai_kinri = self.to_dec(JRB_rates_df.loc[chisai_shoukan_kikan][chisai_sueoki_kikan])
        kitai_bukka_j = self.to_dec(pd.read_csv("src/BOJ_ExpInflRate_down.csv", encoding="shift-jis", skiprows=1).dropna().iloc[-1, 1])
        gonensai_rimawari = self.to_dec(JGB_rates_df.loc["5年"].iloc[0])

        self.edit_inputs = {        
            'chisai_shoukan_kikan': chisai_shoukan_kikan,
            'chisai_sueoki_kikan': chisai_sueoki_kikan,
            'chisai_kinri': chisai_kinri,
            'kijun_kinri': kijun_kinri,
            'kitai_bukka_j': kitai_bukka_j,
            'gonensai_rimawari': gonensai_rimawari,
            'shisetsu_seibi_ikkatsu_hiritsu': shisetsu_seibi_ikkatsu_hiritsu,
            'reduc_shisetsu': reduc_shisetsu,
            'reduc_ijikanri_1': reduc_ijikanri_1,
            'reduc_ijikanri_2': reduc_ijikanri_2,
            'reduc_ijikanri_3': reduc_ijikanri_3,
            'monitoring_costs_PSC': monitoring_costs_PSC,
            'monitoring_costs_LCC': monitoring_costs_LCC,
            'SPC_keihi': SPC_keihi,
            'SPC_fee': SPC_fee,
            'SPC_shihon': SPC_shihon,
            'SPC_yobihi': SPC_yobihi,
            'advisory_fee': advisory_fee,
            'kappu_kinri_spread': kappu_kinri_spread,
        }

# 編集画面からの_calculate_financials
    def _calculate_financials(self):
        
        const_start_date = self.target_inputs['const_start_date']
        proj_type = self.target_inputs['proj_type']

        shisetsu_seibi_org = self.to_dec(self.target_inputs['shisetsu_seibi_org'])
        shisetsu_seibi = self.to_dec(self.target_inputs['shisetsu_seibi'])
        ijikanri_unnei_1_org = self.to_dec(self.target_inputs['ijikanri_unnei_1_org'])
        ijikanri_unnei_1 = self.to_dec(self.target_inputs['ijikanri_unnei_1'])
        ijikanri_unnei_2_org = self.to_dec(self.target_inputs['ijikanri_unnei_2_org'])
        ijikanri_unnei_2 = self.to_dec(self.target_inputs['ijikanri_unnei_2'])
        ijikanri_unnei_3_org = self.to_dec(self.target_inputs['ijikanri_unnei_3_org'])
        ijikanri_unnei_3 = self.to_dec(self.target_inputs['ijikanri_unnei_3'])
    
        shisetsu_seibi_org_LCC = self.to_dec(shisetsu_seibi_org * (Decimal(1.00) - self.edit_inputs['reduc_shisetsu']))
        shisetsu_seibi_LCC = self.to_dec(shisetsu_seibi * (Decimal(1.00) - self.edit_inputs['reduc_shisetsu']))
        ijikanri_unnei_1_org_LCC = self.to_dec(ijikanri_unnei_1_org * (Decimal(1.00) - self.edit_inputs['reduc_ijikanri_1']))
        ijikanri_unnei_1_LCC = self.to_dec(ijikanri_unnei_1 * (Decimal(1.00) - self.edit_inputs['reduc_ijikanri_1']))
        ijikanri_unnei_2_org_LCC = self.to_dec(ijikanri_unnei_2_org * (Decimal(1.00) - self.edit_inputs['reduc_ijikanri_2']))
        ijikanri_unnei_2_LCC = self.to_dec(ijikanri_unnei_2 * (Decimal(1.00) - self.edit_inputs['reduc_ijikanri_2']))
        ijikanri_unnei_3_org_LCC = self.to_dec(ijikanri_unnei_3_org * (Decimal(1.00) - self.edit_inputs['reduc_ijikanri_3']))
        ijikanri_unnei_3_LCC = self.to_dec(ijikanri_unnei_3 * (Decimal(1.00) - self.edit_inputs['reduc_ijikanri_3']))

        chisai_sueoki_kikan = int(self.edit_inputs['chisai_sueoki_kikan']) if self.edit_inputs['chisai_sueoki_kikan'] else int(0)
        kitai_bukka = self.to_dec(self.edit_inputs['kitai_bukka_j'] - self.edit_inputs['gonensai_rimawari'])
        lg_spread = self.to_dec(0.01)


        if proj_type == "DBO(SPCなし)" or proj_type == "BT/DB(いずれもSPCなし)":
            shisetsu_seibi_paymentschedule_ikkatsu = self.to_dec(1)
        else:         
            shisetsu_seibi_paymentschedule_ikkatsu = self.to_dec(self.edit_inputs['shisetsu_seibi_ikkatsu_hiritsu'])

        shisetsu_seibi_paymentschedule_kappu = self.to_dec(Decimal(1) - shisetsu_seibi_paymentschedule_ikkatsu)

        chisai_kinri = Decimal(self.edit_inputs['chisai_kinri'])/Decimal(100) # CSVの％表記を採取しているため、実数表記に切り替える。
        kijun_kinri = Decimal(self.edit_inputs["kijun_kinri"]) /Decimal(100) # CSVの％表記を採取しているため、実数表記に切り替える。
        kitai_bukka = Decimal(self.edit_inputs["kitai_bukka"]) /Decimal(100) # CSVの％表記を採取しているため、実数表記に切り替える。

        discount_rate = self.to_dec(kijun_kinri + kitai_bukka)

        const_years = int(self.target_inputs['const_years'])
        shoukan_kaishi_jiki = const_years + chisai_sueoki_kikan + 1
        ijikanri_unnei_years = self.target_inputs['ijikanri_unnei_years']

        lg_spread = self.to_dec(self.target_inputs['lg_spread'])
        kappu_kinri_spread = self.edit_inputs['kappu_kinri_spread']
        Kappu_kinri = kijun_kinri + lg_spread + kappu_kinri_spread
        Kappu_kinri = self.to_dec(Kappu_kinri)

        if proj_type == "DBO(SPCなし)" or proj_type == "BT/DB(いずれもSPCなし)":
            SPC_keihi = Decimal(0)
            SPC_fee = Decimal(0)
            SPC_shihon = Decimal(0)
            SPC_yobihi = Decimal(0)
        else:
            SPC_keihi = self.to_dec(self.edit_inputs['SPC_keihi'])
            SPC_fee = self.to_dec(self.edit_inputs['SPC_fee'])
            SPC_shihon = self.to_dec(self.edit_inputs['SPC_shihon'])
            SPC_yobihi = self.to_dec(self.edit_inputs['SPC_yobihi'])

        SPC_hiyou_total = SPC_keihi * ijikanri_unnei_years + SPC_shihon
        SPC_hiyou_nen = SPC_fee + SPC_keihi #公共がSPCに毎年払うコスト
        SPC_keihi_LCC = SPC_keihi + SPC_fee + self.target_inputs['houjinjuminzei_kintou'] #SPCが払うコスト(経費、手数料とも全て何かの使途に支払う前提)
        
        ijikanri_unnei = (
            Decimal(ijikanri_unnei_1) + 
            Decimal(ijikanri_unnei_2) + 
            Decimal(ijikanri_unnei_3))
        ijikanri_unnei_LCC = (
            Decimal(ijikanri_unnei_1_LCC) + 
            Decimal(ijikanri_unnei_2_LCC) + 
            Decimal(ijikanri_unnei_3_LCC))
        ijikanri_unnei_org = (
            Decimal(ijikanri_unnei_1_org) + 
            Decimal(ijikanri_unnei_2_org) + 
            Decimal(ijikanri_unnei_3_org))
        ijikanri_unnei_org_LCC = (
            Decimal(ijikanri_unnei_1_org_LCC) +
            Decimal(ijikanri_unnei_2_org_LCC) +
            Decimal(ijikanri_unnei_3_org_LCC))
        
        if proj_type == "DBO(SPCなし)" or proj_type == "BT/DB(いずれもSPCなし)":        
            edit_final_inputs = {
            #return   {
            "advisory_fee": str(self.edit_inputs['advisory_fee']),
            "chisai_kinri": str(chisai_kinri), 
            "chisai_shoukan_kikan": int(self.edit_inputs['chisai_shoukan_kikan']),
            "chisai_sueoki_years": int(self.edit_inputs['chisai_sueoki_kikan']),
            "const_start_date_year": int(self.target_inputs['const_start_date_year']),
            "const_start_date_month": int(self.target_inputs['const_start_date_month']),
            "const_start_date_day": int(self.target_inputs['const_start_date_day']),
            "const_start_date": const_start_date, 
            "const_years": int(const_years),
            "discount_rate": str(discount_rate),
            "first_end_fy": str(self.target_inputs['first_end_fy']),
            "fudousanshutokuzei_hyoujun": str(self.target_inputs["hudousanshutokuzei_hyoujun"]),
            "fudousanshutokuzei_ritsu": str(self.target_inputs["hudousanshutokuzei_ritsu"]),
            "growth": str(self.target_inputs["growth"]),
            "hojo_ritsu": [self.target_inputs["hojo_ritsu"]],
            "houjinzei_ritsu": str(self.target_inputs["houjinzei_ritsu"]),
            "houjinjuminzei_kintou": str(self.target_inputs["houjinjuminzei_kintou"]),
            "houjinjuminzei_ritsu_todouhuken": str(self.target_inputs["houjinjuminzei_ritsu_todouhuken"]),
            "houjinjuminzei_ritsu_shikuchoson": str(self.target_inputs["houjinjuminzei_ritsu_shikuchoson"]),
            "ijikanri_unnei": str(ijikanri_unnei),
            "ijikanri_unnei_LCC": str(ijikanri_unnei_LCC),
            "ijikanri_unnei_org": str(ijikanri_unnei_org),
            "ijikanri_unnei_org_LCC": str(ijikanri_unnei_org_LCC),
            "ijikanri_unnei_1": str(ijikanri_unnei_1),
            "ijikanri_unnei_1_LCC": str(ijikanri_unnei_1_LCC),
            "ijikanri_unnei_1_org": str(ijikanri_unnei_1_org),
            "ijikanri_unnei_1_org_LCC": str(ijikanri_unnei_1_org_LCC),
            "ijikanri_unnei_2": str(ijikanri_unnei_2),
            "ijikanri_unnei_2_LCC": str(ijikanri_unnei_2_LCC),
            "ijikanri_unnei_2_org": str(ijikanri_unnei_2_org),
            "ijikanri_unnei_2_org_LCC": str(ijikanri_unnei_2_org_LCC),
            "ijikanri_unnei_3": str(ijikanri_unnei_3),
            "ijikanri_unnei_3_LCC": str(ijikanri_unnei_3_LCC),
            "ijikanri_unnei_3_org": str(ijikanri_unnei_3_org),
            "ijikanri_unnei_3_org_LCC": str(ijikanri_unnei_3_org_LCC),
            "ijikanri_unnei_years": int(ijikanri_unnei_years),
            "kappu_kinri_spread": str(kappu_kinri_spread),
            "Kappu_kinri": str(Kappu_kinri),
            "kijun_kinri": str(kijun_kinri),
            "kisai_jutou": str(self.target_inputs["kisai_jutou"]),
            "kisai_koufu": str(self.target_inputs["kisai_koufu"]),
            "kitai_bukka": str(kitai_bukka),
            "koteishisanzei_hyoujun": str(self.target_inputs["koteishisanzei_hyoujun"]),
            "koteishisanzei_ritsu": str(self.target_inputs["koteishisanzei_ritsu"]),

            "lg_spread": str(self.target_inputs["lg_spread"]),
            "mgmt_type": self.target_inputs["mgmt_type"],
            "monitoring_costs_PSC": str(self.edit_inputs['monitoring_costs_PSC']),
            "monitoring_costs_LCC": str(self.edit_inputs['monitoring_costs_LCC']),

            "option_02": str(self.target_inputs['option_02']),
            "pre_kyoukouka": bool(self.target_inputs["pre_kyoukouka"]),
            "proj_ctgry": self.target_inputs["proj_ctgry"],
            "proj_type": self.target_inputs["proj_type"],
            "proj_years": int(self.target_inputs["proj_years"]),
            "rakusatsu_ritsu": str(self.target_inputs["rakusatsu_ritsu"]),
            "reduc_shisetsu": str(self.edit_inputs["reduc_shisetsu"]),
            "reduc_ijikanri_1": str(self.edit_inputs["reduc_ijikanri_1"]),
            "reduc_ijikanri_2": str(self.edit_inputs["reduc_ijikanri_2"]),
            "reduc_ijikanri_3": str(self.edit_inputs["reduc_ijikanri_3"]),
            "riyouryoukin_shunyu": str(self.target_inputs['riyouryoukin_shunyu']),

            "shisetsu_seibi": str(shisetsu_seibi),
            "shisetsu_seibi_LCC": str(shisetsu_seibi_LCC),
            "shisetsu_seibi_org": str(shisetsu_seibi_org),
            "shisetsu_seibi_org_LCC": str(shisetsu_seibi_org_LCC),
            "shisetsu_seibi_paymentschedule_ikkatsu": str(shisetsu_seibi_paymentschedule_ikkatsu),
            "shisetsu_seibi_paymentschedule_kappu": str(shisetsu_seibi_paymentschedule_kappu),
            "shoukan_kaishi_jiki": int(shoukan_kaishi_jiki),
            "SPC_keihi": str(SPC_keihi),
            "SPC_fee": str(SPC_fee),
            "SPC_shihon": str(SPC_shihon),
            "SPC_yobihi": str(SPC_yobihi),
            "SPC_hiyou_atsukai": int(1),
            "SPC_hiyou_total": str(SPC_hiyou_total),
            "SPC_hiyou_nen": str(SPC_hiyou_nen),
            "SPC_keihi_LCC": str(SPC_keihi_LCC),

            "target_years": int(self.target_inputs['target_years']),
            "tourokumenkyozei_hyoujun": str(self.target_inputs["tourokumenkyozei_hyoujun"]),
            "tourokumenkyozei_ritsu": str(self.target_inputs["tourokumenkyozei_ritsu"]),
            "yosantanka_hiritsu_shisetsu": str(self.target_inputs["yosantanka_hiritsu_shisetsu"]),
            "yosantanka_hiritsu_ijikanri_1": str(self.target_inputs["yosantanka_hiritsu_ijikanri_1"]),
            "yosantanka_hiritsu_ijikanri_2": str(self.target_inputs["yosantanka_hiritsu_ijikanri_2"]),
            "yosantanka_hiritsu_ijikanri_3": str(self.target_inputs["yosantanka_hiritsu_ijikanri_3"]),
            "zei_total": str(self.target_inputs["zei_total"]),

            }
        else:
            edit_final_inputs = {
            #return   {
            "advisory_fee": str(self.edit_inputs['advisory_fee']),
            "chisai_kinri": str(chisai_kinri), 
            "chisai_shoukan_kikan": int(self.edit_inputs['chisai_shoukan_kikan']),
            "chisai_sueoki_years": int(self.edit_inputs['chisai_sueoki_kikan']),
            "const_start_date_year": int(self.target_inputs['const_start_date_year']),
            "const_start_date_month": int(self.target_inputs['const_start_date_month']),
            "const_start_date_day": int(self.target_inputs['const_start_date_day']),
            "const_start_date": const_start_date, 
            "const_years": int(self.target_inputs["const_years"]),
            "discount_rate": str(discount_rate),

            "first_end_fy": str(self.target_inputs["first_end_fy"]),
            "fudousanshutokuzei_hyoujun": str(self.target_inputs["hudousanshutokuzei_hyoujun"]),
            "fudousanshutokuzei_ritsu": str(self.target_inputs["hudousanshutokuzei_ritsu"]),
            "growth": str(self.target_inputs["growth"]),
            "hojo_ritsu": self.target_inputs["hojo_ritsu"],
            "houjinzei_ritsu": str(self.target_inputs["houjinzei_ritsu"]),
            "houjinjuminzei_kintou": str(self.target_inputs["houjinjuminzei_kintou"]),
            "houjinjuminzei_ritsu_todouhuken": str(self.target_inputs["houjinjuminzei_ritsu_todouhuken"]),
            "houjinjuminzei_ritsu_shikuchoson": str(self.target_inputs["houjinjuminzei_ritsu_shikuchoson"]),
            "ijikanri_unnei": str(ijikanri_unnei),
            "ijikanri_unnei_LCC": str(ijikanri_unnei_LCC),
            "ijikanri_unnei_org": str(ijikanri_unnei_org),
            "ijikanri_unnei_org_LCC": str(ijikanri_unnei_org_LCC),
            "ijikanri_unnei_1": str(ijikanri_unnei_1),
            "ijikanri_unnei_1_LCC": str(ijikanri_unnei_1_LCC),
            "ijikanri_unnei_1_org": str(ijikanri_unnei_1_org),
            "ijikanri_unnei_1_org_LCC": str(ijikanri_unnei_1_org_LCC),
            "ijikanri_unnei_2": str(ijikanri_unnei_2),
            "ijikanri_unnei_2_LCC": str(ijikanri_unnei_2_LCC),
            "ijikanri_unnei_2_org": str(ijikanri_unnei_2_org),
            "ijikanri_unnei_2_org_LCC": str(ijikanri_unnei_2_org_LCC),
            "ijikanri_unnei_3": str(ijikanri_unnei_3),
            "ijikanri_unnei_3_LCC": str(ijikanri_unnei_3_LCC),
            "ijikanri_unnei_3_org": str(ijikanri_unnei_3_org),
            "ijikanri_unnei_3_org_LCC": str(ijikanri_unnei_3_org_LCC),
            "ijikanri_unnei_years": int(ijikanri_unnei_years),
            "kappu_kinri_spread": str(kappu_kinri_spread),
            "Kappu_kinri": str(Kappu_kinri),
            "kijun_kinri": str(kijun_kinri),
            "kisai_jutou": str(self.target_inputs["kisai_jutou"]),
            "kisai_koufu": str(self.target_inputs["kisai_koufu"]),
            "kitai_bukka": str(kitai_bukka), 
            "koteishisanzei_hyoujun": str(self.target_inputs["koteishisanzei_hyoujun"]),
            "koteishisanzei_ritsu": str(self.target_inputs["koteishisanzei_ritsu"]),

            "lg_spread": str(self.target_inputs["lg_spread"]),
            "mgmt_type": self.target_inputs["mgmt_type"],
            "monitoring_costs_PSC": str(self.edit_inputs['monitoring_costs_PSC']),
            "monitoring_costs_LCC": str(self.edit_inputs['monitoring_costs_LCC']),

            "option_02": str(self.target_inputs['option_02']),
            "pre_kyoukouka": bool(self.target_inputs["pre_kyoukouka"]),
            "proj_ctgry": self.target_inputs["proj_ctgry"],
            "proj_type": self.target_inputs["proj_type"],
            "proj_years": int(self.target_inputs["proj_years"]),
            "rakusatsu_ritsu": str(self.target_inputs["rakusatsu_ritsu"]),
            "reduc_shisetsu": str(self.edit_inputs["reduc_shisetsu"]),
            "reduc_ijikanri_1": str(self.edit_inputs["reduc_ijikanri_1"]),
            "reduc_ijikanri_2": str(self.edit_inputs["reduc_ijikanri_2"]),
            "reduc_ijikanri_3": str(self.edit_inputs["reduc_ijikanri_3"]),
            "riyouryoukin_shunyu": str(self.target_inputs['riyouryoukin_shunyu']),

            "shisetsu_seibi": str(shisetsu_seibi),
            "shisetsu_seibi_LCC": str(shisetsu_seibi_LCC),
            "shisetsu_seibi_org": str(shisetsu_seibi_org),
            "shisetsu_seibi_org_LCC": str(shisetsu_seibi_org_LCC),
            "shisetsu_seibi_paymentschedule_ikkatsu": str(shisetsu_seibi_paymentschedule_ikkatsu),
            "shisetsu_seibi_paymentschedule_kappu": str(shisetsu_seibi_paymentschedule_kappu),
            "shoukan_kaishi_jiki": int(shoukan_kaishi_jiki),
            "SPC_keihi": str(SPC_keihi),
            "SPC_fee": str(SPC_fee),
            "SPC_shihon": str(SPC_shihon),
            "SPC_yobihi": str(SPC_yobihi),
            "SPC_hiyou_atsukai": int(1),
            "SPC_hiyou_total": str(SPC_hiyou_total),
            "SPC_hiyou_nen": str(SPC_hiyou_nen),
            "SPC_keihi_LCC": str(SPC_keihi_LCC),

            "target_years": int(self.target_inputs['target_years']),
            "tourokumenkyozei_hyoujun": str(self.target_inputs["tourokumenkyozei_hyoujun"]),
            "tourokumenkyozei_ritsu": str(self.target_inputs["tourokumenkyozei_ritsu"]),
            "yosantanka_hiritsu_shisetsu": str(self.target_inputs["yosantanka_hiritsu_shisetsu"]),
            "yosantanka_hiritsu_ijikanri_1": str(self.target_inputs["yosantanka_hiritsu_ijikanri_1"]),
            "yosantanka_hiritsu_ijikanri_2": str(self.target_inputs["yosantanka_hiritsu_ijikanri_2"]),
            "yosantanka_hiritsu_ijikanri_3": str(self.target_inputs["yosantanka_hiritsu_ijikanri_3"]),
            "zei_total": str(self.target_inputs["zei_total"]),

            }
        return edit_final_inputs


# _save_to_db
    def _save_to_db(self, data):
        if self.page.session.store.contains_key("edit_final_inputs"):
            self.page.session.store.remove("edit_final_inputs")
        self.page.session.store.set("edit_final_inputs",data)
        if os.path.exists("ei_db.json"):
            os.remove("ei_db.json")
        db = TinyDB('ei_db.json')
        db.insert(data)
        db.close()



