import pandas as pd
import openpyxl
from tinydb import TinyDB, Query
from sqlalchemy import create_engine

con = TinyDB("selected_res.json")
dtime = con.all()[0]['selected_datetime']
con.close()

engine = create_engine('sqlite:///VFM.db', echo=False, connect_args={'check_same_thread': False})
        
def export_to_excel():
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

    selected_res_list = []
    for table_name in table_names:
        query = 'select * from ' + table_name + ' where datetime = ' + '"' + dtime + '"'
        table_name = pd.read_sql_query(query, engine)
        selected_res_list.append(table_name)

    dtime_w = dtime.replace(' ', '_').replace(':', '_')
    file_name = 'VFM_result_sheet_' + dtime_w + '.xlsx'
    save_path = 'vfm_output/' + file_name

    wb = openpyxl.Workbook()
    ws = wb['Sheet']
    ws.title = 'Summary_result_sheet'
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

    with pd.ExcelWriter(save_path, engine='openpyxl', if_sheet_exists='overlay', mode='a') as writer:
        res_summ_df.to_excel(writer, sheet_name='Summary_result_sheet')
        PSC_res_df.to_excel(writer, sheet_name='PSC_result_sheet')
        PSC_pv_df.to_excel(writer, sheet_name='PSC_pv_result_sheet')
        LCC_res_df.to_excel(writer, sheet_name='LCC_result_sheet')
        LCC_pv_df.to_excel(writer, sheet_name='LCC_pv_result_sheet')
        SPC_res_df.to_excel(writer, sheet_name='SPC_result_sheet')
        SPC_check_df.to_excel(writer, sheet_name='SPC_check_result_sheet')
        Risk_res_df.to_excel(writer, sheet_name='Risk_result_sheet')
        VFM_res_df.to_excel(writer, sheet_name='VFM_result_sheet')
        PIRR_res_df.to_excel(writer, sheet_name='PIRR_result_sheet')


# 上記をmok dataなしで動かすには、事業費用概算シートへの入力値用の入力画面とDB入力への統合が必要
if __name__ == '__main__':
    export_to_excel()