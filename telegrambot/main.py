import telebot

TOKEN = 'xxxxxxxxxxx'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(message, 'En esta funcion tu puedes iniciar el programa de riego')

@bot.message_handler(commands=['regar'])
def send_help(message):
    bot.reply_to(message, 'empezara el sistema de riego')

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)

if __name__ == "__name__":
    bot.polling(none_stop=True)

bot.infinity_polling()