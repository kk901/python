# !pip install googletrans==4.0.0-rc1
from googletrans import Translator

eng_columns = {}
columns = input_df.columns
translator = Translator()



for column in columns:
    eng_column = translator.translate(column).text
    eng_column = eng_column.replace(' ', '_')
    eng_columns[column] = eng_column

input_df.rename(columns=eng_columns, inplace=True)
