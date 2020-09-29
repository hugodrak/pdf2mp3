from pdf2txt import get_text
from tts import tts
import sys

infile = sys.argv[1]

text = get_text(infile)
name = infile.split(".")[0]
tts(text, name+'.mp3')
