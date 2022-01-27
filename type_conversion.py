#日付がobject等だった時の型変換
input_df['date'] = pd.to_datetime(input_df['date'])
