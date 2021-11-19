import difflib as diff
import glob


path = 'A/'
path2 = 'B/'

folder = 'model/'

prediction_path = 'prediction/

file_path = path+folder+prediction_path
filelist = glob.glob(file_path+'*.csv')
print(len(filelist))

file_path2 = path2+folder2+prediction_path
filelist2 = glob.glob(file_path2+'*.csv')
print(len(filelist2))

diff_cnt = 0
match_cnt = 0
diff_list = []
nothing_list = []
nothing_cnt = 0
for k in filelist:
    file = k
    filename = file.split('\\')[-1]
    with open(file,'r') as f:
        str1 = f.readlines()
#         print(f'比較対象1:{file}')
    if glob.glob(file_path2+ filename):
        with open(file_path2+ filename,'r') as ff:
            str2 = ff.readlines()
    #         print(f'比較対象2:{file_path2+filename}')
        # print(str1)
        # print(str2)
    #     res = diff.context_diff(str1,str2)
    #     for r in res:
    #         if r[0:1] in ['+', '-']:
    #             print(r)
    #     print('\n'.join(res))
        diff_file = []
        for i in diff.context_diff(str1, str2, fromfile=file, tofile=file_path2+filename):
    #         print(i, end='')
            if i :
                diff_file.append('不一致')
            else:
                diff_file.append('合致')
        if set(diff_file) =={'不一致'}:
            result = str(set(diff_file))
            diff_cnt += 1
            diff_list.append(filename)
        else :
            result = str(set({'一致'}))
            match_cnt += 1
        print(filename+':'+result)
    else:
        nothing_list.append(filename)
        nothing_cnt += 1
        print(filename+':{元データなし}')
print(f'一致:{match_cnt} 不一致:{diff_cnt} 元データなし:{nothing_cnt}')
