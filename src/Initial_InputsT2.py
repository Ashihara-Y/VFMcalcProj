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
from scipy.interpolate import PchipInterpolator
import yaml
from models_ii_1 import InitialInputs
#from models_ii_2 import InitialInputs2

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


@ft.control
class Initial_Inputs(ft.Column):

    def __init__(self, ui_init_values:dict=None, current_locale="ja"):
        super().__init__(
            expand=True,
            scroll=ft.ScrollMode.AUTO,
        )
        #self.title = "初期入力"
        self.width = 500
        self.height = 2000
        self.window_height = 2000
        self.window_width = 500
        #self.resizable = 1
        #self.expand=True
        #self.scroll=ft.ScrollMode.AUTO

        self.ui_init_values = ui_init_values or {}
        self.current_locale = current_locale
        self.slider_controls = {}
        self.dropdown_controls = {}

        self._build_ui()

    def _create_dropdowns_from_yaml(self):
            with open("src/ui_config_II.yaml", "r", encoding="utf-8") as f:
                ui_config = yaml.safe_load(f)
                dropdown_config = ui_config[self.current_locale]['dropdowns']
                
                dropdowns = []
                
                for dd_cfg in dropdown_config:
                    dd_id = dd_cfg['id']
                    if dd_id in self.ui_init_values:
                        current_value = self.ui_init_values[dd_id]
                    else:
                        current_value = dd_cfg['default_value']

                    options = [ft.DropdownOption(opt) for opt in dd_cfg['options']]
                    dropdown_control = ft.Dropdown(
                        label=dd_cfg['label'],
                        options=options,
                        value=str(current_value)
                    )
                    self.dropdown_controls[dd_id] = dropdown_control
                    dropdowns.append(dropdown_control)

                return dropdowns

    def handle_slider_change(self, e):
            sl_value = e.control.value
            target_text_control = e.control.data
            target_text_control.value = str(sl_value)
            target_text_control.update()

    def _create_sliders_from_yaml(self):
            with open("src/ui_config_II.yaml", "r", encoding="utf-8") as f:
                ui_config = yaml.safe_load(f)
                slider_configs = ui_config[self.current_locale]['sliders']
                
                sliders =[]
                
                for slider_cfg in slider_configs:
                    sid = slider_cfg['id']
                    if sid in self.ui_init_values:
                        raw_value = self.ui_init_values[sid]
                    else:
                        raw_value = slider_cfg['default_value']

                    current_value = float(raw_value)

                    slider_value_control = ft.Text("", size=30, weight=ft.FontWeight.W_200)
                    slider_value_control.value = str(current_value)

                    slider_control = ft.Slider(
                        value=current_value,
                        min=slider_cfg['min'],
                        max=slider_cfg['max'],
                            divisions=slider_cfg['divisions'],
                            label="{value}" + slider_cfg['unit'],
                            round=slider_cfg['round'],
                            on_change=self.handle_slider_change,
                            data=slider_value_control
                        )
                    
                    self.slider_controls[sid] = slider_control
                    divider = ft.Divider(height=1, color="amber")
                    # slider_controlとslider_value_controlを、表示テキスト、deviderとタブルにまとめて、extend()でリストに追加
                    sliders.extend((ft.Text(slider_cfg['tx']), slider_value_control, slider_control, divider))

                return sliders

    def _build_ui(self):
        """UI部品を生成し、自身(Column)のcontrolsにセットする"""
        # 関数を呼んでリストを取得
        dropdowns_ui = self._create_dropdowns_from_yaml()
        sliders_ui = self._create_sliders_from_yaml()

        b = ft.Button(content="初期値の入力", on_click=self.button_clicked)

        # リストの前に `*` (アスタリスク) を付けて、リストの中身を平坦化(アンパック)して渡します。
        self.controls = [
            *dropdowns_ui,
            ft.Divider(height=1, color="amber"),
            *sliders_ui,
            b,
        ]

    async def button_clicked(self, e):
        inputs = InitialInputs.model_validate(self._extract_inputs())

        calc_results = self._calculate_financials(inputs=inputs)

        self._save_to_db(calc_results)
        await self.page.push_route("/final_inputs")
        

    def _extract_inputs(self):
    
        mgmt_type = self.dropdown_controls['mgmt_type'].value
        proj_ctgry = self.dropdown_controls['proj_ctgry'].value
        proj_type = self.dropdown_controls['proj_type'].value

        proj_years = int(self.dropdown_controls['const_years'].value) if proj_type == "BT/DB(いずれもSPCなし)" else int(self.dropdown_controls['proj_years'].value)

        #proj_years = int(raw_proj_years) if raw_proj_years else 0
        const_years = int(self.dropdown_controls['const_years'].value)
        chisai_shoukan_kikan = int(self.dropdown_controls['chisai_shoukan_kikan'].value)

        ijikanri_unnei_years = proj_years - const_years

        shisetsu_seibi_org_R = self.slider_controls['shisetsu_seibi_org_R'].value
        shisetsu_seibi_org_Y = self.slider_controls['shisetsu_seibi_org_Y'].value
        ijikanri_unnei_1_org_R = self.slider_controls['ijikanri_unnei_1_org_R'].value
        ijikanri_unnei_1_org_Y = self.slider_controls['ijikanri_unnei_1_org_Y'].value
        ijikanri_unnei_2_org_R= self.slider_controls['ijikanri_unnei_2_org_R'].value
        ijikanri_unnei_2_org_Y = self.slider_controls['ijikanri_unnei_2_org_Y'].value
        ijikanri_unnei_3_org_R = self.slider_controls['ijikanri_unnei_3_org_R'].value
        ijikanri_unnei_3_org_Y = self.slider_controls['ijikanri_unnei_3_org_Y'].value

        reduc_shisetsu_pct = self.slider_controls['reduc_shisetsu_pct'].value
        reduc_ijikanri_1_pct = self.slider_controls['reduc_ijikanri_1_pct'].value
        reduc_ijikanri_2_pct = self.slider_controls['reduc_ijikanri_2_pct'].value
        reduc_ijikanri_3_pct = self.slider_controls['reduc_ijikanri_3_pct'].value
        rakusatsu_ritsu_pct = self.slider_controls['rakusatsu_ritsu_pct'].value

        JGB_rates_df = pd.read_csv("JGB_rates.csv", sep="\t", encoding="utf-8", header=None, names=["year", "rate"],).set_index("year")
        JRB_rates_df = pd.read_csv("JRB_rates.csv", sep="\t", encoding="utf-8", names=[0,1,2,3,4,5], index_col=0)

        val_array = JGB_rates_df.iloc[0:,0].to_numpy()
        col_series = JGB_rates_df.T.columns.to_series().apply(lambda x: x[:-1])
        col_array = col_series.values.astype(int)
        pchip_interp = PchipInterpolator(col_array, val_array)
        r1_fl_str = str(pchip_interp(proj_years))
        r1 = Decimal(r1_fl_str).quantize(Decimal('0.000001'), rounding=ROUND_HALF_UP)
        #r1 = Decimal(JGB_rates_df.loc[r_idx].iloc[0])
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

            'reduc_shisetsu_pct': reduc_shisetsu_pct,
            'reduc_ijikanri_1_pct': reduc_ijikanri_1_pct,
            'reduc_ijikanri_2_pct': reduc_ijikanri_2_pct,
            'reduc_ijikanri_3_pct': reduc_ijikanri_3_pct,
            'rakusatsu_ritsu_pct': rakusatsu_ritsu_pct,

            'r1': r1,
            'r2': r2,
            'kitai_bukka_j': kitai_bukka_j,
            'gonensai_rimawari': gonensai_rimawari,
        }
    
    def _calculate_financials(self, inputs):
        def to_dec(val):
            return Decimal(val).quantize(Decimal('0.000001'), ROUND_HALF_UP)

        calc_id = timeflake.random()
        dtime = datetime.datetime.fromtimestamp(calc_id.timestamp // 1000, tz=ZoneInfo("Asia/Tokyo"))
        const_start_date = datetime.date(dtime.year, dtime.month, dtime.day).strftime('%Y-%m-%d')

        shisetsu_seibi_org = to_dec(inputs.shisetsu_seibi_org_R + inputs.shisetsu_seibi_org_Y)
        shisetsu_seibi = to_dec(shisetsu_seibi_org * inputs.rakusatsu_ritsu)
        ijikanri_unnei_1_org = to_dec(inputs.ijikanri_unnei_1_org_R + inputs.ijikanri_unnei_1_org_Y)
        ijikanri_unnei_1 = to_dec(ijikanri_unnei_1_org * inputs.rakusatsu_ritsu)
        ijikanri_unnei_2_org = to_dec(inputs.ijikanri_unnei_2_org_R + inputs.ijikanri_unnei_2_org_Y)
        ijikanri_unnei_2 = to_dec(ijikanri_unnei_2_org * inputs.rakusatsu_ritsu)
        ijikanri_unnei_3_org = to_dec(inputs.ijikanri_unnei_3_org_R + inputs.ijikanri_unnei_3_org_Y)
       
        ijikanri_unnei_3_org = to_dec(inputs.ijikanri_unnei_3_org_R + inputs.ijikanri_unnei_3_org_Y)
        ijikanri_unnei_3 = to_dec(ijikanri_unnei_3_org * inputs.rakusatsu_ritsu)

        yosantanka_hiritsu_shisetsu = to_dec(inputs.shisetsu_seibi_org_Y/shisetsu_seibi_org) if shisetsu_seibi_org else to_dec(0)
        yosantanka_hiritsu_ijikanri_1 = to_dec(inputs.ijikanri_unnei_1_org_Y/ijikanri_unnei_1_org) if ijikanri_unnei_1_org else to_dec(0)
        yosantanka_hiritsu_ijikanri_2 = to_dec(inputs.ijikanri_unnei_2_org_Y/ijikanri_unnei_2_org) if ijikanri_unnei_2_org else to_dec(0)
        yosantanka_hiritsu_ijikanri_3 = to_dec(inputs.ijikanri_unnei_3_org_Y/ijikanri_unnei_3_org) if ijikanri_unnei_3_org else to_dec(0)

        shisetsu_seibi_org_LCC = to_dec(shisetsu_seibi_org * (Decimal(1.00) - inputs.reduc_shisetsu))
        shisetsu_seibi_LCC = to_dec(shisetsu_seibi * (Decimal(1.00) - inputs.reduc_shisetsu))
        ijikanri_unnei_1_org_LCC = to_dec(ijikanri_unnei_1_org * (Decimal(1.00) - inputs.reduc_ijikanri_1))
        ijikanri_unnei_1_LCC = to_dec(ijikanri_unnei_1 * (Decimal(1.00) - inputs.reduc_ijikanri_1))
        ijikanri_unnei_2_org_LCC = to_dec(ijikanri_unnei_2_org * (Decimal(1.00) - inputs.reduc_ijikanri_2))
        ijikanri_unnei_2_LCC = to_dec(ijikanri_unnei_2 * (Decimal(1.00) - inputs.reduc_ijikanri_2))
        ijikanri_unnei_3_org_LCC = to_dec(ijikanri_unnei_3_org * (Decimal(1.00) - inputs.reduc_ijikanri_3))
        ijikanri_unnei_3_LCC = to_dec(ijikanri_unnei_3 * (Decimal(1.00) - inputs.reduc_ijikanri_3))

        chisai_sueoki_kikan = int(inputs.const_years) if inputs.const_years else int(0)
        kitai_bukka = to_dec(inputs.kitai_bukka_j - inputs.gonensai_rimawari)
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

        if inputs.proj_ctgry == "サービス購入型":
            tax_rates['houjinjuminzei_kintou'] = to_dec(0.18)
            if inputs.proj_type == "BOT/BOO":
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
            if inputs.mgmt_type == "国":
                financial_rules['zei_modori'] = Decimal(0.278)
                financial_rules['hojo'] = Decimal(0.0)
                financial_rules['kisai_jutou'] = Decimal(0.0)
                financial_rules['kisai_koufu'] = Decimal(0.0)
            elif inputs.mgmt_type == "都道府県":
                financial_rules['zei_modori'] = Decimal(0.0578)
                financial_rules['hojo'] = Decimal(0.5)
                financial_rules['kisai_jutou'] = Decimal(0.75)
                financial_rules['kisai_koufu'] = Decimal(0.30)
            elif inputs.mgmt_type == "市区町村":
                financial_rules['zei_modori'] = Decimal(0.084)
                financial_rules['hojo'] = Decimal(0.300)
                financial_rules['kisai_jutou'] = Decimal(0.750)
                financial_rules['kisai_koufu'] = Decimal(0.300)
            
            financial_rules['zei_total'] = tax_rates['houjinjuminzei_kintou'] + tax_rates['hudousanshutokuzei_hyoujun'] * tax_rates['hudousanshutokuzei_ritsu'] + tax_rates['koteishisanzei_hyoujun'] * tax_rates['koteishisanzei_ritsu'] + tax_rates['tourokumenkyozei_hyoujun'] * tax_rates['tourokumenkyozei_ritsu']

    
            if inputs.proj_type in ["DBO(SPCなし)", "BT/DB(いずれもSPCなし)"]:
                SPC_costs = {'fee':to_dec(0), 'shihon':to_dec(0), 'yobihi':to_dec(0)}
                SPC_hiyou_atsukai = int(1)
            else:
                SPC_costs = {'keihi':to_dec(20), 'fee':to_dec(20), 'shihon':to_dec(100), 'yobihi':to_dec(50)}
                SPC_hiyou_atsukai = int(1)

            initial_inputs = {
                "mgmt_type": inputs.mgmt_type,
                "proj_ctgry": inputs.proj_ctgry,
                "proj_type": inputs.proj_type,
                "proj_years": inputs.proj_years,
                "const_years": inputs.const_years,
                "ijikanri_unnei_years": inputs.ijikanri_unnei_years,
                "const_start_date": str(const_start_date),
                "kijun_kinri": str(inputs.r1),
                "chisai_kinri": str(inputs.r2),
                "chisai_sueoki_kikan": int(chisai_sueoki_kikan),
                "chisai_shoukan_kikan": inputs.chisai_shoukan_kikan,
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
                "rakusatsu_ritsu": str(inputs.rakusatsu_ritsu),
                "reduc_shisetsu": str(inputs.reduc_shisetsu),
                "reduc_ijikanri_1": str(inputs.reduc_ijikanri_1),
                "reduc_ijikanri_2": str(inputs.reduc_ijikanri_2),
                "reduc_ijikanri_3": str(inputs.reduc_ijikanri_3),
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
        if self.page.session.store.contains_key("initial_inputs"):
            self.page.session.store.remove("initial_inputs")
        self.page.session.store.set("initial_inputs",data)

       
