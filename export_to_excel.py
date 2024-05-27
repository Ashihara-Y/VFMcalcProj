import pandas as pd
import openpyxl
import pathlib
from pathlib import Path
import tinydb
from tinydb import TinyDB, Query
import yaml
import os
import shutil


db = TinyDB("inputs_db.json")
inputs = db.all()[0]

fin = open('to_excel_01.yml')
res_01 = yaml.load(fin, Loader=yaml.FullLoader)
res_list0 = []
for r in res_01['file_sheet']:
    res_list0.append(list(r.values())[0])
book = res_list0[0]
sheet = res_list0[1]
#print(res_list0)
fin.close()

fin = open('to_excel_02.yml')
res_02 = yaml.load(fin, Loader=yaml.FullLoader)
#res_list1 = []
#for r in res_02['file_sheet']:
#    res_list1.append(list(r.values())[0])
#book = res_list1[0]
#sheet = res_list1[1]
#print(res_list1)
fin.close()

jigyouhiyou_sekisan = {
    'shisetsu_seibi_kouritsusei_DBDBO': 0.05,
    'shisetsu_seibi_kouritsusei_BTBTO': 0.05,
    'shisetsu_seibi_PSC_rakusatsu': 0.0,
    'shisetsu_seibi_PSC_yosantanka': 3000.0,
    'ijikanri_jinkenhi_kouritsusei_DBDBO': 0.05,
    'ijikanri_jinkenhi_kouritsusei_BTBTO': 0.05,
    'ijikanri_jinkenhi_bukkajousyou': 0.02,
    'ijikanri_jinkenhi_PSC_rakusatsu': 0.0,
    'ijikanri_jinkenhi_PSC_yosantanka': 30.0,
    'ijikanri_shuzenhi_kouritsusei_DBDBO': 0.05,
    'ijikanri_shuzenhi_kouritsusei_BTBTO': 0.05,
    'ijikanri_shuzenhi_bukkajousyou': 0.02, 
    'ijikanri_shuzenhi_PSC_rakusatsu': 0.0,
    'ijikanri_shuzenhi_PSC_yosantanka': 15.0,
    'ijikanri_douryokuhi_kouritsusei_DBDBO': 0.05,
    'ijikanri_douryokuhi_kouritsusei_BTBTO': 0.05,
    'ijikanri_douryokuhi_bukkajousyou': 0.02,
    'ijikanri_douryokuhi_PSC_rakusatsu': 0.0,
    'ijikanri_douryokuhi_PSC_yosantanka': 5.0,
    'ijikanri_option01_kouritsusei_DBDBO': 0.05,
    'ijikanri_option01_kouritsusei_BTBTO': 0.05,
    'ijikanri_option01_bukkajousyou': 0.02,
    'ijikanri_option01_PSC_rakusatsu': 0.0,
    'ijikanri_option01_PSC_yosantanka': 0.0,
    'ijikanri_option02_kouritsusei_DBDBO': 0.05,
    'ijikanri_option02_kouritsusei_BTBTO': 0.05,
    'ijikanri_option02_bukkajousyou': 0.02,
    'ijikanri_option02_PSC_rakusatsu': 0.0,
    'ijikanri_option02_PSC_yosantanka': 0.0,
}

# まず、標準算定フォーマットのExcelブックを開いて、別名でOutputディレクトリに保存する
file = res_list0[0]
file_els = file.split('.',2)
file_copy = file_els[0] + '_copy.' + file_els[1]

file_copy_outpath = 'vfm_output/' + file_copy

if os.path.exists(file) :
    if os.path.exists("vfm_output"):
        pass
    else:
        os.mkdir("vfm_output")
    shutil.copy(file, file_copy_outpath)

# 保存したブックの「事業費用概算」シートを開いて、初期入力値のうち、Part1を書き込む処理を書く
# テスト用のモックとして、上記のjigyouhiyou_sekisanを書き込む
book = openpyxl.load_workbook(file_copy_outpath)
sheet_01 = book['事業費用概算']

for r in res_01["cell-position_value"]:
    cell = list(r.keys())[0]
    val = list(r.values())[0]
    sheet_01[cell] = jigyouhiyou_sekisan[val]
    #print(cell, val, inputs[val])
book.save(file_copy_outpath)

# 次に、保存したブックの該当事業形式シートを開いて、初期入力値のうち、Part2を書き込む
book = openpyxl.load_workbook(file_copy_outpath)
sheet_02 = book[inputs['proj_type']]

for r in res_02["cell-position_value"]:
    cell = list(r.keys())[0]
    val = list(r.values())[0]
    sheet_02[cell] = inputs[val]
    #print(cell, val, inputs[val])
book.save(file_copy_outpath)

#book = openpyxl.load_workbook('標準算定フォーマット.xlsx')
# 次に、保存したブックの「事業費概算」シートを開いて、初期入力値のうち、Part1を書き込む
#ii_db_01 = TinyDB("ii_01_db.json")
#ii_db_02 = TinyDB("ii_02_db.json")
# initial_inputs_01 = ii_db_01.all()[0]
# initial_inputs_02 = ii_db_02.all()[0]



# 上記を動かすには、事業費概算シートへの入力値用の入力画面が必要
# その後、初期入力値の「事業方式」の値から、入力シートを選択
# 選択したシートに、初期入力値のPart2と最終入力値を書き込む
# 保存したブックを閉じる


#def export_to_excel(final_inputs_file, initial_inputs_file, output_file):
#    # Read the final inputs file
#    final_inputs = pd.read_csv(final_inputs_file)
#
#    # Read the initial inputs file
#    initial_inputs = pd.read_csv(initial_inputs_file)
#
#    # Merge the final inputs and initial inputs dataframes
#    merged_data = pd.merge(final_inputs, initial_inputs, on='common_column')
#
#    # Export the merged data to an Excel file
#    merged_data.to_excel(output_file, index=False)
#
# Example usage
#final_inputs_file = '/path/to/Final-Inputs.csv'
#initial_inputs_file = '/path/to/Initial_Inputs.csv'
#output_file = '/path/to/output.xlsx'

#export_to_excel(final_inputs_file, initial_inputs_file, output_file)