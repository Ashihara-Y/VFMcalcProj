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

class Final_Inputs(ft.Column):
    def __init__(self):
        super().__init__()
        self.title = "最終入力・確認"
        self.width = 500
        self.height = 3000
        self.resizable = True

        self.slider_value01 = ft.Text("", size=30, weight=ft.FontWeight.W_200)
        self.slider_value02 = ft.Text("", size=30, weight=ft.FontWeight.W_200)
        self.slider_value03 = ft.Text("", size=30, weight=ft.FontWeight.W_200)
        self.slider_value04 = ft.Text("", size=30, weight=ft.FontWeight.W_200)
        self.slider_value05 = ft.Text("", size=30, weight=ft.FontWeight.W_200)
        self.slider_value06 = ft.Text("", size=30, weight=ft.FontWeight.W_200)
        self.slider_value07 = ft.Text("", size=30, weight=ft.FontWeight.W_200)
        self.slider_value08 = ft.Text("", size=30, weight=ft.FontWeight.W_200)
        self.slider_value09 = ft.Text("", size=30, weight=ft.FontWeight.W_200)
        self.slider_value10 = ft.Text("", size=30, weight=ft.FontWeight.W_200)
        self.slider_value11 = ft.Text("", size=30, weight=ft.FontWeight.W_200)
        self.slider_value12 = ft.Text("", size=30, weight=ft.FontWeight.W_200)
        self.slider_value13 = ft.Text("", size=30, weight=ft.FontWeight.W_200)
        self.slider_value14 = ft.Text("", size=30, weight=ft.FontWeight.W_200)
        self.slider_value15 = ft.Text("", size=30, weight=ft.FontWeight.W_200)
        self.slider_value16 = ft.Text("", size=30, weight=ft.FontWeight.W_200)
        self.slider_value17 = ft.Text("", size=30, weight=ft.FontWeight.W_200)
        self.slider_value18 = ft.Text("", size=30, weight=ft.FontWeight.W_200)
        self.slider_value19 = ft.Text("", size=30, weight=ft.FontWeight.W_200)
        self.slider_value20 = ft.Text("", size=30, weight=ft.FontWeight.W_200)

        db = TinyDB("ii_db.json")
        self.initial_inputs = db.all()[0]        

    def handle_change_01(self, e):
        sl_value = e.control.value
        self.slider_value01.value = str(sl_value)
        self.page.update()
    def handle_change_02(self, e):
        sl_value = e.control.value
        self.slider_value02.value = str(sl_value)
        self.page.update()
    def handle_change_03(self, e):
        sl_value = e.control.value
        self.slider_value03.value = str(sl_value)
        self.page.update()
    def handle_change_04(self, e):
        sl_value = e.control.value
        self.slider_value04.value = str(sl_value)
        self.page.update()
    def handle_change_05(self, e):
        sl_value = e.control.value
        self.slider_value05.value = str(sl_value)
        self.page.update()
    def handle_change_06(self, e):
        sl_value = e.control.value
        self.slider_value06.value = str(sl_value)
        self.page.update()
    def handle_change_07(self, e):
        sl_value = e.control.value
        self.slider_value07.value = str(sl_value)
        self.page.update()
    def handle_change_08(self, e):
        sl_value = e.control.value
        self.slider_value08.value = str(sl_value)
        self.page.update()
    def handle_change_09(self, e):
        sl_value = e.control.value
        self.slider_value09.value = str(sl_value)
        self.page.update()
    def handle_change_10(self, e):
        sl_value = e.control.value
        self.slider_value10.value = str(sl_value)
        self.page.update()
    def handle_change_11(self, e):
        sl_value = e.control.value
        self.slider_value11.value = str(sl_value)
        self.page.update()
    def handle_change_12(self, e):
        sl_value = e.control.value
        self.slider_value12.value = str(sl_value)
        self.page.update()
    def handle_change_13(self, e):
        sl_value = e.control.value
        self.slider_value13.value = str(sl_value)
        self.page.update()
    def handle_change_14(self, e):
        sl_value = e.control.value
        self.slider_value14.value = str(sl_value)
        self.page.update()
    def handle_change_15(self, e):
        sl_value = e.control.value
        self.slider_value15.value = str(sl_value)
        self.page.update()
    def handle_change_16(self, e):
        sl_value = e.control.value
        self.slider_value16.value = str(sl_value)
        self.page.update()
    def handle_change_17(self, e):
        sl_value = e.control.value
        self.slider_value17.value = str(sl_value)
        self.page.update()
    def handle_change_18(self, e):
        sl_value = e.control.value
        self.slider_value18.value = str(sl_value)
        self.page.update()
    def handle_change_19(self, e):
        sl_value = e.control.value
        self.slider_value19.value = str(sl_value)
        self.page.update()
    def handle_change_20(self, e):
        sl_value = e.control.value
        self.slider_value20.value = str(sl_value)
        self.page.update()


    def build(self):

        date_format = '%Y-%m-%d'
        date_dt = datetime.datetime.strptime(self.initial_inputs["const_start_date"], date_format)
        const_start_year = date_dt.year
        const_start_month = date_dt.month
        const_start_day = date_dt.day

        self.tx0 = ft.Text(str("＜＜初期データ＞＞"))
        self.tx1 = ft.Text(str("発注者区分： " + str(self.initial_inputs["mgmt_type"])))
        self.tx2 = ft.Text(str("事業タイプ： " + str(self.initial_inputs["proj_ctgry"])))
        self.tx3 = ft.Text(str("事業方式： " + str(self.initial_inputs["proj_type"])))
        self.tx4 = ft.Text(str("事業期間： " + str(self.initial_inputs["proj_years"]) + "年"))
        self.tx5 = ft.Text(str("施設整備期間： " + str(self.initial_inputs["const_years"]) + "年"))
        self.tx6 = ft.Text(str("地方債償還据置期間： " + str(self.initial_inputs["chisai_sueoki_kikan"]) + "年"))
    
        self.dt1 = ft.DataTable(
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
        self.dt2 = ft.DataTable(
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

        self.tx7 = ft.Text("地方債償還期間(年)")
        self.sl1 = ft.Slider(
            value=int(self.initial_inputs["chisai_shoukan_kikan"]),
            min=0,
            max=30,
            divisions=30,
            label="{value}年",
            round=0,
            on_change=self.handle_change_01,
        )
        self.tx8 = ft.Text("施設整備費支払 一括払の比率(%)")
        self.sl2 = ft.Slider(
            value=50,
            min=0.0,
            max=100,
            divisions=100,
            label="{value}%",
            round=1,
            on_change=self.handle_change_02,
        )
        self.tx9 = ft.Text("モニタリング等費用(PSC)(百万円、推奨:10)")
        self.sl3 = ft.Slider(
            value=0,
            min=0,
            max=100,
            divisions=100,
            label="{value}百万円",
            round=1,
            on_change=self.handle_change_03,
        )
        self.tx10 = ft.Text("モニタリング等費用(PFI-LCC)(百万円、推奨:6)")
        self.sl4 = ft.Slider(
            value=0,
            min=0,
            max=100,
            divisions=100,
            label="{value}百万円",
            round=1,
            on_change=self.handle_change_04,
        )
        self.tx11 = ft.Text("起債充当率(%)")
        self.sl5 = ft.Slider(
            value:=self.initial_inputs["kisai_jutou"],
            min=0.0,
            max=100.0,
            divisions=100,
            label="{value}%",
            round=1,
            on_change=self.handle_change_05,
        )
        self.tx12 = ft.Text("起債への交付金カバー率(%)")
        self.sl6 = ft.Slider(
            value:=self.initial_inputs["kisai_koufu"],
            min=0.0,
            max=50.0,
            divisions=50,
            label="{value}%",
            round=1,
            on_change=self.handle_change_06,
        )
        self.tx13 = ft.Text("補助率(%)")
        self.sl7 = ft.Slider(
            value:=self.initial_inputs["hojo_ritsu"],
            min=0.0,
            max=70.0,
            divisions=700,
            label="{value}%",
            round=1,
            on_change=self.handle_change_07,
        )
        self.tx14 = ft.Text("SPC経費年額(百万円)")
        self.sl8 = ft.Slider(
            value:=Decimal(self.initial_inputs["SPC_keihi"]),
            min=0,
            max=50,
            divisions=50,
            label="{value}百万円",
            round=1,
            on_change=self.handle_change_08,
        )
        self.tx15 = ft.Text("SPCへの手数料(百万円)")
        self.sl9 = ft.Slider(
            value:=Decimal(self.initial_inputs["SPC_fee"]),
            min=0,
            max=50,
            divisions=50,
            label="{value}百万円",
            round=1,
            on_change=self.handle_change_09,
        )
        self.tx16 = ft.Text("SPC資本金(百万円)")
        self.sl10 = ft.Slider(
            value:=Decimal(self.initial_inputs["SPC_shihon"]),
            min=0,
            max=100,
            divisions=100,
            label="{value}百万円",
            round=1,
            on_change=self.handle_change_10,
        )
        self.tx17 = ft.Text("SPC予備費(百万円)")
        self.sl11 = ft.Slider(
            value:=Decimal(self.initial_inputs["SPC_yobihi"]),
            min=0,
            max=1000,
            divisions=1000,
            label="{value}百万円",
            round=1,
            on_change=self.handle_change_11,
        )
        self.sw01 = ft.Switch(
            label="SPC経費の扱い（デフォルト：サービス対価で支払）",
            value=1,
        )
        self.tx19 = ft.Text("アドバイザリー等経費(百万円)")
        self.sl13 = ft.Slider(
            value=0,
            min=0,
            max=50,
            divisions=50,
            label="{value}百万円",
            round=1,
            on_change=self.handle_change_13,
        )
        self.tx20 = ft.Text("利用料金収入(百万円)")
        self.sl14 = ft.Slider(
            value:=self.initial_inputs["riyou_ryoukin"],
            min=0,
            max=100,
            divisions=100,
            label="{value}百万円",
            round=1,
            on_change=self.handle_change_14,
        )
        self.tx21 = ft.Text("割賦金利へのスプレッド(%)")
        self.sl15 = ft.Slider(
            value=0.00,
            min=0.00,
            max=2.00,
            divisions=200,
            label="{value}％",
            round=2,
            on_change=self.handle_change_15,
        )
        self.tx22 = ft.Text("施設整備開始年")
        self.sl16 = ft.Slider(
            value:=const_start_year,
            min=const_start_year,
            max=(const_start_year + 10),
            divisions=10,
            label="{value}年",
            on_change=self.handle_change_16,
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
        self.tx25 = ft.Text("予備入力（１）")
        self.sl19 = ft.Slider(
            value=0,
            min=0,
            max=1,
            divisions=100,
            label="{value}",
            on_change=self.handle_change_19,
        )
        self.tx26 = ft.Text("予備入力（２）")
        self.sl20 = ft.Slider(
            value=0,
            min=0,
            max=1,
            divisions=100,
            label="{value}",
            on_change=self.handle_change_20,
        )
        self.b = ft.ElevatedButton(text="入力確認・計算", on_click=self.button_clicked)

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

        fi_lv1.controls= [
                    self.tx0, self.tx1, self.tx2,
                    self.tx3, self.tx4, self.tx5, self.tx6,
                    self.dt1, self.dt2, ft.Divider(height=1, color="amber"),
        ]
        fi_lv2.controls= [
                    self.tx7, self.slider_value01, self.sl1, ft.Divider(height=1, color="amber"), 
                    self.tx8, self.slider_value02, self.sl2, ft.Divider(height=1, color="amber"),
                    self.tx9, self.slider_value03, self.sl3, ft.Divider(height=1, color="amber"),
                    self.tx10,self.slider_value04, self.sl4, ft.Divider(height=1, color="amber"),
                    self.tx11,self.slider_value05, self.sl5, ft.Divider(height=1, color="amber"),
                    self.tx12,self.slider_value06, self.sl6, ft.Divider(height=1, color="amber"),
                    self.tx13,self.slider_value07, self.sl7, ft.Divider(height=1, color="amber"),
                    self.tx14,self.slider_value08, self.sl8, ft.Divider(height=1, color="amber"),
                    self.tx15,self.slider_value09, self.sl9, ft.Divider(height=1, color="amber"),
                    self.tx16,self.slider_value10, self.sl10,ft.Divider(height=1, color="amber"),
                    self.tx17,self.slider_value11, self.sl11,ft.Divider(height=1, color="amber"),
                    #self.tx18,self.slider_value12, self.sl12,ft.Divider(height=1, color="amber"),
                    self.sw01,ft.Divider(height=1, color="amber"),
                    self.tx19,self.slider_value13, self.sl13,ft.Divider(height=1, color="amber"),
                    self.tx20,self.slider_value14, self.sl14,ft.Divider(height=1, color="amber"),
                    self.tx21,self.slider_value15, self.sl15,ft.Divider(height=1, color="amber"),
                    self.tx22,self.slider_value16, self.sl16,ft.Divider(height=1, color="amber"),
                    self.dd01,self.dd02,ft.Divider(height=1, color="amber"),
                    self.tx25,self.slider_value19, self.sl19,ft.Divider(height=1, color="amber"),
                    self.tx26,self.slider_value20, self.sl20,ft.Divider(height=1, color="amber"),
                    self.b,

        ]        

        return ft.Container(
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
        )

    def button_clicked(self, e):

        shisetsu_seibi_paymentschedule_ikkatsu = Decimal(self.sl2.value/100).quantize(Decimal('0.000001'), ROUND_HALF_UP)
        shisetsu_seibi_paymentschedule_kappu = Decimal(1 - shisetsu_seibi_paymentschedule_ikkatsu).quantize(Decimal('0.000001'), ROUND_HALF_UP)
        kisai_jutou = Decimal(self.sl5.value).quantize(Decimal('0.000001'), ROUND_HALF_UP)
        kisai_koufu = Decimal(self.sl6.value).quantize(Decimal('0.000001'), ROUND_HALF_UP)
        hojo_ritsu = Decimal(self.sl7.value).quantize(Decimal('0.000001'), ROUND_HALF_UP)
        #kappu_kinri_spread = Decimal(self.sl15.value/100).quantize(Decimal('0.000001'), ROUND_HALF_UP),

        kisai_jutou = str(kisai_jutou)
        kisai_koufu = str(kisai_koufu)
        hojo_ritsu = str(hojo_ritsu)

        const_start_date_year = int(self.sl16.value)
        const_start_date_month = int(self.dd01.value)
        const_start_date_day = int(self.dd02.value)
        #const_start_date_year = self.initial_inputs['const_start_date_year']
        #const_start_date_month = self.initial_inputs['const_start_date_month']
        #const_start_date_day = self.initial_inputs['const_start_date_day']
        const_start_date = str(datetime.date(const_start_date_year, const_start_date_month, const_start_date_day))
        start_year = datetime.datetime.strptime(str(const_start_date), '%Y-%m-%d').year
        start_month = datetime.datetime.strptime(str(const_start_date), '%Y-%m-%d').month

        if start_month < 4:
            first_end_fy = datetime.date(start_year, 3, 31)
        else:
            first_end_fy = datetime.date(start_year + 1, 3, 31)

        chisai_kinri = Decimal(self.initial_inputs['chisai_kinri']) / 100 # CSVの％表記を採取しているため、実数表記に切り替える。
        kijun_kinri = Decimal(self.initial_inputs["kijun_kinri"]) /100 # CSVの％表記を採取しているため、実数表記に切り替える。
        kitai_bukka = Decimal(self.initial_inputs["kitai_bukka"]) /100 # CSVの％表記を採取しているため、実数表記に切り替える。

        discount_rate = kijun_kinri + kitai_bukka
        discount_rate = Decimal(discount_rate).quantize(Decimal('0.000001'), ROUND_HALF_UP)

        target_years = 45
        #proj_years = int(self.initial_inputs['proj_years'])
        const_years = int(self.initial_inputs['const_years'])
        shoukan_kaishi_jiki = const_years + self.initial_inputs['chisai_sueoki_kikan']  + 1

        kappu_kinri_spread = Decimal(self.sl15.value/100).quantize(Decimal('0.000001'), ROUND_HALF_UP)
        lg_spread = Decimal(self.initial_inputs['lg_spread']).quantize(Decimal('0.000001'), ROUND_HALF_UP)
        Kappu_kinri = kijun_kinri + lg_spread + kappu_kinri_spread
        Kappu_kinri = Decimal(str(Kappu_kinri)).quantize(Decimal('0.000001'), ROUND_HALF_UP)

        # First_end_fyを1年追加する必要があるのか、算定シートを確認する必要がある。
        first_end_fy, first_end_fy + dateutil.relativedelta.relativedelta(year=1)

        SPC_keihi = Decimal(self.sl8.value)
        SPC_fee = Decimal(self.sl9.value)
        SPC_shihon = Decimal(self.sl10.value)

        ijikanri_unnei_years = int(self.initial_inputs['ijikanri_unnei_years'])
        houjinjuminzei_kintou = Decimal(self.initial_inputs['houjinjuminzei_kintou'])
        SPC_hiyou_total = SPC_keihi * ijikanri_unnei_years + SPC_shihon
        SPC_hiyou_nen = SPC_fee + SPC_keihi
        SPC_keihi_LCC = SPC_keihi + SPC_fee + houjinjuminzei_kintou
        
        chisai_kinri = Decimal(self.initial_inputs['chisai_kinri']) / 100 # CSVの％表記を採取しているため、実数表記に切り替える。
        kijun_kinri = Decimal(self.initial_inputs["kijun_kinri"]) /100 # CSVの％表記を採取しているため、実数表記に切り替える。
        kitai_bukka = Decimal(self.initial_inputs["kitai_bukka"]) /100 # CSVの％表記を採取しているため、実数表記に切り替える。

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
        
        final_inputs = {
            "advisory_fee": str(self.sl13.value),
            "chisai_kinri": str(chisai_kinri), 
            "chisai_shoukan_kikan": int(self.sl1.value),
            "chisai_sueoki_years": int(self.initial_inputs["chisai_sueoki_kikan"]),
            "const_start_date_year": int(self.sl16.value),
            "const_start_date_month": int(self.dd01.value),
            "const_start_date_day": int(self.dd02.value),
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
            "monitoring_costs_PSC": str(self.sl3.value),
            "monitoring_costs_LCC": str(self.sl4.value),

            "option_01": str(self.sl19.value),
            "option_02": str(self.sl20.value),
            "pre_kyoukouka": bool(self.initial_inputs["pre_kyoukouka"]),
            "proj_ctgry": self.initial_inputs["proj_ctgry"],
            "proj_type": self.initial_inputs["proj_type"],
            "proj_years": int(self.initial_inputs["proj_years"]),
            "rakusatsu_ritsu": str(self.initial_inputs["rakusatsu_ritsu"]),
            "reduc_shisetsu": str(self.initial_inputs["reduc_shisetsu"]),
            "reduc_ijikanri_1": str(self.initial_inputs["reduc_ijikanri_1"]),
            "reduc_ijikanri_2": str(self.initial_inputs["reduc_ijikanri_2"]),
            "reduc_ijikanri_3": str(self.initial_inputs["reduc_ijikanri_3"]),
            "riyouryoukin_shunyu": str(self.sl14.value),

            "shisetsu_seibi": str(self.initial_inputs["shisetsu_seibi"]),
            "shisetsu_seibi_LCC": str(self.initial_inputs["shisetsu_seibi_LCC"]),
            "shisetsu_seibi_org": str(self.initial_inputs["shisetsu_seibi_org"]),
            "shisetsu_seibi_org_LCC": str(self.initial_inputs["shisetsu_seibi_org_LCC"]),
            "shisetsu_seibi_paymentschedule_ikkatsu": str(shisetsu_seibi_paymentschedule_ikkatsu),
            "shisetsu_seibi_paymentschedule_kappu": str(shisetsu_seibi_paymentschedule_kappu),
            "shoukan_kaishi_jiki": shoukan_kaishi_jiki,
            "SPC_keihi": str(self.sl8.value),
            "SPC_fee": str(self.sl9.value),
            "SPC_shihon": str(self.sl10.value),
            "SPC_yobihi": str(self.sl11.value),
            "SPC_hiyou_atsukai": int(self.sw01.value),
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

        #for item in list(final_inputs.values()):
        #    if not item:
        #        ft.page.go("/")
        #    else:
        #        pass


        if os.path.exists("fi_db.json"):
            os.remove("fi_db.json")
        db = TinyDB('fi_db.json')
        db.insert(final_inputs)
        db.close()
        #if os.path.exists("final_inputs.db"):
        #    os.remove("final_inputs.db")
        #con = sqlite3.connect('final_inputs.db')
        #con.close()
        
        VFM_calc()
        self.page.go("/view_saved")
