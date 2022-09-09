def null_creansing_replace(df,target,recover):
    df.loc[df[target].isnull(),target] = df.loc[df[target].isnull(),recover]
    return df
def genrerate_start_end_date(df,tgt_group):
    df['開始日付'] = pd.to_datetime(df['開始日付'])
    df['終了日付'] = pd.to_datetime(df['終了日付'])
    start = df.groupby(tgt_group)['開始日付'].min().reset_index()
    end = df.groupby(tgt_group)['終了日付'].max().reset_index()
    output = pd.merge(start,end,on=tgt_group,how='left')
    return output

def nendo_flag(df,tgt_column):
    for i in range(2018,2022):
        df.loc[((~(df['終了日付']>='1800-01-01'))&(df['開始日付']< f'{i+1}-04-01'))|((df['開始日付']< f'{i+1}-04-01') &(df['終了日付']>= f'{i}-04-01')),f'{i}_{tgt_column}'] = df.loc[((~(df['終了日付']>='1800-01-01'))&(df['開始日付']< f'{i+1}-04-01'))|((df['開始日付']< f'{i+1}-04-01') &(df['終了日付']>= f'{i}-04-01')),tgt_column]
    return df
  
def nendo_flag_0_1(df,tgt_column):
    for i in range(2018,2022):
        df[f'{i}_{tgt_column}_flag'] = 1
        df[f'{i}_{tgt_column}'] = df[f'{i}_{tgt_column}'].fillna('')
        df.loc[df[f'{i}_{tgt_column}']=='',f'{i}_{tgt_column}_flag'] = 0
    return df
  
def get_reccent_value(df,tgt_column):
    output = pd.DataFrame()
    output = df[['識別番号']]
    output = output[~output.duplicated()].reset_index(drop= True)
    df = df.sort_values(['識別番号','開始日付'],ascending=[True,True]).reset_index()
    for i in range(2018,2022):
        col = ['識別番号',f'{i}_{tgt_column}_flag']
        tmp = df[['識別番号',f'{i}_{tgt_column}_flag',f'{i}_{tgt_column}','開始日付']]
        tmp = tmp[tmp[f'{i}_{tgt_column}_flag']==1]
        tmp = tmp.loc[tmp.groupby(col)['開始日付'].idxmax()]
        output = pd.merge(output,tmp[['識別番号',f'{i}_{tgt_column}',f'{i}_{tgt_column}_flag']],on=['識別番号'],how='left')
    return output 

def precessed(df,tgt_group,tgt_column):
    df = genrerate_start_end_date(df,tgt_group)
    df = nendo_flag(df,tgt_column)
    df = nendo_flag_0_1(df,tgt_column)
    df = get_reccent_value(df,tgt_column)
    return df
  
tgt_group = ['識別番号','所属']
tgt_column = '所属'
output1 = precessed(df,tgt_group,tgt_column)
