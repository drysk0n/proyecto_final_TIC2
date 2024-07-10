import sys
import cv2
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtCore import QTimer

import numpy as np
import serial
import time




#Aquí se activa la camara:
class VideoStreamWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.video_label = QLabel(self)
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.video_label)
        self.setLayout(self.layout)

        self.cap = cv2.VideoCapture(0)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)

    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = QImage(frame, frame.shape[1], frame.shape[0], frame.strides[0], QImage.Format.Format_RGB888)
            self.video_label.setPixmap(QPixmap.fromImage(image))

    def closeEvent(self, event):
        self.cap.release()
        event.accept()




class MainWindow(QMainWindow):
    Disp_temp: int

    def setup_serial(self): # Crea la conexión con el arduino
        try:
            self.arduino = serial.Serial('COM6', 9600)  
            self.last_update_time = time.time()
        except serial.SerialException as e:
            print(f"Error al abrir el puerto serial: {e}")
            sys.exit(1)


    def LecturaArduino(self): # Es la función que manda y recibe datos del arduino
        try:
            self.arduino.write('hola'.encode()) # Le manda  información al arduino.
            if self.arduino.in_waiting > 0:
                self.mensaje = self.arduino.readline().decode().strip()  #Recibe, lee y almacena un mensaje mandado desde arduino
                print(self.mensaje,type(self.mensaje))  
                if self.mensaje[0] == "t":
                    self.Disp_temp =  (int(self.mensaje[2:])) #'{:03d}'.format Recibe la temperatura y humedad desde el arduino.
                    self.mensaje = " "    
            self.last_update_time = time.time()  # Actualizar el tiempo de la última actualización
        except serial.SerialException as e:
            print(f"Error al enviar datos a Arduino: {e}")



    def setupUi(self, MainWindow):


        def __init__(self):
            super().__init__()
            self.setWindowTitle("PyQt5 Video Stream")
            self.setGeometry(100, 100, 800, 600)
            
            self.video_stream_widget = VideoStreamWidget()
            self.setCentralWidget(self.video_stream_widget)












#Activa la interfaz
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())