import os
import requests
import telegram
import json
import functions.utils
import functions.geolocator
import functions.buses
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
                candidate_points.append(point["titulo"])

        if len(candidate_points) == 0:
            update.message.reply_text("Não há pontos de ônibus próximos a você!")
            return

        user_data = {
            "center": center,
            "points": candidate_points
        }
        context.chat_data['user_data'] = user_data

        menu = [[InlineKeyboardButton("Sentido Butantã", callback_data='butanta')],
                [InlineKeyboardButton("Sentido Portaria 3", callback_data='p3')]]
        reply_markup = InlineKeyboardMarkup(menu)
        update.message.reply_text(f"Aqui estão os pontos até 250m próximos de você: {str(candidate_points)}", reply_markup=reply_markup)
    else:
        update.message.reply_text("Por favor, compartilhe sua localização comigo para obter os dados dos pontos de ônibus.")

def rank_bus_stops(update, context):
    query = update.callback_query
    query.answer()
    user_data = context.chat_data.get('user_data')
    way = query.data

    context.bot.send_message(chat_id=update.effective_chat.id, text=f"Você selecionou o sentido {way}, está em {user_data['center']} e os pontos candidatos são {str(user_data['points'])}")

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

