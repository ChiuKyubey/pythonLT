# B1: NẠP THƯ VIỆN 
import speech_recognition as sr 
from gtts import gTTS 
import playsound 
 
# B2: CHỌN PHƯƠNG ÁN NHẬP ÂM THANH TỪ MICROPHONE 
 
r = sr.Recognizer() 
 
# B3: XỬ LÝ NHẬN DIỆN MIC 

#Nhập Y (Yes) để nói và in ra câu bạn vừa nói
#Nhập N (No) để không thực hiện cho đến khi nào bấm Y
with sr.Microphone() as Source:     #hiệu chỉnh mic để chuẩn bị nói   
    n=input (("ban muon in hay chua: (Y/N)")) 

    while (n=='N'):
        n=input (("ban muon in hay chua:(Y/N)")) 
        if (n=='Y'): continue
        
    if n=='Y':
        print("Hieu chinh nhieu truoc khi noi!") 
        r.adjust_for_ambient_noise(Source, duration=1) 
        #nhận lời nói của người dùng từ MIc mặc định lưu dữ liệu âm thanh vào audio_data    
        print("Nói tiếng Việt đi, sau 5s sẽ in ra văn bản!")     
        audio_data = r.record(Source, duration = 5)      
        #In ra văn bản text 
        print("KẾT QUẢ NHẬN DIỆN ..................") 
        #chuyển lời nói thành văn bản     
        try: 
            text = r.recognize_google(audio_data,language="vi-VI")     
        except:  
            text = "Quý vị nói gì nghe không rõ...!" 
        #in kết quả ra  
        print("Quý vị đã nói là :  ",format(text))      
