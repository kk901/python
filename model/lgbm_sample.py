# coding: utf-8
import lightgbm as lgb
import datetime as dt
#import jpholiday
import matplotlib.pyplot as plt #Visulization
import seaborn as sns #Visulization
%matplotlib inline
import shap


# print the JS visualization code to the notebook
shap.initjs()

from sklearn.metrics import mean_absolute_error
from sklearn import metrics

# Parallel
import multiprocessing

# Data manipulation
import pandas as pd
import numpy as np

# Options for pandas
pd.options.display.max_columns = 50
pd.options.display.max_rows = 30

# Visualizations
# import plotly
# import plotly.graph_objs as go
# import plotly.offline as ply
# plotly.offline.init_notebook_mode(connected=True)
#import matplotlib as plt
import os
import shutil

# Misc
import glob
import time

from functools import partial
from functools import reduce

from tqdm import tqdm
from openpyxl import load_workbook

# Autoreload extension
if 'autoreload' not in get_ipython().extension_manager.loaded:
    %load_ext autoreload
    
%autoreload 2

# parameter
plt.style.use("seaborn-darkgrid")
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Yu Gothic']
plt.rcParams['font.size'] = 24


input_path = 'data.csv'
output= 'output/'

train_term_start =  '2018-03-01'
train_term_end = '2020-11-30'

val_term_point = '2020-06-01'

test_term_start = '2020-12-01'
test_term_end = '2021-05-31'

#保存時の名前
version = 'v_lgbm_' +str(dt.datetime.today().strftime('%Y-%m-%d'))

# 読み込むファイル
start = time.time()
input_df = pd.read_csv(input_path)
print('実行にかかった時間は{}秒でした'.format(time.time()-start))

input_df.dtypes


#学習に使うカラム
fit_col = ['A','B','C'
]

# drop 対象
drop_list = ['xxx','xxxx','Z','Y']

dt = 'date'

# 学習データとテストデータに分ける
train_df = input_df[(input_df['ds']<= train_term_end) & (input_df['ds']>= train_term_start) ]
test_df = input_df[(input_df['ds']<= test_term_end) & (input_df['ds']>= test_term_start) ]

#学習データの準備

train_train =  input_df[input_df[dt]< val_term_point ]
train_val =  input_df[input_df[dt]>= val_term_point ]

target_col = 'target'

train_y =train_train[target_col]
train_x = train_train[fit_col]

val_y = train_val[target_col]
val_x = train_val[fit_col]

trains = lgb.Dataset(train_x, train_y)
valids = lgb.Dataset(val_x, val_y)

# params = {
#     "objective": "regression",
#     "metrics": "rmse",
#     "learning_rate": "0.1"
# }

params = {
    # 二値分類問題
    'objective': 'binary',
    # AUC の最大化を目指す
    'metric': 'auc',
    # Fatal の場合出力
    'verbosity': -1, # <0:Fatal, =0:Error(Warning), =1:into,>1:Debug
    'learning_rate': '0.05',
    'seed':77,
    'num_leaves':31,# 木の複雑度をコントロールするメインパラメータ,分岐の終着点の数を決める 7,15,31 大きいほどOverfit 2^(mad_depth)*0.7
    'max_depth':9,# 木の最大の深さ 5,7,9 大きいほどOverfit
    'min_date_in_leaf':20, # 歯に行き着くデータの最小数 20,30,50　小さいほどOverfit
    'bagging_fraction':0.9,# baggingで選択されるサンプルの割合(bagging_freqとセットで設定する) 0.8,0.9 大きいほどOverfit?
    'bagging_freq':1,# 何回に一回baggingするか(bagging_fractinoとセットで設定する) 1,3 小さいほどOverfit?
    'feature_fraction':1.0,# 1未満にすることで特徴量を削除することになる 0.9,1.0 大きいほどOverfit?
    # 'lambda_l1':5,# L1正規化 0,2,5 小さいほどOverfit　正直どのくらいがいいかわからないので、下手にいじらないことも
    # 'lamdba_l2':5,# L2正規化 0,2,5 小さいほどOverfit　正直どのくらいがいいかわからないので、下手にいじらないことも
}


# 学習開始
start = time.time()
model = lgb.train(
    params,
    trains,
    valid_sets=valids,
    num_boost_round=1000,
    early_stopping_rounds=100)
print('実行にかかった時間は{}秒でした'.format(time.time()-start))

correct_label = test_df[target_col] 
test_df_features = test_df[fit_col]

y_pred = model.predict(test_df_features)
output_df = test_df
output_df['y_pred'] = y_pred
output_df.to_csv(output+f'output_{version}.csv', encoding='cp932')

# mae 計算（numpy で計算）
mae = np.mean(np.abs(output_df[target_col] - output_df['y_pred']))
print(mae)
dict = {'rmse':[mae]}
pd.DataFrame(dict).to_csv(output+f'mae_all_{version}.csv')
# rmse 計算（numpy で計算）
rmse = np.sqrt(np.mean( (output_df[target_col] - output_df['y_pred']) ** 2))
print(rmse)
dict = {'rmse':[rmse]}
pd.DataFrame(dict).to_csv(output+f'rmse_all_{version}.csv')

# AUC (Area Under the Curve) を計算する
fpr, tpr, thresholds = metrics.roc_curve(y_test, y_pred)
auc = metrics.auc(fpr, tpr)
print(auc)
plt.plot(fpr, tpr, label='ROC curve (area = %.2f)'%auc)
plt.legend()
plt.title('ROC curve')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.grid(True)

# feature importanceを表示

# 可視化（modelはlightgbmで学習させたモデル）
lgb.plot_importance(model, figsize=(8, 20))
plt.savefig(output + f'featire_importance_{version}.png')
plt.show()
# feature importanceを表示
# feature_importance（importance_type = ‘split’）
importance = pd.DataFrame(model.feature_importance(importance_type='split'), index=train_x.columns, columns=['importance'])
importance_split = importance.sort_values('importance', ascending=False)
display(importance_split)
importance_split.to_csv(output + f'feature_importance_split_{version}.csv')

# feature importanceを表示
# feature_importance（importance_type = ‘gain’）
importance = pd.DataFrame(model.feature_importance(importance_type='gain'), index=train_x.columns, columns=['importance'])
importance_gain = importance.sort_values('importance', ascending=False)
display(importance_gain)
importance_gain.to_csv(output+f'feature_importance_gain_{version}.csv')

# shap
# データ読み込み
start= time.time()
shap_train_data = train_df[fit_col]
explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(shap_train_data)
print('実行にかかった時間は{}秒でした'.format(time.time()-start))
start= time.time()
#SHAP Summary Plot
shap.summary_plot(shap_values, shap_train_data, plot_type="bar" )
plt.savefig(output + f'shap_summary_plot_bar_{version}.png')
print('実行にかかった時間は{}秒でした'.format(time.time()-start))
start= time.time()
#SHAP Summary Plot
shap.summary_plot(shap_values, shap_train_data )
plt.savefig(output + f'shap_summary_plot_{version}.png')
print('実行にかかった時間は{}秒でした'.format(time.time()-start))


##########以降はオプション

shap_values.head()
start= time.time()
#Visualize a single prediction
# Note that we use the “display values” data frame so we get nice strings instead of category codes.

shap.force_plot(explainer.expected_value, shap_values[0,:], test_df_features.iloc[0,:])
plt.savefig(output + f'shap_force_plot_{version}.png')
print('実行にかかった時間は{}秒でした'.format(time.time()-start))
#Visualize a single prediction
# Note that we use the “display values” data frame so we get nice strings instead of category codes.

shap.force_plot(explainer.expected_value[1], shap_values[1][0,:], test_df_features.iloc[0,:])
plt.savefig(output + f'shap_force_plot_{version}.png')
#Visualize many predictions
#To keep the browser happy we only visualize 1,000 individuals.
shap.force_plot(explainer.expected_value[1], shap_values[1][:1000,:], X_display.iloc[:1000,:])
plt.savefig(output + f'shap_force_plot_many_predicition_{version}.png')
