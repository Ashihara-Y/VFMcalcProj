import pandas as pd
import openpyxl
from sqlalchemy import create_engine

engine = create_engine('sqlite:///VFM.db', echo=False, connect_args={'check_same_thread': False})
engine_m = create_engine('sqlite:///sel_res.db', echo=False, connect_args={'check_same_thread': False})
        
def export_to_excel():
    df_res = pd.read_sql_table('sel_res', engine_m)
    dtime = df_res['selected_datetime'].iloc[0]
    #dtime = con.all()[0]['selected_datetime']
    #con.close()

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
        'final_inputs_table',
    ]

    selected_res_list = []
    for table_name in table_names:
        query = 'select * from ' + table_name + ' where datetime = ' + '"' + dtime + '"'
        table_name = pd.read_sql_query(query, engine)
        selected_res_list.append(table_name)

    dtime_w = dtime.replace(' ', '_').replace(':', '_').replace('+09_00', '')
    file_name = 'VFM_result_sheet_' + dtime_w + '.xlsx'
    save_path = 'vfm_output/' + file_name

    wb = openpyxl.Workbook()
    ws = wb['Sheet']
    ws.title = '算定結果概要'
    wb.save(save_path)

    PSC_res_df = selected_res_list[0]
    PSC_pv_df = selected_res_list[1]
    LCC_res_df = selected_res_list[2]
    LCC_pv_df = selected_res_list[3]
    SPC_res_df = selected_res_list[4]
    SPC_check_df = selected_res_list[5]
    Risk_res_df = selected_res_list[6]
    VFM_res_df = selected_res_list[7]
    PIRR_res_df = selected_res_list[8]
    res_summ_df = selected_res_list[9]
    final_inputs_df = selected_res_list[10]

    PSC_res_df = PSC_res_df.drop(['datetime', 'user_id', 'calc_id'], axis=1)
    PSC_pv_df =  PSC_pv_df.drop(['datetime', 'user_id', 'calc_id'], axis=1)
    LCC_res_df = LCC_res_df.drop(['datetime', 'user_id', 'calc_id'], axis=1)
    LCC_pv_df = LCC_pv_df.drop(['datetime', 'user_id', 'calc_id'], axis=1)
    SPC_res_df = SPC_res_df.drop(['datetime', 'user_id', 'calc_id'], axis=1)
    SPC_check_df = SPC_check_df.drop(['datetime', 'user_id', 'calc_id'], axis=1)
    Risk_res_df = Risk_res_df.drop(['datetime', 'user_id', 'calc_id'], axis=1)
    VFM_res_df = VFM_res_df.drop(['datetime', 'user_id', 'calc_id'], axis=1)
    PIRR_res_df = PIRR_res_df.drop(['datetime', 'user_id', 'calc_id'], axis=1)
    res_summ_df = res_summ_df.drop(['datetime', 'user_id', 'calc_id'], axis=1)
    final_inputs_df = final_inputs_df.drop('datetime', axis=1)
    res_summ_df['discount_rate'] = res_summ_df['discount_rate'].map(lambda x: round(float(x*100), 4))

    PSC_res_df = PSC_res_df.rename(
         columns={
                'periods':'経過年度', 
                'year':'スケジュール', 
                'hojokin':'補助金', 
                'kouhukin':'交付金', 
                'kisai_gaku':'起債発行額', 
                'riyou_ryoukin':'利用料金収入',
                'income_total':'収入計', 
                'shisetsu_seibihi':'施設整備費用', 
                'ijikanri_unneihi':'維持管理運営費用',
                'monitoring_costs':'モニタリング等費用', 
                'chisai_zansai':'(起債残債)', 
                'kisai_shoukan_gaku':'起債償還額',
                'kisai_shoukansumi_gaku':'(起債償還済額)', 
                'kisai_risoku_gaku':'起債利息', 
                'payments_total':'支出計',
                'net_payments':'収支（キャッシュ・フロー）', 
            }
    )
    PSC_pv_df = PSC_pv_df.rename(
        columns={
                'net_payments':'収支（キャッシュ・フロー）', 
                'discount_factor':'割引係数', 
                'present_value':'収支（キャッシュ・フロー）現在価値', 
            }
    )
    LCC_res_df = LCC_res_df.rename(
        columns={
                'periods':'経過年度', 
                'year':'スケジュール', 
                'hojokin':'補助金', 
                'kouhukin':'交付金', 
                'kisai_gaku':'起債発行額', 
                'zeishu':'税収',
                'income_total':'収入計', 
                'shisetsu_seibihi_ikkatsu':'施設整備サービス対価(一括払)',
                'shisetsu_seibihi_kappugoukei':'(施設整備サービス対価(割賦計）)', 
                'shisetsu_seibihi_kappuganpon':'施設整備サービス対価(割賦元本)',
                'shisetsu_seibihi_kappukinri':'施設整備サービス対価(割賦金利)', 
                'ijikanri_unneihi':'維持管理費サービス対価', 
                'monitoring_costs':'モニタリング等費用',
                'SPC_keihi':'SPC費用', 
                'chisai_zansai':'(起債残債)', 
                'kisai_shoukan_gaku':'起債償還額',
                'kisai_shoukansumi_gaku':'(起債償還済額)', 
                'kisai_risoku_gaku':'起債利息', 
                'payments_total':'支出計',
                'net_payments':'収支', 
            }
    )
    LCC_pv_df = LCC_pv_df.rename(
        columns={
                'net_payments':'収支(キャッシュ・フロー)', 
                'discount_factor':'割引係数', 
                'present_value':'収支(キャッシュ・フロー)現在価値',
            }
    )
    SPC_res_df = SPC_res_df.rename(
        columns={
                'periods':'経過年度', 
                'year':'スケジュール', 
                'shisetsu_seibihi_taika_ikkatsu':'施設整備サービス対価(一括払)',
                'shisetsu_seibihi_taika_kappuganpon':'施設整備サービス対価(割賦元本)',
                'shisetsu_seibihi_taika_kappukinri':'施設整備サービス対価(割賦金利)', 
                'ijikanri_unneihi_taika':'維持管理費サービス対価',
                'SPC_hiyou_taika':'SPC費用サービス対価', 
                'riyou_ryoukin':'利用料金収入', 
                'income_total':'収入計', 
                'shisetsu_seibihi':'施設整備費用',
                'ijikanri_unneihi':'維持管理費', 
                'kariire_ganpon_hensai':'(借入元本返済)', 
                'shiharai_risoku':'支払利息',
                'SPC_keihi':'SPC経費', 
                'SPC_setsuritsuhi':'SPC当初費用（設立費用、予備費）', 
                'houjinzei_etc':'法人税・公租公課', 
                'payments_total_full':'支出計（元本返済込）',
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
                'payments_total_full':'支出計(元本返済込)', 
                'net_income':'収支(キャッシュ・フロー)', 
                'net_income_full':'収支(元本返済込)',
                'Cash_for_P_payment':'元本返済充当可能額', 
                'P_payment_check':'元本返済可否', 
            }
    )
    Risk_res_df = Risk_res_df.rename(
        columns={
                'risk_adjust_gaku':'リスク調整額', 
            }
    )
    VFM_res_df = VFM_res_df.rename(
        columns={
                'VFM':'VFM(金額)', 
                'VFM_percent':'VFM(％)', 
            }
    )
    PIRR_res_df = PIRR_res_df.rename(
        columns={
                'PIRR':'プロジェクト内部収益率', 
                'PIRR_percent':'プロジェクト内部収益率(％)', 
                
            }
    )
    res_summ_df = res_summ_df.rename(
        columns={
                'VFM_percent':'VFM(％)', 
                'PSC_present_value':'PSCでの公共キャッシュ・フロー現在価値(百万円)', 
                'LCC_present_value':'PFI-LCCでの公共キャッシュ・フロー現在価値(百万円)', 
                'PIRR':'プロジェクト内部収益率(％)',
                'SPC_payment_cash':'SPCの元本返済可否', 
                'mgmt_type':'発注者区分', 
                'proj_ctgry':'事業形態', 
                'proj_type':'事業方式',
                'const_years':'施設整備期間', 
                'proj_years':'事業期間', 
                'discount_rate':'割引率(％)', 
                'kariire_kinri':'借入コスト(％)',
                'kappu_kinri':'割賦金利(％)',
                'kappu_kinri_spread':'割賦金利スプレッド(％)',
                'SPC_fee':'SPCへの手数料(百万円)',
            }
    )

    final_inputs_df = final_inputs_df.T.reset_index().rename(columns={"index":"項目名", 0:"値"})
    res_summ_df = res_summ_df.T.reset_index().rename(columns={"index":"項目名", 0:"値"})


    with pd.ExcelWriter(save_path, engine='openpyxl', if_sheet_exists='overlay', mode='a') as writer:
        res_summ_df.to_excel(writer, sheet_name='算定結果概要', index=False)
        PSC_res_df.to_excel(writer, sheet_name='PSC算定結果', index=False)
        PSC_pv_df.to_excel(writer, sheet_name='PSC現在価値算定結果', index=False)
        LCC_res_df.to_excel(writer, sheet_name='LCC算定結果', index=False)
        LCC_pv_df.to_excel(writer, sheet_name='LCC現在価値算定結果', index=False)
        SPC_res_df.to_excel(writer, sheet_name='SPC算定結果', index=False)
        SPC_check_df.to_excel(writer, sheet_name='SPC返済資金チェック結果', index=False)
        Risk_res_df.to_excel(writer, sheet_name='リスク調整額', index=False)
        VFM_res_df.to_excel(writer, sheet_name='VFM算定結果', index=False)
        PIRR_res_df.to_excel(writer, sheet_name='PIRR算定結果', index=False)
        final_inputs_df.to_excel(writer, sheet_name='最終入力等', index=False)


# 上記をmok dataなしで動かすには、事業費用概算シートへの入力値用の入力画面とDB入力への統合が必要
if __name__ == '__main__':
    export_to_excel()