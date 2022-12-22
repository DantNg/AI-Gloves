from gtts import gTTS
import playsound
import os
import speech_recognition as sr
import pyaudio
from pyvi import ViUtils
def convertText2Speech(text):
    output = gTTS(text,lang="vi", slow=False)
    output.save("output.mp3")
    playsound.playsound('output.mp3', True)
    os.remove("output.mp3")

def convertSpeech2Text():  
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source,duration=3)
        print("Mời bạn nói: ")
        audio = r.listen(source)
    try:
        text = r.recognize_google(audio,language="vi-VI")
        print("Bạn -->: {}".format(text))
        return text
    except:
        print("Không nhận được voice!")
        return 0
if __name__ == "__main__":
   text = ViUtils.add_accents('Xin chào mọi người')
   print(text)
   convertText2Speech(text)
    #convertSpeech2Text()