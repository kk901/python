import pandas as pd
import glob
import time
from tqdm.notebook import tqdm

def read_all_csv(input_path):
    start = time.time()
    filelist = glob.glob(input_path+'*.csv')
    print(len(file))
    output = pd.DataFrame(index=[])
    def readcsv(file):
        #file_name取得
        filename = file.split('\\')[-1].split('.')[0]
        input_csv = pd.read_csv(file,encoding='cp932')
        print(filename)
        input_csv['file_name'] = filename
        return input_csv
    output = pd.concat([readcsv(file) for file in tqdm(filelist)],ignore_index=True)
    elapsed_time = time.time()-start
    print("総時間:{}".format(elapsed_time))
    return output


input_path = 'data/'
input_df = read_all_csv(input_path)


input_df.to_csv('output/input.csv', encoding='utf_8_sig')
