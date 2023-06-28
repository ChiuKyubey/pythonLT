# Voice
import speech_recognition as sr
from gtts import gTTS
import playsound

# thư viện cần thiết EDA
import numpy as np  # thư viện về đại số tuyến tính
import pandas as pd  # thư viện xử lý 
from sklearn import preprocessing  # thư viện tiền xử lý 
from scipy import stats  # thư viện cung cấp công cụ thống kê
from sklearn.preprocessing import Binarizer
from sklearn.feature_selection import SelectKBest, chi2 
from sklearn.linear_model import LinearRegression #sử dụng hồi quy tuyến tính 

# tkinter
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog

# Thư viện thời gian thực
from datetime import datetime
# Thư viện vẽ đồ thị
import matplotlib.pyplot as plt
# Thư viện chạy các file bên ngoài
import subprocess
# thư viện os
import os
import time 

#thư viện game
import subprocess
#================================================================
#tạo của sổ
master = tk.Tk()
master.geometry('1500x800')
master.title("29_Nguyễn Diệu Hương_21110489")
master.pack_propagate()
master.resizable(tk.FALSE, tk.FALSE)
def VoiceAssistant():
    vlenh=" "
    label=tk.Label(foot,text=vlenh)
    label.place(x=800, y=20)
    label.destroy()
    r = sr.Recognizer()
    with sr.Microphone() as Source:
        messagebox.showinfo("Cảnh báo", "Hiệu chỉnh nhiễu trước khi nói!")
        r.adjust_for_ambient_noise(Source, duration=1)
        messagebox.showinfo("Sẵn sàng", "Bấm OK để bắt đầu nói tiếng Việt trong 3 giây")
        audio_data = r.record(Source, duration=3)
        try:
            vlenh = r.recognize_google(audio_data, language="vi")

            messagebox.showinfo("Bạn đã nói: ", vlenh)
        except:
            vlenh = "Bạn nói gì tôi nghe không hiểu!"
        label=tk.Label(foot,text=vlenh)
        label.place(x=800, y=20)
        ten = gTTS(text=vlenh, lang='vi')
        # Xuất ra lời nói theo văn bản đã nhập
        filename =os.path.abspath('')+'\huong29.mp3'
        ten.save(filename)
    
def Open():
    global data_origin, data_preprocessed, current_dataset
    btnProcessEDA['state'] = tk.ACTIVE
    btnAnalyze['state'] = tk.DISABLED
    btnChooseAttribute['state'] = tk.DISABLED
    btnExportCSV['state'] = tk.ACTIVE
    btnPredict['state'] = tk.DISABLED

    filename = filedialog.askopenfilename(
        title="Chọn file csv", initialdir='./', filetypes=(("CSV Files", "*.csv"),))
    data_origin = pd.read_csv(filename)
    current_dataset = data_origin
    # Hiển thị tập dữ liệu gốc
    ShowData(data_origin)
    print(data_origin.count().sort_values())

def Close():
    result = messagebox.askokcancel('Thoát', 'Bạn có muốn thoát không?', )
    if result:
        master.destroy()

def ProcessEDA():
    # Hiển thị các nút chức năng sau khi tiền xử lý
    btnChooseAttribute['state'] = tk.ACTIVE
    btnAnalyze['state'] = tk.ACTIVE
    btnExportCSV['state'] = tk.ACTIVE

    global data_preprocessed, current_dataset
    PreProcessing()
    ClearFrame()
    # Hiển thị tập dữ liệu đã được tiền xử lý
    current_dataset = data_preprocessed
    ShowData(data_preprocessed)

def PreProcessing():
    global data_origin, data_preprocessed
    data_preprocessed = data_origin

    # Bước 3: Xử lý cột null
    print(data_preprocessed.count().sort_values())
    # Tất cả các cột đều có 205 giá trị ==> Không có cột nào có dữ liệu null

    # Bước 4: Xử lý dòng null
    # Xóa các cột không cần thiết cho việc xử lý dữ liệu

    data_preprocessed = data_preprocessed.dropna(how='any')
    thirdcol = data_preprocessed.shape[1]/3
    for idx, row in data_preprocessed.iterrows():
        num_zeroes = (row == 0).sum()
        if num_zeroes > thirdcol:
            data_preprocessed = data_preprocessed.drop(idx, axis=0)

    # Bước 5: Loại bỏ các giá trị ngoại lệ isolated
    cols = data_preprocessed.columns[(data_preprocessed.columns != '2019') & (
        data_preprocessed.columns != 'Country Name') & (data_preprocessed.columns != 'ID_Name')]
    z = np.abs(stats.zscore(data_preprocessed[cols]._get_numeric_data()))
    zscoreGraph(data_preprocessed, z)
    data_preprocessed[cols] = (data_preprocessed[cols])[(z <3).all(axis=1)]
    data_preprocessed = data_preprocessed.dropna(how='any')

    # Bước 6: Thay thế các giá trị 0 và 1 bởi YES và NO
    #thêm một cột dự đoán 2019
    data_preprocessed['2019'] = 0

    # Bước 7: Rời rạc hóa dùng MinMaxScaler
    scaler = preprocessing.MinMaxScaler()
    scaler.fit(data_preprocessed[cols])
    data_preprocessed[cols] = pd.DataFrame(scaler.transform(
        data_preprocessed[cols]), index=data_preprocessed.index, columns=cols)

    # Bước 8: Xác định mô hình trích lọc các thuộc tính đặc trưng EDA
    
    X = data_preprocessed.loc[:, (data_preprocessed.columns != '2018') & (data_preprocessed.columns != '2019') & (
        data_preprocessed.columns != 'Country Name') & (data_preprocessed.columns != 'ID_Name')]
    y = data_preprocessed[['2019']]
    binarizer = Binarizer(threshold=0.5)
    y = binarizer.fit_transform(y)

    selector = SelectKBest(chi2, k=3)
    selector.fit(X, y)
    X_new = selector.transform(X)

    print(X.columns[selector.get_support(indices=True)])

def ChooseAttribute():
    global data_preprocessed
    # Hiển thị cửa sổ mới
    chooseAtr_form = tk.Toplevel()
    chooseAtr_form.geometry('560x470')
    chooseAtr_form.resizable(tk.FALSE, tk.FALSE)
    chooseAtr_form.title("Chọn thuộc tính")
    chooseAtr_form.focus()
    chooseAtr_form = chooseAtr_form

    tk.Label(chooseAtr_form, text='Phân tích').place(x=90, y=15)
    listbox1 = tk.Listbox(chooseAtr_form, height=25, width=40,
                          font="Consolas 8", selectmode=tk.EXTENDED)
    listbox1.place(x=15, y=45)
    tk.Label(chooseAtr_form, text='Không phân tích').place(x=370, y=15)
    listbox2 = tk.Listbox(chooseAtr_form, height=25, width=40,
                          font="Consolas 8", selectmode=tk.EXTENDED)
    listbox2.place(x=300, y=45)
    tk.Label(chooseAtr_form, text="Số lượng").place(x=15, y=420)
    lblSoLuong = tk.Label(chooseAtr_form, relief=tk.SUNKEN, font="Times 8",
                          borderwidth=3, width=15, height=1)
    lblSoLuong.place(x=80, y=420)

    tk.Button(chooseAtr_form, text='OK', width=12, height=2,
              command=lambda: DropColumns(list(listbox2.get(0, tk.END)), data_preprocessed, chooseAtr_form)).place(x=450, y=410)

    columns = data_preprocessed.columns
    for col in columns:
        listbox1.insert(tk.END, col)
    lblSoLuong.configure(text=listbox1.size())

    # Các nút chức năng
    btnMoveRight = tk.Button(chooseAtr_form, text=">",
                             width=4, command=lambda: MoveToRight(listbox1, listbox2, lblSoLuong))
    btnMoveRight.place(x=260, y=70)
    btnMoveLeft = tk.Button(chooseAtr_form, text="<",
                            width=4, command=lambda: MoveToLeft(listbox1, listbox2, lblSoLuong))
    btnMoveLeft.place(x=260, y=110)
    btnMoveAllRight = tk.Button(
        chooseAtr_form, text=">>", width=4, command=lambda: MoveAllToRight(listbox1, listbox2, lblSoLuong))
    btnMoveAllRight.place(x=260, y=150)
    btnMoveAllLeft = tk.Button(
        chooseAtr_form, text="<<", width=4, command=lambda: MoveAllToLeft(listbox1, listbox2, lblSoLuong))
    btnMoveAllLeft.place(x=260, y=190)
    btnDeleteAll = tk.Button(chooseAtr_form, text='X', width=4,
                             command=lambda: DeleteAll(listbox1, listbox2, lblSoLuong))
    btnDeleteAll.place(x=260, y=230)
    
def Analyze():
    # Bước 9: Xác định mô hình trích lọc các thuộc tính đặc trưng
    global data_preprocessed, data_analyzed, current_dataset
    data_newa = pd.DataFrame()
    data_newa['TB theo z'] = data_preprocessed.select_dtypes(include='number').drop(columns='2019').mean(axis=1)
    data_newb = data_preprocessed[['ID_Name', 'Country Name', '2018']]
    data_analyzed=pd.concat([data_newb, data_newa], axis=1)
    current_dataset = data_analyzed
    ShowData(data_analyzed)
    data_preprocessed['2019']=data_newa['TB theo z']
    btnPredict['state'] = tk.ACTIVE

def Predict():
    # Chọn các cột quốc gia và số liệu từ 1990 đến 2018
    data_newa = data_preprocessed[['Country Name']]
    data_newb = data_preprocessed.select_dtypes(include='number')
    data_train = pd.concat([data_newa, data_newb], axis=1)

    # Tạo DataFrame chứa dữ liệu dự đoán cho năm 2019
    data_predict = pd.DataFrame(columns=['Country Name', '2019'])

    # Duyệt qua từng quốc gia trong DataFrame
    for index, row in data_train.iterrows():
        country = row['Country Name']
        x_train = row.drop('Country Name').values.reshape(-1, 1)
        y_train = row['2018']
        # Kiểm tra xem có đủ dữ liệu để huấn luyện mô hình hay không
        if not isinstance(y_train, float):
            # Xây dựng mô hình hồi quy tuyến tính
            model = LinearRegression()
            model.fit(x_train, y_train)
            
            # Dự đoán số liệu cho năm 2019
            x_predict = [[2019]]
            y_predict = model.predict(x_predict)
            
            # Thêm dữ liệu dự đoán vào DataFrame
            data_predict.loc[index] = [country, y_predict[0]]

    ShowData(data_predict)

def ClearFrame():
    for widget in body.winfo_children():
        widget.destroy()

trv = None
def ShowData(df):
    global trv
    ClearFrame()

    r_set = df.to_numpy().tolist()
    l1 = list(df)

    # Tạo khung cảnh
    frame = ttk.Frame(body)
    frame.grid(row=4, column=1, columnspan=3, padx=10, pady=20)

    # Tạo thanh cuộn dọc
    scrollbar_y = ttk.Scrollbar(frame)
    scrollbar_y.pack(side=tk.LEFT, fill=tk.Y)

    # Tạo thanh cuộn ngang
    scrollbar_x = ttk.Scrollbar(frame, orient=tk.HORIZONTAL)
    scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)

    # Tạo Treeview với thanh cuộn
    trv = ttk.Treeview(frame, selectmode='browse',
                       height=28, show='headings', columns=l1,
                       yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
    trv.pack(side=tk.LEFT, fill=tk.BOTH)
    scrollbar_y.config(command=trv.yview)
    scrollbar_x.config(command=trv.xview)

    for i in l1:
        trv.column(i, width=90, anchor='c')
        trv.heading(i, text=str(i))
    for dt in r_set:
        v = [r for r in dt]
        item_id = v[0]
    # Kiểm tra xem mục đã tồn tại trong cây danh sách hay chưa
        if not trv.exists(item_id):
            trv.insert("", 'end', iid=item_id, values=v)
    lblShape.configure(text=str(df.shape[0]) + 'x' + str(df.shape[1]))

def MoveToRight(listbox1, listbox2, lblSoLuong):
    i = 0
    selection = listbox1.curselection()
    for i in reversed(selection):
        listbox2.insert(tk.END, listbox1.get(i))
        listbox1.delete(i)
    dem = listbox1.size()
    lblSoLuong.configure(text=dem)

def MoveToLeft(listbox1, listbox2, lblSoLuong):
    i = 0
    selection = listbox2.curselection()
    for i in reversed(selection):
        listbox1.insert(tk.END, listbox2.get(i))
        listbox2.delete(i)
    dem = listbox1.size()
    lblSoLuong.configure(text=dem)

def MoveAllToRight(listbox1, listbox2, lblSoLuong):
    while listbox1.size() != 0:
        listbox2.insert(tk.END, listbox1.get(listbox1.size()-1))
        listbox1.delete(listbox1.size()-1)
    lblSoLuong.configure(text=0)

def MoveAllToLeft(listbox1, listbox2, lblSoLuong):
    while listbox2.size() != 0:
        listbox1.insert(tk.END, listbox2.get(listbox2.size()-1))
        listbox2.delete(listbox2.size()-1)
    lblSoLuong.configure(text=listbox1.size())

def DeleteAll(listbox1, listbox2, lblSoLuong):
    listbox1.delete(0, tk.END)
    listbox2.delete(0, tk.END)
    global data_preprocessed
    columns = data_preprocessed.columns
    for col in columns:
        listbox1.insert(tk.END, col)
    lblSoLuong.configure(text=listbox1.size())

def DropColumns(columns, data, chooseAtr_form):
    if len(columns) == len(data.columns):
        messagebox.showwarning("Thông báo", "Phải chọn ít nhất 1 thuộc tính")
        chooseAtr_form.focus()
        return
    if 'Country Name' in columns or '2018' in columns or '2019' in columns or 'ID_Name' in columns:
        messagebox.showwarning(
            "Thông báo", "Không chọn ID_Name, Country, 2018, 2019 ")
        chooseAtr_form.focus()
        return
    data.drop(columns=columns, inplace=True, axis=1)
    chooseAtr_form.destroy()
    ShowData(data)
    messagebox.showinfo("Thông báo", "Đã drop thành công " +str(len(columns)) + " thuộc tính!")

def zscoreGraph(data, z):
    x = data['ID_Name'].values.tolist()
    numberCol = z.select_dtypes(include='number')
    y = numberCol.mean(axis=1).values.tolist()
    plt.plot(x, y)
    plt.title('Đồ thị z-score')
    plt.axhline(y=3, color='#FF5677', linestyle='-')
    plt.xlabel('ID')
    plt.ylabel('z-score')
    plt.show()

def ExportCSV():
    global current_dataset
    # Tạo thư mục nếu không tồn tại
    os.makedirs('./CSV29_Folder', exist_ok=True)
    try:
        current_time = datetime.now().strftime("%d%m%Y")
        path = f'./CSV29_Folder/Processed_CO2Emission_{current_time}.csv'
        current_dataset.to_csv(path)
        messagebox.showinfo('Thông báo', 'Xuất file CSV thành công!')
    except FileNotFoundError:
        messagebox.showerror('Thông báo', 'Không tìm thấy đường dẫn hoặc tên tệp!')
    except PermissionError:
        messagebox.showerror('Thông báo', 'Không có quyền ghi file!')
    except Exception as e:
        messagebox.showerror('Thông báo', f'Lỗi xuất file CSV: {str(e)}')
        
def Game():
    subprocess.run(['python', 'G329Huong_Game.py'])

#tạo frame
#head
head = tk.Frame(master,bg='#6096B4',  width=1400, height=70, relief=tk.SUNKEN, borderwidth=2)
head.pack()
head_label = tk.Label(head, text="29_21110489: Đồ Án Học Phần: CO2 Emissions", bg='#6096B4', fg="white",font=("Arial", 20 ,"bold"))
head_label.place(x=(1400-600)//2, y=(70-30)//2)

#foot
foot = tk.Frame(master, bg='#93BFCF', width=1400, height=70,  relief=tk.SUNKEN, borderwidth=1)
foot.pack()

btnOpen = tk.Button(foot, text='1.Mở Tệp', width=12, height=2, command=Open)
btnOpen.place(x=20, y=15)

btnProcessEDA = tk.Button(foot, text='2.Tiền Xử Lý', width=12, height=2, state=tk.DISABLED, command=ProcessEDA)
btnProcessEDA.place(x=120, y=15)

btnChooseAttribute = tk.Button(foot, text='3.Chọn Thuộc Tính', width=15, height=2, state=tk.DISABLED, command=ChooseAttribute)
btnChooseAttribute.place(x=220, y=15)

btnAnalyze = tk.Button(foot, text='4.Phân Tích', width=12, height=2, state=tk.DISABLED, command=Analyze)
btnAnalyze.place(x=340, y=15)

btnPredict = tk.Button(foot, text='5.Dự Đoán năm 2019', width=15, height=2, state=tk.DISABLED, command=Predict)
btnPredict.place(x=440, y=15)

btnExportCSV = tk.Button(foot, text='6.Xuất File CSV', width=15, height=2, state=tk.DISABLED, command=ExportCSV)
btnExportCSV.place(x=560, y=15)

lblShape = tk.Label(master, text='0x0', width=10, font=('arial 9'), height=1, relief=tk.SUNKEN)
lblShape.place(x=1350, y=100)

btnVoiceAssistant = tk.Button(foot, text='7.Nói', width=12, height=2, command=VoiceAssistant)
btnVoiceAssistant.place(x=680, y=15)

btnGame = tk.Button(foot, text='8.Game', width=12, height=2, command=Game)
btnGame.place(x=1100, y=15)

btnClose = tk.Button(foot, text='9.Thoát', width=10, height=2, command=Close)
btnClose.place(x=1200, y=15)

#body
body = tk.Frame(master, bg='#F7F5EB', width=1400, height=650, relief=tk.SUNKEN, borderwidth=2)
body.pack()
body.grid_propagate(False)
body = body

#==========================================================================
master.mainloop()
