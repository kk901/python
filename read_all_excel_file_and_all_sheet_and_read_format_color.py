import pandas as pd
import numpy as np
import re
from tqdm import tqdm
import gc
import glob
import openpyxl

#parameter
path = '../data'
skiprows = 4


file = glob.glob(path+'/*.xlsx')

for n in tqdm(file):
    input_path = n
    save_filename= input_path.split('/')[-1].split('.')[0]
    input_book = pd.ExcelFile(input_path)
    input_sheet_name = input_book.sheet_names
    output = pd.DataFrame(index=[])
    for k in tqdm(input_sheet_name):
        target_sheet = k
        input_sheet_df = input_book.parse(target_sheet,
                                          skiprows = skiprows)
        wb = openpyxl.load_workbook(input_path)
        sheet = wb[input_sheet_name]
        max_raw = len(input_sheet_df)
        mylist = []
        for i in range(skiprows+2,max_raw+skiprows+1):
            cell = sheet.cell(row=i, column=4)
            bgcolor = cell.fill.bgColor.value
            # 空白の書式の色の場合True、それ以外はFalse
            if bgcolor=='00000000':
                mylist.append(True)
            else:
                mylist.append(False)
        input_sheet_df['format_no_color'] =   mylist
        input_sheet_df.rename(columns={'Unnamed: 1': 'xxx1', 
                           'Unnamed: 2': 'xxx2',
                           'Unnamed: 4': 'xxx3'
                           }, inplace=True)
        input_sheet_df['sheet_name'] = target_sheet
        output = pd.concat([output,input_sheet_df],ignore_index=True)
    output.to_csv(path+'/output/'+save_filename+'.csv', encoding='cp932')
