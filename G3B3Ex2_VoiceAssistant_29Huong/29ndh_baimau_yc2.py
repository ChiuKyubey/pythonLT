# IN RA TEXT THEO LỜI NÓI PHÂN LOẠI NGÔN NGỮ
# B1: NẠP THƯ VIỆN 
import speech_recognition as sr 
from gtts import gTTS 
import playsound 
 
# B2: CHỌN PHƯƠNG ÁN NHẬP ÂM THANH TỪ MICROPHONE 
 
r = sr.Recognizer() 
 
# B3: XỬ LÝ NHẬN DIỆN MIC 
#lựa chọn ngôn ngữ nói:
print("Chose language: 1. Viet,    2. 日本語,   3. English")
x=input("Numbes: ")
def Lag(x):
    switcher={
            "1":"vi-VI",
            "2":"ja-JP",
            "3":"en-US",
            }
    return switcher.get(x, "0")
if Lag(x)=="0" : exit("ERROR")
with sr.Microphone() as Source:     #hiệu chỉnh mic để chuẩn bị nói   
    print("Start: ") 
    r.adjust_for_ambient_noise(Source, duration=1) 

    #nhận lời nói của người dùng từ MIc mặc định lưu dữ liệu âm thanh vào audio_data    
    if x=="1"  : print("Say with me in Vietnamese")   
    elif x=="2" : print("Say with me in Japanese")
    else: print("Say with me in English")
    audio_data = r.record(Source, duration = 5)

    #In ra văn bản text 
    print("RESULT ..................")

    #chuyển lời nói thành văn bản     
    try: 
        text = r.recognize_google(audio_data,language= Lag(x))     
    except:  
        text = "I DON'T UNDERSTAND WHAT YOU SAY...!" 

    #in 
    print("You said with me:  ",format(text))      
