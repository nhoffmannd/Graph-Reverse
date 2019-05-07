##Este programa toma un archivo de imagen, y lo procesa.
##El primer paso sería tomar un archivo de imagen, y mostrarlo.
##Empecemos por generar la interfase gráfica, usando PyQt5.

from PyQt5.QtWidgets import (QMainWindow, QTextEdit, QAction, QFileDialog, QApplication)
from PyQt5.QtGui import QIcon
import sys

class Example(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):      

        self.textEdit = QTextEdit()
        self.statusBar()

        self.setGeometry(300, 300, 350, 300)
        self.setWindowTitle('Graph Reverser')
        self.show()

if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
