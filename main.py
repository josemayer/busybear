import os
import requests
import telegram
import json
import functions.geolocator
import functions.buses
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

def start(update, context):
    update.message.reply_text("Olá! Eu sou o BusyBear, o bot que encontra o melhor ponto de ônibus para pegar o seu circular na USP!")

def bus(update, context):
    location = update.message.location
    if location:
        center = (location.latitude, location.longitude)

        candidate_points = []
        with open("data/points.json", "r") as points_file:
            points = json.load(points_file)
            for point in points:
                coords_point = (float(point["lat"]), float(point["lng"]))
                if functions.geolocator.is_within_radius(center, coords_point):
                    candidate_points.append(point["titulo"])

        update.message.reply_text("Aqui estão os pontos até 250m próximos de você: {}".format(str(candidate_points)))
    else:
        update.message.reply_text("Por favor, compartilhe sua localização comigo para obter os dados dos pontos de ônibus.")

def list_buses(update, context):
    args = context.args
    
    if len(args) < 1:
        update.message.reply_text("Digite o sentido da linha (*p3* ou *butanta*)!", parse_mode=telegram.ParseMode.MARKDOWN)
        return

    way = args[0]
    buses = functions.buses.retrieve_buses(way)

    with open("data/points.json", "r") as points_file:
        points = json.load(points_file)        
        buses_and_points_str = "*Lista de ônibus nos pontos:* \n\n"
        for bus in buses:
            bus_location = (bus["lat"], bus["lng"])
            closest_point = functions.geolocator.closest_point(bus_location, points)

            buses_and_points_str += f"- *{bus['bus_line']}*: {closest_point['titulo']}\n"

        update.message.reply_text(buses_and_points_str, parse_mode=telegram.ParseMode.MARKDOWN)
        


def main():
    telegram_token = os.environ.get("TELEGRAM_TOKEN")
    updater = Updater(telegram_token, use_context=True)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.location, bus))
    dp.add_handler(CommandHandler("list_buses", list_buses))

    # Start the Bot
    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    main()

