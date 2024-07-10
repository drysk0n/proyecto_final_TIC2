import telebot
from dotenv import load_dotenv
import os
# Carga las variables de entorno desde el archivo .env
load_dotenv()
# Accede al valor del token de tu bot
bot_token = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(bot_token)
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Hola!, quieres saber el estado de tu planta?")

@bot.message_handler(commands=["image"])

def send_image(message):
    photo = open('pothos.jpg', 'rb')
    bot.send_photo(message.chat.id, photo)
    
bot.infinity_polling()