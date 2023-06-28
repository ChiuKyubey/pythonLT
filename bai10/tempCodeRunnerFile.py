"""NẠP & CHỌN CÁC THUỘC TÍNH -> TIỀN XỬ LÝ DỮ LIỆU EDA (B3: XỬ LÝ CỘT NULL)
"""
import tkinter as tk
#Khởi tạo thiết lập đối tượng masterFORM
master = tk.Tk()
master.title("29_Huong_XỬ LÝ CỘT NULL = NẠP & CHỌN CÁC CỘT NULL CẦN XỬ LÝ")
master.geometry("600x500")
master.resizable(tk.FALSE, tk.FALSE)
#Thiết lập label
tk.Label(master, text = "Các Thuộc tính").place(x = 15, y = 15)
#Thiết lập textbox (khi apply = dùng for nạp các thuộc tính vào thay vì nhập từ textbox )
txtSource = tk.Entry(master, width = 30) # Entry = cho nhập DL vào
txtSource.place(x = 120, y = 15)

#Hàm xử lý btnAdd
def InsertData():
    dem = 0
    a = txtSource.get().strip()
    kq = a.ljust(20)
    # kq = chuỗi <-từ- chuỗi a = canh chỉnh left & bên right là fillchar(space) -> chiều dài width
    if(a != ""):
        listbox1.insert(tk.END, kq)
    #Đếm số dòng trong listbox
    dem = listbox1.size()
    #Điền thông tin vào label
    lblSoLuong.configure(text = dem)
    txtSource.delete(0,tk.END) # xóa trống text -> để nhập mới

#Hàm CopyToRight từ listbox1 sang listbox2 (cho phép chọn nhiều)= có thể viết theo cách khác (như bên dưới)
def CopyToRight():
    i = 0
    while i < listbox1.size(): # duyệt listbox1 -> đến từng vị trí chọn
        if(listbox1.select_includes(i) == 1):
        # sự kiện xác định 1 pt tại vị trí i trong listbox1 đang chọn or not
            listbox2.insert(tk.END, listbox1.get(i))
        i = i + 1
    #Clear selectitem listbox1
    listbox1.select_clear(0,tk.END) # bỏ chế độ chọn các pt đã chọn

#Hàm MoveToRight: di chuyên các thuộc tính từ listbox1 sang listbox2 (xóa các thuộc tính đã chuyển listbox1->)
def MoveToRight():
    i = 0
    selection = listbox1.curselection() # lấy ds các vị trí chọn
    for i in reversed(selection): # duyệt ngược = sv tự làm duyệt thuận
        listbox2.insert(tk.END, listbox1.get(i))
        listbox1.delete(i)
    #Đếm lại số dòng trong listbox1
    dem = listbox1.size()
    #Cập nhật vào label
    lblSoLuong.configure(text = dem)
    # không cần bỏ chế độ = vì đã xóa all pt chọn

#Hàm Delete thuộc tính
def Delete():
    i = 0
    selection = listbox1.curselection()
    for i in reversed(selection):
        listbox1.delete(i)
    #Đếm lại dòng trong listbox1
    dem = listbox1.size()
    #Cập nhật vào label
    lblSoLuong.configure(text = dem)
    #Clear selectitem listbox1
    listbox1.select_clear(0,tk.END)

#Lập Menu cho Listbox1:
def ShowPopupMenu(e):
    if listbox1.size() > 0 :
        popMenu = tk.Menu(listbox1, tearoff = tk.FALSE)
        popMenu.add_command(label = "Copy To Right", command = CopyToRight)
        popMenu.add_command(label = "Move To Right", command = MoveToRight)
        popMenu.add_command(label = "Delete", command = Delete)
        popMenu.tk_popup(e.x_root, e.y_root)#phải thiết lập x_root, y_root để showpopup


######################################
#Button Add
btnAdd = tk.Button(master, text = "Add", width = 10, command = InsertData)
btnAdd.place(x = 300, y = 10)
#Listbox1
listbox1 = tk.Listbox(master, height = 25, width = 40, font = "Consolas 8", selectmode = tk.EXTENDED)
listbox1.bind("<Button-3>", ShowPopupMenu) #<Button-3> : đăng ký sự kiện cho chuột phải của listbox = e: vị trí
listbox1.place(x = 15, y = 50)
#Thiết lập listbox2
listbox2 = tk.Listbox(master, height = 25, width = 40, font = "Consolas 8", selectmode = tk.EXTENDED)
listbox2.place(x = 300, y = 50)
#Thiết lập lblSoLuong
tk.Label(master, text = "Số lượng").place(x = 15, y = 420)
lblSoLuong = tk.Label(master, relief = tk.SUNKEN ,font = "Times 8", borderwidth = 3, width = 15, height = 1)
lblSoLuong.place(x = 100, y = 420)
master.mainloop()