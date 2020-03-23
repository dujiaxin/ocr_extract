# Pyqt Application
import time
import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QFileInfo, QBasicTimer
from opencv_wand import img2txt, pdfs2txts, ext_pdfs, ext_pdf, select
from os import path

class MyWindow(QWidget):
    def __init__(self):
        super(MyWindow, self).__init__()
        # implement an inspection to check if tesseract-OCR is selected.
        self.check = self.selectOCR()
        if self.check == '':
            return False
        self.resize(300, 200)
        self.progressbar = QProgressBar(self)

        # btn1
        self.imgButton = QtWidgets.QPushButton(self)
        self.imgButton.setText("IMAGE to TXT")  # converting 'jpg', 'png' and 'tiff' to txt file
        self.imgButton.clicked.connect(self.img_to_txt)

        # btn2
        self.pdfsButton = QtWidgets.QPushButton(self)
        self.pdfsButton.setText("PDF to TXT") # select a folder of pdf file to txt
        self.pdfsButton.clicked.connect(self.pdfs_to_txts)

        # btn3
        self.extsButton = QtWidgets.QPushButton(self)
        self.extsButton.setText("EXTRACT PDF(by folder)") # select a folder of pdf file to txt
        self.extsButton.clicked.connect(self.pdfs_ext)

        # btn 4
        self.extButton = QtWidgets.QPushButton(self)
        self.extButton.setText("EXTRACT PDF(by files)")  # select a folder of pdf file to txt
        self.extButton.clicked.connect(self.pdf_ext)

        # UI status
        self.label = QLabel(self)
        self.label.setText('Waiting...')

        # formating layout
        layout = QVBoxLayout()
        layout.addWidget(self.imgButton)
        layout.addWidget(self.pdfsButton)
        layout.addWidget(self.extsButton)
        layout.addWidget(self.extButton)
        layout.addWidget(self.progressbar)
        layout.addWidget(self.label)
        self.setLayout(layout)

    def selectOCR(self):
        check = select()
        return check

    def img_to_txt(self):
        self.progressbar.setValue(0)
        self.label.setText('Running...')
        fileName,filetype = QFileDialog.getOpenFileNames(self,'Choose multiple image files')
        # print(file_path)  # 打印文件绝对路径（不包括文件名和后缀名）
        num = img2txt(fileName)
        per = 0
        while per < 100:
            print(per)
            per = next(num)
            self.progressbar.setValue(per)
        self.label.setText('Finished!')

    def pdfs_to_txts(self):
        self.progressbar.setValue(0)
        self.label.setText('Running...')
        fileName,filetype = QFileDialog.getOpenFileNames(self,'Choose multiple PDF files')
        # print(file_path)  # 打印文件绝对路径（不包括文件名和后缀名）
        num = pdfs2txts(fileName)
        per = 0
        while per < 100:
            print(per)
            per = next(num)
            self.progressbar.setValue(per)
        self.label.setText('Finished!')

    def pdfs_ext(self):
        self.progressbar.setValue(0)
        self.label.setText('Running...')
        folderName = QFileDialog.getExistingDirectory(self,'Choose target directory')
        fileinfo = QFileInfo(folderName)
        file_path = fileinfo.absolutePath()
        num = ext_pdfs(file_path,folderName)
        per = 0
        while per < 100:
            print(per)
            per = next(num)
            self.progressbar.setValue(per)
        self.label.setText('Finished!')

    def pdf_ext(self):
        self.progressbar.setValue(0)
        self.label.setText('Running...')
        fileName,filetype = QFileDialog.getOpenFileNames(self,'Choose multiple PDF files')
        num = ext_pdf(fileName)
        per = 0
        while per < 100:
            print(per)
            per = next(num)
            self.progressbar.setValue(per)
        self.label.setText('Finished!')

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    myshow = MyWindow()
    myshow.show()
    sys.exit(app.exec_())