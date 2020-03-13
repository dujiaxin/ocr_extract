from wand.image import Image as wi
import cv2
import os
import shutil
import pytesseract
import re
import datetime
import json
import spacy
import pandas as pd
import tkinter as tk
from tkinter import filedialog
from tqdm import tqdm
try:
    from PIL import Image
except ImportError:
    import Image

# install the tesseract package and asign the path to below
root = tk.Tk()
root.withdraw()
pytesseract.pytesseract.tesseract_cmd = filedialog.askopenfilename(title='Select tesseract.exe in Tesseract-OCR directory')
#print(pytesseract.pytesseract.tesseract_cmd)

# convert pdf file to txt file
def pdf2txt(file_path,fileName):
    complete_name = os.path.join(file_path,fileName)
    pdf = wi(filename=complete_name, resolution=750,depth=8,height=50,background='white')
    pdfimage = pdf.convert("jpg")
    i=1
    string = ''
    for img in pdfimage.sequence:
        page = wi(image=img)
        page.save(filename=str(i)+".jpg")
        img_cv = cv2.imread(str(i) + '.jpg')
        # By default OpenCV stores images in BGR format and since pytesseract assumes RGB format,
        # we need to convert from BGR to RGB format/mode:
        # remove image file generate by each page
        os.remove(str(i)+".jpg")
        img_rgb = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)
        string += pytesseract.image_to_string(img_rgb)
        i +=1
    with open(fileName.replace('.pdf','.txt'),'w',encoding='utf-8') as f:
        f.write(string)

# convert the image file (jpg, png, tiff) to txt
def img2txt(file_path,fileName):
    complete_name = os.path.join(file_path,fileName)
    img_cv = cv2.imread(complete_name)
    # By default OpenCV stores images in BGR format and since pytesseract assumes RGB format,
    # we need to convert from BGR to RGB format/mode:
    string = ''
    img_rgb = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)
    string = pytesseract.image_to_string(img_rgb)
    with open(fileName.replace('.pdf','.txt'),'w',encoding='utf-8') as f:
        f.write(string)

# create a directory on desktop to store text files
def create_dir(dir_name):
    if os.path.exists(dir_name):
        shutil.rmtree(dir_name,ignore_errors=True)
    os.mkdir(dir_name)

# convert a floder of pdf files into a floder of txt file
def pdfs2txts(file_path,folderName):
    complete_name = os.path.join(file_path,folderName)
    reports_dir1 = os.listdir(complete_name)
    create_dir('Convert output')
    for elem in tqdm(reports_dir1):
        complete_name = os.path.join(folderName,elem)
        print(complete_name)
        pdf = wi(filename=complete_name, resolution=750,depth=8,height=50,background='white')
        pdfimage = pdf.convert('jpg')
        i=1
        string = ''
        for img in pdfimage.sequence:
            page = wi(image=img)
            page.save(filename=str(i)+'.jpg')
            img_cv = cv2.imread(str(i) + '.jpg')
            # By default OpenCV stores images in BGR format and since pytesseract assumes RGB format,
            # we need to convert from BGR to RGB format/mode:
            # remove image file generate by each page
            os.remove(str(i) + ".jpg")
            img_rgb = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)
            string += pytesseract.image_to_string(img_rgb)
            i +=1
        with open(os.path.join('Convert output',elem.replace('.pdf','')) + '.txt','w',encoding='utf-8') as f:
            f.write(string)

# load in spacy English module
nlp = spacy.load('en_core_web_sm')

### regular expression for RMS
rms_pattern = r'\bRMS[;,.:/]?\ [\s]?[0-9]{2}[-/,.]?[0-9]*\b|\bRMS[;,.:/]?[\s]*[0-9]{2}[-/,.]?[0-9]+\b|[_]RMS[;,.:/]?[0-9]{2}[-/,.]?[0-9]+[_]'

### regular expression extract date between 1900-2100
date_slash_Y = r'\b[0-1][0-9]\/[0-3][0-9]\/[1-2][09][0-9]{2}\b|\b[1-9]\/[0-3][0-9]\/[1-2][09][0-9]{2}\b|\b[1-9]\/[1-9]\/[1-2][09][0-9]{2}\b|\b[1-2][09][0-9]{2}\/[0-1][0-9]\/[0-3][0-9]\b'
date_slash_y = r'|\b[0-1][0-9]\/[0-3][0-9]\/[0-9]{2}\b|\b[0-1][0-9]\/[1-9]\/[0-9]{2}\b|\b[1-9]\/[0-3][0-9]\/[0-9]{2}\b|\b[1-9]\/[1-9]\/[0-9]{2}\b'
date_slash_NY = r'|\b[1-9]\/[0-3][0-9]\b|\b[0-1][0-9]\/[0-3][0-9]\b|\b[1-9]\/[1-9]\b'
date_dash_Y = r'|\b[0-1][0-9]\-[0-3][0-9]\-[1-2][09][0-9]{2}|\b[1-9]\-[0-3][0-9]\-[1-2][09][0-9]{2}|\b[1-9]\-[1-9]\-[1-2][09][0-9]{2}|\b[A-Z][a-z]{2,8}\-[0-3][0-9]\-[1-2][09][0-9]{2}|\b[A-Z][a-z]{2,8}\-[0-3][0-9]\-[0-9]{2}'
date_dash_y = r'|\b[0-1][0-9]\-[0-3][0-9]\-[0-9]{2}\b|\b[1-9]\-[0-3][0-9]\-[0-9]{2}\b|\b[1-9]\-[1-9]\-[0-9]{2}\b'
date_dash_NY = r'|\b[JFMASOND][aepuco][nbrlgptvcy]\-[0-3][0-9]\b'
date_Noseparate = r'|\b[0-1][0-9][0-3][0-9][1-2][09][0-9]{2}'
date_period = r'|\b[0-1][0-9]\.[0-3][0-9]\.[0-9]{2}\b|\b[1-9]\.[0-3][0-9]\.[0-9]{2}\b|\b[1-9]\.[1-9]\.[0-9]{2}\b'
date_space = r'|\b[0-1][0-9]\ [0-3][0-9]\ [0-9]{2}\b|\b[0-1][0-9]\ [0-3][0-9]\ [1-2][09][0-9]{2}'
date_written = r'|\b[A-Z][A-Za-z]{2,8}[.,]?\ [0-3][0-9][.,]?[\s]?[1-2][09][0-9]{2}|\b[A-Z][A-Za-z]{2,8}[.]?[\s]?[1-9],[\s]?[1-2][09][0-9]{2}\b|\b[A-Z][A-Za-z]{2,8}\,[1-2][09][0-9]{2}\b|\b[A-Z][A-za-z]{2,8}.\ [0-3][0-9]\,[\s]?[1-2][09][0-9]{2}\b|\b[0-3][0-9][.,]?\ [A-Z][A-za-z]{2,8}[.,]?\ [1-2][09][0-9]{2}\b|\b[A-Z][A-Za-z]{2,8}\ [0-3]?[0-9][tT][hH][,.]?\ [1-2][09][0-9]{2}\b'
date_written_NY = r'|\b[A-Z][a-z]{2,8}\ [0-3][0-9]th\b'
date_written_ND = r'|\b[0-9]?[0-9]?[\s]?[JFMASOND][aepuco][nbrlgptvcy]\w*\ [1-2][09][0-9]{2}'
hours = r'[\d]{4,6}[\s]?[H][O]?[U]?[R][S]?\b|[\d]{0,2}[:]?[\d]+[\s]?[AaPp][Mm]\b|[\d]{0,2}[:][\d]{1,2}\ Hrs.'
### combine date pattern (must follow the sequence above)
date_pattern = date_slash_Y + date_slash_y + date_slash_NY + date_dash_Y + date_dash_y + date_dash_NY + date_Noseparate + date_period + date_space + date_written + date_written_NY + date_written_ND
#date_pattern = r'\b[0-1][0-9]\/[0-3][0-9]\/[1-2][09][0-9]{2}|\b[1-9]\/[0-3][0-9]\/[1-2][09][0-9]{2}|\b[1-9]\/[1-9]\/[1-2][09][0-9]{2}|\b[0-1][0-9]\/[0-3][0-9]\/[0-9]{2}|\b[0-1][0-9]\/[1-9]\/[0-9]{2}|\b[1-9]\/[0-3][0-9]\/[0-9]{2}|\b[1-2][09][0-9]{2}\/[0-1][0-9]\/[0-3][0-9]|\b[1-9]\/[1-9]\/[0-9]{2}|\b[1-9]\/[0-3][0-9]\b|\b[0-1][0-9]\/[0-3][0-9]|\b[1-9]\/[1-9]|\b[0-1][0-9]\-[0-3][0-9]\-[1-2][09][0-9]{2}|\b[1-9]\-[0-3][0-9]\-[1-2][09][0-9]{2}|\b[0-1][0-9]\-[0-3][0-9]\-[0-9]{2}|\b[1-9]\-[0-3][0-9]\-[0-9]{2}|\b[1-9]\-[1-9]\-[0-9]{2}|\b[JFMASOND][aepuco][nbrlgptvcy]\-[0-3][0-9]\b|\b[A-Z][a-z]{2,8}\-[0-3][0-9]\-[1-2][09][0-9]{2}|\b[A-Z][a-z]{2,8}\-[0-3][0-9]\-[0-9]{2}|\b[0-1][0-9][0-3][0-9][1-2][09][0-9]{2}|\b[0-1][0-9]\.[0-3][0-9]\.[0-9]{2}\b|\b[1-9]\.[0-3][0-9]\.[0-9]{2}\b|\b[1-9]\.[1-9]\.[0-9]{2}\b|\b[0-1][0-9]\ [0-3][0-9]\ [0-9]{2}\b|\b[0-1][0-9]\ [0-3][0-9]\ [1-2][09][0-9]{2}|\b[A-Z][a-z]{2,8}\ [0-3][0-9]\,[1-2][09][0-9]{2}\b|\b[A-Z][a-z]{2,8}\ [1-9]\,[1-2][09][0-9]{2}\b|\b[A-Z][a-z]{2,8}\ [0-3][0-9]\b|\b[A-Z][a-z]{2,8}\ [0-3][0-9]th\b|\b[A-Z][a-z]{2,8}\,[1-2][09][0-9]{2}\b|\b[A-Z][a-z]{2,8}.\ [0-3][0-9]\,[1-2][09][0-9]{2}\b'

extract_pattern = r'Date[:][\s]?[\d]|Date\/Time|\bLocation\b'

def ner(nlp_text_file): # load spacy to formate the context and split the sentence
    sentence = []
    for num,sen in enumerate(nlp_text_file.sents):
        sentence.append(str(sen))
    return(sentence)

def getDate(sentence_text): # retrive datetime to 'DD-MM-YYYY HH:MM:SS'
    date_modified = []
# pattern_hidden = [date_slash_NY,date_dash_NY,date_Noseparate,date_written_NY]
    date_time = re.search(date_pattern,sentence_text)
    if date_time != None:
        hour = re.search(hours,sentence_text)
        if hour != None:
            # print(hour.group())
            orig = date_time.group() + ' ' + hour.group()
            united = pd.to_datetime(orig.replace('Hrs',''),errors='ignore')
            if type(united) != str:
                united = datetime.datetime.strftime(united,'%m-%d-%Y %H:%M:%S')
                date_modified = sentence_text.replace(orig,united)
                # date_modified = sentence_text.replace(str(hour.group()),'')
            else:
                date_modified = sentence_text #### Some pattern of dates pandas can not detect, return original sentence
        else:
            united = pd.to_datetime(date_time.group(),errors='ignore')
            if type(united) != str:
                united = datetime.datetime.strftime(united,'%m-%d-%Y %H:%M:%S')
                date_modified = sentence_text.replace(str(date_time.group()), united)
            else:
                date_modified = sentence_text #### Some pattern of dates pandas can not detect, return original sentence
    else:
        date_modified = sentence_text #### return if there is no date detected in sentence
    return(date_modified)


# convert date and abbreviation in one report
def date_abbreviation_convert(report_text):
    doc = nlp(report_text)
    sen = ner(doc)
    d = ''
    for j in range(len(sen)):
        date_modified = getDate(sen[j])
        d = d + date_modified
        #print(d)
    return(d)


def ext_pdf(file_path,fileName):
    pdf2txt(file_path,fileName)
    complete_name = os.path.join(file_path,fileName.replace('.pdf','.txt'))
    with open(complete_name,'r',encoding='utf-8') as f:
        text = f.read()
        # modified_content = date_abbreviation_convert(text)
        modified_content = text.split('\n')
    output = ''
    # print(modified_content)
    for sen in modified_content:
        # print(sen)
        obj = re.search(extract_pattern,sen)
        if obj != None:
            output = output + '\n' + sen
    with open(fileName.replace('.pdf','.txt'),'w',encoding='utf-8') as f:
        f.write(output)