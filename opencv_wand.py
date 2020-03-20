from wand.image import Image as wi
import csv
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

# convert pdf file to txt file
def pdf2txt(file_path,fileName):
    # print('path',file_path)
    # print("name",fileName)
    complete_name = os.path.join(file_path,fileName)
    print('PATH:',complete_name)
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

# convert the image file (jpg, png, tiff) to txt all file name must be in English!
def img2txt(file_path,folderName):
    output_dir = filedialog.askdirectory(title='Select the output directory')
    complete_name = os.path.join(file_path,folderName)
    reports_dir1 = os.listdir(complete_name)
    # output a progress number.
    total = len(reports_dir1)
    for i in range(len(reports_dir1)):
        complete_name = os.path.join(folderName,reports_dir1[i])
        img_cv = cv2.imread(complete_name)
        # By default OpenCV stores images in BGR format and since pytesseract assumes RGB format,
        # we need to convert from BGR to RGB format/mode:
        string = ''
        img_rgb = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)
        string += pytesseract.image_to_string(img_rgb)
        with open(os.path.join(output_dir,reports_dir1[i].replace('.pdf','')) + '.txt','w',encoding='utf-8') as f:
            f.write(string)
        yield 100*((i+1)/total)

# convert a floder of pdf files into a floder of txt file
def pdfs2txts(file_path,folderName):
    # select output directory
    output_dir = filedialog.askdirectory(title='Select the output directory')
    complete_name = os.path.join(file_path,folderName)
    reports_dir1 = os.listdir(complete_name)
    total = len(reports_dir1)
    print(total)
    for o in range(len(reports_dir1)):
        complete_name = os.path.join(folderName,reports_dir1[o])
        print(complete_name)
        pdf = wi(filename=complete_name, resolution=750,depth=8,height=50,background='white')
        pdfimage = pdf.convert('jpg')
        i=1
        string = ''
        for img in pdfimage.sequence:
            page = wi(image=img)
            page.save(filename=str(i)+'.jpg')
            img_cv = cv2.imread(str(i) + '.jpg')
            # remove image file generate by each page
            os.remove(str(i) + ".jpg")
            img_rgb = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)
            string += pytesseract.image_to_string(img_rgb)
            i +=1
        with open(os.path.join(output_dir,reports_dir1[o].replace('.pdf','')) + '.txt','w',encoding='utf-8') as f:
            f.write(string)
        # print(100*((o+1)/total))
        yield 100*((o+1)/total)

# load in spacy English module
nlp = spacy.load('en_core_web_sm')

# regular expression extracting information
extract_pattern = r'Date[:]|Date\/Time|\bLocation\b|\b[Rr]ace[\s]?[:]\b|\b[Ee]yes[\s]?[:.]\b|\b[Aa]ge[\s]?[:]\b|\bD\.O\.B\b|\b[Hh]air[\s]?[:.]\b'

def ner(nlp_text_file): # load spacy to formate the context and split the sentence
    sentence = []
    for num,sen in enumerate(nlp_text_file.sents):
        sentence.append(str(sen))
    return(sentence)

# extract Date, Location from pdf file and generate a csv file.
def ext_pdf(file_path,fileName):
    pdf2txt(file_path,fileName)
    complete_name = os.path.join(file_path,fileName.replace('.pdf','.txt'))
    with open(complete_name,'r',encoding='utf-8') as f:
        text = f.read()
        # modified_content = date_abbreviation_convert(text)
        modified_content = text.split('\n')
    output = []
    # print(modified_content)
    for sen in modified_content:
        # print(sen)
        obj = re.search(extract_pattern,sen)
        if obj != None:
            if sen not in output:
                output.append([obj.group(),sen])
    os.remove(complete_name)
    with open(fileName.replace('.pdf','.csv'),'w',encoding='utf-8',newline='') as f:
        writer = csv.writer(f,delimiter=',')
        for item in output:
            # print(item)
            writer.writerow(item)



# extract multiple pdf files
def ext_pdfs(file_path,folderName):
    complete_name = os.path.join(file_path,folderName)
    reports_dir1 = os.listdir(complete_name)
    # select output directory
    output_dir = filedialog.askdirectory(title='Select the output directory')
    total = len(reports_dir1)
    for o in range(len(reports_dir1)):
        pdf2txt(folderName, os.path.join(folderName,reports_dir1[o]))
        complete_name = os.path.join(folderName,reports_dir1[o].replace('.pdf','.txt'))
        #print('.txt path:',complete_name)
        with open(complete_name, 'r', encoding='utf-8') as f:
            text = f.read()
            # modified_content = date_abbreviation_convert(text)
            modified_content = text.split('\n')
        os.remove(complete_name)
        output = []
        for sen in modified_content:
            # print(sen)
            obj = re.search(extract_pattern, sen)
            if obj != None:
                if sen not in output:
                    output.append([obj.group(),sen])
        if output != []:
            with open(os.path.join(output_dir,reports_dir1[o].replace('.pdf','')) + '.csv','w',encoding='utf-8',newline='') as f:
                writer = csv.writer(f,delimiter=',')
                for item in output:
                    writer.writerow(item)
        else:
            print('NO CONTENT:',complete_name)
            break
        yield 100*((o+1)/total)