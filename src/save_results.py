import sys
sys.dont_write_bytecode = True
#import os
import pandas as pd
#import duckdb
from ulid import ULID
import timeflake
import datetime
import uuid6
from tinydb import TinyDB, Query
import make_inputs_df
#import decimal
import decimal
from sqlalchemy import create_engine
import sqlite3
from zoneinfo import ZoneInfo

engine = create_engine('sqlite:///VFM.db', echo=False, connect_args={'check_same_thread': False})
conn = sqlite3.connect('VFM.db')
c = conn.cursor()

user_id = ULID.from_datetime(datetime.datetime.now(tz=ZoneInfo("Asia/Tokyo")))
calc_id = uuid6.uuid7()
timestamp = calc_id.int >> 80
dtime = datetime.datetime.fromtimestamp(timestamp // 1000.0, tz=ZoneInfo("Asia/Tokyo"))
#fromtimestamp(timestamp_ms / 1000.0, tz=timezone.utc)

df_name_list=[]

def make_df_addID_saveDB():
    inputs_pdt = make_inputs_df.main()

    PSC_df = pd.read_sql_query("SELECT * FROM PSC_table", engine)
    PSC_pv_df = pd.read_sql_query("SELECT * FROM PSC_pv_table", engine)
    LCC_df = pd.read_sql_query("SELECT * FROM LCC_table", engine)
    LCC_pv_df = pd.read_sql_query("SELECT * FROM LCC_pv_table", engine)
    SPC_df = pd.read_sql_query("SELECT * FROM SPC_table", engine)
    SPC_check_df = pd.read_sql_query("SELECT * FROM SPC_check_table", engine)
    Risk_df = pd.read_sql_query("SELECT * FROM Risk_table", engine)
    VFM_df = pd.read_sql_query("SELECT * FROM VFM_table", engine)
    PIRR_df = pd.read_sql_query("SELECT * FROM PIRR_table", engine)

    # make summary
    PSC_pv_summary_org = PSC_pv_df[['present_value']].sum()
    LCC_pv_summary_org = LCC_pv_df[['present_value']].sum()
    SPC_check_summary_org = SPC_check_df.loc[int(inputs_pdt.const_years)+1:int(inputs_pdt.proj_years), 'P_payment_check'].to_list()
    VFM_summary_df = VFM_df[['VFM','VFM_percent']]
    PIRR_summary_df = PIRR_df[['PIRR_percent']]

    def payment_check(bool):
        if bool == 'True':
            return "返済資金は十分"
        elif bool == 'False':
            return "返済資金が不足"

    SPC_check_mod = str('False' not in SPC_check_summary_org)
    SPC_check_res = payment_check(SPC_check_mod)

    VFM_calc_summary_df = pd.DataFrame(columns=['VFM_percent','PSC_present_value','LCC_present_value','PIRR','SPC_payment_cash'], index=['0'])

    #VFM_calc_summary_df['VFM'] = VFM_summary_df['VFM'].iloc[0]
    VFM_calc_summary_df['VFM_percent'] = VFM_summary_df['VFM_percent'].iloc[0]
    VFM_calc_summary_df['PSC_present_value'] = PSC_pv_summary_org.iloc[0]
    VFM_calc_summary_df['LCC_present_value'] = LCC_pv_summary_org.iloc[0]
    VFM_calc_summary_df['PIRR'] = PIRR_summary_df['PIRR_percent'].iloc[0]
    VFM_calc_summary_df['SPC_payment_cash'] = SPC_check_res

    kijun_kinri = decimal.Decimal(str(inputs_pdt.kijun_kinri)).quantize(decimal.Decimal('0.00001'), 'ROUND_HALF_UP')
    #kitai_bukka = Decimal(str(inputs_pdt.kitai_bukka)).quantize(Decimal('0.001'), 'ROUND_HALF_UP')
    lg_spread = decimal.Decimal(str(inputs_pdt.lg_spread)).quantize(decimal.Decimal('0.00001'), 'ROUND_HALF_UP')

    #discount_rate = Decimal((kijun_kinri + kitai_bukka)*100).quantize(Decimal('0.001'), 'ROUND_HALF_UP')
    kariire_kinri = decimal.Decimal((kijun_kinri + lg_spread)*100).quantize(decimal.Decimal('0.001'), 'ROUND_HALF_UP')

    final_inputs_short_dic = {
        'mgmt_type': inputs_pdt.mgmt_type,
        'proj_ctgry': inputs_pdt.proj_ctgry,
        'proj_type': inputs_pdt.proj_type,
        'const_years': inputs_pdt.const_years,
        'proj_years': inputs_pdt.proj_years,
        'discount_rate': round(float(inputs_pdt.discount_rate),6),
        'kariire_kinri': round(float(kariire_kinri),6),
        'Kappu_kinri': round(float(inputs_pdt.Kappu_kinri)*100,6),
        'kappu_kinri_spread': round(float(inputs_pdt.kappu_kinri_spread)*100,6),
        'SPC_fee': round(float(inputs_pdt.SPC_fee),1),
    }

    final_inputs_short_df = pd.DataFrame(final_inputs_short_dic, index=['0'])
    #print(inputs_pdt.kijun_kinri, inputs_pdt.lg_spread)
    res_summ_df = VFM_calc_summary_df.join(final_inputs_short_df)


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
    #final_inputs_df['datetime'] = self.dtime

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

        #final_inputs_df.to_sql('final_inputs_table', engine, if_exists='replace', index=False)

    def addID(x_df):
        x_df['datetime'] = str(dtime)
        x_df['user_id'] = str(user_id)
        x_df['calc_id'] = str(calc_id)

        return x_df

    df_list = [
        PSC_df,
        PSC_pv_df,
        LCC_df,
        LCC_pv_df,
        SPC_df,
        SPC_check_df,
        Risk_df,
        VFM_df,
        PIRR_df, 
        res_summ_df,
        final_inputs_df
        ]
    df_name_list = [
        (PSC_df,'PSC_df'),
        (PSC_pv_df,'PSC_pv_df'),
        (LCC_df,'LCC_df'),
        (LCC_pv_df,'LCC_pv_df'),
        (SPC_df,'SPC_df'),
        (SPC_check_df,'SPC_check_df'),
        (Risk_df,'Risk_df'),
        (VFM_df,'VFM_df'),
        (PIRR_df,'PIRR_df'),
        (res_summ_df,'res_summ_df'),
        (final_inputs_df,'final_inputs_df')
        ]

    for i in df_list:
            addID(i)

    for x_df in df_name_list:
        x_df[0].applymap(lambda x: float(x) if isinstance(x, decimal.Decimal) else x)
        x_df[0].to_sql(x_df[1].replace('_df','') + '_res_table', engine, if_exists='append', index=False)
    


if __name__ == "__main__":
    make_df_addID_saveDB()
