def read_csv(input_path)
    start = time.time()
    df = pd.read_csv(input_path , encoding='utf_8_sig')
    elapsed_time = time.time() - start
    print ("elapsed_time:{0}".format(elapsed_time) + "[sec]")
    return df
