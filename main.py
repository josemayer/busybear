import os
import telegram
from telegram.ext import Updater, CommandHandler

def start(update, context):
    update.message.reply_text("Olá! Eu sou o BusyBear, o bot que encontra o melhor ponto de ônibus para pegar o seu circular na USP!")

def bus(update, context):
    update.message.reply_text("Ainda não tenho acesso à API de ônibus da USP. Sinto muito! =(")

def main():
    telegram_token = os.environ.get("TELEGRAM_TOKEN")
    updater = Updater(telegram_token, use_context=True)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("bus", bus))

    # Start the Bot
    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    main()

