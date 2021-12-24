def read_csv_time(input_path):
    start = time.time()
    df = pd.read_csv(input_path , encoding='utf_8_sig')
    elapsed_time = time.time() - start
    print(input_paht)
    print ("elapsed_time:{0}".format(elapsed_time) + "[sec]")
    return df

input_path = 'input/input.csv'
input_df = read_csv_time(input_path)
