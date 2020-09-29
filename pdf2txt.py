import pdfminer.high_level as pm

def get_text(file):
    text = pm.extract_text(file)
    return text
