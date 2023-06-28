import speech_recognition as sr
import tkinter as tk 
from gtts import gTTS 
import playsound 
import os
from googletrans import Translator
r = sr.Recognizer()


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('29_NDH: NHAN DIEN GIONG NOI')
        self.geometry('450x300')

        self.lbl_text = tk.Label(self, text='CHƯƠNG TRÌNH NHẬN DIỆN GIỌNG NÓI \n\n Bạn sẵn sàng nói chưa?', font=("Arial ",10, "bold"),width=40,  relief="sunken", fg="red")
        self.lbl_text.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        self.btn_ok = tk.Button(self, width=10, text = 'BẮT ĐẦU', command = self.speech_recognition, bg="black", fg="white")
    
        self.lbl_text.grid(column=0, row=0, padx=40, pady=20)
        self.btn_ok.grid(column=0, row=1, padx=5, pady=5)

    def speech_recognition(self):
        with sr.Microphone() as Source: #personalize
            #print("Hiệu chỉnh nhiễu trước khi nói") 
            self.btn_ok.grid_remove()
            self.lbl_text.config(text='Hiệu chỉnh nhiễu ...')
            self.lbl_text.update()
            r.adjust_for_ambient_noise(Source, duration=1)
            #print("Nói tiếng Việt đi, sau 5s sẽ in ra văn bản!") 
            self.lbl_text.config(text='Nói tiếng Việt đi, sau 5s sẽ in ra văn bản!')
            self.lbl_text.update()
            audio_data = r.record(Source, duration = 5) #personalize
            #print("KẾT QUẢ NHẬN DIỆN")
            self.lbl_text.config(text='KẾT QUẢ NHẬN DIỆN')
            self.lbl_text.update()
            try:
                text = r.recognize_google(audio_data,language="vi") 
            except:
                    text = "Quý vị nói gì nghe không rõ...!" 
            self.lbl_text.config(text= format(text), height=5)
            self.lbl_text.update()
            vtext = gTTS(text=text, lang="vi")
            ndh29_FILE='29ndh.mp3'
            #ndh29_FILE =os.path.abspath('')+'\\'+'29ndh.mp3'
            filename ='29ndh.mp3'
            vtext.save(ndh29_FILE)
            playsound.playsound(ndh29_FILE)

if __name__ == "__main__":
    app = App()
    app.mainloop()