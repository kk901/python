import pandas as pd
import numpy as np
import re
from tqdm import tqdm
import gc
import glob
import openpyxl

###parameter
#データ格納のpath
path = '../data'
#excelシートのスキップする行数
skiprows = 4

###pathのエクセルのファイル名を全て取得してエクセルごとに、すべてのシートを一つに集約して保存

#pathのエクセルのファイル名を全て取得
file = glob.glob(path+'/*.xlsx')

for n in tqdm(file):
    #ファイルから読み取りpath作成
    input_path = n
    #保存時は同じ名前でcsvで保存する
    save_filename= input_path.split('/')[-1].split('.')[0]
    #データ読み取り
    input_book = pd.ExcelFile(input_path)
    #シート名を全て読み取り
    input_sheet_name = input_book.sheet_names
    # シートごとにデータフレームを作成して全てを一つにまとめる
    output = pd.DataFrame(index=[])
    for k in tqdm(input_sheet_name):
        target_sheet = k
        input_sheet_df = input_book.parse(target_sheet,
                                          skiprows = skiprows)
### 書式の色の読み取り
        wb = openpyxl.load_workbook(input_path)
        sheet = wb[input_sheet_name]
        #書式の色を読み取りに行くセルの最大行を取得
        max_raw = len(input_sheet_df)
        mylist = []
        for i in range(skiprows+2,max_raw+skiprows+1):
            # 指定したカラム番号の色を読み取る
            cell = sheet.cell(row=i, column=4)
            bgcolor = cell.fill.bgColor.value
            # 空白の書式の色の場合True、それ以外はFalse
            if bgcolor=='00000000':
                mylist.append(True)
            else:
                mylist.append(False)
        # 色の情報のカラムを追加
        input_sheet_df['format_no_color'] =   mylist
        #カラム名前の変更
        input_sheet_df.rename(columns={'Unnamed: 1': 'xxx1', 
                           'Unnamed: 2': 'xxx2',
                           'Unnamed: 4': 'xxx4'
                           }, inplace=True)
        #シートの名前をDataFrameに追加
        input_sheet_df['sheet_name'] = target_sheet
        #一つのDataFrameに集約
        output = pd.concat([output,input_sheet_df],ignore_index=True)
###エクセルごとに全シートを一つに集約したものを保存
    output.to_csv(path+'/output/'+save_filename+'.csv', encoding='cp932')
