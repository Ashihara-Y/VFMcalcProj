import sys
sys.dont_write_bytecode = True
import os
import pandas as pd
import flet as ft
from simpledt import DataFrame
from tinydb import TinyDB, Query
#import openpyxl
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
#import make_inputs_df
#import decimal
from decimal import Decimal, ROUND_HALF_UP
#import timeflake
import datetime
#from zoneinfo import ZoneInfo
from VFMcalc2 import VFM_calc
from scipy.interpolate import PchipInterpolator
from flet.auth.providers.auth0_oauth_provider import Auth0OAuthProvider
from auth_manager import setup_auth, get_auth0_provider
import save_results as sr
from Editcalc import VFM_calc
import asyncio

"""
「詳細表示画面でボタンクリックの後」
・詳細表示の画面で「調整・再計算」（仮）ボタンをクリック ⇒
・当該算定結果のdatetimeとcalc_idがセッションストレージに格納され、「調整画面」に渡される ⇒
「調整画面が表示されるまで」
・datetimeとcalc_idで指定された算定結果から、「結果要約」「入力データ」が抽出される ⇒
・この２つのデータを、スライダー付きレイアウトの画面に表示する ⇒
「スライダー操作された後」
・スライダーが動いている最中は、その値は後の計算過程には渡されない ⇒
・スライダーの移動が停止してから0.2秒（？）後に、その変更値（スライダー変更の手が一度止まれば一度計算されるので、
  一度の算定で対象となる入力パラメータの変更箇所は１つだけ！）を反映した「編集後の入力データ」を抽出・計算に通す ⇒
・抽出・計算に通した後の辞書を、VFM算定過程（Editcalc）に渡す ⇒
・編集した入力によるVFM算定結果を、インメモリのDBにReplaceで書き込む（Editcalcの最後の関数に、インメモリ保存用のcalc_idを渡す） ⇒
・DBから、上記算定結果のうち、「算定結果要約」と「入力値」を抽出する。
・DBからの抽出条件は？ メモリ用の書き込みはReplaceにしたので、各テーブルのレコードは１つだけのはず。それならば、条件なしでfrom _sqlを実施してDFに格納するだけで十分か？ ⇒
・前者は「編集後の算定結果」表の更新へ、後者は元のUI部品で、スライダーの位置だけ入力した値の場所にするのに使う（「元に戻せる」
  観点から、UIは元のままで値だけ最後の入力値のままにする） ⇒
「算定結果保存がクリックされた後」
・「この算定結果を保存」（仮）ボタンをクリックすると、その時点での「編集後算定結果」（インメモリＤＢ上の各テーブルに残っている）を抽出して、
  ファイルＤＢに書き込む。この処理コードも新たに追加する必要がある ⇒
・新たに保存した算定結果を含む要約リスト画面に遷移する。
"""

#setup_auth(page: ft.Page, on_login_success)
#auth0_provider = get_auth0_provider()

@ft.control
class Edit_result(ft.Stack):
    def __init__(self, selected_datetime):
        super().__init__()
        #self.title = "結果 詳細"
        self.width = 2100
        self.height = 1000
        #self.resizable = True

        self.dtime = selected_datetime
        self.disk_engine = create_engine('sqlite:///VFM.db', echo=False, connect_args={'check_same_thread': False})
        self.memory_engine = create_engine('sqlite:///:memory:', echo=False, connect_args={'check_same_thread': False}, poolclass=StaticPool)

        self.current_calc_id = "temp_calc_id" 

        table_names = [
            'res_summ_res_table',
            'final_inputs_res_table',
        ]
        # final_inputs_res_tableの方は、編集前後の入力値等を算定過程も通じて作成するための材料
        # res_summ_res_tableの方は、結果要約の表を作るための材料。

        self.selected_res_list = []
        for table_name in table_names:
            query = 'select * from ' + table_name + ' where datetime = ' + '"' + self.dtime + '"'
            table_name = pd.read_sql_query(query, self.disk_engine)
            self.selected_res_list.append(table_name)
        target_summ_df = self.selected_res_list[0]
        target_inputs_df = self.selected_res_list[1]
        # Targetu_Inputsは、EditcalcのVFMcalcには渡さない。渡すのはEdit_Inputs

        # 以下は、内部の計算やUIへのセットで参照するための辞書
        self.target_inputs = target_inputs_df.iloc[0].to_dict()

        target_summ_df['discount_rate'] = target_summ_df['discount_rate'] * 100 # できれば、こういう処理は消しておきたい。
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

        # 編集対象になる方の算定結果要約の表を作成
        target_summ_df_t = target_summ_df_J.transpose().reset_index()
        self.target_summ_df_t = target_summ_df_t.rename(columns={"index":"項目名", 0:"値"})
        #simpledt_target_summ_df = DataFrame(target_summ_df_t)
        #simpledt_target_summ_dt = simpledt_target_summ_df.datatable
        #self.table_target_summ = simpledt_target_summ_dt

        new_df = self.target_summ_df_t
        old_df = new_df.copy() # 初期状態では、比較対象は同じDF。スライダー操作後に、new_dfを丸ごと更新して、比較。       


        def create_comparison_datatable(new_df, old_df=None):
            """
            DataFrameからft.DataTableを生成する。(itertuplesによる高速化版)
            old_dfが渡された場合、new_dfと値を比較し、異なれば赤字にする。← 「赤字」にする必要があるのは、
            new_dfの方。できれば、実装が簡便なのでSimpleDTを使いたいが、DF段階で、「新旧を比較して差分を
            把握」する処理は、できれば追加したいので、当面はファイルに残しておく。
            """
            columns = [ft.DataColumn(ft.Text(str(col), weight=ft.FontWeight.BOLD)) for col in new_df.columns]
            rows = []
        
            for row in new_df.itertuples(index=True):
                # row.Index でインデックス（行ラベル）を取得できます
                current_index = row.Index 
                cells = []
            
                for col_name in new_df.columns:
                    # getattr を使って、文字列の列名から namedtuple の値を取得
                    new_val = getattr(row, col_name)
                    text_color = ft.Colors.ON_SURFACE
                    text_color = ft.Colors.ON_SURFACE
                
                    if old_df is not None and col_name != "項目名":
                        # old_dfからの取得は loc のままでOK（インデックス検索のため）
                        old_val = old_df.loc[current_index, col_name]
                    
                        if str(new_val) != str(old_val):
                            text_color = ft.Colors.RED_400
                            text_color = ft.Colors.RED_400
                    # ここで、該当セルの字の色を赤にセットしている。単なるDFではこれは無理でも
                    # simpleDTでも、行ごと、セルごとの処理はできたはず。
                    cells.append(ft.DataCell(ft.Text(str(new_val), color=text_color)))
            
                rows.append(ft.DataRow(cells=cells))
            
            return ft.DataTable(
                columns=columns, 
                rows=rows, 
                border=ft.Border.all(1, ft.Colors.OUTLINE_VARIANT),
                vertical_lines=ft.border.BorderSide(1, ft.Colors.OUTLINE_VARIANT),
                horizontal_lines=ft.border.BorderSide(1, ft.Colors.OUTLINE_VARIANT)
                )   

        # 1. 表のインスタンス生成
        # 元の算定結果要約表（比較対象なし = 黒字）
        self.original_summ_table = self.create_comparison_datatable(self.target_summ_df_t)
        
        # 再算定結果要約表（初期表示は元データと全く同じものを表示）
        self.recalc_summ_table = self.create_comparison_datatable(self.target_summ_df_t)

        # 再算定表は後で差し替えるため、Containerでラップしておく
        self.recalc_table_container = ft.Container(content=self.recalc_summ_table)

        slider_value03 = ft.Text("", size=30, weight=ft.FontWeight.W_200)
        slider_value04 = ft.Text("", size=30, weight=ft.FontWeight.W_200)
        slider_value05 = ft.Text("", size=30, weight=ft.FontWeight.W_200)
        slider_value06 = ft.Text("", size=30, weight=ft.FontWeight.W_200)
        slider_value07 = ft.Text("", size=30, weight=ft.FontWeight.W_200)
        slider_value10 = ft.Text("", size=30, weight=ft.FontWeight.W_200)
        slider_value11 = ft.Text("", size=30, weight=ft.FontWeight.W_200)
        slider_value12 = ft.Text("", size=30, weight=ft.FontWeight.W_200)
        slider_value13 = ft.Text("", size=30, weight=ft.FontWeight.W_200)
        slider_value15 = ft.Text("", size=30, weight=ft.FontWeight.W_200)
            
        def handle_slider_change(e):
            sl_value = e.control.value
            target_text_control = e.control.data
            target_text_control.value = str(sl_value)
            target_text_control.update()
            if self.calc_task and not self.calc_task.done():
              self.calc_task.cancel()
            self.calc_task = asyncio.create_task(self._debounced_calculate())

        tx3 = ft.Text("施設整備費支払 一括払の比率(%)")
        self.sl3 = ft.Slider(
            value=float(self.target_inputs["shisetsu_seibi_paymentschedule_ikkatsu"]),
            min=0.5*float(self.target_inputs["shisetsu_seibi_paymentschedule_ikkatsu"]),
            max=100.00,
            divisions=750,
            label="{value}%",
            round=2,
            width=400,
            on_change=handle_slider_change,
            data=slider_value03,
        )
        tx4 = ft.Text("施設整備費の削減率(%)")
        self.sl4 = ft.Slider(
            value=float(self.target_inputs["reduc_shisetsu"]),
            min=0.0,
            max=5.0,
            divisions=500,
            label="{value}%",
            round=1,
            width=400,
            on_change=handle_slider_change,
            data=slider_value04,
        )
        tx5 = ft.Text("維持管理運営費（人件費）の削減率(%)")
        self.sl5 = ft.Slider(
            value=float(self.target_inputs["reduc_ijikanri_1"]),
            min=0.0,
            max=5.0,
            divisions=500,
            label="{value}%",
            round=1,
            width=400,
            on_change=handle_slider_change,
            data=slider_value05,
        ) 
        tx6 = ft.Text("維持管理運営費（修繕費）の削減率(%)")
        self.sl6 = ft.Slider(
            value=float(self.target_inputs["reduc_ijikanri_2"]),
            min=0.0,
            max=5.0,
            divisions=500,
            label="{value}%",
            round=1,
            width=400,
            on_change=handle_slider_change,
            data=slider_value06,
        )
        tx7 = ft.Text("維持管理運営費(動力費)の削減率(%)")
        self.sl7 = ft.Slider(
            value=float(self.target_inputs["reduc_ijikanri_3"]),
            min=0.0,
            max=5.0,
            divisions=500,
            label="{value}%",
            round=1,
            width=400,
            on_change=handle_slider_change,
            data=slider_value07,
        )
        tx10 = ft.Text("SPC経費年額(百万円)")
        self.sl10 = ft.Slider(
            value=float(self.target_inputs["SPC_keihi"]),
            min=0.75*float(self.target_inputs["SPC_keihi"]),
            max=1.25*float(self.target_inputs["SPC_keihi"]),
            divisions=500,
            label="{value}百万円",
            round=1,
            width=400,
            on_change=handle_slider_change,
            data=slider_value10,
        )
        tx11 = ft.Text("SPCへの手数料(百万円)")
        self.sl11 = ft.Slider(
            value=float(self.target_inputs["SPC_fee"]),
            min=0,
            max=100,
            divisions=100,
            label="{value}百万円",
            round=1,
            width=400,
            on_change=handle_slider_change,
            data=slider_value11,
        )
        tx12 = ft.Text("SPC資本金(百万円)")
        self.sl12 = ft.Slider(
            value=float(self.target_inputs["SPC_shihon"]),
            min=0.75*float(self.target_inputs["SPC_shihon"]),
            max=1.25*float(self.target_inputs["SPC_shihon"]),
            divisions=500,
            label="{value}百万円",
            round=1,
            width=400,
            on_change=handle_slider_change,
            data=slider_value12,
        )
        tx13 = ft.Text("SPC準備金(違約金相当、百万円)")
        self.sl13 = ft.Slider(
            value=float(self.target_inputs["SPC_yobihi"]),
            min=0,
            max=0.1 * (float(self.target_inputs["shisetsu_seibi_org_LCC"]) + float(self.target_inputs["ijikanri_unnei_org_LCC"])),
            divisions=1000,
            label="{value}百万円",
            round=1,
            width=400,
            on_change=handle_slider_change,
            data=slider_value13,
        )
        tx15 = ft.Text("割賦金利へのスプレッド(%)")
        self.sl15 = ft.Slider(
            value=float(self.target_inputs["kappu_kinri_spread"]),
            min=0.75*float(self.target_inputs["kappu_kinri_spread"]),
            max=1.25*float(self.target_inputs["kappu_kinri_spread"]),
            divisions=500,
            label="{value}%",
            round=2,
            width=400,
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
                    tx3, slider_value03, self.sl3,  ft.Divider(height=1, color="amber"),
                    tx4, slider_value04, self.sl4,  ft.Divider(height=1, color="amber"),
                    tx5, slider_value05, self.sl5,  ft.Divider(height=1, color="amber"),
                    tx6, slider_value06, self.sl6,  ft.Divider(height=1, color="amber"),
                    tx7, slider_value07, self.sl7,  ft.Divider(height=1, color="amber"),
                    tx10,slider_value10, self.sl10, ft.Divider(height=1, color="amber"),
                    tx11,slider_value11, self.sl11, ft.Divider(height=1, color="amber"),
                    tx12,slider_value12, self.sl12, ft.Divider(height=1, color="amber"),
                    tx13,slider_value13, self.sl13, ft.Divider(height=1, color="amber"),
                    tx15,slider_value15, self.sl15, ft.Divider(height=1, color="amber"),
                    b,
        ]        
        fi_lv2.controls= [
                    tx4, slider_value04, self.sl4,  ft.Divider(height=1, color="amber"),
                    tx5, slider_value05, self.sl5,  ft.Divider(height=1, color="amber"),
                    tx6, slider_value06, self.sl6,  ft.Divider(height=1, color="amber"),
                    tx7, slider_value07, self.sl7,  ft.Divider(height=1, color="amber"),
                    tx13,slider_value13, self.sl13, ft.Divider(height=1, color="amber"),
                    b,
        ]        



        # 2. 左右のパネルを構築
        # 【左パネル】表を縦に2つ並べる
        left_panel = ft.Column(
            expand=1, 
            scroll=ft.ScrollMode.AUTO,
            spacing=20,
            controls=[
                ft.Text("再算定結果（シミュレーション）", size=18, weight=ft.FontWeight.BOLD),
                self.recalc_table_container, # ここを更新する
                ft.Divider(height=2, color="amber"),
                ft.Text("元の算定結果", size=18, weight=ft.FontWeight.BOLD),
                self.original_summ_table,
            ]
        )
        
        if self.target_inputs["proj_type"] == "DBO(SPCなし)" or self.target_inputs["proj_type"] == "BT/DB(いずれもSPCなし)":
        # 【右パネル】スライダー群
          right_panel = ft.Column(
              expand=1, 
              scroll=ft.ScrollMode.AUTO,
              spacing=10,
              controls=[
                ft.Text("パラメータ調整", size=18, weight=ft.FontWeight.BOLD),
                # fi_lv2の中身を展開して配置　←　展開されるか要確認！
                *fi_lv2.controls 
              ]
          )
        else:
        # 【右パネル】スライダー群
          right_panel = ft.Column(
              expand=1, 
              scroll=ft.ScrollMode.AUTO,
              spacing=10,
              controls=[
                ft.Text("パラメータ調整", size=18, weight=ft.FontWeight.BOLD),
                # fi_lv1の中身を展開して配置　←　展開されるか要確認！
                *fi_lv1.controls 
              ]
          )

        # 3. 親コンテナ(self)に左右のパネルをセット
        self.controls = [
            ft.Row(
                expand=True,
                alignment=ft.MainAxisAlignment.START,
                #cross_alignment=ft.CrossAxisAlignment.START,
                controls=[
                    ft.Container(content=left_panel, expand=1, padding=10),
                    ft.VerticalDivider(width=1, color=ft.Colors.OUTLINE_VARIANT),
                    ft.Container(content=right_panel, expand=1, padding=10)
                ]
            )
        ]

# button_clicked
    async def button_clicked(self, e):
        self._extract_inputs()

        edit_results = self._calculate_financials()
        
        self._save_to_db(edit_results)
        # 呼ばれているのは、Editcalcの関数になっている必要に注意！
        VFM_calc() # ここで「インメモリ用のcalc_idとＤＢ指定」を引数として渡す必要がある。
        # ＤＢ書き込み関数を、どう動かせばいいか？
        await self.page.push_route("/view_saved")
        
# Gemini提案のコード
        self.current_calc_id = "temp_sim_001" # シミュレーション用の一時ID
        # ... (UI初期化処理など) ...
    def create_comparison_datatable(self, new_df, old_df=None):
        """
        DataFrameからft.DataTableを生成する。
        old_dfが渡された場合、new_dfと値を比較し、異なれば赤字にする。
        ※インデックス列(項目名)も表示する想定で記述。
        """
        # 列名（ヘッダー）の作成
        columns = [ft.DataColumn(ft.Text(str(col), weight=ft.FontWeight.BOLD)) for col in new_df.columns]
        rows = []
        
        for index, row in new_df.iterrows():
            cells = []
            for col_name in new_df.columns:
                new_val = row[col_name]
                text_color = ft.Colors.ON_SURFACE # デフォルト（通常）の色
                
                # 比較対象があり、かつ「項目名」列以外の場合に値を比較する
                if old_df is not None and col_name != "項目名":
                    # old_dfとインデックスで突き合わせる
                    old_val = old_df.loc[index, col_name]
                    
                    # 浮動小数点の表示上の誤差を吸収するため、文字列にして比較するか、
                    # または特定の小数点以下で丸めて比較します。
                    if str(new_val) != str(old_val):
                        text_color = ft.Colors.RED_400 # 変更があれば赤色
                        
                cells.append(ft.DataCell(ft.Text(str(new_val), color=text_color)))
            
            rows.append(ft.DataRow(cells=cells))
            
        return ft.DataTable(
            columns=columns, 
            rows=rows, 
            border=ft.Border.all(1, ft.Colors.OUTLINE_VARIANT), # 表の枠線
            vertical_lines=ft.border.BorderSide(1, ft.Colors.OUTLINE_VARIANT),
            horizontal_lines=ft.border.BorderSide(1, ft.Colors.OUTLINE_VARIANT)
        )


#2. レイアウトの構築（左右2ペイン構造）
#__init__ メソッドの後半で、先ほどの関数を使って表を生成し、左右の画面（ft.Row）に配置します。
#Python
       # --- (前略：target_summ_df_t などのDataFrame準備) ---

        # 1. 表のインスタンス生成
        # 元の算定結果要約表（比較対象なし = 黒字）
        self.original_summ_table = self.create_comparison_datatable(self.target_summ_df_t)
        
        # 再算定結果要約表（初期表示は元データと全く同じものを表示）
        self.recalc_summ_table = self.create_comparison_datatable(self.target_summ_df_t)

        # 再算定表は後で差し替えるため、Containerでラップしておく
        self.recalc_table_container = ft.Container(content=self.recalc_summ_table)

        # 2. 左右のパネルを構築
        # 【左パネル】表を縦に2つ並べる(変動させる側を上に置く)
        left_panel = ft.Column(
            expand=1, 
            scroll=ft.ScrollMode.AUTO,
            spacing=20,
            controls=[
                ft.Text("再算定結果（シミュレーション）", size=18, weight=ft.FontWeight.BOLD),
                self.recalc_table_container, # ここを更新する
                ft.Divider(height=2, color="amber"),
                ft.Text("元の算定結果", size=18, weight=ft.FontWeight.BOLD),
                self.original_summ_table,
            ]
        )
        
        # 【右パネル】スライダー群
        right_panel = ft.Column(
            expand=1, 
            scroll=ft.ScrollMode.AUTO,
            spacing=10,
            controls=[
                ft.Text("パラメータ調整", size=18, weight=ft.FontWeight.BOLD),
                # 既存のListView(fi_lv1)の中身を展開して配置　←　展開されるか要確認！
                *fi_lv1.controls 
            ]
        )

        # 3. 親コンテナ(self)に左右のパネルをセット
        self.controls = [
            ft.Row(
                expand=True,
                #alignment=ft.MainAxisAlignment.START,
                alignment=ft.CrossAxisAlignment.START,
                controls=[
                    ft.Container(content=left_panel, expand=1, padding=10),
                    ft.VerticalDivider(width=1, color=ft.Colors.OUTLINE_VARIANT),
                    ft.Container(content=right_panel, expand=1, padding=10),
                ]
            )
        ]

#3. 非同期更新の反映処理
#前回のデバウンス処理の最後に呼ばれる _update_result_tables を実装します。
#新しく計算されたDataFrame（new_summ_df_t）と、初期表示時に保存しておいた元のDataFrame（target_summ_df_t）を比較させます。
#Python
    def _update_result_tables(self, new_summ_df_t):
        """
        計算完了後に呼ばれる。再算定表を、赤字ハイライト付きの新しい表に差し替える。
        """
        # 新しいDataFrameと元のDataFrameを渡して、赤字ハイライト付きの表を生成
        updated_table = self.create_comparison_datatable(
            new_df=new_summ_df_t, 
            old_df=self.target_summ_df_t # __init__で保持している元のDF (self.target_summ_df_t 等にしておくと確実です)
        )
        
        # Containerの中身(content)を、新しい表インスタンスに差し替える
        self.recalc_table_container.content = updated_table
        
        # 画面の更新を要求
        self.update()


    async def _debounced_calculate(self):
        """スライダーが動いた時のシミュレーション処理（非同期）"""
        try:
            # 1. 編集画面の入力値から、VFMcalc用のパラメータを生成
            params = self._calculate_financials()
            
            # 2. VFM_calc を実行し、結果のDataFrameセットを受け取る
            # ※ VFM_calc が直接DBに書くのではなく、DFを返すように調整されている前提
            results_dict = VFM_calc(params)
            
            # 3. 【インメモリDB】へ書き込み (memory_engineを渡す)
            save_vfm_results(self.current_calc_id, results_dict, target_engine=self.memory_engine)
            
            # 4. 【インメモリDB】から読み出してUIを更新する
            self._update_result_tables(self.memory_engine)
            
        except Exception as e:
            print(f"Error: {e}")

    def on_save_button_click(self, e):
        """「最終結果を保存」ボタンが押された時の処理"""
        # インメモリDBにある最新のシミュレーション結果を読み出す
        final_df_summ = pd.read_sql_query(f"SELECT * FROM res_summ_res_table WHERE calc_id='{self.current_calc_id}'", self.memory_engine)
        final_df_inputs = pd.read_sql_query(f"SELECT * FROM final_inputs_res_table WHERE calc_id='{self.current_calc_id}'", self.memory_engine)
        
        # 新しい正式な calc_id を発行
        formal_calc_id = generate_new_calc_id()
        
        results_dict = {
            'res_summ_res_table': final_df_summ,
            'final_inputs_res_table': final_df_inputs
        }
        
        # 【物理DB】へ書き込み (disk_engineを渡す、あるいは省略してデフォルト挙動にする)
        save_vfm_results(formal_calc_id, results_dict, target_engine=self.disk_engine)
        
        # 保存完了のメッセージ表示など

    # Tabは使わないので大半削除したが、新UIでもこの条件分岐は必要なので、判定部分のみ残しておく。
       # if self.target_inputs["proj_type"] == "DBO(SPCなし)" or self.target_inputs["proj_type"] == "BT/DB(いずれもSPCなし)":
       # else:

# button_clicked
    async def button_clicked(self, e):
        self._extract_inputs()

        edit_results = self._calculate_financials()
        
        self._save_to_db(edit_results)
        # 呼ばれているのは、Editcalcの関数になっている必要に注意！
        VFM_calc() # ここで「インメモリ用のcalc_idとＤＢ指定」を引数として渡す必要がある。
        # ＤＢ書き込み関数を、どう動かせばいいか？
        await self.page.push_route("/view_saved")
        


# Gemini提案以前のコードの残り
# 編集画面からの_extract_inputs
    def to_dec(self, val):
            return Decimal(val).quantize(Decimal('0.000001'), ROUND_HALF_UP)

# IIの抽出処理？
    def _extract_inputs(self):

        proj_years = int(self.target_inputs["proj_years"])

        chisai_shoukan_kikan = int(self.sl1.value)
        chisai_sueoki_kikan = int(self.sl2.value)
        shisetsu_seibi_ikkatsu_hiritsu = self.to_dec(str(self.sl3.value)) / self.to_dec(100)
        reduc_shisetsu = self.to_dec(str(self.sl4.value)) / self.to_dec(100)
        reduc_ijikanri_1 = self.to_dec(str(self.sl5.value)) / self.to_dec(100)
        reduc_ijikanri_2 = self.to_dec(str(self.sl6.value)) / self.to_dec(100)
        reduc_ijikanri_3 = self.to_dec(str(self.sl7.value)) / self.to_dec(100)
        monitoring_costs_PSC = self.to_dec(str(self.sl8.value))
        monitoring_costs_LCC = self.to_dec(str(self.sl9.value))
        SPC_keihi = self.to_dec(str(self.sl10.value))
        SPC_fee = self.to_dec(str(self.sl11.value))
        SPC_shihon = self.to_dec(str(self.sl12.value))
        SPC_yobihi = self.to_dec(str(self.sl13.value))    
        advisory_fee = self.to_dec(str(self.sl14.value))
        kappu_kinri_spread = self.to_dec(str(self.sl15.value))  / self.to_dec(100)

        JGB_rates_df = pd.read_csv("src/JGB_rates.csv", sep="\t", encoding="utf-8", header=None, names=["year", "rate"],).set_index("year")
        JRB_rates_df = pd.read_csv("src/JRB_rates.csv", sep="\t", encoding="utf-8", names=[0,1,2,3,4,5], index_col=0)

        #y, d = divmod(proj_years, 5)
        #if y >= 1:
        #    r_idx = str((y + 1) * 5) + "年" if d > 2 else str(y * 5) + "年"
        #else:
        #    r_idx = str(d) + "年"

        val_array = JGB_rates_df.iloc[0:,0].to_numpy()
        col_series = JGB_rates_df.T.columns.to_series().apply(lambda x: x[:-1])
        col_array = col_series.values.astype(int)
        pchip_interp = PchipInterpolator(col_array, val_array)
        r1_fl_str = str(pchip_interp(proj_years))

        kijun_kinri = self.to_dec(r1_fl_str)
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
        const_start_date_year = int(const_start_date[:4])
        const_start_date_month = int(const_start_date[5:7])
        const_start_date_day = int(const_start_date[8:10]) 

        if const_start_date_month < 4:
            first_end_fy = datetime.date(const_start_date_year, 3, 31)
        else:
            first_end_fy = datetime.date(const_start_date_year + 1, 3, 31)



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
        kitai_bukka = Decimal(kitai_bukka) /Decimal(100) # CSVの％表記を採取しているため、実数表記に切り替える。

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

        SPC_hiyou_total = SPC_keihi * self.to_dec(ijikanri_unnei_years) + SPC_shihon
        SPC_hiyou_nen = SPC_fee + SPC_keihi #公共がSPCに毎年払うコスト
        SPC_keihi_LCC = SPC_keihi + SPC_fee + self.to_dec(self.target_inputs['houjinjuminzei_kintou'])#SPCが払うコスト(経費、手数料とも全て何かの使途に支払う前提)
        
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
            "const_start_date_year": const_start_date_year,
            "const_start_date_month": const_start_date_month,
            "const_start_date_day": const_start_date_day,
            "const_start_date": const_start_date, 
            "const_years": int(const_years),
            "discount_rate": str(discount_rate),
            "first_end_fy": str(first_end_fy),
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
            "const_start_date_year": const_start_date_year,
            "const_start_date_month": const_start_date_month,
            "const_start_date_day": const_start_date_day,
            "const_start_date": const_start_date,
            "const_years": int(self.target_inputs["const_years"]),
            "discount_rate": str(discount_rate),

            "first_end_fy": str(first_end_fy),
            "fudousanshutokuzei_hyoujun": str(self.target_inputs["fudousanshutokuzei_hyoujun"]),
            "fudousanshutokuzei_ritsu": str(self.target_inputs["fudousanshutokuzei_ritsu"]),
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



