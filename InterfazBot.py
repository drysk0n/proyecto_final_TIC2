

import sys
import cv2

from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QDial, QLCDNumber,QLabel, QPushButton
from PyQt6.QtGui import QImage, QPixmap, QFont
from PyQt6.QtCore import QTimer, QRect
import telebot
import threading
from dotenv import load_dotenv
import os

import numpy as np
import serial
import time

load_dotenv()

#Aquí se activa la camara:
class VideoStreamWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.video_label = QLabel(self)

        #Tamaño de la ventana
        self.video_label.setGeometry(0, 0, 300, 400)  
        self.cap = cv2.VideoCapture(0)
        self.current_frame = None

        #Toma la resolución maxima de la camara
        self.max_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.max_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        #Redefine el tamaño en funcion de la resolución maxima
        self.video_label.setFixedSize(self.max_width, self.max_height)

        self.timer = QTimer(self) #Actualiza el frame mostrado cada 30 milisegundos
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)

    def update_frame(self):  #La función que se encarga de acutalizar el frame
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.current_frame = frame
            image = QImage(frame, frame.shape[1], frame.shape[0], frame.strides[0], QImage.Format.Format_RGB888)
            self.video_label.setPixmap(QPixmap.fromImage(image))

    def save_image(self): #Guarda la imagen en un archivo:
        if self.current_frame is not None:
            filename = 'ImagenGuardada.png'
            frame_bgr = cv2.cvtColor(self.current_frame, cv2.COLOR_RGB2BGR)
            cv2.imwrite(filename, frame_bgr)
            print(f"se guardo la imagen como: {filename}")


    def closeEvent(self, event):
        self.cap.release()
        event.accept()




# Obtiene el token del bot desde el archivo .env
bot_token = os.getenv("BOT_TOKEN")

bot = telebot.TeleBot(bot_token)
window = None

#Registra la tempera y humedad desde el arduino:
Disp_temp: int = 0
Disp_hum: int = 0 

UltimoModo: str 

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.x = 120 #Prueba de que el bot lee corectamente la interfaz.
        self.setWindowTitle("Interfaz del regador")
        self.setGeometry(0, 0, 1000, 800)


        # Imagen de Fondo:
        background_label = QLabel(self)
        pixmap = QPixmap('FondoInterfaz.png')  # Replace with your image path
        background_label.setPixmap(pixmap)
        background_label.setGeometry(0, 0, 1000, 800)  # Set size to match window size 
        background_label.lower()  # Lower the background label to the bottom

        #Elemento central de la Interfaz
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Camara
        self.video_stream_widget = VideoStreamWidget()
        layout.addWidget(self.video_stream_widget)

        # Boton Guardar Imagen:
        self.save_button = QPushButton("Guardar Imagen", self)
        self.save_button.setGeometry(0, 500, 650, 50)  # posicioon (x,y) y tamaño (ancho, largo)
        self.save_button.clicked.connect(self.video_stream_widget.save_image)


        #Medidor de temperatura y humedad:
        self.number_label = QLabel(self)
        self.number_label.setGeometry(680, 70, 150, 50)  
        font = QFont()
        font.setPointSize(24)  
        self.number_label.setFont(font)
        self.number_label.setText(str(f"{Disp_temp}"))


        #Texto sobre el medidor:
        self.label_3 = QLabel(self)
        self.label_3.setGeometry(680, 60, 220, 12)
        font = QFont()
        font.setPointSize(10)
        self.label_3.setFont(font)
        self.label_3.setText("Temperatura y Humedad:")


        #Boton Modo Automatico:
        self.pushButton_Auto = QPushButton(self)
        self.pushButton_Auto.setGeometry(80, 680, 171, 61)
        font = QFont()
        font.setPointSize(9)
        self.pushButton_Auto.setFont(font)
        self.pushButton_Auto.clicked.connect(self.MensajeArduino1)
        self.pushButton_Auto.setText("Alternar automatico/manual")


        #Boton Activar bomba
        self.pushButton_Riego = QPushButton(self)
        self.pushButton_Riego.setGeometry(280, 680, 171, 61)
        font = QFont()
        font.setPointSize(9)
        self.pushButton_Riego.setFont(font)
        self.pushButton_Riego.clicked.connect(self.MensajeArduino2)
        self.pushButton_Riego.setText("Regar")









        # Manda el mensaje inicial al bot
        chat_id = 1402695223
        bot.send_message(chat_id, "Hola! este es el bot que controla remotamente el regado de tu planta, si necesitas ver la lista de comandos porfavor escribe  /help.")



        self.setup_serial()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.LecturaArduino)
        self.timer.start(1000)  # llama a LecturaArduino cada segundo


    def setup_serial(self):  # Crea la conexión con el arduino
        try:
            self.arduino = serial.Serial('COM6', 9600)
            self.last_update_time = time.time()
        except serial.SerialException as e:
            print(f"Error al abrir el puerto serial: {e}")
            sys.exit(1)

    def LecturaArduino(self):  # Es la función que recibe datos del arduino
        try:
            if self.arduino.in_waiting > 0:
                self.mensaje = self.arduino.readline().decode().strip()  # Recibe, lee y almacena un mensaje mandado desde arduino
                print(self.mensaje, type(self.mensaje))
                if self.mensaje[0] == "t":
                    global Disp_temp 
                    global Disp_hum
                    Disp_temp = (int(self.mensaje[2:5]))  # Recibe la temperatura y humedad desde el arduino.
                    Disp_hum = (int(self.mensaje[8:11]))  # Recibe la temperatura y humedad desde el arduino.
                    self.number_label.setText(str(f"{Disp_temp}C°, {Disp_hum}%")) #Actualiza la temperatura y la humedad mostradas en el arduino
                    self.mensaje = " "
                    print(Disp_temp,Disp_hum)
                elif self.mensaje[0] == "M":
                    global UltimoModo 
                    UltimoModo = self.mensaje
            self.last_update_time = time.time()  # Actualizar el tiempo de la última actualización
        except serial.SerialException as e:
            print(f"Error al recibir datos del Arduino: {e}")

    def MensajeArduino1(self):  # Es la función que manda datos al arduino
        try:
            self.arduino.write('auto'.encode())  # Le manda información al arduino.
        except serial.SerialException as e:
            print(f"Error al enviar datos al Arduino: {e}")

    def MensajeArduino2(self):  # Es la función que manda datos al arduino
        try:
            self.arduino.write('watr'.encode())  # Le manda información al arduino.
        except serial.SerialException as e:
            print(f"Error al enviar datos al Arduino: {e}")



#Comandos del bot de telegram:


@bot.message_handler(commands=['start'])
def handle_valor(message):
    bot.reply_to(message, "Hola! este es el bot que controla remotamente el regado de tu planta, si necesitas ver la lista de comandos porfavor escribe  /help.")
    print(f"El id del usuario que envió el mensaje es: {message.chat.id}")


@bot.message_handler(commands=['check_x'])
def handle_valor(message):
    value = window.x
    bot.reply_to(message, f"El valor de x es: {value} y {Disp_temp}")
    print(f"El id del usuario que envió el mensaje es: {message.chat.id}")

@bot.message_handler(commands=['data'])
def handle_valor(message):
    value = window.x
    bot.reply_to(message, f"La temperatura de la planta es {Disp_temp}C° y la humedad registrada es de {Disp_temp}%")
    print(f"El id del usuario que envió el mensaje es: {message.chat.id}")

@bot.message_handler(commands=['help'])
def handle_valor(message):
    bot.reply_to(message, "Los comandos implementados en este bot son los siguientes: \n \n /start: inicializa el bot \n \n /help: da una lista de comandos. \n \n /regar: Activa remotamente la bomba. \n \n /camera: entrega una imagen de la planta. \n \n /auto: activa el regado automatico de la planta. \n \n /data: entrega la información de humedad y temperatura del sensor.")

@bot.message_handler(commands=["camera"])
def send_image(message):    
    global window
    if window:
        window.video_stream_widget.save_image()
    bot.reply_to(message, "Aquí tienes una imagen del estado de tu planta:")
    photo = open('ImagenGuardada.png', 'rb')
    bot.send_photo(message.chat.id, photo)

@bot.message_handler(commands=["regar"])
def handle_valor(message):    
    global window
    if window:
        window.MensajeArduino2()
    bot.reply_to(message, "Activando regado de la planta")


@bot.message_handler(commands=["auto"])
def handle_valor(message):    
    global window
    if window:
        window.MensajeArduino1()
    time.sleep(4)
    AuxText = "Modificando modo de regado, ahora corresponde a:" + UltimoModo
    bot.reply_to(message, AuxText )






def iniciar_bot():
    bot.infinity_polling()




def main():
    global window
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()



if __name__ == '__main__':
    bot_thread = threading.Thread(target=iniciar_bot)
    bot_thread.start()
    main()