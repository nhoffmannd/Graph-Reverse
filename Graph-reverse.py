from PyQt5.QtWidgets import (QMainWindow, QAction, QApplication)
from PyQt5.QtWidgets import (QTextEdit, QFileDialog)
from PyQt5.QtGui import QIcon
from GraphReverseDefinitions import new_function
import sys
import matplotlib.pyplot as plt
import numpy as np

class Example(QMainWindow):
    ##Esto es estándar de PyQt5.
    def __init__(self):
        super().__init__()
        self.initUI()

    ##Aquí se controla la ventana obtenida.
    def initUI(self):      
        self.textEdit = QTextEdit()
        self.setCentralWidget(self.textEdit)
        self.statusBar()
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')

        ##Definimos funciones mas sencillamente.        
        openFile = new_function('web.png', 'Open', 'Ctrl+O', 'Abre', self, fileMenu)
        openFile.triggered.connect(self.open_file)
        exitProgram = new_function('web.png','Cerrar','Ctrl+X','Exit', self, fileMenu)
        exitProgram.triggered.connect(self.salir)

        ##Esta es la ventana que sale.
        self.setGeometry(300, 300, 350, 300)
        self.setWindowTitle('Graph Reverser')
        self.show()

    def open_file(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', "", "Image Files (*.jpg, *.bmp, *.png)")
        self.textEdit.setText(fname[0])

    def salir(self):
        self.textEdit.setText("jaja.")
        sys.exit()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
