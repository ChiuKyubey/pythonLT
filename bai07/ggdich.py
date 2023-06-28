import speech_recognition as sr
import tkinter as tk
from gtts import gTTS 
import playsound 
import os
from googletrans import Translator
r = sr.Recognizer()
G329huong_FILE = os.path.abspath("") + "\G329huong.mp3"

class App(tk.Tk):
        
    def __init__(self):
        super().__init__()
        self.title('29_NDH: Google dich')
        self.geometry('400x300')

        self.lbl_text = tk.Label(self, text='GOOGLE DICH', width=45,  relief="sunken")
        self.lbl1 = tk.Label(self, text = "Chọn ngôn ngữ muốn nói: ", relief = "sunken", font=("Arial Bold", 10), borderwidth = 3, width = 25)
        

        #self.radio1 = tk.Radiobutton(self, text="Tiếng Anh",variable= radio, value = 1, font=("Arial Bold", 14))
        #self.radio2 = tk.Radiobutton(self, text="Tiếng Việt",variable = radio,  value = 2, font=("Arial Bold", 14))
        self.btn_ok = tk.Button(self, width=10, text = 'BẮT ĐẦU', command = self.speech_recognition, bg="black", fg="white")
       
        self.lbl_text.grid(column=0, row=0, padx=25, pady=2)
        self.btn_ok.grid(column=0, row=1, padx=5, pady=5)


    def speech_recognition(self):
        with sr.Microphone() as Source: #personalize
            self.btn_ok.grid_remove()
            self.lbl_text.config(text='Hiệu chỉnh nhiễu trước khi nói')
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
            #print("Quý vị đã nói là : ",format(text))
            self.lbl_text.config(text= format(text), height=5)
            self.lbl_text.update()
if __name__ == "__main__":
    app = App()
    app.mainloop()