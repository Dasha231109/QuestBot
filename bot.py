import random
import telebot
from game import *
from telebot import types
from data import *

TOKEN = '6669866373:AAFqqSNb2BzbMSsnwy2Hzbd46ddTBoOvY5w'  # @UninhabitedIsland_bot и ссылка на облако
bot = telebot.TeleBot(token=TOKEN)                        # https://disk.yandex.ru/a/_ucGGh2iPzhmiA



@bot.message_handler(commands=['start', 'help', 'rules'])
def send_commands(message):
    if message.text == "/start":
        bot.send_message(message.chat.id, commands["start"])
        user_data[message.chat.id] = {"location": "start"}
        send_location(message.chat.id)
    elif message.text == "/help":
        bot.send_message(message.chat.id, commands["help"])
    elif message.text == "/rules":
        bot.send_message(message.chat.id, commands["rules"])


def send_location(chat_id):
    current_location = user_data[chat_id]["location"]
    quest_data = quest[current_location]
    description = quest_data["description"]
    answer = quest_data["options"]
    image = random.choice(quest_data["img"])

    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)

    for text in answer.keys():
        markup.add(text)

    with open(image, "rb") as photo:
        bot.send_photo(chat_id, photo)

    bot.send_message(chat_id, description, reply_markup=markup)


@bot.message_handler(func=lambda message: True)
def handle_answer(message):
    chat_id = message.chat.id
    if chat_id not in user_data:
        bot.send_message(message.chat.id, "Пожалуйста, начните игру с помощью команды /start")
        return
    current_location = user_data[chat_id]["location"]
    answer = quest[current_location]["options"]

    if message.text not in answer:
        with open("img/ошибка.jpg", "rb") as photo:
            bot.send_photo(chat_id, photo)
            bot.send_message(message.chat.id, "Неверный ввод, пожалуйста, выберите один из предложенных вариантов.")
        return

    user_data[chat_id]["location"] = answer[message.text]
    send_location(chat_id)

    save_data_user(user_data)


bot.polling(non_stop=True)
