import pandas as pd
import openpyxl
import pathlib
from pathlib import Path
import tinydb
from tinydb import TinyDB, Query
import yaml

# まず、標準算定フォーマットのExcelブックを開いて、別名（ファイル名にUID＋CalcIDを追加）でOutputディレクトリに保存する
book = openpyxl.load_workbook('標準算定フォーマット.xlsx')
# 次に、保存したブックの「事業費概算」シートを開いて、初期入力値のうち、Part1を書き込む
#ii_db_01 = TinyDB("ii_01_db.json")
#ii_db_02 = TinyDB("ii_02_db.json")
# initial_inputs_01 = ii_db_01.all()[0]
# initial_inputs_02 = ii_db_02.all()[0]

# この部分のセル：変数名の対応を、YAMLファイルから読み込むように変更する
sheet_01 = book['事業費概算']
sheet_01['H5'] = initial_inputs_01['reduc_shisetsu_db']
sheet_01['I5'] = initial_inputs_01['reduc_shisetsu_bt']
sheet_01['G6'] = initial_inputs_01['shisetsuseibi_raku']
sheet_01['G7'] = initial_inputs_01['shisetsuseibi_tan']

sheet_01['H11'] = initial_inputs_01['reduc_jinkenhi_db']
sheet_01['I11'] = initial_inputs_01['reduc_jinkenhi_bt']
sheet_01['J11'] = initial_inputs_01['jinkenhi_bukka']
sheet_01['G12'] = initial_inputs_01['jinkenhi_raku']
sheet_01['G13'] = initial_inputs_01['jinkenhi_tan']

sheet_01['H14'] = initial_inputs_01['reduc_shuzen_db']
sheet_01['I14'] = initial_inputs_01['reduc_shuzen_bt']
sheet_01['J14'] = initial_inputs_01['shuzenhi_bukka']
sheet_01['G15'] = initial_inputs_01['shuzen_raku']
sheet_01['G16'] = initial_inputs_01['shuzen_tan']

sheet_01['H17'] = initial_inputs_01['reduc_doryoku_db']
sheet_01['I17'] = initial_inputs_01['reduc_doryoku_bt']
sheet_01['J17'] = initial_inputs_01['doryoku_bukka']
sheet_01['G18'] = initial_inputs_01['doryoku_raku']
sheet_01['G19'] = initial_inputs_01['doryoku_tan']

sheet_01['H20'] = initial_inputs_01['reduc_option01_db']
sheet_01['I20'] = initial_inputs_01['reduc_option01_bt']
sheet_01['J20'] = initial_inputs_01['option01_bukka']
sheet_01['G21'] = initial_inputs_01['option01_raku']
sheet_01['G22'] = initial_inputs_01['option01_tan']

sheet_01['H23'] = initial_inputs_01['reduc_option02_db']
sheet_01['I23'] = initial_inputs_01['reduc_option02_bt']
sheet_01['J23'] = initial_inputs_01['option02_bukka']
sheet_01['G24'] = initial_inputs_01['option02_raku']
sheet_01['G25'] = initial_inputs_01['option02_tan']

# 17行目からのコードを改善できないか？
# セルへの入力は、sheet.cell(column=4, row=2, value='test')とも書けるらしい。
# これなら、CSVからセル情報と入力変数名を読み取って、DataFrameか辞書に格納した上で、
# リストにして、For文で読み込ませて、連続入力できるか？
# 入力セルに変更があった場合の修正も、CSVの値を変更するだけなので、保守しやすいのでは?


# そのためには、事業費概算シートへの入力値用の入力画面が必要
# その後、初期入力値の「事業方式」の値から、入力シートを選択
# 選択したシートに、初期入力値のPart2と最終入力値を書き込む
# 保存したブックを閉じる


def export_to_excel(final_inputs_file, initial_inputs_file, output_file):
    # Read the final inputs file
    final_inputs = pd.read_csv(final_inputs_file)

    # Read the initial inputs file
    initial_inputs = pd.read_csv(initial_inputs_file)

    # Merge the final inputs and initial inputs dataframes
    merged_data = pd.merge(final_inputs, initial_inputs, on='common_column')

    # Export the merged data to an Excel file
    merged_data.to_excel(output_file, index=False)

# Example usage
final_inputs_file = '/path/to/Final-Inputs.csv'
initial_inputs_file = '/path/to/Initial_Inputs.csv'
output_file = '/path/to/output.xlsx'

export_to_excel(final_inputs_file, initial_inputs_file, output_file)