from gtts import gTTS
import os

def tts(text_in, mp3_out):
    speech = gTTS(text=text_in, lang="en", slow=False)
    speech.save(mp3_out)
