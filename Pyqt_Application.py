# Pyqt Application
import time
import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QFileInfo, QBasicTimer
from opencv_wand import img2txt, pdfs2txts, ext_pdfs
from os import path


class MyWindow(QWidget):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.resize(300, 200)
        self.progressbar = QProgressBar(self)
        self.timer = QBasicTimer()

        # btn2
        self.imgButton = QtWidgets.QPushButton(self)
        self.imgButton.setText("IMAGE to TXT")  # converting 'jpg', 'png' and 'tiff' to txt file
        self.imgButton.clicked.connect(self.img_to_txt)
        self.imgButton.clicked.connect(self.doAction)
        self.imgButton.clicked.connect(self.timerEvent)

        # btn3
        self.pdfsButton = QtWidgets.QPushButton(self)
        self.pdfsButton.setText("PDF to TXT") # select a folder of pdf file to txt
        self.pdfsButton.clicked.connect(self.pdfs_to_txts)
        self.pdfsButton.clicked.connect(self.doAction)
        self.pdfsButton.clicked.connect(self.timerEvent)

        # btn5
        self.extsButton = QtWidgets.QPushButton(self)
        self.extsButton.setText("EXTRACT PDF") # select a folder of pdf file to txt
        self.extsButton.clicked.connect(self.pdfs_ext)
        self.extsButton.clicked.connect(self.doAction)
        self.extsButton.clicked.connect(self.timerEvent)
       
        # formating layout
        layout = QVBoxLayout()
        layout.addWidget(self.imgButton)
        layout.addWidget(self.pdfsButton)
        layout.addWidget(self.extsButton)
        layout.addWidget(self.progressbar)
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

    def img_to_txt(self):
        self.progressbar.setValue(0)
        folderName = QFileDialog.getExistingDirectory(self)
        fileinfo = QFileInfo(folderName)
        file_path = fileinfo.absolutePath()
        # print(file_path)  # 打印文件绝对路径（不包括文件名和后缀名）
        # print(fileName)
        img2txt(file_path,folderName)

    def pdfs_to_txts(self):
        self.progressbar.setValue(0)
        folderName = QFileDialog.getExistingDirectory(self)
        # print(file_path)  # 打印文件绝对路径（不包括文件名和后缀名）
        fileinfo = QFileInfo(folderName)
        file_path = fileinfo.absolutePath()
        pdfs2txts(file_path,folderName)

    def pdfs_ext(self):
        self.progressbar.setValue(0)
        folderName = QFileDialog.getExistingDirectory(self)
        # print(file_path)  # 打印文件绝对路径（不包括文件名和后缀名）
        fileinfo = QFileInfo(folderName)
        file_path = fileinfo.absolutePath()
        ext_pdfs(file_path,folderName)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    myshow = MyWindow()
    myshow.show()
    sys.exit(app.exec_())