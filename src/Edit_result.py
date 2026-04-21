import sys
sys.dont_write_bytecode = True
import pandas as pd
import flet as ft
from simpledt import DataFrame
from tinydb import TinyDB, Query
import openpyxl
from sqlalchemy import create_engine
import make_inputs_df
import decimal


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
        #slider_value12 = ft.Text("", size=30, weight=ft.FontWeight.W_200)
        slider_value13 = ft.Text("", size=30, weight=ft.FontWeight.W_200)
        slider_value14 = ft.Text("", size=30, weight=ft.FontWeight.W_200)
        slider_value15 = ft.Text("", size=30, weight=ft.FontWeight.W_200)
        #slider_value16 = ft.Text("", size=30, weight=ft.FontWeight.W_200)
        #slider_value17 = ft.Text("", size=30, weight=ft.FontWeight.W_200)
        #slider_value18 = ft.Text("", size=30, weight=ft.FontWeight.W_200)
        slider_value19 = ft.Text("", size=30, weight=ft.FontWeight.W_200)
        slider_value20 = ft.Text("", size=30, weight=ft.FontWeight.W_200)

        #db = TinyDB("ii_db.json")
        #self.initial_inputs = db.all()[0]   
        self.initial_inputs = initial_inputs
    
        #if not self.initial_inputs or len(self.initial_inputs) == 0:
        #    self.result_text.value = "Error: No data in SessionStorage from Initial_Inputs."
        #    self.update()
        #   return
            
 
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
            value=10,
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
            value=6,
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
            value=float(self.initial_inputs["kisai_jutou"])*100,
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
            value=float(self.initial_inputs["kisai_koufu"])*100,
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
            value=float(self.initial_inputs["hojo_ritsu"])*100,
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
            value=float(self.initial_inputs["SPC_keihi"]),
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
            value=float(self.initial_inputs["SPC_fee"]),
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
            value=float(self.initial_inputs["SPC_shihon"]),
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
            value=float(self.initial_inputs["SPC_yobihi"]),
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
            value=True,
        )
        tx19 = ft.Text("アドバイザリー等経費(百万円)")
        self.sl13 = ft.Slider(
            value=0,
            min=0,
            max=50,
            divisions=50,
            label="{value}百万円",
            round=1,
            on_change=handle_slider_change,
            data=slider_value13,
        )
        tx20 = ft.Text("利用料金収入(百万円)")
        self.sl14 = ft.Slider(
            value=float(self.initial_inputs["riyou_ryoukin"]),
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
        b = ft.Button(content="入力確認・計算", on_click=self.button_clicked)

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
                    tx7, slider_value01, self.sl1,  ft.Divider(height=1, color="amber"), 
                    tx25, slider_value19,self.sl19, ft.Divider(height=1, color="amber"), 
                    tx9, slider_value03, self.sl3,  ft.Divider(height=1, color="amber"),
                    tx10,slider_value04, self.sl4,  ft.Divider(height=1, color="amber"),
                    tx11,slider_value05, self.sl5,  ft.Divider(height=1, color="amber"),
                    tx12,slider_value06, self.sl6,  ft.Divider(height=1, color="amber"),
                    tx13,slider_value07, self.sl7,  ft.Divider(height=1, color="amber"),
                    tx19,slider_value13, self.sl13, ft.Divider(height=1, color="amber"),
                    self.dd00,self.dd01,self.dd02, ft.Divider(height=1, color="amber"), 
                    tx26,slider_value20, self.sl20, ft.Divider(height=1, color="amber"),
                    b,
        ]        
        if self.initial_inputs["proj_type"] == "DBO(SPCなし)" or self.initial_inputs["proj_type"] == "BT/DB(いずれもSPCなし)":
            self.controls = [
                   fi_lv1,
                   fi_lv3,
            ]
        else:
            self.controls = [
                    fi_lv1,
                    fi_lv2,
            ]


# IIからのbutton_clicked
    async def button_clicked(self, e):
        input_data = self._extract_inputs()

        calc_results = self._calculate_financials(input_data)
        
        self._save_to_db(calc_results)
        await self.page.push_route("/final_inputs")
        
# FIからのbutton_clicked
    async def button_clicked(self, e):
        input_data = self._extract_inputs()

        calc_results = self._calculate_financials(input_data)
        
        self._save_to_db(calc_results)
        VFM_calc()
        await self.page.push_route("/view_saved")
        

# IIからの_extract_inputs
    def _extract_inputs(self):
        mgmt_type = self.dd1.value
        proj_ctgry = self.dd2.value
        proj_type = self.dd3.value

        raw_proj_years = self.dd6.value if proj_type == "BT/DB(いずれもSPCなし)" else self.dd4.value

        proj_years = int(raw_proj_years) if raw_proj_years else 0
        const_years = int(self.dd6.value) if self.dd6.value else 0
        chisai_shoukan_kikan = int(self.dd5.value) if self.dd5.value else 0

        if proj_years < const_years:
            raise ValueError("事業期間は施設整備期間より長い必要があります。")
        ijikanri_unnei_years = proj_years - const_years

        shisetsu_seibi_org_R = Decimal(self.sl0.value)
        shisetsu_seibi_org_Y = Decimal(self.sl1.value)
        ijikanri_unnei_1_org_R = Decimal(self.sl2.value)
        ijikanri_unnei_1_org_Y = Decimal(self.sl3.value)
        ijikanri_unnei_2_org_R= Decimal(self.sl4.value)
        ijikanri_unnei_2_org_Y = Decimal(self.sl5.value)
        ijikanri_unnei_3_org_R = Decimal(self.sl6.value)
        ijikanri_unnei_3_org_Y = Decimal(self.sl7.value)

        reduc_shisetsu = Decimal(self.sl8.value) / Decimal(100)
        reduc_ijikanri_1 = Decimal(self.sl9.value) / Decimal(100)
        reduc_ijikanri_2 = Decimal(self.sl10.value) / Decimal(100)
        reduc_ijikanri_3 = Decimal(self.sl11.value) / Decimal(100)
        rakusatsu_ritsu = Decimal(self.sl12.value) / Decimal(100)

        JGB_rates_df = pd.read_csv("src/JGB_rates.csv", sep="\t", encoding="utf-8", header=None, names=["year", "rate"],).set_index("year")
        JRB_rates_df = pd.read_csv("src/JRB_rates.csv", sep="\t", encoding="utf-8", names=[0,1,2,3,4,5], index_col=0)

        y, d = divmod(proj_years, 5)
        if y >= 1:
            r_idx = str((y + 1) * 5) + "年" if d > 2 else str(y * 5) + "年"
        else:
            r_idx = str(d) + "年"

        r1 = Decimal(JGB_rates_df.loc[r_idx].iloc[0])
        r2 = Decimal(JRB_rates_df.loc[chisai_shoukan_kikan][const_years])
        kitai_bukka_j = Decimal(pd.read_csv("src/BOJ_ExpInflRate_down.csv", encoding="shift-jis", skiprows=1).dropna().iloc[-1, 1])
        gonensai_rimawari = Decimal(JGB_rates_df.loc["5年"].iloc[0])
        
        return {
            'mgmt_type': mgmt_type,
            'proj_ctgry': proj_ctgry,
            'proj_type': proj_type,

            'proj_years': proj_years,
            'const_years': const_years,
            'chisai_shoukan_kikan': chisai_shoukan_kikan,
            'ijikanri_unnei_years': ijikanri_unnei_years,

            'shisetsu_seibi_org_R': shisetsu_seibi_org_R,
            'shisetsu_seibi_org_Y': shisetsu_seibi_org_Y,
            'ijikanri_unnei_1_org_R': ijikanri_unnei_1_org_R,
            'ijikanri_unnei_1_org_Y': ijikanri_unnei_1_org_Y,
            'ijikanri_unnei_2_org_R': ijikanri_unnei_2_org_R,
            'ijikanri_unnei_2_org_Y': ijikanri_unnei_2_org_Y,
            'ijikanri_unnei_3_org_R': ijikanri_unnei_3_org_R,
            'ijikanri_unnei_3_org_Y': ijikanri_unnei_3_org_Y,

            'reduc_shisetsu': reduc_shisetsu,
            'reduc_ijikanri_1': reduc_ijikanri_1,
            'reduc_ijikanri_2': reduc_ijikanri_2,
            'reduc_ijikanri_3': reduc_ijikanri_3,
            'rakusatsu_ritsu': rakusatsu_ritsu,

            'r1': r1,
            'r2': r2,
            'kitai_bukka_j': kitai_bukka_j,
            'gonensai_rimawari': gonensai_rimawari,
        }

# FIからのExtract_inputs
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

        JRB_rates_df = pd.read_csv(
            "src/JRB_rates.csv",
            encoding="utf-8",
            sep='\t', 
            names=[0,1,2,3,4,5], 
            index_col=0)

        chisai_kinri = JRB_rates_df.loc[chisai_shoukan_kikan][chisai_sueoki_kikan]

        return {
            'const_start_date_year': const_start_date_year,
            'const_start_date_month': const_start_date_month,
            'const_start_date_day': const_start_date_day,

            'chisai_shoukan_kikan': chisai_shoukan_kikan,
            'chisai_kinri': chisai_kinri,
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
    
# IIからの_calculate_financials
    def _calculate_financials(self, inputs):
        def to_dec(val):
            return Decimal(val).quantize(Decimal('0.000001'), ROUND_HALF_UP)

        calc_id = timeflake.random()
        dtime = datetime.datetime.fromtimestamp(calc_id.timestamp // 1000, tz=ZoneInfo("Asia/Tokyo"))
        const_start_date = datetime.date(dtime.year, dtime.month, dtime.day).strftime('%Y-%m-%d')

        shisetsu_seibi_org = to_dec(inputs['shisetsu_seibi_org_R'] + inputs['shisetsu_seibi_org_Y'])
        shisetsu_seibi = to_dec(shisetsu_seibi_org * inputs['rakusatsu_ritsu'])
        ijikanri_unnei_1_org = to_dec(inputs['ijikanri_unnei_1_org_R'] + inputs['ijikanri_unnei_1_org_Y'])
        ijikanri_unnei_1 = to_dec(ijikanri_unnei_1_org * inputs['rakusatsu_ritsu'])
        ijikanri_unnei_2_org = to_dec(inputs['ijikanri_unnei_2_org_R'] + inputs['ijikanri_unnei_2_org_Y'])
        ijikanri_unnei_2 = to_dec(ijikanri_unnei_2_org * inputs['rakusatsu_ritsu'])        
        ijikanri_unnei_3_org = to_dec(inputs['ijikanri_unnei_3_org_R'] + inputs['ijikanri_unnei_3_org_Y'])
        ijikanri_unnei_3 = to_dec(ijikanri_unnei_3_org * inputs['rakusatsu_ritsu'])

        yosantanka_hiritsu_shisetsu = to_dec(inputs['shisetsu_seibi_org_Y']/shisetsu_seibi_org) if shisetsu_seibi_org else to_dec(0)
        yosantanka_hiritsu_ijikanri_1 = to_dec(inputs['ijikanri_unnei_1_org_Y']/ijikanri_unnei_1_org) if ijikanri_unnei_1_org else to_dec(0)
        yosantanka_hiritsu_ijikanri_2 = to_dec(inputs['ijikanri_unnei_2_org_Y']/ijikanri_unnei_2_org) if ijikanri_unnei_2_org else to_dec(0)
        yosantanka_hiritsu_ijikanri_3 = to_dec(inputs['ijikanri_unnei_3_org_Y']/ijikanri_unnei_3_org) if ijikanri_unnei_3_org else to_dec(0)

        shisetsu_seibi_org_LCC = to_dec(shisetsu_seibi_org * (Decimal(1.00) - inputs['reduc_shisetsu']))
        shisetsu_seibi_LCC = to_dec(shisetsu_seibi * (Decimal(1.00) - inputs['reduc_shisetsu']))
        ijikanri_unnei_1_org_LCC = to_dec(ijikanri_unnei_1_org * (Decimal(1.00) - inputs['reduc_ijikanri_1']))
        ijikanri_unnei_1_LCC = to_dec(ijikanri_unnei_1 * (Decimal(1.00) - inputs['reduc_ijikanri_1']))
        ijikanri_unnei_2_org_LCC = to_dec(ijikanri_unnei_2_org * (Decimal(1.00) - inputs['reduc_ijikanri_2']))
        ijikanri_unnei_2_LCC = to_dec(ijikanri_unnei_2 * (Decimal(1.00) - inputs['reduc_ijikanri_2']))
        ijikanri_unnei_3_org_LCC = to_dec(ijikanri_unnei_3_org * (Decimal(1.00) - inputs['reduc_ijikanri_3']))
        ijikanri_unnei_3_LCC = to_dec(ijikanri_unnei_3 * (Decimal(1.00) - inputs['reduc_ijikanri_3']))

        chisai_sueoki_kikan = int(inputs['const_years']) if inputs['const_years'] else int(0)
        kitai_bukka = to_dec(inputs['kitai_bukka_j'] - inputs['gonensai_rimawari'])
        lg_spread = to_dec(0.01)

        tax_rates = {
            'houjinzei_ritsu': Decimal(0.0),
            'houjinjuminzei_kintou': Decimal(0.0),
            'hudousanshutokuzei_hyoujun': Decimal(0.0),
            'hudousanshutokuzei_ritsu': Decimal(0.0),
            'koteishisanzei_hyoujun': Decimal(0.0),
            'koteishisanzei_ritsu': Decimal(0.0),
            'tourokumenkyozei_hyoujun': Decimal(0.0),
            'tourokumenkyozei_ritsu': Decimal(0.0),
            'houjinjuminzei_ritsu_todouhuken': Decimal(0.0),
            'houjinjuminzei_ritsu_shikuchoson': Decimal(0.0),
            'riyou_ryoukin': Decimal(0.0),
}

        if inputs['proj_ctgry'] == "サービス購入型":
            tax_rates['houjinjuminzei_kintou'] = to_dec(0.18)
            if inputs['proj_type'] == "BOT/BOO":
                tax_rates['houjinzei_ritsu'] = Decimal(0.0)
                tax_rates['hudousanshutokuzei_hyoujun'] = shisetsu_seibi_org_LCC
                tax_rates['hudousanshutokuzei_ritsu'] = Decimal(0.04)
                tax_rates['koteishisanzei_hyoujun'] = shisetsu_seibi_org_LCC
                tax_rates['koteishisanzei_ritsu'] = Decimal(0.014)
                tax_rates['tourokumenkyozei_hyoujun'] = shisetsu_seibi_org_LCC
                tax_rates['tourokumenkyozei_ritsu'] = Decimal(0.004)
                tax_rates['houjinjuminzei_ritsu_todouhuken'] = Decimal(0.0)
                tax_rates['houjinjuminzei_ritsu_shikuchoson'] = Decimal(0.0)
                tax_rates['riyou_ryoukin'] = Decimal(0.0)

            financial_rules = {'zei_modori': Decimal(0.278), 'hojo': Decimal(0.0), 'kisai_jutou': Decimal(0.0), 'kisai_koufu': Decimal(0.0)}
            if inputs['mgmt_type'] == "国":
                financial_rules['zei_modori'] = Decimal(0.278)
                financial_rules['hojo'] = Decimal(0.0)
                financial_rules['kisai_jutou'] = Decimal(0.0)
                financial_rules['kisai_koufu'] = Decimal(0.0)
            elif inputs['mgmt_type']  == "都道府県":
                financial_rules['zei_modori'] = Decimal(0.0578)
                financial_rules['hojo'] = Decimal(0.5)
                financial_rules['kisai_jutou'] = Decimal(0.75)
                financial_rules['kisai_koufu'] = Decimal(0.30)
            elif inputs['mgmt_type']  == "市町村":
                financial_rules['zei_modori'] = Decimal(0.084)
                financial_rules['hojo'] = Decimal(0.300)
                financial_rules['kisai_jutou'] = Decimal(0.750)
                financial_rules['kisai_koufu'] = Decimal(0.300)
            
            financial_rules['zei_total'] = tax_rates['houjinjuminzei_kintou'] + tax_rates['hudousanshutokuzei_hyoujun'] * tax_rates['hudousanshutokuzei_ritsu'] + tax_rates['koteishisanzei_hyoujun'] * tax_rates['koteishisanzei_ritsu'] + tax_rates['tourokumenkyozei_hyoujun'] * tax_rates['tourokumenkyozei_ritsu']

    
            if inputs['proj_type'] in ["DBO(SPCなし)", "BT/DB(いずれもSPCなし)"]:
                SPC_costs = {'fee':to_dec(0), 'shihon':to_dec(0), 'yobihi':to_dec(0)}
                SPC_hiyou_atsukai = int(1)
            else:
                SPC_costs = {'keihi':to_dec(20), 'fee':to_dec(20), 'shihon':to_dec(100), 'yobihi':to_dec(456)}
                SPC_hiyou_atsukai = int(1)

            initial_inputs = {
                "mgmt_type": inputs['mgmt_type'],
                "proj_ctgry": inputs['proj_ctgry'],
                "proj_type": inputs['proj_type'],
                "proj_years": inputs['proj_years'],
                "const_years": inputs['const_years'],
                "ijikanri_unnei_years": inputs['ijikanri_unnei_years'],
                "const_start_date": str(const_start_date),
                "kijun_kinri": str(inputs['r1']),
                "chisai_kinri": str(inputs['r2']),
                "chisai_sueoki_kikan": int(chisai_sueoki_kikan),
                "chisai_shoukan_kikan": inputs['chisai_shoukan_kikan'],
                "lg_spread": str(lg_spread),
                "zei_modori": str(financial_rules['zei_modori']),
                "zei_total": str(Decimal(0.18).quantize(Decimal('0.000001'), ROUND_HALF_UP)),
                "riyou_ryoukin": str(tax_rates['riyou_ryoukin']),
                "growth": str(to_dec(0.0)),
                "kitai_bukka": str(Decimal(kitai_bukka)),
                "shisetsu_seibi": str(shisetsu_seibi),
                "shisetsu_seibi_org": str(shisetsu_seibi_org),
                "shisetsu_seibi_org_LCC": str(shisetsu_seibi_org_LCC),
                "shisetsu_seibi_LCC": str(shisetsu_seibi_LCC),
                "ijikanri_unnei_1": str(ijikanri_unnei_1),
                "ijikanri_unnei_1_org": str(ijikanri_unnei_1_org),
                "ijikanri_unnei_1_org_LCC": str(ijikanri_unnei_1_org_LCC),
                "ijikanri_unnei_1_LCC": str(ijikanri_unnei_1_LCC),
                "ijikanri_unnei_2": str(ijikanri_unnei_2),
                "ijikanri_unnei_2_org": str(ijikanri_unnei_2_org),
                "ijikanri_unnei_2_org_LCC": str(ijikanri_unnei_2_org_LCC),
                "ijikanri_unnei_2_LCC": str(ijikanri_unnei_2_LCC),
                "ijikanri_unnei_3": str(ijikanri_unnei_3),
                "ijikanri_unnei_3_org": str(ijikanri_unnei_3_org),
                "ijikanri_unnei_3_org_LCC": str(ijikanri_unnei_3_org_LCC),
                "ijikanri_unnei_3_LCC": str(ijikanri_unnei_3_LCC),
                "yosantanka_hiritsu_shisetsu": str(yosantanka_hiritsu_shisetsu),
                "yosantanka_hiritsu_ijikanri_1": str(yosantanka_hiritsu_ijikanri_1),
                "yosantanka_hiritsu_ijikanri_2": str(yosantanka_hiritsu_ijikanri_2),
                "yosantanka_hiritsu_ijikanri_3": str(yosantanka_hiritsu_ijikanri_3),
                "rakusatsu_ritsu": str(inputs['rakusatsu_ritsu']),
                "reduc_shisetsu": str(inputs['reduc_shisetsu']),
                "reduc_ijikanri_1": str(inputs['reduc_ijikanri_1']),
                "reduc_ijikanri_2": str(inputs['reduc_ijikanri_2']),
                "reduc_ijikanri_3": str(inputs['reduc_ijikanri_3']),
                "pre_kyoukouka": True,
                "kisai_jutou": str(financial_rules['kisai_jutou']),
                "kisai_koufu": str(financial_rules['kisai_koufu']),
                "hojo_ritsu": str(financial_rules['hojo']),
                "zeimae_rieki": str(to_dec(0.0)),
                "SPC_keihi": str(SPC_costs['keihi']),
                "SPC_fee": str(SPC_costs['fee']),
                "SPC_shihon": str(SPC_costs['shihon']),
                "SPC_yobihi": str(SPC_costs['yobihi']),
                "SPC_hiyou_atsukai": SPC_hiyou_atsukai,
                "houjinzei_ritsu": str(tax_rates['houjinzei_ritsu']),
                "houjinjuminzei_kintou": str(tax_rates['houjinjuminzei_kintou']),
                "hudousanshutokuzei_hyoujun": str(tax_rates['hudousanshutokuzei_hyoujun']),
                "hudousanshutokuzei_ritsu": str(tax_rates['hudousanshutokuzei_ritsu']),
                "koteishisanzei_hyoujun": str(tax_rates['koteishisanzei_hyoujun']),
                "koteishisanzei_ritsu": str(tax_rates['koteishisanzei_ritsu']),
                "tourokumenkyozei_hyoujun": str(tax_rates['tourokumenkyozei_hyoujun']),
                "tourokumenkyozei_ritsu": str(tax_rates['tourokumenkyozei_ritsu']),
                "houjinjuminzei_ritsu_todouhuken": str(tax_rates['houjinjuminzei_ritsu_todouhuken']),
                "houjinjuminzei_ritsu_shikuchoson": str(tax_rates['houjinjuminzei_ritsu_shikuchoson']),
            }

        return initial_inputs
       

# FIからの_calculate_financials    
    def _calculate_financials(self,inputs):
        def to_dec(val):
            return Decimal(val).quantize(Decimal('0.000001'), ROUND_HALF_UP)

        if self.initial_inputs["proj_type"] == "DBO(SPCなし)" or self.initial_inputs["proj_type"] == "BT/DB(いずれもSPCなし)":
            shisetsu_seibi_paymentschedule_ikkatsu = to_dec(1)
        else:         
            shisetsu_seibi_paymentschedule_ikkatsu = inputs['shisetsu_seibi_ikkatsu_hiritsu']

        shisetsu_seibi_paymentschedule_kappu = to_dec(Decimal(1) - shisetsu_seibi_paymentschedule_ikkatsu)
        #kappu_kinri_spread = Decimal(self.sl15.value/100).quantize(Decimal('0.000001'), ROUND_HALF_UP),

        kisai_jutou = str(inputs['kisai_jutou'])
        kisai_koufu = str(inputs['kisai_koufu'])
        hojo_ritsu = str(inputs['hojo_ritsu'])

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

        chisai_kinri = Decimal(inputs['chisai_kinri'])/Decimal(100) # CSVの％表記を採取しているため、実数表記に切り替える。
        kijun_kinri = Decimal(self.initial_inputs["kijun_kinri"]) /Decimal(100) # CSVの％表記を採取しているため、実数表記に切り替える。
        kitai_bukka = Decimal(self.initial_inputs["kitai_bukka"]) /Decimal(100) # CSVの％表記を採取しているため、実数表記に切り替える。

        discount_rate = to_dec(kijun_kinri + kitai_bukka)
        #discount_rate = to_dec(discount_rate)

        target_years = 45
        #proj_years = int(self.initial_inputs['proj_years'])
        const_years = int(self.initial_inputs['const_years'])
        chisai_sueoki_kikan = inputs['chisai_sueoki_kikan']
        shoukan_kaishi_jiki = const_years + chisai_sueoki_kikan + 1

        lg_spread = to_dec(self.initial_inputs['lg_spread'])
        kappu_kinri_spread = inputs['kappu_kinri_spread']
        Kappu_kinri = kijun_kinri + lg_spread + kappu_kinri_spread
        Kappu_kinri = to_dec(Kappu_kinri)


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
        SPC_keihi_LCC = SPC_keihi + SPC_fee + houjinjuminzei_kintou #SPCが払うコスト(経費、手数料とも全て何かの使途に支払う前提)
        
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
            #return   {
            "advisory_fee": str(inputs['advisory_fee']),
            "chisai_kinri": str(chisai_kinri), 
            "chisai_shoukan_kikan": int(inputs['chisai_shoukan_kikan']),
            "chisai_sueoki_years": int(inputs['chisai_sueoki_kikan']),
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
            #return   {
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
        return final_inputs

# IIからの_save_to_db
    def _save_to_db(self, data):
        if os.path.exists("ii_db.json"):
            os.remove("ii_db.json")
        db = TinyDB('ii_db.json')
        db.insert(data)
        db.close()
        if self.page.session.store.contains_key("initial_inputs"):
            self.page.session.store.remove("initial_inputs")
        self.page.session.store.set("initial_inputs",data)


# FIからの_save_to_db
    def _save_to_db(self, data):
        if self.page.session.store.contains_key("final_inputs"):
            self.page.session.store.remove("final_inputs")
        if os.path.exists("fi_db.json"):
            os.remove("fi_db.json")
        db = TinyDB('fi_db.json')
        db.insert(data)
        db.close()
        self.page.session.store.set("final_inputs",data)


#「要約」カラムと「入力値等」カラムの材料
    #def build(self):
        PSC_res_df = self.selected_res_list[0]
        PSC_pv_df = self.selected_res_list[1]
        LCC_res_df = self.selected_res_list[2]
        LCC_pv_df = self.selected_res_list[3]
        SPC_res_df = self.selected_res_list[4]
        SPC_check_df = self.selected_res_list[5]
        Risk_res_df = self.selected_res_list[6]
        VFM_res_df = self.selected_res_list[7]
        PIRR_res_df = self.selected_res_list[8]
        res_summ_df = self.selected_res_list[9]
        final_inputs_df = self.selected_res_list[10]

        PSC_res_df['year'] = PSC_res_df['year'].apply(lambda x: str(x).replace('00:00:00.000000',''))
        LCC_res_df['year'] = LCC_res_df['year'].apply(lambda x: str(x).replace('00:00:00.000000',''))
        SPC_res_df['year'] = SPC_res_df['year'].apply(lambda x: str(x).replace('00:00:00.000000',''))
        SPC_check_df['year'] = SPC_check_df['year'].apply(lambda x: str(x).replace('00:00:00.000000',''))
        res_summ_df['discount_rate'] = res_summ_df['discount_rate'] * 100

        PSC_res_df = PSC_res_df.drop(['chisai_zansai', 'kisai_shoukansumi_gaku', 'datetime', 'user_id', 'calc_id'], axis=1)
        PSC_pv_df =  PSC_pv_df.drop(['datetime', 'user_id', 'calc_id'], axis=1)
        LCC_res_df = LCC_res_df.drop(['shisetsu_seibihi_kappugoukei', 'chisai_zansai', 'kisai_shoukansumi_gaku', 'datetime', 'user_id', 'calc_id'], axis=1)
        LCC_pv_df = LCC_pv_df.drop(['datetime', 'user_id', 'calc_id'], axis=1)
        SPC_res_df = SPC_res_df.drop(['payments_total_full', 'datetime', 'user_id', 'calc_id'], axis=1)
        SPC_check_df = SPC_check_df.drop(['payments_total_full', 'net_income_full',  'datetime', 'user_id', 'calc_id'], axis=1)
        Risk_res_df = Risk_res_df.drop(['datetime', 'user_id', 'calc_id'], axis=1)
        VFM_res_df = VFM_res_df.drop(['datetime', 'user_id', 'calc_id'], axis=1)
        PIRR_res_df = PIRR_res_df.drop(['datetime', 'user_id', 'calc_id'], axis=1)
        res_summ_df = res_summ_df.drop(['datetime', 'user_id', 'calc_id'], axis=1)
        final_inputs_df = final_inputs_df.drop(['datetime', 'user_id', 'calc_id'], axis=1)

        PSC_res_income_df = PSC_res_df[['periods','year','hojokin', 'kouhukin', 'kisai_gaku', 'riyou_ryoukin', 'income_total']]
        PSC_res_payments_df = PSC_res_df[['periods','year','shisetsu_seibihi', 'ijikanri_unneihi', 'monitoring_costs', 'kisai_shoukan_gaku', 'kisai_risoku_gaku', 'payments_total', 'net_payments']]
        LCC_res_income_df = LCC_res_df[['periods','year','hojokin', 'kouhukin', 'kisai_gaku', 'zeishu', 'income_total']]
        LCC_res_payments_df = LCC_res_df[['periods','year','shisetsu_seibihi_ikkatsu', 'shisetsu_seibihi_kappuganpon', 'shisetsu_seibihi_kappukinri', 'ijikanri_unneihi', 'monitoring_costs', 'SPC_keihi', 'kisai_shoukan_gaku', 'kisai_risoku_gaku', 'payments_total', 'net_payments']]
        SPC_res_income_df = SPC_res_df[['periods','year','shisetsu_seibihi_taika_ikkatsu', 'shisetsu_seibihi_taika_kappuganpon', 'shisetsu_seibihi_taika_kappukinri', 'ijikanri_unneihi_taika', 'SPC_hiyou_taika', 'riyou_ryoukin', 'income_total']]
        SPC_res_payments_df = SPC_res_df[['periods','year','shisetsu_seibihi', 'ijikanri_unneihi', 'shiharai_risoku', 'SPC_keihi', 'SPC_setsuritsuhi', 'houjinzei_etc', 'payments_total', 'net_income']]

        PSC_res_income_df = PSC_res_income_df.rename(
            columns={
                'periods':'経過年度', 
                'year':'スケジュール', 
                'hojokin':'補助金', 
                'kouhukin':'交付金', 
                'kisai_gaku':'起債発行額', 
                'riyou_ryoukin':'利用料金収入',
                'income_total':'収入計', 
            }
        )
        PSC_res_payments_df = PSC_res_payments_df.rename(
            columns={
                'periods':'経過年度', 
                'year':'スケジュール', 
                'shisetsu_seibihi':'施設整備費用', 
                'ijikanri_unneihi':'維持管理運営費用',
                'monitoring_costs':'モニタリング等費用', 
                'kisai_shoukan_gaku':'起債償還額',
                'kisai_risoku_gaku':'起債利息', 
                'payments_total':'支出計',
                'net_payments':'収支（キャッシュ・フロー）', 
            }
        )
        PSC_pv_df = PSC_pv_df.rename(
            columns={
                'period':'経過年数',
                'net_payments':'収支（キャッシュ・フロー）', 
                'discount_factor':'割引係数', 
                'present_value':'収支（キャッシュ・フロー）現在価値', 
            }
        )
        LCC_res_income_df = LCC_res_income_df.rename(
            columns={
                'periods':'経過年度', 
                'year':'スケジュール', 
                'hojokin':'補助金', 
                'kouhukin':'交付金', 
                'kisai_gaku':'起債発行額', 
                'zeishu':'税収',
                'income_total':'収入計', 
            }
        )
        LCC_res_payments_df = LCC_res_payments_df.rename(
            columns={
                'periods':'経過年度', 
                'year':'スケジュール', 
                'shisetsu_seibihi_ikkatsu':'施設整備対価(一括払)',
                'shisetsu_seibihi_kappuganpon':'施設整備対価(割賦元本)',
                'shisetsu_seibihi_kappukinri':'施設整備対価(割賦金利)', 
                'ijikanri_unneihi':'維持管理費対価', 
                'monitoring_costs':'モニタリング等費用',
                'SPC_keihi':'SPC費用', 
                'kisai_shoukan_gaku':'起債償還額',
                'kisai_risoku_gaku':'起債利息', 
                'payments_total':'支出計',
                'net_payments':'収支', 
            }
        )
        LCC_pv_df = LCC_pv_df.rename(
            columns={
                'period':'経過年数',
                'net_payments':'収支(キャッシュ・フロー)', 
                'discount_factor':'割引係数', 
                'present_value':'収支(キャッシュ・フロー)現在価値',
            }
        )
        SPC_res_income_df = SPC_res_income_df.rename(
            columns={
                'periods':'経過年度', 
                'year':'スケジュール', 
                'shisetsu_seibihi_taika_ikkatsu':'施設整備対価(一括払)',
                'shisetsu_seibihi_taika_kappuganpon':'施設整備対価(割賦元本)',
                'shisetsu_seibihi_taika_kappukinri':'施設整備対価(割賦金利)', 
                'ijikanri_unneihi_taika':'維持管理費対価',
                'SPC_hiyou_taika':'SPC費用対価', 
                'riyou_ryoukin':'利用料金収入', 
                'income_total':'収入計', 
            }
        )
        SPC_res_payments_df = SPC_res_payments_df.rename(
            columns={
                'periods':'経過年度', 
                'year':'スケジュール', 
                'shisetsu_seibihi':'施設整備費用',
                'ijikanri_unneihi':'維持管理費', 
                'kariire_ganpon_hensai':'(借入元本返済)', 
                'shiharai_risoku':'支払利息',
                'SPC_keihi':'SPC経費', 
                'SPC_setsuritsuhi':'SPC当初費用（設立費用、予備費）', 
                'houjinzei_etc':'法人税・公租公課', 
                'payments_total':'支出計', 
                'net_income':'収支(キャッシュ・フロー)', 
            }
        )
        SPC_check_df = SPC_check_df.rename(
            columns={
                'year':'スケジュール', 
                'income_total':'収入計', 
                'kariire_ganpon_hensai':'借入元本返済', 
                'payments_total':'支出計',
                'net_income':'収支(キャッシュ・フロー)', 
                'Cash_for_P_payment':'元本返済充当可能額', 
                'P_payment_check':'元本返済可否', 
            }
        )
        Risk_res_df = Risk_res_df.rename(
            columns={
                'risk_adjust_gaku':'リスク調整額', 
            }
        )
        res_summ_df = res_summ_df.rename(
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
        self.final_inputs_df = final_inputs_df.transpose().reset_index().rename(columns={"index":"項目名", 0:"値"})
        simpledt_finalinputs_df = DataFrame(self.final_inputs_df)
        simpledt_finalinputs_dt = simpledt_finalinputs_df.datatable
        self.table_finalinputs = simpledt_finalinputs_dt

        simpledt_PSC_income_df = DataFrame(PSC_res_income_df)
        simpledt_PSC_income_dt = simpledt_PSC_income_df.datatable
        self.table_PSC_income = simpledt_PSC_income_dt
        simpledt_PSC_payments_df = DataFrame(PSC_res_payments_df)
        simpledt_PSC_payments_dt = simpledt_PSC_payments_df.datatable
        simpledt_PSC_payments_dt.column_spacing = 10
        simpledt_PSC_payments_dt.headline_row_height =30 
        self.table_PSC_payments = simpledt_PSC_payments_dt

        PSC_pv_df['経過年数'] = PSC_pv_df['経過年数'].apply(lambda i: int(i))
        simpledt_PSC_pv_df = DataFrame(PSC_pv_df)
        simpledt_PSC_pv_dt = simpledt_PSC_pv_df.datatable
        self.table_PSC_pv = simpledt_PSC_pv_dt

        LCC_pv_df['経過年数'] = LCC_pv_df['経過年数'].apply(lambda i: int(i))
        simpledt_LCC_income_df = DataFrame(LCC_res_income_df)
        simpledt_LCC_income_dt = simpledt_LCC_income_df.datatable
        self.table_LCC_income = simpledt_LCC_income_dt
        simpledt_LCC_payments_df = DataFrame(LCC_res_payments_df)
        simpledt_LCC_payments_dt = simpledt_LCC_payments_df.datatable
        simpledt_LCC_payments_dt.column_spacing = 10
        simpledt_LCC_payments_dt.headline_row_height =30 
        self.table_LCC_payments = simpledt_LCC_payments_dt

        simpledt_LCC_pv_df = DataFrame(LCC_pv_df)
        simpledt_LCC_pv_dt = simpledt_LCC_pv_df.datatable
        self.table_LCC_pv = simpledt_LCC_pv_dt

        simpledt_SPC_income_df = DataFrame(SPC_res_income_df)
        simpledt_SPC_income_dt = simpledt_SPC_income_df.datatable
        self.table_SPC_income = simpledt_SPC_income_dt
        simpledt_SPC_payments_df = DataFrame(SPC_res_payments_df)
        simpledt_SPC_payments_dt = simpledt_SPC_payments_df.datatable
        self.table_SPC_payments = simpledt_SPC_payments_dt

        simpledt_SPC_check_df = DataFrame(SPC_check_df)
        simpledt_SPC_check_dt = simpledt_SPC_check_df.datatable
        self.table_SPC_check = simpledt_SPC_check_dt

        simpledt_Risk_df = DataFrame(Risk_res_df)
        simpledt_Risk_dt = simpledt_Risk_df.datatable
        self.table_Risk = simpledt_Risk_dt

        res_summ_df_t = res_summ_df.transpose().reset_index()
        res_summ_df_t = res_summ_df_t.rename(columns={"index":"項目名", 0:"値"})
        simpledt_res_summ_df = DataFrame(res_summ_df_t)
        simpledt_res_summ_dt = simpledt_res_summ_df.datatable
        self.table_res_summ = simpledt_res_summ_dt

        lv_01 = ft.ListView(
            expand=True, spacing=10, padding=10, auto_scroll=True, horizontal=False
        )
        lv_01.controls.append(ft.Text('算定結果要約'))
        lv_01.controls.append(self.table_res_summ)

        lv_02 = ft.ListView(
            expand=True, spacing=10, padding=10, auto_scroll=True, horizontal=False
        )
        lv_02.controls.append(ft.Text('PSCでの公共側収支（収入）'))
        lv_02.controls.append(self.table_PSC_income)
        lv_02.controls.append(ft.Text('PSCでの公共側収支（支出）'))
        lv_02.controls.append(self.table_PSC_payments)
        lv_02.controls.append(ft.Divider())
        lv_02.controls.append(ft.Text('PSCでの公共側キャッシュ・フローとその現在価値'))
        lv_02.controls.append(self.table_PSC_pv)
        lv_02.controls.append(ft.Divider())
        lv_02.controls.append(ft.Text('PFI-LCCでの公共側収支（収入）'))
        lv_02.controls.append(self.table_LCC_income)
        lv_02.controls.append(ft.Text('PFI-LCCでの公共側収支（支出）'))
        lv_02.controls.append(self.table_LCC_payments)
        lv_02.controls.append(ft.Divider())
        lv_02.controls.append(ft.Text('PFI-LCCでの公共側キャッシュ・フローとその現在価値'))
        lv_02.controls.append(self.table_LCC_pv)
        lv_02.controls.append(ft.Divider())
        lv_02.controls.append(ft.Text('PSCへのリスク調整'))
        lv_02.controls.append(self.table_Risk)

        lv_03 = ft.ListView(
            expand=True, spacing=10, padding=10, auto_scroll=True, horizontal=False
        )
        lv_03.controls.append(ft.Text('PFI-LCCでのSPC側収支（収入）'))
        lv_03.controls.append(self.table_SPC_income)
        lv_03.controls.append(ft.Text('PFI-LCCでのSPC側収支（支出）'))
        lv_03.controls.append(self.table_SPC_payments)
        lv_03.controls.append(ft.Divider())
        lv_03.controls.append(ft.Text('PFI-LCCでのSPCの返済資金確認結果'))
        lv_03.controls.append(self.table_SPC_check)

        lv_04 = ft.ListView(
            expand=True, spacing=10, padding=10, auto_scroll=True, horizontal=False
        )
        lv_04.controls.append(ft.Text('入力値・パラメータ等一覧'))
        lv_04.controls.append(self.table_finalinputs)

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
                                    label="結果・入力の要約",
                                ),
                                ft.Tab(
                                    label="PSC, LCCでの公共側収支等",
                                ),
                                ft.Tab(
                                    label="SPC収支等",
                                ),
                                ft.Tab(
                                    label="入力値等一覧",
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
                                            lv_02,
                                        ],
                                    alignment=ft.MainAxisAlignment.SPACE_AROUND,
                                    ),
                                    width=2100,
                                    padding=10,
                                    height=4000,
                                    margin=10,
                                ),
                                ft.Container(
                                    content=ft.Column(
                                        controls=[
                                            lv_03,
                                        ],
                                    alignment=ft.MainAxisAlignment.SPACE_AROUND,
                                    ),
                                    width=2100,
                                    padding=10,
                                    height=2000,
                                    margin=10,
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
                            ],       
                        )
                    ],
                ),
            )
        ]

