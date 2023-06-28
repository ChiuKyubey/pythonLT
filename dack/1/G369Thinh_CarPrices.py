# Bước 1: Nạp thư viện
# speech
import speech_recognition as sr
from gtts import gTTS
import playsound

# tkinter
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog

# thư viện os
import os

# thư viện cần thiết EDA
import numpy as np  # thư viện về đại số tuyến tính
import pandas as pd  # thư viện xử lý dữ liệu
from scipy import stats  # thư viện cung cấp công cụ thống kê
from sklearn import preprocessing  # thư viện tiền xử lý dữ liệu
from sklearn.preprocessing import Binarizer

# Thư viện phân tích dữ liệu thăm dò
from sklearn.feature_selection import SelectKBest, chi2

# Thư viện thời gian thực
from datetime import datetime

# Thư viện vẽ đồ thị
import matplotlib.pyplot as plt

# Thư viện chạy các file bên ngoài
import subprocess

# Bước 2: Khai báo tên thư mục & File lưu thông tin bài làm
thinh69_FILE = os.path.abspath('') + '\\' + 'thinh69.mp3'  # lưu tên file input

# Các hàm thực hiện chức năng


def VoiceAssistant():
    r = sr.Recognizer()
    with sr.Microphone() as Source:
        messagebox.showinfo("Nhắc nhở", "Hiệu chỉnh nhiễu trước khi nói!")
        r.adjust_for_ambient_noise(Source, duration=1)
        messagebox.showinfo(
            "Sẵn sàng", "Bấm OK để bắt đầu nói tiếng Việt trong 3 giây")
        audio_data = r.record(Source, duration=3)
        try:
            vlenh = r.recognize_google(audio_data, language="vi")
        except:
            vlenh = "Tôi không nghe rõ!"
        vText = gTTS(text=vlenh, lang='vi')
        # Xuất ra lời nói theo văn bản đã nhập
        vText.save(thinh69_FILE)
        tk.Label(mid_frame, text=vlenh).place(x=20, y=20)
        playsound.playsound(thinh69_FILE)


def LoadOriginData():
    global data_origin, data_preprocessed, current_dataset
    btnProcessEDA['state'] = tk.ACTIVE
    btnAnalyze['state'] = tk.DISABLED
    btnChooseAttribute['state'] = tk.DISABLED
    btnExportCSV['state'] = tk.DISABLED
    btnPredictPrice['state'] = tk.DISABLED

    filename = filedialog.askopenfilename(
        title="Chọn file csv", initialdir='./', filetypes=(("CSV Files", "*.csv"),))
    data_origin = pd.read_csv(filename)
    current_dataset = data_origin
    # Hiển thị tập dữ liệu gốc
    ShowCSVData(data_origin)
    print(data_origin.count().sort_values())


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
    ShowCSVData(data_preprocessed)


def CloseWindow():
    result = messagebox.askokcancel('Thoát', 'Bạn có muốn thoát không?', )
    if result:
        root_69thinh.destroy()


def PreProcessing():

    global data_origin, data_preprocessed
    data_preprocessed = data_origin

    # Bước 3: Xử lý cột null
    print(data_preprocessed.count().sort_values())
    # Tất cả các cột đều có 205 giá trị ==> Không có cột nào có dữ liệu null

    # Bước 4: Xử lý dòng null
    data_preprocessed = data_preprocessed.dropna(how='any')

    # Xóa các cột không cần thiết cho việc xử lý dữ liệu
    data_preprocessed = data_preprocessed.drop(columns=['aspiration', 'symboling', 'doornumber', 'fueltype',
                                                        'carbody', 'drivewheel', 'enginelocation', 'enginetype', 'fuelsystem'])

    # Đổi cylinderNumber từ string sang số
    data_preprocessed.cylindernumber = data_preprocessed.cylindernumber.str.lower()
    for _, numberText in enumerate(data_preprocessed.cylindernumber.unique()):
        if numberText == 'two':
            data_preprocessed.cylindernumber.replace('two', 2, inplace=True)
        if numberText == 'three':
            data_preprocessed.cylindernumber.replace('three', 3, inplace=True)
        if numberText == 'four':
            data_preprocessed.cylindernumber.replace('four', 4, inplace=True)
        if numberText == 'five':
            data_preprocessed.cylindernumber.replace('five', 5, inplace=True)
        if numberText == 'six':
            data_preprocessed.cylindernumber.replace('six', 6, inplace=True)
        if numberText == 'eight':
            data_preprocessed.cylindernumber.replace('eight', 8, inplace=True)
        if numberText == 'twelve':
            data_preprocessed.cylindernumber.replace(
                'twelve', 12, inplace=True)

    # Bước 5: Loại bỏ các giá trị ngoại lệ isolated
    cols = data_preprocessed.columns[(data_preprocessed.columns != 'car_ID') & (
        data_preprocessed.columns != 'CarName')]
    z = np.abs(stats.zscore(
        data_preprocessed[cols]._get_numeric_data()))
    # print("\nMa tran z-score:\n", z)
    zscoreChart(data_preprocessed, z)
    data_preprocessed[cols] = (data_preprocessed[cols])[(z < 3).all(axis=1)]
    data_preprocessed = data_preprocessed.dropna(how='any')

    # Bước 6: Thay thế các giá trị 0 và 1 bởi YES và NO

    # Bước 7: Rời rạc hóa dùng MinMaxScaler
    scaler = preprocessing.MinMaxScaler()
    scaler.fit(data_preprocessed[cols])
    data_preprocessed[cols] = pd.DataFrame(scaler.transform(
        data_preprocessed[cols]), index=data_preprocessed.index, columns=cols)

    # Bước 8: Xác định mô hình trích lọc các thuộc tính đặc trưng EDA
    X = data_preprocessed.loc[:, (data_preprocessed.columns != 'price') & (
        data_preprocessed.columns != 'car_ID') & (data_preprocessed.columns != 'CarName')]
    y = data_preprocessed[['price']]
    binarizer = Binarizer(threshold=0.5)
    y = binarizer.fit_transform(y)

    selector = SelectKBest(chi2, k=3)
    selector.fit(X, y)
    X_new = selector.transform(X)
    # print("X new: \n", X_new)
    # print("y: \n", y)

    print(X.columns[selector.get_support(indices=True)])
    # Ouptut ==> 3 thuộc tính quan trọng: curbweight, enginesize, horsepower


def Analyze():
    # Bước 9: Xác định mô hình trích lọc các thuộc tính đặc trưng
    global data_preprocessed, data_analyzed, current_dataset
    data_analyzed = data_preprocessed[[
        'car_ID', 'curbweight', 'enginesize', 'horsepower']]
    current_dataset = data_analyzed
    ShowCSVData(data_analyzed)
    messagebox.showinfo('Kết quả',
                        '3 thuộc tính quan trọng là: \ncurbweight\nenginesize\nhorsepower')
    btnPredictPrice['state'] = tk.ACTIVE


def PredictPrice():
    atr_predict_form = tk.Toplevel()
    atr_predict_form.geometry('300x100')
    atr_predict_form.resizable(tk.FALSE, tk.FALSE)
    atr_predict_form.title('Chọn thuộc tính để dự đoán giá')
    atr_predict_form.focus()

    # B10: EDA theo nhu cầu thực tế
    var1 = tk.IntVar()
    var2 = tk.IntVar()
    var3 = tk.IntVar()
    cols = ['car_ID']
    cb1 = tk.Checkbutton(atr_predict_form, text='Curb weight',
                         variable=var1, onvalue=1, offvalue=0, command=lambda: cols.append('curbweight'))
    cb1.place(x=10, y=10)
    cb2 = tk.Checkbutton(atr_predict_form, text='Engine size',
                         variable=var2, onvalue=1, offvalue=0, command=lambda: cols.append('enginesize'))
    cb2.place(x=10, y=30)
    cb3 = tk.Checkbutton(atr_predict_form, text='Horse power',
                         variable=var3, onvalue=1, offvalue=0, command=lambda: cols.append('horsepower'))
    cb3.place(x=10, y=50)
    btnSubmit = tk.Button(atr_predict_form, text='Dự đoán', width=10, height=2,
                          command=lambda: SubmitPredictPrice(cols, atr_predict_form))
    btnSubmit.place(x=180, y=25)


def SubmitPredictPrice(cols, form):
    # Bước 10: EDA theo nhu cầu thực tế
    global data_preprocessed, current_dataset
    cols.append('price')
    data_predict = data_preprocessed[cols]
    current_dataset = data_predict
    ShowCSVData(data_predict)
    form.destroy()


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

    # Load dữ liệu
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


def ExportCSV():
    global current_dataset
    os.makedirs('./CSVFolder', exist_ok=True)
    try:
        time = str(datetime.now().strftime("%d%m%Y"))
        path = './G369Thinh_CarPrices/Processed_CarPrices_' + time + '.csv'
        current_dataset.to_csv(path)
        messagebox.showinfo('Thông báo', 'Xuất file CSV thành công!')
    except:
        messagebox.showerror('Thông báo', 'Khôgn xuất được file CSV!')


def ClearFrame():
    for widget in mid_frame.winfo_children():
        widget.destroy()


def ShowCSVData(df):
    ClearFrame()

    r_set = df.to_numpy().tolist()
    l1 = list(df)
    trv = ttk.Treeview(mid_frame, selectmode='browse',
                       height=28, show='headings', columns=l1)
    trv.grid(row=4, column=1, columnspan=3, padx=10, pady=20)

    for i in l1:
        trv.column(i, width=90, anchor='c')
        trv.heading(i, text=str(i))
    for dt in r_set:
        v = [r for r in dt]
        trv.insert("", 'end', iid=v[0], values=v)

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
    if 'car_ID' in columns or 'price' in columns:
        if 'car_ID' in columns and 'price' in columns:
            messagebox.showwarning(
                "Thông báo", "Không được drop car_ID và price")
            chooseAtr_form.focus()
            return
        if 'car_ID' in columns:
            messagebox.showwarning("Thông báo", "Không được drop car_ID")
            chooseAtr_form.focus()
            return
        if 'price' in columns:
            messagebox.showwarning("Thông báo", "Không được drop price")
            chooseAtr_form.focus()
            return
    data.drop(columns=columns, inplace=True, axis=1)
    chooseAtr_form.destroy()
    ShowCSVData(data)
    messagebox.showinfo("Thông báo", "Đã drop thành công " +
                        str(len(columns)) + " thuộc tính!")


def zscoreChart(data, z):
    x = data['car_ID'].values.tolist()
    y = z['horsepower'].values.tolist()
    plt.plot(x, y)
    plt.title('Đồ thị z-score horsepower')
    plt.axhline(y=3, color='r', linestyle='-')
    plt.xlabel('car_ID')
    plt.ylabel('z-score')
    plt.show()


def Game():
    subprocess.run(['python', 'G369Thinh_Game.py'])


def CutVideo():
    subprocess.run(['python', 'G369Thinh_CutVideo.py'])


# Tạo cửa sổ chính
root_69thinh = tk.Tk()
root_69thinh.title(
    "69 Nguyễn Khang Thịnh, 211103C, Đồ Án Học Phần: Lập trình Python, T5.2023")
root_69thinh.geometry('1200x800')
root_69thinh.pack_propagate()
root_69thinh.resizable(tk.FALSE, tk.FALSE)

# Tạo frames
top_frame = tk.Frame(root_69thinh, background='#32a852',
                     width=1400, height=100)
top_frame.pack()
mid_frame = tk.Frame(root_69thinh, background='#ffffff', width=1400,
                     height=630, relief=tk.SUNKEN, borderwidth=2)
mid_frame.pack()
mid_frame.grid_propagate(False)
mid_frame = mid_frame
bot_frame = tk.Frame(root_69thinh, background='#32a852',
                     width=1400, height=70)
bot_frame.pack()

# Các thành phần của top_frame
t = "69 Nguyễn Khang Thịnh, 211103C, Đồ Án Học Phần: Lập trình Python: EDA Car Prices"
lblDT = tk.Label(top_frame, text=t, background="yellow", fg="blue", relief=tk.SUNKEN, font=(
    "Arial Bold", 13), borderwidth=3, height=3, width=116).place(x=15, y=15)

# Các thành phần của mid_frame
# Các thành phần của bot_frame
btnClose = tk.Button(bot_frame, text='Thoát', width=10,
                     height=2, command=CloseWindow)
btnClose.place(x=1100, y=15)

btnVoiceAssistant = tk.Button(
    bot_frame, text='Trợ Lý Ảo', width=12, height=2, command=VoiceAssistant)
btnVoiceAssistant.place(x=800, y=15)

btnLoadData = tk.Button(bot_frame, text='Tải Dữ Liệu', width=12,
                        height=2, command=LoadOriginData)
btnLoadData.place(x=20, y=15)

btnProcessEDA = tk.Button(bot_frame, text='Tiền Xử Lý',
                          width=12, height=2, state=tk.DISABLED, command=ProcessEDA)
btnProcessEDA.place(x=120, y=15)

btnChooseAttribute = tk.Button(
    bot_frame, text='Chọn Thuộc Tính', width=15, height=2, state=tk.DISABLED, command=ChooseAttribute)
btnChooseAttribute.place(x=220, y=15)

btnAnalyze = tk.Button(bot_frame, text='Phân Tích',
                       width=12, height=2, state=tk.DISABLED, command=Analyze)
btnAnalyze.place(x=340, y=15)

btnPredictPrice = tk.Button(
    bot_frame, text='Dự Đoán Giá', width=15, height=2, state=tk.DISABLED, command=PredictPrice)
btnPredictPrice.place(x=440, y=15)

btnExportCSV = tk.Button(bot_frame, text='Xuất File CSV',
                         width=15, height=2, state=tk.DISABLED, command=ExportCSV)
btnExportCSV.place(x=560, y=15)

lblShape = tk.Label(root_69thinh, text='0x0', width=10, font=('arial 9'),
                    height=1, relief=tk.SUNKEN)
lblShape.place(x=12, y=708)

btnGame = tk.Button(bot_frame, text='Game', width=12, height=2, command=Game)
btnGame.place(x=900, y=15)

btnCutVideo = tk.Button(bot_frame, text='Cut Video',
                        width=12, height=2, command=CutVideo)
btnCutVideo.place(x=1000, y=15)

# Chạy app
root_69thinh.mainloop()
