from PySide6 import QtCore, QtWidgets, QtGui

class Custom_Widget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
    
        self.title = 'py test qt widget'
        self.button = QtWidgets.QPushButton("Button")
        self.text = QtWidgets.QLabel("Hello World",
                                        alignment=QtCore.Qt.AlignCenter)
        
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.button)

        self.button.clicked.connect(self.browser_file)

    def browser_file(self):
        fname = QtWidgets.QFileDialog.getOpenFileName(self,
                                        self.tr("Open file"),
                                        self.tr("Data Files (*.csv *.xls *.xlsx);;"))
        self.text.setText(fname[0])

    @QtCore.Slot()
    def magic(self):
        self.text.setText(self.title)
