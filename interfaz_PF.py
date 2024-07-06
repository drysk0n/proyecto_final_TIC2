from PyQt6 import QtCore, QtGui, QtWidgets
import matplotlib
import random
import sys
import cv2
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

class Ui_hum(object):
    def setupUi(self, hum):
        hum.setObjectName("hum")
        hum.resize(600, 600)
        self.title_hum = QtWidgets.QLabel(parent=hum)
        self.title_hum.setGeometry(QtCore.QRect(200, 40, 300, 40))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.title_hum.setFont(font)
        self.title_hum.setObjectName("title_hum")
        self.gridLayoutWidget = QtWidgets.QWidget(parent=hum)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(50, 90, 521, 441))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.graf_hum = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.graf_hum.setContentsMargins(0, 0, 0, 0)
        self.graf_hum.setObjectName("graf_hum")

        self.canvas = MplCanvas(self.gridLayoutWidget, width=5, height=4, dpi=100)
        self.graf_hum.addWidget(self.canvas)

        self.timer = QtCore.QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.update_plot)
        self.timer.start()

        self.retranslateUi(hum)
        QtCore.QMetaObject.connectSlotsByName(hum)

    def retranslateUi(self, hum):
        _translate = QtCore.QCoreApplication.translate
        hum.setWindowTitle(_translate("hum", "Gráficos de Humedad"))
        self.title_hum.setText(_translate("hum", "Gráficos de humedad"))

    def update_plot(self):
        self.canvas.axes.cla()
        xdata = [0, 1, 2, 3, 4]
        ydata = [random.randint(0, 10) for _ in range(5)]
        self.canvas.axes.plot(xdata, ydata)
        self.canvas.draw()
#dibuja la grafica
class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)

class Ui_temp(object):
    def setupUi(self, temp):
        temp.setObjectName("temp")
        temp.resize(600, 600)
        self.gridLayoutWidget = QtWidgets.QWidget(parent=temp)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(50, 90, 521, 441))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.graftemp = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.graftemp.setContentsMargins(0, 0, 0, 0)
        self.graftemp.setObjectName("graftemp")
        self.title_temp = QtWidgets.QLabel(parent=temp)
        self.title_temp.setGeometry(QtCore.QRect(170, 40, 300, 40))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.title_temp.setFont(font)
        self.title_temp.setObjectName("title_temp")

        self.canvas = MplCanvas(self.gridLayoutWidget, width=5, height=4, dpi=100)
        self.graftemp.addWidget(self.canvas)

        self.timer = QtCore.QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.update_plot)
        self.timer.start()

        self.retranslateUi(temp)
        QtCore.QMetaObject.connectSlotsByName(temp)

    def retranslateUi(self, temp):
        _translate = QtCore.QCoreApplication.translate
        temp.setWindowTitle(_translate("temp", "Form"))
        self.title_temp.setText(_translate("temp", "Gráficos de temperatura"))

    def update_plot(self):
        self.canvas.axes.cla()
        xdata = [0, 1, 2, 3, 4]
        ydata = [random.randint(0, 10) for _ in range(5)]
        self.canvas.axes.plot(xdata, ydata)
        self.canvas.draw()




class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1060, 849)
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(parent=self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(390, 680, 281, 91))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(parent=self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(730, 680, 281, 91))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(parent=self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(350, 560, 371, 101))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_3.setFont(font)
        self.pushButton_3.setObjectName("pushButton_3")
        self.Temperatura_en_grados = QtWidgets.QLabel(parent=self.centralwidget)
        self.Temperatura_en_grados.setGeometry(QtCore.QRect(880, 10, 161, 51))
        self.Temperatura_en_grados.setObjectName("Temperatura_en_grados")
        self.Camara = QtWidgets.QLabel(parent=self.centralwidget)
        self.Camara.setGeometry(QtCore.QRect(140, 70, 781, 471))
        self.Camara.setObjectName("Camara")
        self.pushButton_4 = QtWidgets.QPushButton(parent=self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(50, 680, 281, 91))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_4.setFont(font)
        self.pushButton_4.setObjectName("pushButton_4")
        self.label = QtWidgets.QLabel(parent=self.centralwidget)
        self.label.setGeometry(QtCore.QRect(760, 10, 111, 41))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1060, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # Conectar botones a métodos para mostrar widgets
        self.pushButton.clicked.connect(self.mostrar_detalle_temperatura)
        self.pushButton_4.clicked.connect(self.mostrar_detalle_humedad)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "Detalle de temperatura"))
        self.pushButton_2.setText(_translate("MainWindow", "Mandar foto a Telegram"))
        self.pushButton_3.setText(_translate("MainWindow", "Activar riego automático"))
        self.Temperatura_en_grados.setText(_translate("MainWindow", "TextLabel"))
        self.Camara.setText(_translate("MainWindow", "TextLabel"))
        self.pushButton_4.setText(_translate("MainWindow", "Detalle de humedad"))
        self.label.setText(_translate("MainWindow", "Último riego:"))

    def mostrar_detalle_temperatura(self):
        self.detalle_temperatura = QtWidgets.QWidget()
        self.ui_temperatura = Ui_temp()
        self.ui_temperatura.setupUi(self.detalle_temperatura)
        self.detalle_temperatura.show()

    def mostrar_detalle_humedad(self):
        self.detalle_humedad = QtWidgets.QWidget()
        self.ui_humedad = Ui_hum()
        self.ui_humedad.setupUi(self.detalle_humedad)
        self.detalle_humedad.show()

#Integración de la camara en la interfaz
class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.cap = cv2.VideoCapture(0)  # 0 for default webcam
        self.timer.start(30)  # Update frame every 30 milliseconds

    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert frame to RGB format
            img = QtGui.QImage(frame, frame.shape[1], frame.shape[0], QtGui.QImage.Format_RGB888)
            pixmap = QtGui.QPixmap.fromImage(img)
            self.Camara.setPixmap(pixmap.scaled(self.Camara.size(), QtCore.Qt.KeepAspectRatio))
  

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())
