# Pyqt Application
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QFileInfo
from opencv_wand import pdf2txt, img2txt, pdfs2txts, ext_pdf, ext_pdfs
from os import path


class MyWindow(QWidget):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.resize(300, 200)

        # btn1
        self.pdfButton = QtWidgets.QPushButton(self)
        self.pdfButton.setText("Convert pdf to txt")
        self.pdfButton.clicked.connect(self.pdf_to_txt)

        # btn2
        self.imgButton = QtWidgets.QPushButton(self)
        self.imgButton.setText("Convert image to txt")  # converting 'jpg', 'png' and 'tiff' to txt file
        self.imgButton.clicked.connect(self.img_to_txt)

        # btn3
        self.pdfsButton = QtWidgets.QPushButton(self)
        self.pdfsButton.setText("Convert pdf to txt (folder)") # select a folder of pdf file to txt
        self.pdfsButton.clicked.connect(self.pdfs_to_txts)

        # btn4
        self.extButton = QtWidgets.QPushButton(self)
        self.extButton.setText("Extract pdf") # select a folder of pdf file to txt
        self.extButton.clicked.connect(self.pdf_ext)

        # btn5
        self.extsButton = QtWidgets.QPushButton(self)
        self.extsButton.setText("Extract pdfs") # select a folder of pdf file to txt
        self.extsButton.clicked.connect(self.pdfs_ext)
       
        # formating layout
        layout = QVBoxLayout()
        layout.addWidget(self.pdfButton)
        layout.addWidget(self.imgButton)
        layout.addWidget(self.pdfsButton)
        layout.addWidget(self.extButton)
        layout.addWidget(self.extsButton)
        # layout.addWidget(self.nonsButton)
        self.setLayout(layout)

    def pdf_to_txt(self):
        fileName, filetype = QFileDialog.getOpenFileName(self)
        fileinfo = QFileInfo(fileName)
        file_path = fileinfo.absolutePath()
        # print(file_path)  # 打印文件绝对路径（不包括文件名和后缀名）
        print(fileName)
        pdf2txt(file_path,fileName)

    def img_to_txt(self):
        fileName, filetype = QFileDialog.getOpenFileName(self)
        fileinfo = QFileInfo(fileName)
        file_path = fileinfo.absolutePath()
        # print(file_path)  # 打印文件绝对路径（不包括文件名和后缀名）
        print(fileName)
        img2txt(file_path,fileName)

    def pdfs_to_txts(self):
        fileName = QFileDialog.getExistingDirectory(self)
        # print(file_path)  # 打印文件绝对路径（不包括文件名和后缀名）
        print(fileName)
        fileinfo = QFileInfo(fileName)
        file_path = fileinfo.absolutePath()
        print('fileNmae:',fileName)
        print('filepath',file_path)
        pdfs2txts(file_path,fileName)

    def pdf_ext(self):
        fileName, filetype = QFileDialog.getOpenFileName(self)
        fileinfo = QFileInfo(fileName)
        file_path = fileinfo.absolutePath()
        # print(file_path)  # 打印文件绝对路径（不包括文件名和后缀名）
        print(fileName)
        ext_pdf(file_path,fileName)

    def pdfs_ext(self):
        fileName = QFileDialog.getExistingDirectory(self)
        # print(file_path)  # 打印文件绝对路径（不包括文件名和后缀名）
        fileinfo = QFileInfo(fileName)
        file_path = fileinfo.absolutePath()
        print(fileName)
        ext_pdfs(file_path,fileName)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    myshow = MyWindow()
    myshow.show()
    sys.exit(app.exec_())