import os
import requests
import telegram
import json
import functions.utils
import functions.geolocator
import functions.buses
import functions.messages
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackQueryHandler, Filters

def start(update, context):
    update.message.reply_text("Olá! Eu sou o BusyBear, o bot que encontra o melhor ponto de ônibus para pegar o seu circular na USP!")

def bus(update, context):
    location = update.message.location
    if location:
        center = (location.latitude, location.longitude)

        candidate_points = []
        points = functions.utils.get_json_data("data/points.json")
        for point in points:
            coords_point = (float(point["lat"]), float(point["lng"]))
            if functions.geolocator.is_within_radius(center, coords_point):
                candidate_points.append(point)
        candidate_points_names = [point["titulo"] for point in candidate_points]

        if len(candidate_points) == 0:
            update.message.reply_text("Não há pontos de ônibus próximos a você!")
            return

        user_data = {
            "center": center,
            "candidate_points": candidate_points
        }
        context.chat_data['user_data'] = user_data

        menu = [[InlineKeyboardButton("Sentido Butantã", callback_data='butanta')],
                [InlineKeyboardButton("Sentido Portaria 3", callback_data='p3')]]
        reply_markup = InlineKeyboardMarkup(menu)
        points_str = functions.messages.format_bullets(candidate_points_names)
        update.message.reply_text(f"Aqui estão os pontos até 250 m próximos de você:\n\n{points_str}\n\nQual o sentido do seu circular?", reply_markup=reply_markup)
    else:
        update.message.reply_text("Por favor, compartilhe sua localização comigo para obter os dados dos pontos de ônibus.")

def rank_bus_stops(update, context):
    query = update.callback_query
    query.answer()
    user_data = context.chat_data.get('user_data')
    way = query.data
    
    buses_and_points = functions.buses.buses_at_points_with_way(way)

    if len(buses_and_points) == 0:
        query.edit_message_text(text="Não há ônibus circulando no momento!")
        return

    ranked_points = functions.buses.rank_points(user_data["candidate_points"], user_data["center"], buses_and_points, way)
    
    if len(ranked_points) == 0:
        query.edit_message_text(text="Não há nenhum ônibus indo para o seu destino nos pontos próximos :(")
        return

    ranked_points_str = functions.messages.format_buses_arrival(ranked_points, "buses")
    query.edit_message_text(text=ranked_points_str, parse_mode=telegram.ParseMode.MARKDOWN)

def list_buses(update, context):
    args = context.args
    
    if len(args) < 1:
        update.message.reply_text("Digite o sentido da linha (*p3* ou *butanta*)!", parse_mode=telegram.ParseMode.MARKDOWN)
        return

    way = args[0]
    buses_and_points = functions.buses.buses_at_points_with_way(way)

    buses_and_points_str = "*Lista de ônibus nos pontos:* \n\n"
    for state in buses_and_points:
        buses_and_points_str += f"- *{state['bus']['bus_line']}*: {state['point']['titulo']}\n"

    update.message.reply_text(buses_and_points_str, parse_mode=telegram.ParseMode.MARKDOWN)

def main():
    telegram_token = os.environ.get("TELEGRAM_TOKEN")
    updater = Updater(telegram_token, use_context=True)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.location, bus))
    dp.add_handler(CommandHandler("list_buses", list_buses))
    dp.add_handler(CallbackQueryHandler(rank_bus_stops, pass_chat_data=True))

    # Start the Bot
    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    main()

