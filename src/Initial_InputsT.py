import sys
sys.dont_write_bytecode = True
import os
import flet as ft
# from flet_core.session_storage import SessionStorage
import pandas as pd
import pyarrow as pa
import datetime
import timeflake
from tinydb import TinyDB, Query
from decimal import *
from zoneinfo import ZoneInfo
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


@ft.control
class Initial_Inputs(ft.Column):

    def init(self):
        #super().__init__()
        self.title = "初期入力"
        self.width = 500
        self.height = 2000
        self.window_width = 500
        self.window_height = 2000
        self.resizable = 1
        self.expand=True
        self.scroll=ft.ScrollMode.AUTO

        slider_value00 = ft.Text("", size=30, weight=ft.FontWeight.W_200)
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

        def get_options(list):
            options=[]
            for i in list:
                options.append(
                    ft.DropdownOption(
                        key=i['key'], 
                        content = ft.Text(value=i['key'])
                    )
                )
            return options

        def handle_slider_change(e):
            sl_value = e.control.value
            target_text_control = e.control.data
            target_text_control.value = str(sl_value)
            target_text_control.update()


        options_1 = [
            {'key':"国"},
            {'key':"都道府県"},
            {'key':"市町村"},
        ]
        options_2 = [
            {'key':"サービス購入型"},
            #{key:"コンセッション（スタジアム・アリーナタイプ）"},
            #{key: "コンセッション（下水道タイプ）"},
        ]
        options_3 = [
            {'key':"BTO"},
            {'key':"DBO(SPCなし)"},
            {'key':"BOT/BOO"},
            {'key':"BT/DB(いずれもSPCなし)"},
        ]
        options_4 = [
            {'key':"1"}, {'key':"2"}, {'key':"3"}, {'key':"4"}, {'key':"5"},
            {'key':"6"}, {'key':"7"}, {'key':"8"}, {'key':"9"}, {'key':"10"},
            {'key':"11"},{'key':"12"},{'key':"13"},{'key':"14"},{'key':"15"},
            {'key':"16"},{'key':"17"},{'key':"18"},{'key':"19"},{'key':"20"},
            {'key':"21"},{'key':"22"},{'key':"23"},{'key':"24"},{'key':"25"},
            {'key':"26"},{'key':"27"},{'key':"28"},{'key':"29"},{'key':"30"},
        ]
        options_5 = [
            {'key':"1"}, {'key':"2"}, {'key':"3"}, {'key':"4"}, {'key':"5"},
            {'key':"6"}, {'key':"7"}, {'key':"8"}, {'key':"9"}, {'key':"10"},
            {'key':"11"},{'key':"12"},{'key':"13"},{'key':"14"},{'key':"15"},
            {'key':"16"},{'key':"17"},{'key':"18"},{'key':"19"},{'key':"20"},
            {'key':"21"},{'key':"22"},{'key':"23"},{'key':"24"},{'key':"25"},
            {'key':"26"},
        ]
        options_6 = [
            {'key':"1"}, {'key':"2"}, {'key':"3"}, {'key':"4"}, {'key':"5"},
        ]
    
        self.dd1 = ft.Dropdown(
            label="管理者の種別",
            #hint_text="管理者の種別を選択してください",
            #width=400,
            options=get_options(options_1),
        )
        self.dd2 = ft.Dropdown(
            label="事業の方式",
            #hint_text="事業の方式を選択してください",
            #width=400,
            options=get_options(options_2),
        )
        self.dd3 = ft.Dropdown(
            label="事業の類型",
            #hint_text="事業の類型を選択してください",
            #width=400,
            options=get_options(options_3),
        )
        self.dd4 = ft.Dropdown(
            label="事業期間",
            #hint_text="事業期間を選択してください(施設整備期間以上)",
            #width=400,
            #value="20",
            options=get_options(options_4),
        )
        self.dd5 = ft.Dropdown(
            label="地方債償還期間",
            #hint_text="地方債償還期間を選択してください",
            #width=400,
            #value="20",
            options=get_options(options_5),
        )
        self.dd6 = ft.Dropdown(
            label="施設整備期間",
            #hint_text="施設整備期間を選択してください",
            #width=400,
            #value="1",
            options=get_options(options_6),
        )
        tx0 = ft.Text("施設整備費 落札価格ベース(百万円)")
        self.sl0 = ft.Slider(
            value=0,
            min=0,
            max=50000,
            divisions=50000,
            label="{value}百万円",
            round=0,
            on_change=handle_slider_change,
            data=slider_value00
        )
        tx1 = ft.Text("施設整備費 予算単価ベース(百万円)")
        self.sl1 = ft.Slider(
            value=0,
            min=0,
            max=50000,
            divisions=50000,
            label="{value}百万円",
            round=0,
            on_change=handle_slider_change,
            data=slider_value01
        )
        tx2 = ft.Text("維持管理運営費(年額)人件費 落札価格ベース(百万円)")
        self.sl2 = ft.Slider(
            value=0,
            min=0,
            max=500,
            divisions=500,
            label="{value}百万円",
            round=0,
            on_change=handle_slider_change,
            data=slider_value02
        )
        tx3 = ft.Text("維持管理運営費(年額)人件費 予算単価ベース(百万円)")
        self.sl3 = ft.Slider(
            value=0,
            min=0,
            max=500,
            divisions=500,
            on_change=handle_slider_change,
            data=slider_value03,
            label="{value}百万円",
            round=0,
        )
        tx4 = ft.Text("維持管理運営費(年額)修繕費 落札価格ベース(百万円)")
        self.sl4 = ft.Slider(
            value=0,
            min=0,
            max=100,
            divisions=100,
            label="{value}百万円",
            round=0,
            on_change=handle_slider_change,
            data=slider_value04
        )
        tx5 = ft.Text("維持管理運営費(年額)修繕費 予算単価ベース(百万円)")
        self.sl5 = ft.Slider(
            value=0,
            min=0,
            max=100,
            divisions=100,
            label="{value}百万円",
            round=0,
            on_change=handle_slider_change,
            data=slider_value05
        )
        tx6 = ft.Text("維持管理運営費(年額)動力費 落札価格ベース(百万円)")
        self.sl6 = ft.Slider(
            value=0,
            min=0,
            max=100,
            divisions=100,
            label="{value}百万円",
            round=0,
            on_change=handle_slider_change,
            data=slider_value06
        )
        tx7 = ft.Text("維持管理運営費(年額)動力費 予算単価ベース(百万円)")
        self.sl7 = ft.Slider(
            value=0,
            min=0,
            max=100,
            divisions=100,
            label="{value}百万円",
            round=0,
            on_change=handle_slider_change,
            data=slider_value07
        )
        tx8 = ft.Text("施設整備費の効率性(%)(推奨:5%")
        self.sl8 = ft.Slider(
            value=5,
            min=0.0,
            max=20,
            divisions=200,
            label="{value}%",
            round=1,
            on_change=handle_slider_change,
            data=slider_value08
        )
        tx9 = ft.Text("維持管理運営費の効率性(人件費,%)(推奨:5%)")
        self.sl9 = ft.Slider(
            value=5,
            min=0.0,
            max=20,
            divisions=200,
            label="{value}%",
            round=1,
            on_change=handle_slider_change,
            data=slider_value09
        )
        tx10 = ft.Text("維持管理運営費の効率性(修繕費,%)(推奨:5%)")
        self.sl10 = ft.Slider(
            value=5,
            min=0.0,
            max=20,
            divisions=200,
            label="{value}%",
            round=1,
            on_change=handle_slider_change,
            data=slider_value10
        )
        tx11 = ft.Text("維持管理運営費の効率性(動力費,%)(推奨:5%)")
        self.sl11 = ft.Slider(
            value=5,
            min=0.0,
            max=20,
            divisions=200,
            label="{value}%",
            round=1,
            on_change=handle_slider_change,
            data=slider_value11
        )
        tx12 = ft.Text("落札率(競争の効果反映,%)(推奨:95%)")
        self.sl12 = ft.Slider(
            value=95,
            min=0,
            max=100,
            divisions=100,
            label="{value}%",
            on_change=handle_slider_change,
            data=slider_value12
        )
        b = ft.Button(content="初期値の入力", on_click=self.button_clicked)

        self.controls = [
            #ft.Page.title = "初期入力",

            self.dd1,  self.dd2, self.dd3,  self.dd4,  self.dd5,  self.dd6, 
            ft.Divider(height=1, color="amber"),
            tx0,  slider_value00, self.sl0, ft.Divider(height=1, color="amber"),
            tx1,  slider_value01, self.sl1, ft.Divider(height=1, color="amber"), 
            tx2,  slider_value02, self.sl2, ft.Divider(height=1, color="amber"),
            tx3,  slider_value03, self.sl3, ft.Divider(height=1, color="amber"),
            tx4,  slider_value04, self.sl4, ft.Divider(height=1, color="amber"),
            tx5,  slider_value05, self.sl5, ft.Divider(height=1, color="amber"),
            tx6,  slider_value06, self.sl6, ft.Divider(height=1, color="amber"),
            tx7,  slider_value07, self.sl7, ft.Divider(height=1, color="amber"),
            tx8,  slider_value08, self.sl8, ft.Divider(height=1, color="amber"),
            tx9,  slider_value09, self.sl9, ft.Divider(height=1, color="amber"),
            tx10, slider_value10, self.sl10,ft.Divider(height=1, color="amber"),
            tx11, slider_value11, self.sl11,ft.Divider(height=1, color="amber"),
            tx12, slider_value12, self.sl12,ft.Divider(height=1, color="amber"),
            b
        ]

    async def button_clicked(self, e):
        input_data = self._extract_inputs()

        calc_results = self._calculate_financials(input_data)
        
        self._save_to_db(calc_results)
        await self.page.push_route("/final_inputs")
        

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
            'rakusatsu_ritsu': rakusatsu_ritsu
        }
    
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

        JGB_rates_df = pd.read_csv("src/JGB_rates.csv", sep="\t", encoding="utf-8", header=None, names=["year", "rate"],).set_index("year")
        JRB_rates_df = pd.read_csv("src/JRB_rates.csv", sep="\t", encoding="utf-8", names=[0,1,2,3,4,5], index_col=0)

        y, d = divmod(inputs['proj_years'], 5)
        if y >= 1:
            r_idx = str((y + 1) * 5) + "年" if d > 2 else str(y * 5) + "年"
        else:
            r_idx = str(d) + "年"

        r1 = Decimal(JGB_rates_df.loc[r_idx].iloc[0])
        r2 = Decimal(JRB_rates_df.loc[inputs['chisai_shoukan_kikan']][inputs['const_years']])
        kitai_bukka_j = Decimal(pd.read_csv("src/BOJ_ExpInflRate_down.csv", encoding="shift-jis", skiprows=1).dropna().iloc[-1, 1])
        
        chisai_sueoki_kikan = int(inputs['const_years']) if inputs['const_years'] else int(0)
        gonensai_rimawari = Decimal(JGB_rates_df.loc["5年"].iloc[0])
        kitai_bukka = to_dec(kitai_bukka_j - gonensai_rimawari)
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
                "kijun_kinri": str(r1),
                "chisai_kinri": str(r2),
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

    def _save_to_db(self, data):
        if os.path.exists("ii_db.json"):
            os.remove("ii_db.json")
        db = TinyDB('ii_db.json')
        db.insert(data)
        db.close()
        self.page.session.store.set("initial_inputs",data)

       
#def main(page: ft.Page):
#    page.width = 500
#    page.height = 2000
#    page.title = "初期入力"
#    page.window_width = 500
#    page.window_height = 2000
#    page.window_resizable = True
#    page.expand=True
#    page.scroll=ft.ScrollMode.AUTO
#    #initial_inputs = Initial_Inputs()
#    page.add(
#            Initial_Inputs()
#    )


#ft.run(main)

