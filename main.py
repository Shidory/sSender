"""
import sys
import time

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QBrush, QColor, QPalette
from PyQt5.QtWidgets import QApplication, qApp

from qroundprogressbar import QRoundProgressBar


app = QApplication(sys.argv)

progress = QRoundProgressBar()
progress.setBarStyle(QRoundProgressBar.BarStyle.DONUT)

# style accordingly via palette
palette = QPalette()
brush = QBrush(QColor(0, 0, 255))
brush.setStyle(Qt.SolidPattern)
palette.setBrush(QPalette.Active, QPalette.Highlight, brush)

progress.setPalette(palette)
progress.show()

# simulate delayed time that a process may take to execute
# from demonstration purposes only
for i in range(0, 100, 20):
    progress.setValue(i)
    qApp.processEvents()
    time.sleep(3)

sys.exit(app.exec_())

"""

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUiType
import os
import sys
import time


class Progress(QThread):
    mysignal = pyqtSignal(int)

    def __init__(self, parent=None):
        QThread.__init__(self, parent)

    def run(self):
        i = 0
        while i < 101:
            time.sleep(0.1)
            self.mysignal.emit(i)
            i += 1


FROM_SPLASH, _ = loadUiType(os.path.join(os.path.dirname(__file__), "splash.ui"))
FROM_MAIN, _ = loadUiType(os.path.join(os.path.dirname(__file__), "main.ui"))

#################################################################################
#           Class Main                                                          #
#################################################################################
class Main(QMainWindow, FROM_MAIN):
    def __init__(self, parent=None):
        super(Main, self).__init__(parent)
        self.setupUi(self)
        QMainWindow.setFixedSize(self, 900, 900)
        self.btn_send.clicked.connect(self.open_dir)

        size_screen = QDesktopWidget().screenGeometry()#Get size screen
        size_window = self.geometry()#get window size

       #self.lbl_logo.setText = "ejfkjeojgjkloiejgkkljoijekjoigj"

    def open_dir(self):
        name = QFileDialog.getOpenFileName(self, 'Choose file')

#################################################################################
#           Class Splash                                                        #
#################################################################################
class Splash(QMainWindow, FROM_SPLASH):

    def __init__(self, parent=None):

        super(Splash, self).__init__(parent)
        QMainWindow.__init__(self)
        QMainWindow.setFixedSize(self,580, 900)
        self.setupUi(self)
        pixmap = QPixmap("logo.png")
        self.splash_image.setPixmap(pixmap.scaled(350, 300))
        progress = Progress(self)
        progress.mysignal.connect(self.progress)
        progress.start()

    @pyqtSlot(int)
    def progress(self, i):
        self.progressBar.setValue(i)
        if i == 100:
            self.hide()
            main = Main(self)
            main.show()


def main():
    app = QApplication(sys.argv)
    window = Splash()
    window.show()
    app.exec_()


if __name__ == '__main__':
    try:
        main()
    except Exception as why:
        print(why)

#install pyinstaller

