from wand.image import Image as wi
import csv
import cv2
import os
import pytesseract
import re
import tkinter as tk
from tkinter import filedialog
try:
    from PIL import Image
except ImportError:
    import Image

def select():
# install the tesseract package and assign the path to below
    default_dir = r'C:\Program Files' # set the default initial path to select tesseract-OCR
    root = tk.Tk()
    root.withdraw()
    pytesseract.pytesseract.tesseract_cmd = filedialog.askopenfilename(title='Select tesseract.exe in Tesseract-OCR directory',initialdir=(os.path.expanduser(default_dir)))
    return pytesseract.pytesseract.tesseract_cmd

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
def img2txt(fileNames):
    output_dir = filedialog.askdirectory(title='Select the output directory')
    # output number of reports.
    total = len(fileNames)
    for o in range(len(fileNames)):
        complete_name = fileNames[o]
        img_cv = cv2.imread(complete_name)
        # By default OpenCV stores images in BGR format and since pytesseract assumes RGB format,
        # we need to convert from BGR to RGB format/mode:
        string = ''
        img_rgb = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)
        string += pytesseract.image_to_string(img_rgb)
        elem_name = os.path.basename(fileNames[o].replace('.pdf', '.txt'))
        with open(os.path.join(output_dir,elem_name),'w',encoding='utf-8') as f:
            f.write(string)
        yield 100*((o+1)/total)

# convert a floder of pdf files into a floder of txt file
def pdfs2txts(fileNames):
    # select output directory
    output_dir = filedialog.askdirectory(title='Select the output directory')
    total = len(fileNames)
    for o in range(len(fileNames)):
        complete_name = fileNames[o]
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
        elem_name = os.path.basename(fileNames[o].replace('.pdf', '.txt'))
        with open(os.path.join(output_dir,elem_name),'w',encoding='utf-8') as f:
            f.write(string)
        # print(100*((o+1)/total))
        yield 100*((o+1)/total)

# regular expression extracting information
extract_pattern = r'Date[:]|Date\/Time|\bLocation\b|\b[Rr]ace[\s]?[:]\b|\b[Ee]yes[\s]?[:.]\b|\b[Aa]ge[\s]?[:]\b|\bD\.O\.B\b|\b[Hh]air[\s]?[:.]\b'

# extract Date, Location from pdf file and generate a csv file.
def ext_pdf(fileNames):
    output_dir = filedialog.askdirectory(title='Select the output directory')
    total = len(fileNames)
    for o in range(len(fileNames)):
        pdf2txt(os.path.basename(fileNames[o]),fileNames[o])
        complete_name = fileNames[o].replace('.pdf','.txt')
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
        if output != []:
            elem_name = os.path.basename(fileNames[o].replace('.pdf', '.csv'))
            with open(os.path.join(output_dir,elem_name),'w',encoding='utf-8',newline='') as f:
                writer = csv.writer(f,delimiter=',')
                for item in output:
                    # print(item)
                    writer.writerow(item)
        else:
            elem_name = os.path.basename(fileNames[o].replace('.pdf', '') + 'NO_CONTENT' + '.csv')
            with open(os.path.join(output_dir,elem_name),'w',encoding='utf-8',newline='') as f:
                writer = csv.writer(f,delimiter=',')
                for item in output:
                    # print(item)
                    writer.writerow(item)
        yield 100*((o+1)/total)


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
            with open(os.path.join(output_dir,reports_dir1[o].replace('.pdf','')) + 'NO_CONTENT' + '.csv','w',encoding='utf-8',newline='') as f:
                writer = csv.writer(f,delimiter=',')
                for item in output:
                    writer.writerow(item)
        yield 100*((o+1)/total)