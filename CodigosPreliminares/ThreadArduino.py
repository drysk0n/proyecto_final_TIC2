import sys
import cv2

from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QPushButton
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtCore import QTimer
import telebot
import threading
from dotenv import load_dotenv
import os

import numpy as np
import serial
import time


load_dotenv()

# Aquí se activa la camara:
class VideoStreamWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.video_label = QLabel(self)
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.video_label)

        # Add a button to save the image
        self.save_button = QPushButton("Guardar Imagen")
        self.save_button.clicked.connect(self.save_image)
        self.layout.addWidget(self.save_button)

        self.setLayout(self.layout)

        self.cap = cv2.VideoCapture(0)
        self.current_frame = None

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)

    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.current_frame = frame
            image = QImage(frame, frame.shape[1], frame.shape[0], frame.strides[0], QImage.Format.Format_RGB888)
            self.video_label.setPixmap(QPixmap.fromImage(image))

    def save_image(self):
        if self.current_frame is not None:
            # Save the current frame using OpenCV
            filename = 'captured_image.jpg'
            frame_bgr = cv2.cvtColor(self.current_frame, cv2.COLOR_RGB2BGR)
            cv2.imwrite(filename, frame_bgr)
            print(f"Image saved as {filename}")

    def closeEvent(self, event):
        self.cap.release()
        event.accept()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Interfaz del regador")
        self.x = 120
        self.setGeometry(100, 100, 800, 600)

        self.video_stream_widget = VideoStreamWidget()
        self.setCentralWidget(self.video_stream_widget)

        self.setup_serial()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.LecturaArduino)
        self.timer.start(1000)  # Call LecturaArduino every second

        # Replace this with the actual chat id
        chat_id = 1402695223
        bot.send_message(chat_id, "La interfaz se ha iniciado")

    def setup_serial(self):  # Crea la conexión con el arduino
        try:
            self.arduino = serial.Serial('COM6', 9600)
            self.last_update_time = time.time()
        except serial.SerialException as e:
            print(f"Error al abrir el puerto serial: {e}")
            sys.exit(1)

    def LecturaArduino(self):  # Es la función que manda y recibe datos del arduino
        try:
            self.arduino.write('hola'.encode())  # Le manda información al arduino.
            if self.arduino.in_waiting > 0:
                self.mensaje = self.arduino.readline().decode().strip()  # Recibe, lee y almacena un mensaje mandado desde arduino
                print(self.mensaje, type(self.mensaje))
                if self.mensaje[0] == "t" and self.gol_widget.game.RecibeTemp == True:
                    Disp_temp = (int(self.mensaje[2:]))  # '{:03d}'.format Recibe la temperatura y humedad desde el arduino.
                    self.mensaje = " "
            self.last_update_time = time.time()  # Actualizar el tiempo de la última actualización
        except serial.SerialException as e:
            print(f"Error al enviar datos a Arduino: {e}")


# Access the bot token from your .env file
bot_token = os.getenv("BOT_TOKEN")

bot = telebot.TeleBot(bot_token)
window = None


@bot.message_handler(commands=['check_x'])
def handle_valor(message):
    value = window.x
    bot.reply_to(message, f"El valor de x es: {value}")
    print(f"El id del usuario que envió el mensaje es: {message.chat.id}")


@bot.message_handler(commands=['check_y'])
def handle_valor(message):
    value = window.x
    bot.reply_to(message, f"El valor de y es: {value}")
    print(f"El id del usuario que envió el mensaje es: 2 {message.chat.id}")




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