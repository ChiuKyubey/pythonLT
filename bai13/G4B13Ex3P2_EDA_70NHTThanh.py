from tkinter import messagebox
import numpy as np
import pandas as pd
import tkinter as tk
from tkinter import ttk
from scipy import stats
from sklearn import preprocessing
from sklearn.feature_selection import SelectKBest, chi2, f_classif
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split

win_70thanh = tk.Tk()
win_70thanh.geometry('1600x750')
win_70thanh.title("70 _ Nguyễn Hồ Thiên Thanh")
win_70thanh.resizable(tk.FALSE, tk.FALSE)
tthanh_70 = pd.read_csv('D:/LTPython/G470NHTThanh_DAHP.PyPro_CarPrices/G470NHTThanh_CarPrices.csv')
thanh = tthanh_70.copy()
def Output():
    thienthanh_70 = pd.read_csv('D:/LTPython/G470NHTThanh_DAHP.PyPro_CarPrices/G470NHTThanh_CarPrices.csv')

    selected_step_70thanh = steps.get()
    
    if selected_step_70thanh == 'Xử lý cột':
        output_text.delete('1.0', tk.END)
        thanh_70 = thanh.drop(columns =['name','seller_type', 'transmission', 'owner'])
        output_text.insert(tk.END, thanh_70)
        
    elif selected_step_70thanh == 'Xử lý dòng':
        output_text.delete('1.0', tk.END)
        thanh_70  =  thanh.dropna(how = 'any')
        output_text.insert(tk.END, thanh_70)
        
    elif selected_step_70thanh == 'Xử lý cá biệt':
        output_text.delete('1.0', tk.END)
        z = np.abs(stats.zscore(thanh._get_numeric_data()))
        thanh_70 = thanh[(z<3).all(axis=1)]
        output_text.insert(tk.END, "MA TRAN Z-SCORE:\n")
        output_text.insert(tk.END, str(z) + "\n")
        
    elif selected_step_70thanh == 'Thay thế giá trị':
        output_text.delete('1.0', tk.END)
        thanh['owner'].replace({'First Owner': '1', 'Second Owner' :'2', 'Third Owner':'3', 'Fourth & Above Owner':'4', 'Test Drive Car':'5'}, inplace =True)
        output_text.insert(tk.END, thanh.to_string(index = False, header =True))
        
    elif selected_step_70thanh == 'Chuẩn hóa dữ liệu':
        output_text.delete('1.0', tk.END)
        select_cols=['year', 'selling_price', 'km_driven']
        data_selected=thienthanh_70.loc[:,select_cols]   
        output_text.insert(tk.END,"Các cột được chọn để chuẩn hóa dữ liệu: \n")
        output_text.insert(tk.END,data_selected) 
        scaler = preprocessing.MinMaxScaler()
        scaler.fit(data_selected)
        thienthanh_70 = pd.DataFrame(scaler.transform(data_selected), index=data_selected.index, columns=data_selected.columns)  
        output_text.insert(tk.END,"\n")
        output_text.insert(tk.END,data_selected.iloc[4:10]) 
        output_text.insert(tk.END,"\n") 
        
def FeatureSelection():
    selected = method.get()
    num_k = int(k.get())
    if selected == 'Chi2':
        output_text.delete('1.0', tk.END)
        tthanh_70['owner'].replace({'First Owner': '1', 'Second Owner' :'2', 'Third Owner':'3', 'Fourth & Above Owner':'4', 'Test Drive Car':'5'}, inplace =True)
        thienthanh = tthanh_70[['year','selling_price', 'km_driven','owner']]
        a = thienthanh.loc[:, thienthanh.columns != 'selling_price']
        b = thienthanh[['selling_price']]
        selector = SelectKBest(chi2, k = num_k)
        selector.fit(a,b)
        a_new = selector.transform(a)
        selected_columns = a.columns[selector.get_support(indices = True)]
        output_text.insert('end', 'Các đặc trưng quan trọng: \n' )
        for col in selected_columns:
            output_text.insert('end', '-{}\n'.format(col))
        output_text.insert(tk.END, str(a_new))
        output_text.insert(tk.END, "\n")
        
    elif selected == 'f_classif':
        output_text.delete('1.0', tk.END)
        tthanh_70['owner'].replace({'First Owner': '1', 'Second Owner' :'2', 'Third Owner':'3', 'Fourth & Above Owner':'4', 'Test Drive Car':'5'}, inplace =True)
        thienthanh = tthanh_70[['year','selling_price', 'km_driven','owner']]
        a = thienthanh.loc[:, thienthanh.columns != 'selling_price']
        b = thienthanh['selling_price'].ravel()
        selector = SelectKBest(f_classif, k = num_k)
        selector.fit(a,b)
        a_new = selector.transform(a)
        selected_columns = a.columns[selector.get_support(indices=True)]
        output_text.insert('end', 'Các đặc trưng quan trọng: \n' )
        for col in selected_columns:
            output_text.insert('end', '-{}\n'.format(col))
        output_text.insert(tk.END, str(a_new))
        output_text.insert(tk.END, "\n")
        
def RMSE(selected_colnames):
    nhtthanh_70 = pd.read_csv('D:/LTPython/G470NHTThanh_DAHP.PyPro_CarPrices/G470NHTThanh_CarPrices.csv')
    nhtthanh_70['fuel'] = nhtthanh_70['fuel'].astype('category')
    nhtthanh_70['transmission'] = nhtthanh_70['transmission'].astype('category')
    nhtthanh_70['owner'] = nhtthanh_70['owner'].astype('category')
    nhtthanh_70['seller_type'] = nhtthanh_70['seller_type'].astype('category')

    nhtthanh_70 = pd.get_dummies(nhtthanh_70, columns=['fuel', 'transmission','owner','seller_type'])
    for col_name in selected_colnames:   
        if col_name == 'year':
            X = ['year']
        elif col_name =='km_driven':
            X = ['km_driven']
        elif col_name== 'fuel':
            X = ['fuel_Diesel', 'fuel_Electric', 'fuel_LPG', 'fuel_Petrol', 'fuel_CNG']   
        elif col_name == 'owner':
            X = ['owner_Test Drive Car', 'owner_First Owner', 'owner_Fourth & Above Owner', 'owner_Second Owner','owner_Third Owner'] 
        elif col_name == 'transmission':
            X = ['transmission_Automatic', 'transmission_Manual']
        elif col_name =='seller_type':
            X =['seller_type_Dealer','seller_type_Individual']
        else:
            raise ValueError("Invalid column name(s) passed. Please make sure to pass the correct column name(s).")

        X_data = nhtthanh_70[X]
        y_data = nhtthanh_70['selling_price'].astype('int')
        
        
        X_train, X_test, y_train, y_test = train_test_split(X_data, y_data, test_size=0.1, random_state=42)

        X_test = X_test.dropna()

        rmse_list = []
        regressor = LinearRegression()
        regressor.fit(X_train, y_train)
        
        output_text.delete('1.0', tk.END)
        
        feature_names = X_train.columns
        X_test = X_test[feature_names]
        for index, row in X_test.iterrows():
            sample = np.array(row).reshape(1,-1) 
            y_pred = regressor.predict(sample)
            rmse = mean_squared_error([y_test[index]], [y_pred], squared=False)
            rmse_list.append(int(rmse))
        X_test = X_test.sort_index()
        X_test['RMSE'] = rmse_list 
        output_text.insert(tk.END, X_test)


def Calculate_RMSE():
    selected_indices = listbox.curselection()
    selected_colnames = [listbox.get(i) for i in selected_indices]
    
    if len(selected_colnames) == 0:
        messagebox.showerror("Error", "Please select at least one column to calculate RMSE.")
        return
    
    selected_columns['column'] = selected_colnames
    
    RMSE(selected_colnames)     
    
        
steps_label = tk.Label(win_70thanh, text='Select preprocessing steps:')
steps_label.place( x = 1275, y = 50)
steps_list = ['Xử lý cột', 'Xử lý dòng', 'Xử lý cá biệt', 'Thay thế giá trị', 'Chuẩn hóa dữ liệu']
steps = ttk.Combobox(win_70thanh, values=steps_list, state='readonly')
steps.place(x = 1275 ,y =80)
steps.current(0)

output_button = tk.Button(win_70thanh, text='Output data after preprocessing', command=Output)
output_button.place(x= 1280 , y = 110)

output_text = tk.Text(win_70thanh, bg="azure", fg='brown', height=35, width=125)
output_text.place(x = 5, y =20)
output_text.tag_configure("left", justify='left')

scrollbar = tk.Scrollbar(win_70thanh, command= output_text.xview)
scrollbar.pack(side = tk.RIGHT, fill = tk.X)
output_text.config(xscrollcommand=scrollbar.set)


method_label = tk.Label(win_70thanh, text='Select method:')
method_label.place( x = 1275, y = 150)
method_list = ['Chi2' , 'f_classif']
method = ttk.Combobox(win_70thanh, values=method_list, state='readonly')
method.place(x = 1275 ,y = 180)
method.current(0)

k_label = tk.Label(win_70thanh, text = "Choose the k (k<=3): ")
k_label.place (x = 1280, y= 210)
k = tk.Entry(win_70thanh, width=10)
k.place(x = 1280, y= 240)


method_button = tk.Button(win_70thanh, text='Output data after feature selection', command= FeatureSelection)
method_button.place(x= 1280 , y = 270)

feature_selection = tk.Button(win_70thanh, text= 'Feature Selection', command= Calculate_RMSE)
feature_selection.place(x = 1280, y = 500 )

selected_columns = pd.DataFrame(columns=['column'])

listbox_label  = tk.Label(win_70thanh, text="Select columns to calculate RMSE:")
listbox_label.place(x=1280 ,y = 340)
listbox = tk.Listbox(win_70thanh, selectmode=tk.MULTIPLE, width=30, height=5)
listbox.place(x = 1280, y =370)
listbox.insert(tk.END, "year")
listbox.insert(tk.END, 'seller_type')
listbox.insert(tk.END, 'transmission')
listbox.insert(tk.END, 'owner')
listbox.insert(tk.END, 'km_driven')
win_70thanh.mainloop()
