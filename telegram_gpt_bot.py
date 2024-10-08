import requests
import telebot
from telebot import types

bot = telebot.TeleBot('7762731734:AAE2lTiIPZD8kz6Zd55AzIL6ie8RUg_AIJs')


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    with open('C:/Users/User/OneDrive/Рабочий стол/2.png', 'rb') as photo:
        bot.send_photo(message.from_user.id, photo, caption='Привет!', reply_markup=markup, parse_mode='Markdown')


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    prompt = {
        "modelUri": "gpt://b1g1nh4208ekvnfp0nrv/yandexgpt/latest",
        "completionOptions": {
            "stream": False,
            "temperature": 0.6,
            "maxTokens": "2000"
        },
        "messages": [
            {
                "role": "system",
                "text": "Ты BauAI — строительный консультант, который помогает находить проверенные компании и решения по широкому спектру строительных задач."
            },
            {
                "role": "user",
                "text": message.text
            }
        ]
    }

    url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Api-KeyAQVNzXbvmsYXgEzZXhwk-aLs7nEnRYTzfGZUjJL4"
    }

    response = requests.post(url, headers=headers, json=prompt)
    result = response.json()
    text_response = result["result"]["alternatives"][0]["message"]["text"]

    bot.send_message(message.from_user.id, text_response,parse_mode='Markdown')

bot.polling(none_stop=True, interval=0)
