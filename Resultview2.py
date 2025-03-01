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

# savedir = pathlib.Path(mkdtemp(prefix=None, suffix=None, dir='.')) # 一時ディレクトリを作成
class Results(ft.Stack):
    def __init__(self):
        super().__init__()
        self.title = "結果 詳細"
        self.width = 2100
        self.height = 1000
        self.resizable = True

        engine = create_engine('sqlite:///VFM.db', echo=False, connect_args={'check_same_thread': False})
        #con = TinyDB("selected_res.json")
        engine_m = create_engine('sqlite:///sel_res.db', echo=False, connect_args={'check_same_thread': False})
        df_res = pd.read_sql_table('sel_res', engine_m)
        self.dtime = df_res['selected_datetime'].iloc[0]
        #con.close()

        inputs_pdt = make_inputs_df.main()
        inputs_dic = inputs_pdt.model_dump()
        final_inputs_df = pd.DataFrame(inputs_dic, index=[0])
        final_inputs_df = final_inputs_df.drop(
            [
                'const_start_date_year',
                'const_start_date_month', 
                'const_start_date_day',
                'first_end_fy',
                'growth',
                'houjinjuminzei_ritsu_todouhuken',
                'houjinjuminzei_ritsu_shikuchoson',
                'ijikanri_unnei_LCC',
                'ijikanri_unnei_1_LCC',
                'ijikanri_unnei_2_LCC',
                'ijikanri_unnei_3_LCC',
                'pre_kyoukouka',
                'shisetsu_seibi_LCC',
                'target_years',
                'yosantanka_hiritsu_shisetsu',
                'yosantanka_hiritsu_ijikanri_1',
                'yosantanka_hiritsu_ijikanri_2',
                'yosantanka_hiritsu_ijikanri_3',
                'zei_total',
            ], 
        axis=1)

        final_inputs_df['SPC_setsuritsuhi'] = inputs_pdt.SPC_shihon + inputs_pdt.SPC_yobihi

        final_inputs_df = final_inputs_df[[
                'mgmt_type',
                'proj_ctgry',
                'proj_type',
                'proj_years',
                'const_years',
                'const_start_date',
                'ijikanri_unnei_years',
                'rakusatsu_ritsu',
                'reduc_shisetsu',
                'reduc_ijikanri_1',
                'reduc_ijikanri_2',
                'reduc_ijikanri_3',
                'shisetsu_seibi',
                'shisetsu_seibi_org',
                'shisetsu_seibi_org_LCC',
                'ijikanri_unnei',
                'ijikanri_unnei_org',
                'ijikanri_unnei_org_LCC',
                'ijikanri_unnei_1',
                'ijikanri_unnei_1_org',
                'ijikanri_unnei_1_org_LCC',
                'ijikanri_unnei_2',
                'ijikanri_unnei_2_org',
                'ijikanri_unnei_2_org_LCC',
                'ijikanri_unnei_3',
                'ijikanri_unnei_3_org',
                'ijikanri_unnei_3_org_LCC',
                'hojo_ritsu',
                'kisai_jutou',
                'kisai_koufu',
                'advisory_fee',
                'monitoring_costs_PSC',
                'monitoring_costs_LCC',
                'SPC_hiyou_atsukai',
                'SPC_fee',
                'SPC_keihi',
                'SPC_setsuritsuhi',
                'SPC_hiyou_total',
                'SPC_hiyou_nen',
                'SPC_keihi_LCC',
                'SPC_shihon',
                'SPC_yobihi',
                'riyouryoukin_shunyu',
                'shisetsu_seibi_paymentschedule_ikkatsu',
                'shisetsu_seibi_paymentschedule_kappu',
                'kijun_kinri',
                'lg_spread',
                'kitai_bukka',
                'discount_rate',
                'Kappu_kinri',
                'kappu_kinri_spread',
                'chisai_kinri',
                'chisai_shoukan_kikan',
                'chisai_sueoki_years',
                'houjinzei_ritsu',
                'houjinjuminzei_kintou',
                'fudousanshutokuzei_hyoujun',
                'fudousanshutokuzei_ritsu',
                'koteishisanzei_hyoujun',
                'koteishisanzei_ritsu',
                'tourokumenkyozei_hyoujun',
                'tourokumenkyozei_ritsu',            
            ]]

        final_inputs_df['rakusatsu_ritsu'] = final_inputs_df['rakusatsu_ritsu'].apply(lambda x: x * 100)
        final_inputs_df['reduc_shisetsu'] = final_inputs_df['reduc_shisetsu'].apply(lambda x: x * 100)
        final_inputs_df['reduc_ijikanri_1'] = final_inputs_df['reduc_ijikanri_1'].apply(lambda x: x * 100)
        final_inputs_df['reduc_ijikanri_2'] = final_inputs_df['reduc_ijikanri_2'].apply(lambda x: x * 100)
        final_inputs_df['reduc_ijikanri_3'] = final_inputs_df['reduc_ijikanri_3'].apply(lambda x: x * 100)
        final_inputs_df['hojo_ritsu'] = final_inputs_df['hojo_ritsu'].apply(lambda x: x * 100)
        final_inputs_df['kisai_jutou'] = final_inputs_df['kisai_jutou'].apply(lambda x: x * 100)
        final_inputs_df['kisai_koufu'] = final_inputs_df['kisai_koufu'].apply(lambda x: x * 100)
        final_inputs_df['shisetsu_seibi_paymentschedule_ikkatsu'] = final_inputs_df['shisetsu_seibi_paymentschedule_ikkatsu'].apply(lambda x: x * 100)
        final_inputs_df['shisetsu_seibi_paymentschedule_kappu'] = final_inputs_df['shisetsu_seibi_paymentschedule_kappu'].apply(lambda x: x * 100)
        final_inputs_df['kijun_kinri'] = final_inputs_df['kijun_kinri'].apply(lambda x: x * 100)
        final_inputs_df['lg_spread'] = final_inputs_df['lg_spread'].apply(lambda x: x * 100)
        final_inputs_df['kitai_bukka'] = final_inputs_df['kitai_bukka'].apply(lambda x: x * 100)
        final_inputs_df['discount_rate'] = final_inputs_df['discount_rate'].apply(lambda x: x * 100)
        final_inputs_df['Kappu_kinri'] = final_inputs_df['Kappu_kinri'].apply(lambda x: x * 100)
        final_inputs_df['kappu_kinri_spread'] = final_inputs_df['kappu_kinri_spread'].apply(lambda x: x * 100)
        final_inputs_df['chisai_kinri'] = final_inputs_df['chisai_kinri'].apply(lambda x: x * 100)
        final_inputs_df['houjinzei_ritsu'] = final_inputs_df['houjinzei_ritsu'].apply(lambda x: x * 100)
        final_inputs_df['fudousanshutokuzei_ritsu'] = final_inputs_df['fudousanshutokuzei_ritsu'].apply(lambda x: x * 100)
        final_inputs_df['koteishisanzei_ritsu'] = final_inputs_df['koteishisanzei_ritsu'].apply(lambda x: x * 100)
        final_inputs_df['tourokumenkyozei_ritsu'] = final_inputs_df['tourokumenkyozei_ritsu'].apply(lambda x: x * 100)
        final_inputs_df['datetime'] = self.dtime

        final_inputs_df = final_inputs_df.map(lambda x: round(float(x), 3) if isinstance(x, decimal.Decimal) else str(x))

        final_inputs_df = final_inputs_df.rename(
            columns={
                'datetime':'datetime',
                'mgmt_type':'施設管理者区分',
                'proj_ctgry':'事業形態',
                'proj_type':'事業方式',
                'proj_years':'事業期間',
                'const_years':'施設整備期間',
                'const_start_date':'施設整備開始日',
                'ijikanri_unnei_years':'維持管理運営費期間',
                'rakusatsu_ritsu':'落札率(%)',
                'reduc_shisetsu':'施設整備削減率(%)',
                'reduc_ijikanri_1':'維持管理運営費（人件費）削減率(%)',
                'reduc_ijikanri_2':'維持管理運営費（修繕費）削減率(%)',
                'reduc_ijikanri_3':'維持管理運営費（動力費）削減率(%)',
                'shisetsu_seibi':'施設整備費(競争効果反映後)(百万円)',
                'shisetsu_seibi_org':'施設整備費原額(百万円)',
                'shisetsu_seibi_org_LCC':'LCC施設整備費（削減率適用）(百万円)',
                'ijikanri_unnei':'維持管理運営費総額(競争効果反映後)(百万円)',
                'ijikanri_unnei_org':'維持管理運営費総額原額(百万円)',
                'ijikanri_unnei_org_LCC':'LCC維持管理運営費総額（削減率適用）(百万円)',
                'ijikanri_unnei_1':'維持管理運営費(人件費)(競争効果反映後)(百万円)',
                'ijikanri_unnei_1_org':'維持管理運営費(人件費)原額(百万円)',
                'ijikanri_unnei_1_org_LCC':'LCC維持管理運営費(人件費)（削減率適用）(百万円)',
                'ijikanri_unnei_2':'維持管理運営費(修繕費)(競争効果反映後)(百万円)',
                'ijikanri_unnei_2_org':'維持管理運営費(修繕費)原額(百万円)',
                'ijikanri_unnei_2_org_LCC':'LCC維持管理運営費(修繕費)（削減率適用）(百万円)',
                'ijikanri_unnei_3':'維持管理運営費(動力費)(競争効果反映後)(百万円)',
                'ijikanri_unnei_3_org':'維持管理運営費(動力費)原額(百万円)',
                'ijikanri_unnei_3_org_LCC':'LCC維持管理運営費(動力費)（削減率適用）(百万円)',
                'hojo_ritsu':'補助率(%)',
                'kisai_jutou':'起債充当率(%)',
                'kisai_koufu':'起債交付金カバー率(%)',
                'advisory_fee':'アドバイザリー手数料(百万円)',
                'monitoring_costs_LCC':'PFI-LCCでのモニタリング等費用(百万円)',
                'monitoring_costs_PSC':'PSCでのモニタリング等費用(百万円)',
                'SPC_hiyou_atsukai':'SPC費用の処理（デフォルト：サービス対価に含める）',
                'SPC_fee':'SPC手数料(百万円)',
                'SPC_keihi':'SPC経費(百万円)',
                'SPC_setsuritsuhi':'SPC設立費用(百万円)',
                'SPC_hiyou_total':'SPC費用総額(百万円)',
                'SPC_hiyou_nen':'SPC費用年額(百万円)',
                'SPC_keihi_LCC':'LCCでのSPC経費(百万円)',
                'SPC_shihon':'SPC資本金(百万円)',
                'SPC_yobihi':'SPC予備費(百万円)',
                'riyouryoukin_shunyu':'利用料金収入(百万円)',
                'shisetsu_seibi_paymentschedule_ikkatsu':'施設整備対価一括払比率(%)',
                'shisetsu_seibi_paymentschedule_kappu':'施設整備対価割賦払比率(%)',
                'kijun_kinri':'基準金利(%)',
                'lg_spread':'官民スプレッド(%)',
                'kitai_bukka':'期待物価上昇率(%)',
                'discount_rate':'割引率(%)',
                'Kappu_kinri':'割賦金利(%)',
                'kappu_kinri_spread':'割賦スプレッド(%)',
                'chisai_kinri':'地方債金利(%)',
                'chisai_shoukan_kikan':'地方債償還期間',
                'chisai_sueoki_years':'地方債償還据置期間',
                'houjinzei_ritsu':'法人税率(%)',
                'houjinjuminzei_kintou':'法人住民税均等割(百万円)',
                'fudousanshutokuzei_hyoujun':'不動産取得税課税標準(百万円)',
                'fudousanshutokuzei_ritsu':'不動産取得税率(%)',
                'koteishisanzei_hyoujun':'固定資産税課税標準(百万円)',
                'koteishisanzei_ritsu':'固定資産税率(%)',
                'tourokumenkyozei_hyoujun':'登録免許税課税標準(百万円)',
                'tourokumenkyozei_ritsu':'登録免許税率(%)',
            }
        )

        final_inputs_df.to_sql('final_inputs_table', engine, if_exists='replace', index=False)
        final_inputs_df = final_inputs_df.drop(columns='datetime')
        self.final_inputs_df = final_inputs_df.transpose().reset_index().rename(columns={"index":"項目名", 0:"値"})

        table_names = [
            'PSC_res_table', 
            'PSC_pv_res_table', 
            'LCC_res_table', 
            'LCC_pv_res_table', 
            'SPC_res_table', 
            'SPC_check_res_table',
            'Risk_res_table',
            'VFM_res_table',
            'PIRR_res_table',
            'res_summ_res_table',
        ]
        self.selected_res_list = []
        for table_name in table_names:
            query = 'select * from ' + table_name + ' where datetime = ' + '"' + self.dtime + '"'
            table_name = pd.read_sql_query(query, engine)
            self.selected_res_list.append(table_name)

    def build(self):
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

        #period_col = pd.DataFrame(index=range(45+1),columns=['period'])
        #period_col['period'] = period_col.index.to_series()

        #PSC_pv_df = period_col.join(PSC_pv_df)
        #LCC_pv_df = period_col.join(LCC_pv_df)

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

        return ft.Tabs(
                selected_index=1,
                animation_duration=300,
                tabs=[
                    ft.Tab(
                        text="結果・入力の要約",
                        content=ft.Card(
                            content=ft.Container(
                                content=ft.Column(
                                    controls=[
                                        #self.graph,
                                        lv_01,
                                    ],
                                    alignment=ft.MainAxisAlignment.SPACE_AROUND,
                                ),
                                width=2100,
                                padding=10,
                            )
                        ),
                    ),
                    ft.Tab(
                        text="PSC,LCCでの公共側収支等",
                        content=ft.Card(
                            content=ft.Container(
                                content=ft.Column(
                                    controls=[
                                        #self.graph,
                                        lv_02,
                                    ],
                                    alignment=ft.MainAxisAlignment.SPACE_AROUND,
                                ),
                                width=2100,
                                padding=10,
                            )
                        )
                    ),
                    ft.Tab(
                        text="SPC収支等",
                        content=ft.Card(
                            content=ft.Container(
                                content=ft.Column(
                                    controls=[
                                        #self.graph,
                                        lv_03,
                                    ],
                                    alignment=ft.MainAxisAlignment.SPACE_AROUND,
                                ),
                                width=2100,
                                padding=10,
                            )
                        )
                    ),
                    ft.Tab(
                        text="入力値等一覧",
                        content=ft.Card(
                            content=ft.Container(
                                content=ft.Column(
                                    controls=[
                                        #self.graph,
                                        lv_04,
                                    ],
                                    alignment=ft.MainAxisAlignment.SPACE_AROUND,
                                ),
                                width=2100,
                                padding=10,
                            )
                        )
                    ),
                ],
            )
 
