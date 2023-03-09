#GOOGLE DỊCH
import speech_recognition as sr 
from gtts import gTTS 
import playsound 
import os
from googletrans import Translator
r = sr.Recognizer()
#LỰA CHỌN NGÔN NGỮ NÓI ĐẦU VÀO
print("Chose language to translate: 1. Viet,    2. 日本語,   3. English")
x=input("Language in: ")
print("Chose language to out: 1. Viet,    2. 日本語,   3. English")
y=input("Language out: ")
def Lag(x):
    switcher={
            "1":"vi",
            "2":"ja",
            "3":"en",
            }
    return switcher.get(x, "0")
if Lag(x)=="0" : exit("ERROR")
if Lag(y)=="0" : exit("ERROR")

#XỬ LÝ ĐẦU VÀO
with sr.Microphone() as Source:      
    print("Start: ") 
    r.adjust_for_ambient_noise(Source, duration=1) 

    #nhận lời nói của người dùng từ MIc mặc định lưu dữ liệu âm thanh vào audio_data    
    if x=="1"  : print("Say with me in Vietnamese")   
    elif x=="2" : print("Say with me in Japanese")
    else: print("Say with me in English")
    audio_data = r.record(Source, duration = 5)

    #In ra văn bản text 
    print("RESULT ..................")

    #chuyển lời nói thành văn bản đưa vào để dịch     
    try: 
        text = r.recognize_google(audio_data,language= Lag(x))     
    except:  
        exit  ("I DON'T UNDERSTAND WHAT YOU SAY...!" )
    
    #in lời nói đầu vào dưới dạng văn bản 
    print("You said with me:  ",format(text))


#DỊCH NGÔN NGỮ THÀNH NGÔN NGỮ ĐÃ CHỌN
translator = Translator()
result = translator.translate(text, src= Lag(x), dest=Lag(y))
#in ra sau khi dịch 
print(result.text)
#nghe cách đọc 
listen = gTTS(result.text, lang = Lag(y)) 
filename =os.path.abspath('')+'\Listen.mp3'     
listen.save(filename) 
print("Lisen : ")
playsound.playsound(filename) 



