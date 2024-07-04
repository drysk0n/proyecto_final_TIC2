import sys
from PyQt5 import QtWidgets, uic, QtCore, QtGui
from testcamararaw4 import Ui_MainWindow
import cv2

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.cap = cv2.VideoCapture(0)  # 0 for default webcam
        self.timer.start(30)  # Update frame every 30 milliseconds

        self.btencender.clicked.connect(self.encender_led)
        self.btencender.clicked.connect(self.fn_activar)
        self.btapagar.clicked.connect(self.fn_desactivar)
        self.btapagar.clicked.connect(self.apagar_led)
        self.btencender.clicked.connect(self.mostrar_imagen_encendido)
        self.btapagar.clicked.connect(self.mostrar_imagen_apagado)


    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert frame to RGB format
            img = QtGui.QImage(frame, frame.shape[1], frame.shape[0], QtGui.QImage.Format_RGB888)
            pixmap = QtGui.QPixmap.fromImage(img)
            self.label.setPixmap(pixmap.scaled(self.label.size(), QtCore.Qt.KeepAspectRatio))

    def encender_led(self):
        print("LED encendido")

    def apagar_led(self):
        print("LED apagado")
    
    def fn_activar(self):
        self.btapagar.setEnabled(True)
        self.btencender.setEnabled(False)

    def fn_desactivar(self):
        self.btapagar.setEnabled(False)
        self.btencender.setEnabled(True)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
