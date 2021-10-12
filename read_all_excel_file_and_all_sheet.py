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
        input_sheet_df.rename(columns={'Unnamed: 1': 'xxx1', 
                           'Unnamed: 2': 'xxx2',
                           'Unnamed: 4': 'xxx3'
                           }, inplace=True)
        input_sheet_df['sheet_name'] = target_sheet
        output = pd.concat([output,input_sheet_df],ignore_index=True)
    output.to_csv(path+'/output/'+save_filename+'.csv', encoding='cp932')
