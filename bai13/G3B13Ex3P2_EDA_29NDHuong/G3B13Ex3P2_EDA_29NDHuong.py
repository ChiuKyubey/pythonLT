from tkinter import messagebox
import numpy as np
import pandas as pd
import tkinter as tk
from tkinter import ttk
from scipy import stats
from sklearn.preprocessing import StandardScaler
from sklearn.feature_selection import SelectKBest, chi2, f_classif
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split

master = tk.Tk()
master.geometry('1500x800')
master.title("29_Nguyễn Diệu Hương")
master.resizable(tk.FALSE, tk.FALSE)
df0 = pd.read_csv('./CO2_Emissions.csv')
df = df0.copy()
def Output():
    df_29 = pd.read_csv('./CO2_Emissions.csv')
    selected_step = steps.get()
    
    if selected_step == 'Xử lý cột':
        output_text.delete('1.0', tk.END)
        df_29 = df.drop(columns=['Country Name'],axis=1)
        output_text.insert(tk.END, df_29)
        
    elif selected_step == 'Xử lý dòng':
        output_text.delete('1.0', tk.END)
        df_29  =  df.dropna(how = 'any')
        output_text.insert(tk.END, df_29)
        
    elif selected_step == 'Xử lý cá biệt':
        output_text.delete('1.0', tk.END)
        z = np.abs(stats.zscore(df._get_numeric_data()))
        df_29 = df[(z > 0.0001 ).all(axis=1)]
        output_text.insert(tk.END, "MA TRAN Z-SCORE:\n")
        output_text.insert(tk.END, str(z) + "\n")
        
    elif selected_step == 'Chuẩn hóa dữ liệu':
        output_text.delete('1.0', tk.END)
        select_cols=df_29.columns.tolist()
        data_selected=df_29.loc[:,select_cols]   
        output_text.insert(tk.END,"Các cột được chọn để chuẩn hóa dữ liệu: \n")
        output_text.insert(tk.END,data_selected) 
        scaler = preprocessing.MinMaxScaler()
        scaler.fit(data_selected)
        df_29 = pd.DataFrame(scaler.transform(data_selected), index=data_selected.index, columns=data_selected.columns)  
        output_text.insert(tk.END,"\n")
        output_text.insert(tk.END,data_selected.iloc[4:10]) 
        output_text.insert(tk.END,"\n") 

def FeatureSelection():
    selected = method.get()
    num_k = int(k.get())
    if selected == 'Chi2':
        output_text.delete('1.0', tk.END)
        
        a = df0.loc[:, df0.columns != 'Country Name']
        b = df0[['2018']]
        selector = SelectKBest(chi2, k = num_k)
        selector.fit(a,b)
        a_new = selector.transform(a)
        selected_columns = a.columns[selector.get_support(indices = True)]
        output_text.insert('end', 'Các đặc trưng quan trọng: \n' )
        for col in selected_columns:
            output_text.insert('end', '-{}\n'.format(col))
        output_text.insert(tk.END, str(a_new))
        output_text.insert(tk.END, "\n")
        
def B9(selected_colnames):
    df_29 = pd.read_csv('./CO2_Emissions.csv')
    df_29 = df[:, :]

   
        
steps_label = tk.Label(master, text='Select preprocessing steps:')
steps_label.place( x = 1275, y = 50)
steps_list = ['Xử lý cột', 'Xử lý dòng', 'Xử lý cá biệt', 'Thay thế giá trị', 'Chuẩn hóa dữ liệu']
steps = ttk.Combobox(master, values=steps_list, state='readonly')
steps.place(x = 1275 ,y =80)
steps.current(0)

output_button = tk.Button(master, text='Output data after preprocessing', command=Output, bg="black", fg="white")
output_button.place(x= 1280 , y = 110)

output_text = tk.Text(master, bg="#B9FFFC",  height=45, width=150)
output_text.place(x = 5, y =20)
output_text.tag_configure("left", justify='left')

scrollbar = tk.Scrollbar(master, command= output_text.xview)
scrollbar.pack(side = tk.RIGHT, fill = tk.X)
output_text.config(xscrollcommand=scrollbar.set)


method_label = tk.Label(master, text='Select method:')
method_label.place( x = 1275, y = 150)
method_list = ['Chi2' , 'f_classif']
method = ttk.Combobox(master, values=method_list, state='readonly')
method.place(x = 1275 ,y = 180)
method.current(0)

k_label = tk.Label(master, text = "Choose the k: ")
k_label.place (x = 1280, y= 210)
k = tk.Entry(master, width=10)
k.place(x = 1280, y= 240)

method_button = tk.Button(master, text='Output data after feature selection',  bg="black", fg="white")
method_button.place(x= 1280 , y = 270)



selected_columns = pd.DataFrame(columns=['column'])

master.mainloop()