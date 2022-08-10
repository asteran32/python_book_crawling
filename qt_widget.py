from ctypes import alignment
from PySide6 import QtCore, QtWidgets, QtGui

class Custom_Widget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        self.fopen = QtWidgets.QPushButton("Open File")
        self.fpath = QtWidgets.QLabel("", alignment=QtCore.Qt.AlignCenter)
        self.msgbox = QtWidgets.QTextBrowser()
        self.fstart = QtWidgets.QPushButton("Start")

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.fopen)
        self.layout.addWidget(self.fpath)
        self.layout.addWidget(self.fstart)
        self.layout.addWidget(self.msgbox)

        self.fopen.clicked.connect(self.browser_file)
        self.fstart.clicked.connect(self.crawling_aladin)

    def show_dialog(self, text):
        self.msgbox.setPlainText(text)

    def browser_file(self):
        fname = QtWidgets.QFileDialog.getOpenFileName(self,
                                        self.tr("Open file"),
                                        self.tr("Data Files (*.xls *.xlsx);;"))
        self.fpath.setText(fname[0])

    def crawling_aladin(self):
        self.msgbox.setPlainText("Start crawling file {}".format(self.fpath.text()))

