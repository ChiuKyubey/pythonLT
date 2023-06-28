import numpy as np #Numeric Python: Thư viện về Đại số tuyến tính tính
import pandas as pd #Python Analytic on Data System: For data processing (Thư viện xử lý dữ liệu)
from scipy import stats # thư viện cung cấp các công cụ thống kê [statistics] sub-lib của science python [các công cụ khoa học]
from sklearn import preprocessing # Thư viện tiền xử lý DL (XL ngoại lệ: Isolated)
from sklearn.feature_selection import SelectKBest, chi2 # Nạp hàm Thư viện phân tích dữ liệu thăm 
from sklearn.preprocessing import StandardScaler
df = pd.read_csv('./CO2_Emissions.csv')
print ('Độ lớn của bảng [frame]: ', df.shape)
print (df[0:5])
# GIAI ĐOẠN 2: TIỀN XỬ LÝ (PRE-PROCESSING)
# Bước 3: Xử lý CỘT dữ liệu NULL quá nhiều OR không có giá trị phân tích
print(df.count().sort_values())
df = df.drop(columns=['Country Name'],axis=1)
print(df.shape) 

# Bước 4: Xử lý DÒNG dữ liệu NULL
# 30 dòng bôi vàng
# Timor không bị xóa
df = df.dropna(how='any')
print(df.shape) # kiểm tra lại số lượng cột & dòng của df sau khi XL NULL các dòng DL
# Bước 5: Xử lý loại bỏ các giá trị ngoại lệ (cá biệt): isolated
#nhỏ nhất 0, lớn nhất 50
z = np.abs(stats.zscore(df._get_numeric_data())) # Dò tìm và lấy các giá trị cá biệt trong tập dữ liệu gốc thông qua điểm z (z_score)
print('MA TRAN Z-SCORE\n')
print(z) 
df= df[(z > 0.0001 ).all(axis=1)]
print(df.shape)
print (df[190:200])
scaler = preprocessing.MinMaxScaler()
scaler.fit(df)
df = pd.DataFrame(scaler.transform(df), index=df.index, columns=df.columns) 
df.iloc[4:10]
print(df)

