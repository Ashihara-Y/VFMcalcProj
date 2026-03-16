import sys
sys.dont_write_bytecode = True
import os
import flet as ft
import pandas as pd
import datetime
import tinydb
from tinydb import TinyDB, Query
#import VFMcalc2 as vc
from VFMcalc2 import VFM_calc
#import save_results as sr
from decimal import *
import dateutil
import timeflake

@ft.control
class Final_Inputs(ft.Column):
    def init(self):
        #super().__init__()
        self.title = "最終入力・確認"
        self.width = 500
        self.height = 3000
        self.window_width = 500
        self.window_height = 2000
        self.resizable = True
        self.expand=True
        self.scroll=ft.ScrollMode.AUTO
        self.alignment=ft.MainAxisAlignment.START
        self.horizontal_alignment=ft.CrossAxisAlignment.START


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
        slider_value17 = ft.Text("", size=30, weight=ft.FontWeight.W_200)
        slider_value18 = ft.Text("", size=30, weight=ft.FontWeight.W_200)
        slider_value19 = ft.Text("", size=30, weight=ft.FontWeight.W_200)
        slider_value20 = ft.Text("", size=30, weight=ft.FontWeight.W_200)

        db = TinyDB("ii_db.json")
        self.initial_inputs = db.all()[0]   
        #self.initial_inputs.update(page.session.get("initial_inputs", {}))

        def handle_slider_change(e):
            sl_value = e.control.value
            target_text_control = e.control.data
            target_text_control.value = str(sl_value)
            target_text_control.update()


        date_format = '%Y-%m-%d'
        date_dt = datetime.datetime.strptime(self.initial_inputs["const_start_date"], date_format)
        const_start_year = date_dt.year
        const_start_month = date_dt.month
        const_start_day = date_dt.day

        tx0 = ft.Text(str("＜＜初期データ＞＞"))
        tx1 = ft.Text(str("発注者区分： " + str(self.initial_inputs["mgmt_type"])))
        tx2 = ft.Text(str("事業タイプ： " + str(self.initial_inputs["proj_ctgry"])))
        tx3 = ft.Text(str("事業方式： " + str(self.initial_inputs["proj_type"])))
        tx4 = ft.Text(str("事業期間： " + str(self.initial_inputs["proj_years"]) + "年"))
        tx5 = ft.Text(str("施設整備期間： " + str(self.initial_inputs["const_years"]) + "年"))
        tx6 = ft.Text(str("地方債償還据置期間： " + str(self.initial_inputs["chisai_sueoki_kikan"]) + "年"))
    
        dt1 = ft.DataTable(
            width=1800,
            data_row_max_height=80,
            heading_row_height=80,
            columns=[
                ft.DataColumn(ft.Text("事業費項目")),
                ft.DataColumn(ft.Text("入力値"), numeric=True),
                ft.DataColumn(ft.Text("競争の効果反映(PSC)"), numeric=True),
                ft.DataColumn(ft.Text("効率性反映(PFI-LCC)"), numeric=True), 
            ],         
            rows=[
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("施設整備費")),
                        ft.DataCell(ft.Text(self.initial_inputs["shisetsu_seibi_org"])),
                        ft.DataCell(ft.Text(self.initial_inputs["shisetsu_seibi"])),
                        ft.DataCell(ft.Text(self.initial_inputs["shisetsu_seibi_org_LCC"])),                
                        ],
                ),
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("維持管理運営費(人件費)")),
                        ft.DataCell(ft.Text(self.initial_inputs["ijikanri_unnei_1_org"])),
                        ft.DataCell(ft.Text(self.initial_inputs["ijikanri_unnei_1"])),
                        ft.DataCell(ft.Text(self.initial_inputs["ijikanri_unnei_1_org_LCC"])),                
                        ],
                ),
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("維持管理運営費(修繕費)")),
                        ft.DataCell(ft.Text(self.initial_inputs["ijikanri_unnei_2_org"])),
                        ft.DataCell(ft.Text(self.initial_inputs["ijikanri_unnei_2"])),
                        ft.DataCell(ft.Text(self.initial_inputs["ijikanri_unnei_2_org_LCC"])),                
                        ],
                ),
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("維持管理運営費(動力費)")),
                        ft.DataCell(ft.Text(self.initial_inputs["ijikanri_unnei_3_org"])),
                        ft.DataCell(ft.Text(self.initial_inputs["ijikanri_unnei_3"])),
                        ft.DataCell(ft.Text(self.initial_inputs["ijikanri_unnei_3_org_LCC"])),                
                        ],
                ),
            ],
        )
        dt2 = ft.DataTable(
            width=1800,
            columns=[
                ft.DataColumn(ft.Text("税目")),
                ft.DataColumn(ft.Text("標準／均等割"), numeric=True),
                ft.DataColumn(ft.Text("税率"), numeric=True),
            ],         
            rows=[
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("法人税")),
                        ft.DataCell(ft.Text("-")),
                        ft.DataCell(ft.Text(self.initial_inputs["houjinzei_ritsu"])),
                        ],
                ),
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("法人住民税(都道府県)")),
                        ft.DataCell(ft.Text(self.initial_inputs["houjinjuminzei_kintou"])),
                        ft.DataCell(ft.Text(self.initial_inputs["houjinjuminzei_ritsu_todouhuken"])),
                        ],
                ),
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("法人住民税(市区町村)")),
                        ft.DataCell(ft.Text(self.initial_inputs["houjinjuminzei_kintou"])),
                        ft.DataCell(ft.Text(self.initial_inputs["houjinjuminzei_ritsu_shikuchoson"])),
                        ],
                ),
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("不動産取得税")),
                        ft.DataCell(ft.Text(self.initial_inputs["hudousanshutokuzei_hyoujun"])),
                        ft.DataCell(ft.Text(self.initial_inputs["hudousanshutokuzei_ritsu"])),
                        ],
                ),
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("固定資産税")),
                        ft.DataCell(ft.Text(self.initial_inputs["koteishisanzei_hyoujun"])),
                        ft.DataCell(ft.Text(self.initial_inputs["koteishisanzei_ritsu"])),
                        ],
                ),
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("登録免許税")),
                        ft.DataCell(ft.Text(self.initial_inputs["tourokumenkyozei_hyoujun"])),
                        ft.DataCell(ft.Text(self.initial_inputs["tourokumenkyozei_ritsu"])),
                        ],
                ),
            ],
        )

        tx7 = ft.Text("地方債償還期間(年)")
        self.sl1 = ft.Slider(
            value=int(self.initial_inputs["chisai_shoukan_kikan"]),
            min=0,
            max=30,
            divisions=30,
            label="{value}年",
            round=0,
            on_change=handle_slider_change,
            data=slider_value01,
        )
        tx8 = ft.Text("施設整備費支払 一括払の比率(%)")
        self.sl2 = ft.Slider(
            value=50,
            min=0.0,
            max=100,
            divisions=100,
            label="{value}%",
            round=1,
            on_change=handle_slider_change,
            data=slider_value02,
        )
        tx9 = ft.Text("モニタリング等費用(PSC)(百万円、BT/DB:5程度、その他:10程度)")
        self.sl3 = ft.Slider(
            value=0,
            min=0,
            max=50,
            divisions=50,
            label="{value}百万円",
            round=1,
            on_change=handle_slider_change,
            data=slider_value03,
        )
        tx10 = ft.Text("モニタリング等費用(PFI-LCC)(百万円、BT/DB:3程度、その他:6程度)")
        self.sl4 = ft.Slider(
            value=0,
            min=0,
            max=50,
            divisions=50,
            label="{value}百万円",
            round=1,
            on_change=handle_slider_change,
            data=slider_value04,
        )
        tx11 = ft.Text("起債充当率(%)")
        self.sl5 = ft.Slider(
            value:=Decimal(self.initial_inputs["kisai_jutou"])*100,
            min=0.0,
            max=100.0,
            divisions=100,
            label="{value}%",
            round=1,
            on_change=handle_slider_change,
            data=slider_value05,
        )
        tx12 = ft.Text("起債への交付金カバー率(%)")
        self.sl6 = ft.Slider(
            value:=Decimal(self.initial_inputs["kisai_koufu"])*100,
            min=0.0,
            max=50.0,
            divisions=50,
            label="{value}%",
            round=1,
            on_change=handle_slider_change,
            data=slider_value06,
        )
        tx13 = ft.Text("補助率(%)")
        self.sl7 = ft.Slider(
            value:=Decimal(self.initial_inputs["hojo_ritsu"])*100,
            min=0.0,
            max=70.0,
            divisions=700,
            label="{value}%",
            round=1,
            on_change=handle_slider_change,
            data=slider_value07,
        )
        tx14 = ft.Text("SPC経費年額(百万円)")
        self.sl8 = ft.Slider(
            value:=Decimal(self.initial_inputs["SPC_keihi"]),
            min=0,
            max=50,
            divisions=50,
            label="{value}百万円",
            round=1,
            on_change=handle_slider_change,
            data=slider_value08,
        )
        tx15 = ft.Text("SPCへの手数料(百万円)")
        self.sl9 = ft.Slider(
            value:=Decimal(self.initial_inputs["SPC_fee"]),
            min=0,
            max=50,
            divisions=50,
            label="{value}百万円",
            round=1,
            on_change=handle_slider_change,
            data=slider_value09,
        )
        tx16 = ft.Text("SPC資本金(百万円)")
        self.sl10 = ft.Slider(
            value:=Decimal(self.initial_inputs["SPC_shihon"]),
            min=0,
            max=100,
            divisions=100,
            label="{value}百万円",
            round=1,
            on_change=handle_slider_change,
            data=slider_value10,
        )
        tx17 = ft.Text("SPC予備費(百万円)")
        self.sl11 = ft.Slider(
            value:=Decimal(self.initial_inputs["SPC_yobihi"]),
            min=0,
            max=1000,
            divisions=1000,
            label="{value}百万円",
            round=1,
            on_change=handle_slider_change,
            data=slider_value11,
        )
        self.sw01 = ft.Switch(
            label="SPC経費の扱い（デフォルト：サービス対価で支払）",
            value=1,
        )
        tx19 = ft.Text("アドバイザリー等経費(百万円)")
        self.sl13 = ft.Slider(
            value=0,
            min=0,
            max=50,
            divisions=50,
            label="{value}百万円",
            round=1,
            on_change=self.handle_change_13,
        )
        tx20 = ft.Text("利用料金収入(百万円)")
        self.sl14 = ft.Slider(
            value:=self.initial_inputs["riyou_ryoukin"],
            min=0,
            max=100,
            divisions=100,
            label="{value}百万円",
            round=1,
            on_change=handle_slider_change,
            data=slider_value14,
        )
        tx21 = ft.Text("割賦金利へのスプレッド(%)")
        self.sl15 = ft.Slider(
            value=0.00,
            min=0.00,
            max=2.00,
            divisions=200,
            label="{value}％",
            round=2,
            on_change=handle_slider_change,
            data=slider_value15,
        )
        self.dd00 = ft.Dropdown(
            value=const_start_year,
            label="施設整備開始年",
            hint_text="施設整備開始年を選択してください",
            width=400,
            options=[
                ft.dropdown.Option(str(const_start_year)), 
                ft.dropdown.Option(str(const_start_year+1)), 
                ft.dropdown.Option(str(const_start_year+2)), 
                ft.dropdown.Option(str(const_start_year+3)),
                ft.dropdown.Option(str(const_start_year+4)), 
                ft.dropdown.Option(str(const_start_year+5)), 
                ft.dropdown.Option(str(const_start_year+6)),
                ft.dropdown.Option(str(const_start_year+7)), 
                ft.dropdown.Option(str(const_start_year+8)), 
                ft.dropdown.Option(str(const_start_year+9)),
                ft.dropdown.Option(str(const_start_year+10)),
            ],
        )
        self.dd01 = ft.Dropdown(
            label="施設整備開始月",
            hint_text="施設整備開始月を選択してください",
            width=400,
            value=const_start_month,
            options=[
                ft.dropdown.Option("1"),  ft.dropdown.Option("2"),  ft.dropdown.Option("3"),
                ft.dropdown.Option("4"),  ft.dropdown.Option("5"),  ft.dropdown.Option("6"),
                ft.dropdown.Option("7"),  ft.dropdown.Option("8"),  ft.dropdown.Option("9"),
                ft.dropdown.Option("10"), ft.dropdown.Option("11"), ft.dropdown.Option("12"),
            ],
        )
        self.dd02 = ft.Dropdown(
            label="施設整備開始日",
            hint_text="施設整備開始日を選択してください",
            width=400,
            value=const_start_day,
            options=[
                ft.dropdown.Option("1"),  ft.dropdown.Option("2"),  ft.dropdown.Option("3"),
                ft.dropdown.Option("4"),  ft.dropdown.Option("5"),  ft.dropdown.Option("6"),
                ft.dropdown.Option("7"),  ft.dropdown.Option("8"),  ft.dropdown.Option("9"),
                ft.dropdown.Option("10"), ft.dropdown.Option("11"), ft.dropdown.Option("12"),
                ft.dropdown.Option("13"), ft.dropdown.Option("14"), ft.dropdown.Option("15"),
                ft.dropdown.Option("16"), ft.dropdown.Option("17"), ft.dropdown.Option("18"),
                ft.dropdown.Option("19"), ft.dropdown.Option("20"), ft.dropdown.Option("21"),
                ft.dropdown.Option("22"), ft.dropdown.Option("23"), ft.dropdown.Option("24"),
                ft.dropdown.Option("25"), ft.dropdown.Option("26"), ft.dropdown.Option("27"),
                ft.dropdown.Option("28"), ft.dropdown.Option("29"), ft.dropdown.Option("30"),
                ft.dropdown.Option("31"), 
            ],
        )
        tx25 = ft.Text("地方債償還据置期間")
        self.sl19 = ft.Slider(
            value=self.initial_inputs['chisai_sueoki_kikan'],
            min=0,
            max=5,
            divisions=5,
            label="{value}年",
            on_change=handle_slider_change,
            data=slider_value19,
        )
        tx26 = ft.Text("予備入力")
        self.sl20 = ft.Slider(
            value=0,
            min=0,
            max=1,
            divisions=100,
            label="{value}",
            on_change=handle_slider_change,
            data=slider_value20,
        )
        b = ft.ElevatedButton(text="入力確認・計算", on_click=self.button_clicked)

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
            item_extent=1500,
            first_item_prototype=False,
            horizontal=False,
        )
        fi_lv3 = ft.ListView(
            expand=True,
            spacing=10,
            padding=5,
            #auto_scroll=True,
            item_extent=1500,
            first_item_prototype=False,
            horizontal=False,
        )
        fi_lv1.controls= [
            tx0, tx1, tx2, tx3, tx4, tx5, tx6,
            dt1, dt2, ft.Divider(height=1, color="amber"),
        ]
        fi_lv2.controls= [
                    tx7, slider_value01, self.sl1,  ft.Divider(height=1, color="amber"), 
                    tx25, slider_value19, self.sl19, ft.Divider(height=1, color="amber"),
                    tx8, slider_value02, self.sl2, ft.Divider(height=1, color="amber"),
                    tx9, slider_value03, self.sl3, ft.Divider(height=1, color="amber"),
                    tx10,slider_value04, self.sl4, ft.Divider(height=1, color="amber"),
                    tx11,slider_value05, self.sl5,  ft.Divider(height=1, color="amber"),
                    tx12,slider_value06, self.sl6,  ft.Divider(height=1, color="amber"),
                    tx13,slider_value07, self.sl7,  ft.Divider(height=1, color="amber"),
                    tx14,slider_value08, self.sl8,  ft.Divider(height=1, color="amber"),
                    tx15,slider_value09, self.sl9,  ft.Divider(height=1, color="amber"),
                    tx16,slider_value10, self.sl10, ft.Divider(height=1, color="amber"),
                    tx17,slider_value11, self.sl11, ft.Divider(height=1, color="amber"),
                    self.sw01,ft.Divider(height=1, color="amber"),
                    tx19,slider_value13, self.sl13, ft.Divider(height=1, color="amber"),
                    tx20,slider_value14, self.sl14, ft.Divider(height=1, color="amber"),
                    tx21,slider_value15, self.sl15, ft.Divider(height=1, color="amber"),
                    self.dd00,self.dd01,self.dd02, ft.Divider(height=1, color="amber"),
                    tx26,slider_value20, self.sl20, ft.Divider(height=1, color="amber"),
                    b,

        ]        
        fi_lv3.controls= [
                    self.tx7, slider_value01, self.sl1,  ft.Divider(height=1, color="amber"), 
                    self.tx25, slider_value19,self.sl19, ft.Divider(height=1, color="amber"), 
                    self.tx9, slider_value03, self.sl3,  ft.Divider(height=1, color="amber"),
                    self.tx10,slider_value04, self.sl4,  ft.Divider(height=1, color="amber"),
                    self.tx11,slider_value05, self.sl5,  ft.Divider(height=1, color="amber"),
                    self.tx12,slider_value06, self.sl6,  ft.Divider(height=1, color="amber"),
                    self.tx13,slider_value07, self.sl7,  ft.Divider(height=1, color="amber"),
                    self.tx19,slider_value13, self.sl13, ft.Divider(height=1, color="amber"),
                    self.dd00,self.dd01,self.dd02, ft.Divider(height=1, color="amber"), 
                    self.tx26,slider_value20, self.sl20, ft.Divider(height=1, color="amber"),
                    b,

        ]        
        if self.initial_inputs["proj_type"] == "DBO(SPCなし)" or self.initial_inputs["proj_type"] == "BT/DB(いずれもSPCなし)":
            self.controls = [ft.Container(
                content=ft.Column(controls=[
                        fi_lv1,
                        fi_lv3,
                    ],
                    #scroll=ft.ScrollMode.HIDDEN,
                    alignment=ft.MainAxisAlignment.START,
                    horizontal_alignment=ft.CrossAxisAlignment.START,            #height=2000,
                    width=float("inf"),
                    height=2000,
                    spacing=10,
                    #expand=True,
                ),
                    width=float("inf"),
                    height=2100,
                    padding=10,
                    margin=10,
            )]
        else:
            self.controls = [ft.Container(
                content=ft.Column(controls=[
                        fi_lv1,
                        fi_lv2,
                    ],
                    #scroll=ft.ScrollMode.HIDDEN,
                    alignment=ft.MainAxisAlignment.START,
                    horizontal_alignment=ft.CrossAxisAlignment.START,            #height=2000,
                    width=float("inf"),
                    height=2000,
                    spacing=10,
                    #expand=True,
                ),
                    width=float("inf"),
                    height=2100,
                    padding=10,
                    margin=10,
            )]

    def button_clicked(self, e):
        input_data = self._extract_inputs()

        calc_results = self._calculate_financials(input_data)
        
        self._save_to_db(calc_results)
        self.page.push_route("/final_inputs")

    def _extract_inputs(self):
        const_start_date_year = int(self.dd00.value)
        const_start_date_month = int(self.dd01.value)
        const_start_date_day = int(self.dd02.value)

        chisai_shoukan_kikan = int(self.sl1.value)
        shisetsu_seibi_ikkatsu_hiritsu = Decimal(self.sl2.value)/Decimal(100)
        monitoring_costs_PSC = Decimal(self.sl3.value)
        monitoring_costs_LCC = Decimal(self.sl4.value)
        kisai_jutou = Decimal(self.sl5.value)/Decimal(100)
        kisai_koufu = Decimal(self.sl6.value)/Decimal(100)
        hojo_ritsu = Decimal(self.sl7.value)/Decimal(100)
        SPC_keihi = Decimal(self.sl8.value)
        SPC_fee = Decimal(self.sl9.value)
        SPC_shihon = Decimal(self.sl10.value)
        SPC_yobihi = Decimal(self.sl11.value)

        advisory_fee = Decimal(self.sl13.value)
        riyouryoukin_shunyu = Decimal(self.sl14.value)
        kappu_kinri_spread = Decimal(self.sl15.value)/Decimal(100)
        
        chisai_sueoki_kikan = int(self.sl19.value)
        option_02 = Decimal(self.sl20.value)

        return {
            'const_start_date_year': const_start_date_year,
            'const_start_date_month': const_start_date_month,
            'const_start_date_day': const_start_date_day,

            'chisai_shoukan_kikan': chisai_shoukan_kikan,
            'shisetsu_seibi_ikkatsu_hiritsu': shisetsu_seibi_ikkatsu_hiritsu,
            'monitoring_costs_PSC': monitoring_costs_PSC,
            'monitoring_costs_LCC': monitoring_costs_LCC,
            'kisai_jutou': kisai_jutou,
            'kisai_koufu': kisai_koufu,
            'hojo_ritsu': hojo_ritsu,
            'SPC_keihi': SPC_keihi,
            'SPC_fee': SPC_fee,
            'SPC_shihon': SPC_shihon,
            'SPC_yobihi': SPC_yobihi,

            'advisory_fee': advisory_fee,
            'riyouryoukin_shunyu': riyouryoukin_shunyu,
            'kappu_kinri_spread': kappu_kinri_spread,
            'chisai_sueoki_kikan': chisai_sueoki_kikan,
            'option_02': option_02,
            }
        
    def _calculate_financials(self,inputs):
        def to_dec(val):
            return Decimal(val).quantize(Decimal('0.000001'), ROUND_HALF_UP)

        if self.initial_inputs["proj_type"] == "DBO(SPCなし)" or self.initial_inputs["proj_type"] == "BT/DB(いずれもSPCなし)":
            shisetsu_seibi_paymentschedule_ikkatsu = Decimal(1).quantize(Decimal('0.000001'), ROUND_HALF_UP)
        else:         
            shisetsu_seibi_paymentschedule_ikkatsu = inputs['shisetsu_seibi_ikkatsu_hiritsu']

        shisetsu_seibi_paymentschedule_kappu = to_dec(Decimal(1) - shisetsu_seibi_paymentschedule_ikkatsu)
        #kappu_kinri_spread = Decimal(self.sl15.value/100).quantize(Decimal('0.000001'), ROUND_HALF_UP),

        kisai_jutou = str(kisai_jutou)
        kisai_koufu = str(kisai_koufu)
        hojo_ritsu = str(hojo_ritsu)

        const_start_date_year = inputs['const_start_date_year']
        const_start_date_month = inputs['const_start_date_month']
        const_start_date_day = inputs['const_start_date_day']
        const_start_date = str(datetime.date(const_start_date_year, const_start_date_month, const_start_date_day))
        start_year = datetime.datetime.strptime(str(const_start_date), '%Y-%m-%d').year
        start_month = datetime.datetime.strptime(str(const_start_date), '%Y-%m-%d').month

        if start_month < 4:
            first_end_fy = datetime.date(start_year, 3, 31)
        else:
            first_end_fy = datetime.date(start_year + 1, 3, 31)

        #chisai_kinri = Decimal(self.initial_inputs['chisai_kinri']) / Decimal(100) # CSVの％表記を採取しているため、実数表記に切り替える。
        kijun_kinri = Decimal(self.initial_inputs["kijun_kinri"]) /Decimal(100) # CSVの％表記を採取しているため、実数表記に切り替える。
        kitai_bukka = Decimal(self.initial_inputs["kitai_bukka"]) /Decimal(100) # CSVの％表記を採取しているため、実数表記に切り替える。

        discount_rate = kijun_kinri + kitai_bukka
        discount_rate = to_dec(discount_rate)

        target_years = 45
        #proj_years = int(self.initial_inputs['proj_years'])
        const_years = int(self.initial_inputs['const_years'])
        chisai_sueoki_kikan = inputs['chisai_sueoki_kikan']
        shoukan_kaishi_jiki = const_years + chisai_sueoki_kikan + 1

        lg_spread = to_dec(self.initial_inputs['lg_spread'])
        kappu_kinri_spread = inputs['kappu_kinri_spread']
        Kappu_kinri = kijun_kinri + lg_spread + kappu_kinri_spread
        Kappu_kinri = to_dec(Kappu_kinri)

        JRB_rates_df = pd.read_csv(
            "src/JRB_rates.csv",
            encoding="utf-8",
            sep='\t', 
            names=[0,1,2,3,4,5], 
            index_col=0)

        chisai_shoukan_kikan = inputs['chisai_shoukan_kikan']
        chisai_kinri = JRB_rates_df.loc[chisai_shoukan_kikan][chisai_sueoki_kikan]
        # First_end_fyを1年追加する必要があるのか、算定シートを確認する必要がある。
        #first_end_fy = first_end_fy + dateutil.relativedelta.relativedelta(year=1)

        if self.initial_inputs["proj_type"] == "DBO(SPCなし)" or self.initial_inputs["proj_type"] == "BT/DB(いずれもSPCなし)":
            SPC_keihi = Decimal(0)
            SPC_fee = Decimal(0)
            SPC_shihon = Decimal(0)
            SPC_yobihi = Decimal(0)
        else:
            SPC_keihi = inputs['SPC_keihi']
            SPC_fee = inputs['SPC_fee']
            SPC_shihon = inputs['SPC_shihon']
            SPC_yobihi = inputs['SPC_yobihi']

        ijikanri_unnei_years = int(self.initial_inputs['ijikanri_unnei_years'])
        houjinjuminzei_kintou = Decimal(self.initial_inputs['houjinjuminzei_kintou'])
        SPC_hiyou_total = SPC_keihi * ijikanri_unnei_years + SPC_shihon
        SPC_hiyou_nen = SPC_fee + SPC_keihi #公共がSPCに毎年払うコスト
        SPC_keihi_LCC = SPC_keihi + SPC_fee + houjinjuminzei_kintou #SPCが払うコスト
        
        chisai_kinri = chisai_kinri / Decimal(100) # CSVの％表記を採取しているため、実数表記に切り替える。
        #kijun_kinri = Decimal(self.initial_inputs["kijun_kinri"]) /100 # 上記と重複　CSVの％表記を採取しているため、実数表記に切り替える。
        #kitai_bukka = Decimal(self.initial_inputs["kitai_bukka"]) /100 # 上記と重複　CSVの％表記を採取しているため、実数表記に切り替える。

        ijikanri_unnei = (
            Decimal(self.initial_inputs["ijikanri_unnei_1"]) + 
            Decimal(self.initial_inputs["ijikanri_unnei_2"]) + 
            Decimal(self.initial_inputs["ijikanri_unnei_3"]))
        ijikanri_unnei_LCC = (
            Decimal(self.initial_inputs["ijikanri_unnei_1_LCC"]) + 
            Decimal(self.initial_inputs["ijikanri_unnei_2_LCC"]) + 
            Decimal(self.initial_inputs["ijikanri_unnei_3_LCC"]))
        ijikanri_unnei_org = (
            Decimal(self.initial_inputs["ijikanri_unnei_1_org"]) + 
            Decimal(self.initial_inputs["ijikanri_unnei_2_org"]) + 
            Decimal(self.initial_inputs["ijikanri_unnei_3_org"]))
        ijikanri_unnei_org_LCC = (
            Decimal(self.initial_inputs["ijikanri_unnei_1_org_LCC"]) +
            Decimal(self.initial_inputs["ijikanri_unnei_2_org_LCC"]) +
            Decimal(self.initial_inputs["ijikanri_unnei_3_org_LCC"]))
        
        if self.initial_inputs["proj_type"] == "DBO(SPCなし)" or self.initial_inputs["proj_type"] == "BT/DB(いずれもSPCなし)":        
            final_inputs = {
            "advisory_fee": str(inputs['advisory_fee']),
            "chisai_kinri": str(chisai_kinri), 
            "chisai_shoukan_kikan": int(chisai_shoukan_kikan),
            "chisai_sueoki_years": int(chisai_sueoki_kikan),
            "const_start_date_year": int(const_start_date_year),
            "const_start_date_month": int(const_start_date_month),
            "const_start_date_day": int(const_start_date_day),
            "const_start_date": const_start_date, 
            "const_years": int(const_years),
            "discount_rate": str(discount_rate),
            "first_end_fy": str(first_end_fy),
            "fudousanshutokuzei_hyoujun": str(self.initial_inputs["hudousanshutokuzei_hyoujun"]),
            "fudousanshutokuzei_ritsu": str(self.initial_inputs["hudousanshutokuzei_ritsu"]),
            "growth": str(self.initial_inputs["growth"]),
            "hojo_ritsu": hojo_ritsu,
            "houjinzei_ritsu": str(self.initial_inputs["houjinzei_ritsu"]),
            "houjinjuminzei_kintou": str(self.initial_inputs["houjinjuminzei_kintou"]),
            "houjinjuminzei_ritsu_todouhuken": str(self.initial_inputs["houjinjuminzei_ritsu_todouhuken"]),
            "houjinjuminzei_ritsu_shikuchoson": str(self.initial_inputs["houjinjuminzei_ritsu_shikuchoson"]),
            "ijikanri_unnei": str(ijikanri_unnei),
            "ijikanri_unnei_LCC": str(ijikanri_unnei_LCC),
            "ijikanri_unnei_org": str(ijikanri_unnei_org),
            "ijikanri_unnei_org_LCC": str(ijikanri_unnei_org_LCC),
            "ijikanri_unnei_1": str(self.initial_inputs["ijikanri_unnei_1"]),
            "ijikanri_unnei_1_LCC": str(self.initial_inputs["ijikanri_unnei_1_LCC"]),
            "ijikanri_unnei_1_org": str(self.initial_inputs["ijikanri_unnei_1_org"]),
            "ijikanri_unnei_1_org_LCC": str(self.initial_inputs["ijikanri_unnei_1_org_LCC"]),
            "ijikanri_unnei_2": str(self.initial_inputs["ijikanri_unnei_2"]),
            "ijikanri_unnei_2_LCC": str(self.initial_inputs["ijikanri_unnei_2_LCC"]),
            "ijikanri_unnei_2_org": str(self.initial_inputs["ijikanri_unnei_2_org"]),
            "ijikanri_unnei_2_org_LCC": str(self.initial_inputs["ijikanri_unnei_2_org_LCC"]),
            "ijikanri_unnei_3": str(self.initial_inputs["ijikanri_unnei_3"]),
            "ijikanri_unnei_3_LCC": str(self.initial_inputs["ijikanri_unnei_3_LCC"]),
            "ijikanri_unnei_3_org": str(self.initial_inputs["ijikanri_unnei_3_org"]),
            "ijikanri_unnei_3_org_LCC": str(self.initial_inputs["ijikanri_unnei_3_org_LCC"]),
            "ijikanri_unnei_years": int(ijikanri_unnei_years),
            "kappu_kinri_spread": str(kappu_kinri_spread),
            "Kappu_kinri": str(Kappu_kinri),
            "kijun_kinri": str(kijun_kinri),
            "kisai_jutou": kisai_jutou,
            "kisai_koufu": kisai_koufu,
            "kitai_bukka": str(kitai_bukka), 
            "koteishisanzei_hyoujun": str(self.initial_inputs["koteishisanzei_hyoujun"]),
            "koteishisanzei_ritsu": str(self.initial_inputs["koteishisanzei_ritsu"]),

            "lg_spread": str(self.initial_inputs["lg_spread"]),
            "mgmt_type": self.initial_inputs["mgmt_type"],
            "monitoring_costs_PSC": str(inputs['monitoring_costs_PSC']),
            "monitoring_costs_LCC": str(inputs['monitoring_costs_LCC']),

            "option_02": str(inputs['option_02']),
            "pre_kyoukouka": bool(self.initial_inputs["pre_kyoukouka"]),
            "proj_ctgry": self.initial_inputs["proj_ctgry"],
            "proj_type": self.initial_inputs["proj_type"],
            "proj_years": int(self.initial_inputs["proj_years"]),
            "rakusatsu_ritsu": str(self.initial_inputs["rakusatsu_ritsu"]),
            "reduc_shisetsu": str(self.initial_inputs["reduc_shisetsu"]),
            "reduc_ijikanri_1": str(self.initial_inputs["reduc_ijikanri_1"]),
            "reduc_ijikanri_2": str(self.initial_inputs["reduc_ijikanri_2"]),
            "reduc_ijikanri_3": str(self.initial_inputs["reduc_ijikanri_3"]),
            "riyouryoukin_shunyu": str(inputs['riyouryoukin_shunyu']),

            "shisetsu_seibi": str(self.initial_inputs["shisetsu_seibi"]),
            "shisetsu_seibi_LCC": str(self.initial_inputs["shisetsu_seibi_LCC"]),
            "shisetsu_seibi_org": str(self.initial_inputs["shisetsu_seibi_org"]),
            "shisetsu_seibi_org_LCC": str(self.initial_inputs["shisetsu_seibi_org_LCC"]),
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

            "target_years": int(target_years),
            "tourokumenkyozei_hyoujun": str(self.initial_inputs["tourokumenkyozei_hyoujun"]),
            "tourokumenkyozei_ritsu": str(self.initial_inputs["tourokumenkyozei_ritsu"]),
            "yosantanka_hiritsu_shisetsu": str(self.initial_inputs["yosantanka_hiritsu_shisetsu"]),
            "yosantanka_hiritsu_ijikanri_1": str(self.initial_inputs["yosantanka_hiritsu_ijikanri_1"]),
            "yosantanka_hiritsu_ijikanri_2": str(self.initial_inputs["yosantanka_hiritsu_ijikanri_2"]),
            "yosantanka_hiritsu_ijikanri_3": str(self.initial_inputs["yosantanka_hiritsu_ijikanri_3"]),
            "zei_total": str(self.initial_inputs["zei_total"]),

            }
        else:
            final_inputs = {
            "advisory_fee": str(inputs['advisory_fee']),
            "chisai_kinri": str(chisai_kinri), 
            "chisai_shoukan_kikan": int(self.sl1.value),
            "chisai_sueoki_years": int(self.initial_inputs["chisai_sueoki_kikan"]),
            "const_start_date_year": int(inputs['const_start_date_year']),
            "const_start_date_month": int(inputs['const_start_date_month']),
            "const_start_date_day": int(inputs['const_start_date_day']),
            "const_start_date": const_start_date, 
            "const_years": int(self.initial_inputs["const_years"]),
            "discount_rate": str(discount_rate),

            "first_end_fy": str(first_end_fy),
            "fudousanshutokuzei_hyoujun": str(self.initial_inputs["hudousanshutokuzei_hyoujun"]),
            "fudousanshutokuzei_ritsu": str(self.initial_inputs["hudousanshutokuzei_ritsu"]),
            "growth": str(self.initial_inputs["growth"]),
            "hojo_ritsu": hojo_ritsu,
            "houjinzei_ritsu": str(self.initial_inputs["houjinzei_ritsu"]),
            "houjinjuminzei_kintou": str(self.initial_inputs["houjinjuminzei_kintou"]),
            "houjinjuminzei_ritsu_todouhuken": str(self.initial_inputs["houjinjuminzei_ritsu_todouhuken"]),
            "houjinjuminzei_ritsu_shikuchoson": str(self.initial_inputs["houjinjuminzei_ritsu_shikuchoson"]),
            "ijikanri_unnei": str(ijikanri_unnei),
            "ijikanri_unnei_LCC": str(ijikanri_unnei_LCC),
            "ijikanri_unnei_org": str(ijikanri_unnei_org),
            "ijikanri_unnei_org_LCC": str(ijikanri_unnei_org_LCC),
            "ijikanri_unnei_1": str(self.initial_inputs["ijikanri_unnei_1"]),
            "ijikanri_unnei_1_LCC": str(self.initial_inputs["ijikanri_unnei_1_LCC"]),
            "ijikanri_unnei_1_org": str(self.initial_inputs["ijikanri_unnei_1_org"]),
            "ijikanri_unnei_1_org_LCC": str(self.initial_inputs["ijikanri_unnei_1_org_LCC"]),
            "ijikanri_unnei_2": str(self.initial_inputs["ijikanri_unnei_2"]),
            "ijikanri_unnei_2_LCC": str(self.initial_inputs["ijikanri_unnei_2_LCC"]),
            "ijikanri_unnei_2_org": str(self.initial_inputs["ijikanri_unnei_2_org"]),
            "ijikanri_unnei_2_org_LCC": str(self.initial_inputs["ijikanri_unnei_2_org_LCC"]),
            "ijikanri_unnei_3": str(self.initial_inputs["ijikanri_unnei_3"]),
            "ijikanri_unnei_3_LCC": str(self.initial_inputs["ijikanri_unnei_3_LCC"]),
            "ijikanri_unnei_3_org": str(self.initial_inputs["ijikanri_unnei_3_org"]),
            "ijikanri_unnei_3_org_LCC": str(self.initial_inputs["ijikanri_unnei_3_org_LCC"]),
            "ijikanri_unnei_years": int(ijikanri_unnei_years),
            "kappu_kinri_spread": str(kappu_kinri_spread),
            "Kappu_kinri": str(Kappu_kinri),
            "kijun_kinri": str(kijun_kinri),
            "kisai_jutou": kisai_jutou,
            "kisai_koufu": kisai_koufu,
            "kitai_bukka": str(kitai_bukka), 
            "koteishisanzei_hyoujun": str(self.initial_inputs["koteishisanzei_hyoujun"]),
            "koteishisanzei_ritsu": str(self.initial_inputs["koteishisanzei_ritsu"]),

            "lg_spread": str(self.initial_inputs["lg_spread"]),
            "mgmt_type": self.initial_inputs["mgmt_type"],
            "monitoring_costs_PSC": str(inputs['monitoring_costs_PSC']),
            "monitoring_costs_LCC": str(inputs['monitoring_costs_LCC']),

            "option_02": str(inputs['option_02']),
            "pre_kyoukouka": bool(self.initial_inputs["pre_kyoukouka"]),
            "proj_ctgry": self.initial_inputs["proj_ctgry"],
            "proj_type": self.initial_inputs["proj_type"],
            "proj_years": int(self.initial_inputs["proj_years"]),
            "rakusatsu_ritsu": str(self.initial_inputs["rakusatsu_ritsu"]),
            "reduc_shisetsu": str(self.initial_inputs["reduc_shisetsu"]),
            "reduc_ijikanri_1": str(self.initial_inputs["reduc_ijikanri_1"]),
            "reduc_ijikanri_2": str(self.initial_inputs["reduc_ijikanri_2"]),
            "reduc_ijikanri_3": str(self.initial_inputs["reduc_ijikanri_3"]),
            "riyouryoukin_shunyu": str(inputs['riyouryoukin_shunyu']),

            "shisetsu_seibi": str(self.initial_inputs["shisetsu_seibi"]),
            "shisetsu_seibi_LCC": str(self.initial_inputs["shisetsu_seibi_LCC"]),
            "shisetsu_seibi_org": str(self.initial_inputs["shisetsu_seibi_org"]),
            "shisetsu_seibi_org_LCC": str(self.initial_inputs["shisetsu_seibi_org_LCC"]),
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

            "target_years": int(target_years),
            "tourokumenkyozei_hyoujun": str(self.initial_inputs["tourokumenkyozei_hyoujun"]),
            "tourokumenkyozei_ritsu": str(self.initial_inputs["tourokumenkyozei_ritsu"]),
            "yosantanka_hiritsu_shisetsu": str(self.initial_inputs["yosantanka_hiritsu_shisetsu"]),
            "yosantanka_hiritsu_ijikanri_1": str(self.initial_inputs["yosantanka_hiritsu_ijikanri_1"]),
            "yosantanka_hiritsu_ijikanri_2": str(self.initial_inputs["yosantanka_hiritsu_ijikanri_2"]),
            "yosantanka_hiritsu_ijikanri_3": str(self.initial_inputs["yosantanka_hiritsu_ijikanri_3"]),
            "zei_total": str(self.initial_inputs["zei_total"]),

            }


#        if os.path.exists("fi_db.json"):
#            os.remove("fi_db.json")
#        db = TinyDB('fi_db.json')
#        db.insert(final_inputs)
#        db.close()
        #if os.path.exists("final_inputs.db"):
        #    os.remove("final_inputs.db")
        #con = sqlite3.connect('final_inputs.db')
        #con.close()

    #def _extract_inputs(self):

    #    self.controls = [
    #       #ft.Page.title = "初期入力",
    #
    #        self.dd1,  self.dd2, self.dd3,  self.dd4,  self.dd5,  self.dd6, 
    #        ft.Divider(height=1, color="amber"),
    #        tx0,  slider_value00, self.sl0, ft.Divider(height=1, color="amber"),
    #        tx1,  slider_value01, self.sl1, ft.Divider(height=1, color="amber"), 
    #        tx2,  slider_value02, self.sl2, ft.Divider(height=1, color="amber"),
    #        tx3,  slider_value03, self.sl3, ft.Divider(height=1, color="amber"),
    #        tx4,  slider_value04, self.sl4, ft.Divider(height=1, color="amber"),
    #        tx5,  slider_value05, self.sl5, ft.Divider(height=1, color="amber"),
    #        tx6,  slider_value06, self.sl6, ft.Divider(height=1, color="amber"),
    #        tx7,  slider_value07, self.sl7, ft.Divider(height=1, color="amber"),
    #        tx8,  slider_value08, self.sl8, ft.Divider(height=1, color="amber"),
    #        tx9,  slider_value09, self.sl9, ft.Divider(height=1, color="amber"),
    #        tx10, slider_value10, self.sl10,ft.Divider(height=1, color="amber"),
    #        tx11, slider_value11, self.sl11,ft.Divider(height=1, color="amber"),
    #        tx12, slider_value12, self.sl12,ft.Divider(height=1, color="amber"),
    #        b
    #    ]



    def button_clicked(self, e):
        input_data = self._extract_inputs()

        calc_results = self._calculate_financials(input_data)
        
        self._save_to_db(calc_results)
        VFM_calc()
        self.page.push_route("/view_saved")
        

    def _save_to_db(self, data):
        if os.path.exists("fi_db.json"):
            os.remove("fi_db.json")
        db = TinyDB('fi_db.json')
        db.insert(data)
        db.close()
        self.page.session.store.set("final_inputs",data)

       
def main(page: ft.Page):
    page.width = 500
    page.height = 2000
    page.title = "初期入力"
    page.window_width = 500
    page.window_height = 2000
    page.window_resizable = True
    page.expand=True
    page.scroll=ft.ScrollMode.AUTO
    #initial_inputs = Initial_Inputs()
    page.add(
            Final_Inputs()
    )


ft.run(main)
