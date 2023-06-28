import tkinter as tk
from tkinter import *
from tkinter import filedialog # thu vien SUB-LIB tkinter = Hop thoai ho tro Mo file
from tkinter import messagebox as msg # thu vien SUB-LIB tkinter = Hop thong bao = messagebox
#B2: THIET LAP & KHOI TAO DOI TUONG FORM
master = tk.Tk()
master.title("G3_29_Baimau")
master.geometry("900x500")
master.resizable(tk.FALSE, tk.FALSE)
#B3: LAP HAM ClearText = Xoa van ban cu
def ClearText():
    #Dùng delete cho Text
    lblFileText.delete("1.0", tk.END)
    scroll_y.set(0.0,1.0)
#B4: HAM DOC file txt
def OpenTextFile():
    global filepath # bien toan cuc
    #Hop thoai Mo thu muc
    filepath = filedialog.askopenfilename(title = "29 Nguyen Dieu Huong_ Open Text File", filetypes = (("TextFile (.txt)", "*.txt"),("CSV File (.csv)", "*.csv")))
    #Mo file co dau TV encoding="utf-8"
    f1 = open(filepath, "r", encoding="utf-8")
    data = f1.read()
    #ClearText
    ClearText()
    #Nap noi dung file vao label text
    lblFileText.configure(state=tk.NORMAL)#set normal = cho phep sua text
    lblFileText.insert(tk.END,data)
    lblFileText.configure(state=tk.DISABLED) # .. chon KO cho chinh sua nua = readonly
    # dong doi tuong file
    f1.close()
#B5: HAM THUC HIEN CAC XU LY DOC FILE _ SUA FILE LIEN QUAN
def XuLy():
    # Mo file text co dau TV = encoding="utf-8"
    f1 = open(filepath, "r", encoding="utf-8")
    s=""
    list = []
    # doc tung line
    for line in f1:
        # Cắt toàn bộ kí tự khoảng trắng của mỗi dòng
        line = line.strip()
        # Kiểm tra dòng tiep theo có khác rỗng không = Nếu không thì đọc từng dòng đã bỏ khoảng trắng
        if line != "":
            kytu = line[0] #Lấy ký tự đầu tiên
            if(kytu >= "0" and kytu <= "9"):
                vitri = line.find(":", 0, -1)
                if(vitri == -1):
                    #kytu = line[:vitri] #test thử
                    line = line[0:] #lấy vị trí từ 0 đến ký tự \n
                    list.append(line) #add phần tử vào mảng
                    s=s+line+"\n"""
# nếu ký tự đầu không phải chữ = bỏ qua
#Sắp xếp phần từ trong mảng list
    list.sort()
#Đọc phần tử trong mảng
    s=""
    s=list[0]
    key = list[0]
    dem = 1
    for i in list:
        #Kiểm tra nếu phần tử trùng thì bỏ qua không cộng vào s
        if i == key:
            s=s+""
        else :
            key = i
            s=s+i+"\n"
            dem = dem + 1
    #Thiết lập đóng file
    f1.close()
    #ClearText
    ClearText()
    #Thiết lập nội dung vào label text
    lblXuLy.configure(state=tk.NORMAL)#set normal để cho chỉnh sửa text
    lblXuLy.insert(tk.END,s)
    lblXuLy.configure(state=tk.DISABLED)#sau khi chỉnh sửa text thì không cho chỉnh sửa chỉ cho đọc readonly
    #Thiết lập biến đếm
    lblCount.configure(text = "Số lượng SV: %d" %dem)
    #Sau khi đọc file xong thì thực hiện lưu file
    f_new = open("KetQua.txt", "w+", encoding="utf-8")
    f_new.write(s+"\n"+"Số lượng SV: %d" %dem)
#Thiết lập 1 button
btnOpenTextFile = tk.Button(master,text = "Open text File", command = OpenTextFile)
btnOpenTextFile.place(x=5, y=5)
#Thiết lập 1 frame chứa thông tin của text
frame = tk.Frame(master, width = 380, height = 300, relief = tk.SUNKEN, borderwidth = 3)
frame.place(x=5,y=40)
#Thiết kế label để đọc file text có chứa scroll
lblFileText = tk.Text(frame, width = 50, state=tk.DISABLED)
scroll_y = tk.Scrollbar(frame, command = lblFileText.yview, orient = tk.VERTICAL)
lblFileText.configure(yscrollcommand = scroll_y.set)
#Thiết lập vị trí cho scroll
scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
#Thiết lập vị trì cho fileText. i thiết lập cho scroll ms thiết lập sau cho label
lblFileText.pack(side=tk.LEFT, fill=tk.BOTH)
#Thiết lập 1 button xử lý
btnXuLy = tk.Button(master,text = "Xử lý", command = XuLy)
btnXuLy.place(x=450, y=5)
#Thiết lập 1 frame2 chứa thông tin của text
frame2 = tk.Frame(master, width = 380, height = 300, relief = tk.SUNKEN, borderwidth = 3)
frame2.place(x=450,y=40)
#Thiết kế label để đọc file text có chứa scroll
lblXuLy = tk.Text(frame2, width = 50, state=tk.DISABLED)
scroll_y = tk.Scrollbar(frame2, command = lblXuLy.yview, orient = tk.VERTICAL)
lblXuLy.configure(yscrollcommand = scroll_y.set)
#Thiết lập vị trí cho scroll
scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
#Thiết lập vị trì cho fileText. i thiết lập cho scroll ms thiết lập sau cho label
lblXuLy.pack(side=tk.LEFT, fill=tk.BOTH)
#Thiết lập label đếm số lượng sv
lblCount = tk.Label(master,text="Số lượng SV: 0",relief = tk.SUNKEN, width = 25)
lblCount.place(x=700, y=470)
master.mainloop()