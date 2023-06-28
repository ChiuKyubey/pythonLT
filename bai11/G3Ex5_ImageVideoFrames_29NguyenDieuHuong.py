import cv2
import tkinter as tk
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox as msg
import os


class MyApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("G3_29_NDHuong")
        self.geometry("350x300")
        self.resizable(tk.FALSE, tk.FALSE)

        self.btnFolder = tk.Button(self, text="Chọn file mở", width=15, bg = "green", command=self.open_file)
        self.btnFolder.place(x=10, y=20)

        self.fileName = None
        self.txtFolderName = tk.Label(width=35,text="",relief=tk.SUNKEN)
        self.txtFolderName.place(x=10, y=50)

        self.labelCap = tk.Button(self, text="Cap theo giây", width=10, command=self.cut_frame)
        self.labelCap.place(x=110, y=95)

        self.spinbox = tk.Spinbox(self, from_=0, to=100, width=5)
        self.spinbox.place(x=5, y=100)

        self.lablespin = tk.Label(self, text="giây")
        self.lablespin.place(x=70, y=100)

        self.labelfd = tk.Label(self, text="Nhập tên muốn lưu")
        self.labelfd.place(x=5, y=150)
        self.entr = tk.Entry(self, width=20, relief=SUNKEN)
        self.entr.place(x=5, y=170)

        self.btnfd = tk.Button(self, text="Chọn đường dẫn", command=self.Chon_duong_Dan)
        self.btnfd.place(x=5, y=190)

        self.btnXulyAnh = tk.Button(self, text='XỬ LÝ', width=10, font=("Arial ",10, "bold"), bg="blue", command=self.capture_frames)
        self.btnXulyAnh.place(x=110, y=250)



    def Get_value(self):
        self.value = int(self.spinbox.get())

    def cut_frame(self):
        self.Get_value()
        cap = cv2.VideoCapture(self.fileName)
        fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        time_to_cut = self.value 
        frame_to_cut = int(time_to_cut * fps)
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_to_cut)
        ret, frame = cap.read()
        if not ret:
            print("Không thể đọc frame.")
            return
        cv2.imshow('Frame', frame)
        cv2.imwrite(self.savepath, frame)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def open_file(self):
        file_path = filedialog.askopenfilename(title="Mở file", filetypes=(("mp4 file(.mp4)", "*.mp4"), ("mov file(.mov)", "*.mov")))
        self.fileName = file_path
        self.txtFolderName.config(text=self.fileName)

    def Chon_duong_Dan(self):
        self.savepath = filedialog.askdirectory(title="Chọn folder lưu ảnh")
        self.savepath += f"/{self.entr.get()}.jpg"
        tk.Label(self, text=self.savepath).place(x=10, y=220)

    def capture_frames(self):
        # mở cửa sổ chọn file
        file_path = self.fileName
        # kiểm tra file có tồn tại không
        if not file_path:
            return
        # khởi tạo đối tượng VideoCapture
        cap = cv2.VideoCapture(file_path)
        # khởi tạo biến lưu frame số
        frame_count = 0
        # đọc frame từ video
        while True:
            # đọc frame tiếp theo
            ret, frame = cap.read()
            # kiểm tra nếu đọc hết video
            if not ret:
                break
            # hiển thị frame
            cv2.imshow('frame', frame)
            # chờ sự kiện từ bàn phím
            key = cv2.waitKey(25)
            # kiểm tra nếu nhấn space
            if key == ord(' '):
                # lưu frame vào file
                cv2.imwrite(self.savepath, frame)
                frame_count += 1
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    # giải phóng tài nguyên
        cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    app = MyApp()
    app.mainloop()
