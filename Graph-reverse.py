from PyQt5.QtWidgets import QMainWindow, QAction, QApplication, QWidget
from PyQt5.QtWidgets import QTextEdit, QFileDialog, QLabel, QVBoxLayout
from PyQt5.QtGui import QIcon, QPixmap
from GraphReverseDefinitions import new_function
from scipy import misc
from matplotlib import pyplot as plt
import sys
import PIL
import numpy

class Example(QMainWindow):
    ##Esto es estándar de PyQt5.
    def __init__(self):
        super().__init__()
        self.initUI()

    ##Aquí se controla la ventana obtenida.
    def initUI(self):      
        self.statusBar()
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')

        ##Una caja de texto.
        self.label = QTextEdit()
        self.setCentralWidget(self.label)

        ##Definimos funciones mas sencillamente.        
        openFile    = new_function('web.png', 'Open', 'Ctrl+O', 'Abre', self, fileMenu)
        exitProgram = new_function('web.png','Cerrar','Ctrl+X', 'Exit', self, fileMenu)
        openFile.triggered.connect(self.open_file)
        exitProgram.triggered.connect(self.salir)

        ##Esta es la ventana que sale.
        self.setWindowTitle('Graph Reverser')
        self.show()

    def salir(self):
        sys.exit()
        ##Las funciones más sencillas primero.

    def open_file(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', "", "Image Files (*.jpg, *.bmp, *.png)")
        workfile = misc.imread('face.png')
        mi = workfile.shape[1]
        histogram = numpy.full((mi,1),0)
        ##ESTO ANDA
        for a in range (0, mi):
            histogram(a, 1) = workfile[]
        


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
