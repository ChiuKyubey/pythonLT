
import numpy as np 
import pandas as pd 
from scipy import stats 
from sklearn import preprocessing 
#sửa lỗi
from sklearn.preprocessing import StandardScaler
from sklearn.feature_selection import SelectKBest, chi2 
df = pd.read_csv('./29ndh_weatherAUS.csv') 
print('Độ lớn của bảng [frame] dữ liệu thời tiết:',df.shape) 
print(df[0:5])
print(df.count().sort_values())
df=df.drop(columns=['Sunshine','Evaporation','Cloud3pm','Cloud9am','Location','Date','RISK_MM'],axis=1) 
print(df.shape)
df = df.dropna(how='any')
print(df.shape) 
z = np.abs(stats.zscore(df._get_numeric_data()))
#ADAPTING TO THE ISO 3166 STANDARD
print('MA TRAN Z-SCORE\n')
print(z) # in ra tập (ma trận) các giá trị z-score từ tập dữ liệu gốc
df= df[(z < 3).all(axis=1)] #z-score < 3 # {loại các giá trị >= 3} vì các giá trị z-score >=3 tướng ứng với số liệu quá khác biệt so với các số liệu còn lại (“cá biệt” = “ngoại lệ” = isolated}
print(df.shape) # xác định số dòng & cột dữ liệu sau khu xử lý các giá trị cá biệt
df['RainToday'].replace({'KHONG': 'No', 'CO': 'Yes'},inplace = True)
df['RainTomorrow'].replace({'KHONG': 'No', 'CO': 'Yes'},inplace = True)
scaler = preprocessing.MinMaxScaler()
print(df.shape)
