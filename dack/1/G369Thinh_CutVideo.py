import cv2
import tkinter as tk
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox as msg
import os


def choose_video():
    btnNhap.config(state=tk.ACTIVE)
    global filepath, cap
    filepath = filedialog.askopenfilename(title="Mở file", filetypes=(
        ("mp4 file(.mp4)", "*.mp4"), ("mov file(.mov)", "*.mov")))
    if filepath is not None:
        cap = cv2.VideoCapture(filepath)

    global end, start
    start = cv2.getTrackbarPos('start', 'video')
    end = cv2.getTrackbarPos('end', 'video')

    # Đặt chỉ số khung hình của video tại thời điểm bắt đầu
    cap.set(cv2.CAP_PROP_POS_FRAMES, start)


def XuLy():
    global name, savepath
    name = ''

    count = 0
    space_press = False

    while cap.isOpened():
        ret, frame = cap.read()

        if ret:
            cv2.imshow('Khung Hinh', frame)
            if space_press:
                if savepath is not None:
                    cv2.imwrite(os.path.join(
                        savepath, "{}{}.jpg".format(name, count)), frame)
                else:
                    cv2.imwrite("Khunghinh{}.jpg".format(count), frame)

                count += 1  # tang bien dem len 1 don vi
                space_press = False
        else:
            break

        key = cv2.waitKey(10) & 0xFF
        if key == ord('q'):
            break
        elif key == ord(' '):
            space_press = True

    cap.release()
    cv2.destroyWindow('Khung Hinh')

    if savepath is None:
        name = input("Nhập tên cho các khung hình: ")
        savepath = input("Nhập đường dẫn lưu trữ các khung hình: ")

    print("Đã lưu {} khung hình".format(count))


def save_input(e):
    btnChonFolder.config(state=tk.ACTIVE)
    global name
    name = txtInput.get("1.0", "end-1c")
    txtInput.delete("1.0", "end-1c")
    print(name)


def choose_folder():
    btnXuLy.config(state=tk.ACTIVE)
    global savepath
    savepath = filedialog.askdirectory(title="Chọn folder lưu ảnh")
    print(savepath)
    lblPath.config(text=savepath)

# tkinter window


root = tk.Tk()
root.title("G369 THINH")
root.geometry("600x300")
root.resizable(tk.FALSE, tk.FALSE)

btnChonVideo = tk.Button(root, width=10, height=1,
                         text="Chọn video", command=choose_video)
btnChonVideo.place(x=10, y=5)

btnXuLy = tk.Button(root, width=10, height=5,
                    text="Xử lý", command=XuLy, state=tk.DISABLED)
btnXuLy.place(x=200, y=50)
lblspace = tk.Label(root, text="Nhấn Space để cắt ảnh")
lblspace.place(x=200, y=140)

lblName = tk.Label(root, text="Nhập tên muốn lưu ảnh: ")
lblName.place(x=5, y=50)

btnNhap = tk.Button(root, width=10, text="Nhập",
                    command=lambda: save_input(None), state=tk.DISABLED)
btnNhap.place(x=100, y=70)

txtInput = tk.Text(root, width=10, height=1)
txtInput.place(x=5, y=70)
txtInput.bind("<Return>", save_input)

btnChonFolder = tk.Button(
    root, width=10, height=1, text="Chọn folder", command=choose_folder, state=tk.DISABLED)
btnChonFolder.place(x=5, y=120)

lblPath = tk.Label(root, text="Đường dẫn:")
lblPath.place(x=5, y=160)

# huong dan
lb_hd1 = tk.Label(root, text="1. Chon video .mp4 hoac .mov")
lb_hd1.place(x=350, y=10)
lb_hd2 = tk.Label(root, text="2. Dat ten cho khung hinh -> Click nhap")
lb_hd2.place(x=350, y=40)
lb_hd3 = tk.Label(root, text="3. Chon folder luu hinh")
lb_hd3.place(x=350, y=70)
lb_hd4 = tk.Label(root, text="4. Click xu ly -> Space de cat anh")
lb_hd4.place(x=350, y=100)
lb_hd5 = tk.Label(root, text="5. Nhan q de thoat")
lb_hd5.place(x=350, y=130)

root.mainloop()
