#sudung thu vien cua Google
#để SpeechRecognition xử lí phần Microphone cần cài thêm pyaudio
#speech to text
#text to speech
import speech_recognition as sr
import speech_recognition as sr 
from gtts import gTTS 
import os
import time 
import playsound 
# NGHE NÓI => VIẾT RA CHỮ VIỆT
r = sr.Recognizer()
with sr.Microphone() as source:
    #điều chỉnh tiếng ồn 
    print("Adjusting noise ")
    r.adjust_for_ambient_noise(source, duration=1)
    print("Nói bằng tiếng Việt đi bạn 5s sau sẽ in ra Text...")
    # read the audio data from the default microphone
    # ghi dữ liệu cho r.recognize_google
    audio_data1 = r.record(source, duration=5)

    print("Kết quả nhận diện...")
    try:
        text1 = r.recognize_google(audio_data1,language="vi")
    except:
        text1 = "bạn nói gì mình không hiểu!"
    print("Bạn đã nói là: {}".format(text1))
#PHẦN 2: XUẤT RA LỜI NÓI THEO VĂN BẢN ĐÃ NHẬP = Trả lời bằng tiếng Việt : Text => Nói tiếng Việt      
# ĐỌC CHỮ VIỆT => NÓI RA TIẾNG VIỆT 
def HoTen(text): 
    Ten = gTTS(text=text, lang = 'vi') 
    filename =os.path.abspath('')+'\sttHoTen.mp3'     
    Ten.save(filename) 
    playsound.playsound(filename)      
HoTen("số thứ tự 29, họ tên: Leora .Là sinh viên của TRƯỜNG ĐẠI HỌC Sư Phạm Kỹ Thuật Thành phố Hồ Chí Minh.") 
