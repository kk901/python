name = '分類観点1'
column_name = '項目名'
word_list_df = pd.read_csv('data/word_list.csv')
input_df = pd.read_csv('data/input.csv')


def classify_target(name,column_name,target_wordlist_df,input_df):
    '''
    対象ワードを元に、部分一致でフラグをつける
    '''
    output=input_df
    output[name] =0
    output['分類_'+name] = '対象外'
    for n in target_wordlist_df['ワード']:
        print(n)
        output[n] =0
        output[n].loc[output[column_name].str.contains(n) == True] = 1
        output.loc[output[column_name].str.contains(n) == True,'分類_'+name] = n 
        output[name] = output[name]+ output[n]
        print(input_df[column_name].str.contains(n).value_counts())
    output[name].loc[output[name]>=1] = 1
    return output
    
output = classify_target(name,word_list_df,input_df)
