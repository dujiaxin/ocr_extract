# Pyqt Application
import time
import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QFileInfo, QBasicTimer
from opencv_wand import pdf2txt, img2txt, pdfs2txts, ext_pdf, ext_pdfs
from os import path


class MyWindow(QWidget):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.resize(300, 200)
        self.progressbar = QProgressBar(self)
        self.timer = QBasicTimer()

        # btn1
        self.pdfButton = QtWidgets.QPushButton(self)
        self.pdfButton.setText("PDF to TXT")
        self.pdfButton.clicked.connect(self.pdf_to_txt)
        self.pdfButton.clicked.connect(self.doAction)
        self.pdfButton.clicked.connect(self.timerEvent)

        # btn2
        self.imgButton = QtWidgets.QPushButton(self)
        self.imgButton.setText("IMAGE to TXT")  # converting 'jpg', 'png' and 'tiff' to txt file
        self.imgButton.clicked.connect(self.img_to_txt)
        self.imgButton.clicked.connect(self.doAction)
        self.imgButton.clicked.connect(self.timerEvent)

        # btn3
        self.pdfsButton = QtWidgets.QPushButton(self)
        self.pdfsButton.setText("PDF to TXT(folder)") # select a folder of pdf file to txt
        self.pdfsButton.clicked.connect(self.pdfs_to_txts)
        self.pdfsButton.clicked.connect(self.doAction)
        self.pdfsButton.clicked.connect(self.timerEvent)

        # btn4
        self.extButton = QtWidgets.QPushButton(self)
        self.extButton.setText("EXTRACT PDF") # select a folder of pdf file to txt
        self.extButton.clicked.connect(self.pdf_ext)
        self.extButton.clicked.connect(self.doAction)
        self.extButton.clicked.connect(self.timerEvent)

        # btn5
        self.extsButton = QtWidgets.QPushButton(self)
        self.extsButton.setText("EXTRACT PDF(folder)") # select a folder of pdf file to txt
        self.extsButton.clicked.connect(self.pdfs_ext)
        self.extsButton.clicked.connect(self.doAction)
        self.extsButton.clicked.connect(self.timerEvent)
       
        # formating layout
        layout = QVBoxLayout()
        layout.addWidget(self.pdfButton)
        layout.addWidget(self.imgButton)
        layout.addWidget(self.pdfsButton)
        layout.addWidget(self.extButton)
        layout.addWidget(self.extsButton)
        layout.addWidget(self.progressbar)
        # layout.addWidget(self.nonsButton)
        self.setLayout(layout)

    def timerEvent(self, e):
        self.step = 0
        while self.step < 100:
            self.step = self.step + 10
            self.progressbar.setValue(self.step)
        if self.step >= 100:
            self.timer.stop()
            return

    def doAction(self):
        if self.timer.isActive():
            self.timer.stop()
        else:
            self.timer.start(100, self)

    def pdf_to_txt(self):
        self.progressbar.setValue(0)
        fileName, filetype = QFileDialog.getOpenFileName(self)
        fileinfo = QFileInfo(fileName)
        file_path = fileinfo.absolutePath()
        # print(file_path)  # 打印文件绝对路径（不包括文件名和后缀名）
        # print(fileName)
        pdf2txt(file_path,fileName)

    def img_to_txt(self):
        self.progressbar.setValue(0)
        fileName, filetype = QFileDialog.getOpenFileName(self)
        fileinfo = QFileInfo(fileName)
        file_path = fileinfo.absolutePath()
        # print(file_path)  # 打印文件绝对路径（不包括文件名和后缀名）
        print(fileName)
        img2txt(file_path,fileName)

    def pdfs_to_txts(self):
        self.progressbar.setValue(0)
        fileName = QFileDialog.getExistingDirectory(self)
        # print(file_path)  # 打印文件绝对路径（不包括文件名和后缀名）
        print(fileName)
        fileinfo = QFileInfo(fileName)
        file_path = fileinfo.absolutePath()
        # print('fileNmae:',fileName)
        # print('filepath',file_path)
        pdfs2txts(file_path,fileName)

    def pdf_ext(self):
        self.progressbar.setValue(0)
        fileName, filetype = QFileDialog.getOpenFileName(self)
        fileinfo = QFileInfo(fileName)
        file_path = fileinfo.absolutePath()
        # print(file_path)  # 打印文件绝对路径（不包括文件名和后缀名）
        # print(fileName)
        ext_pdf(file_path,fileName)

    def pdfs_ext(self):
        self.progressbar.setValue(0)
        fileName = QFileDialog.getExistingDirectory(self)
        # print(file_path)  # 打印文件绝对路径（不包括文件名和后缀名）
        fileinfo = QFileInfo(fileName)
        file_path = fileinfo.absolutePath()
        print(fileName)
        ext_pdfs(file_path,fileName)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    myshow = MyWindow()
    myshow.show()
    sys.exit(app.exec_())