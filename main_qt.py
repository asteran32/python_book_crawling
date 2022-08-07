import sys
import qt_widget
from PySide6 import QtCore, QtWidgets, QtGui

def main():
    app = QtWidgets.QApplication([])

    widget = qt_widget.Custom_Widget()
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec())
                   
if __name__ == "__main__":
    main()
