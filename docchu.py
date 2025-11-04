from gtts import gTTS
from playsound import playsound
import os

# đọc chữ
def chiGoogle(cau):
    speech = gTTS(text=cau, lang='vi')
    speech.save ('speech.mp3')
    playsound('speech.mp3')
    os.remove('speech.mp3')
    return
