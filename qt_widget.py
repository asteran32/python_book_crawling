from PySide6 import QtCore, QtWidgets, QtGui

class Custom_Widget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        self.button = QtWidgets.QPushButton("Open File")
        self.fpath = QtWidgets.QLabel("", alignment=QtCore.Qt.AlignCenter)
        self.msgbox = QtWidgets.QTextBrowser()

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.button)
        self.layout.addWidget(self.fpath)
        self.layout.addWidget(self.msgbox)

        self.button.clicked.connect(self.browser_file)

    def show_dialog(self):
        self.msgbox.setPlainText("textbox")

        
    def browser_file(self):
        fname = QtWidgets.QFileDialog.getOpenFileName(self,
                                        self.tr("Open file"),
                                        self.tr("Data Files (*.xls *.xlsx);;"))
        self.fpath.setText(fname[0])

