import os
import requests
import telegram
import functions.geolocator
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

def start(update, context):
    update.message.reply_text("Olá! Eu sou o BusyBear, o bot que encontra o melhor ponto de ônibus para pegar o seu circular na USP!")

def bus(update, context):
    location = update.message.location
    if location:
        center = (location.latitude, location.longitude)

        points = requests.get('https://uspdigital.usp.br/mobile/servicos/mapa/locais?campus=cidade-universitaria&categorias=transportes').json()
        candidate_points = []

        for point in points:
            coords_point = (float(point["latitude"]), float(point["longitude"]))
            if functions.geolocator.is_within_radius(center, coords_point):
                candidate_points.append(point["titulo"])

        update.message.reply_text("Aqui estão os pontos até 250m próximos de você: {}".format(str(candidate_points)))
    else:
        update.message.reply_text("Por favor, compartilhe sua localização comigo para obter os dados dos pontos de ônibus.")

def main():
    telegram_token = os.environ.get("TELEGRAM_TOKEN")
    updater = Updater(telegram_token, use_context=True)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.location, bus))

    # Start the Bot
    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    main()

