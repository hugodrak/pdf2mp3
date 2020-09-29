import pdfminer.high_level as pm
from gtts import gTTS
import os


def convert(infile):
    text = pm.extract_text(infile)
    name = infile.split(".")[0]
    speech = gTTS(text=text, lang="en", slow=False)
    speech.save(name+'.mp3')
    print(3, "converted")
    return name+'.mp3'
