import speech_recognition as sr
import speech_recognition as sr 
from gtts import gTTS 
import os
import time 
import playsound 
def HoTen(text): 
    Ten = gTTS(text=text, lang = 'vi') 
    name=input("nhap ten file (vd: test.mp3): ")
    filename =os.path.abspath('')+'\\'+name     
    Ten.save(filename) 
    playsound.playsound(filename)      
HoTen("số thứ tự 29, họ tên: Leora .Là sinh viên của TRƯỜNG ĐẠI HỌC Sư Phạm Kỹ Thuật Thành phố Hồ Chí Minh.")