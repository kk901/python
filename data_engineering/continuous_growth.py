# 時系列特徴量の作成

#ある会社の年月毎の売上合計データに対して
#ユーザID毎に何か月連続で売上が上昇しているか

#想定データ
# ユーザID	期間	売上
# 0	A	2020-01	93349
# 1	B	2020-01	32477
# 2	A	2020-02	95348
# 3	B	2020-02	37225
# 4	C	2020-02	61392
# ・
# ・
# ・

file_name = 'data.xlsx'
df_raw = pd.read_excel(file_name)
df_raw.drop_duplicates(inplace=True)
# 並び替えと複数行ある場合は足し合わせ
df = df_raw.groupby(['ユーザID','期間']).sum().reset_index()

# 前月売上比の成長を計算して、それを元に何カ月連続で売上成長しているかを計算
output=pd.DataFrame()
for k in df['ユーザID'].unique():
    user_df = df[df['ユーザID']==k]
    #前月比成長しているかを計算
    user_df['前月売上'] = user_df['売上'].shift(1)
    user_df.loc[user_df['売上']>user_df['前月売上'],'前月比売上上昇フラグ'] =1
    user_df.loc[~(user_df['売上']>user_df['前月売上']),'前月比売上上昇フラグ'] =0
#     user_df['前々月比売上上昇フラグ']=user_df['前月比売上上昇フラグ'].shift(1)
    user_df['前月比売上上昇フラグ'].fillna(0)
    #print(user_df)
    #何カ月連続で上昇しているかを計算
    continuous_growth = []
    growth_flag = 0
    for n in user_df.iterrows():
        if n[1]['前月比売上上昇フラグ']==1:
            growth_flag +=1
        else :
            growth_flag =0
        continuous_growth.append(growth_flag)
    #print(continuous_growth)
    user_df['何カ月連続で売上が上昇しているか'] = continuous_growth
    print(user_df)
    output = pd.concat([output,user_df],axis =0)
