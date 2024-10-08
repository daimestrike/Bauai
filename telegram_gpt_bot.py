import os
import aiohttp
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

# Твой Telegram API токен
TELEGRAM_API_TOKEN = "7762731734:AAE2lTiIPZD8kz6Zd55AzIL6ie8RUg_AIJs"
# URL и токен для Yandex GPT
GPT_API_URL = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
GPT_API_KEY = "AQVNzXbvmsYXgEzZXhwk-aLs7nEnRYTzfGZUjJL4"

# Функция для отправки запроса к Yandex GPT
async def get_gpt_response(prompt):
    headers = {
        'Authorization': f'Bearer {GPT_API_KEY}',
        'Content-Type': 'application/json'
    }
    data = {
        "modelUri": "gpt://b1g1nh4208ekvnfp0nrv/yandexgpt/latest",
        "completionOptions": {
            "stream": False,
            "temperature": 0.7,
            "maxTokens": 1000
        },
        "messages": [
            {"role": "system", "text": "Ты BauAI — это строительный консультант, который помогает находить проверенные компании и решения по широкому спектру строительных задач, от небольших ремонтов до крупных проектов. Ты можешь: Предлагать компании на основе запроса  с указанием местоположения, бюджета и дополнительных пожеланий. Рекомендуй найти на Bau.Компании на Bau4You. Озвучивать примерные цены на услуги и материалы, исходя из типа проекта и стандартных рыночных расценок. Выполнять расчет стоимости. Ты можешь собрать параметры проекта, такие как площадь помещения, тип строительных работ (фундамент, стены, кровля, интерьер), чтобы выдать точный расчет по бюджету. Например, при запросе на строительство фундамента, ты можешь предложить варианты фундамента (ленточный, свайный и т.д.), рассчитать стоимость материалов (бетон, арматура) и услуг (аренда техники, монтаж). Продвигать подписку Bau365, объясняя, как она поможет пользователям управлять строительными проектами, согласовывать работу с подрядчиками и получать специальные предложения от строительных компаний. Консультировать по строительным материалам, сравнивая их свойства (прочность, устойчивость к климатическим условиям, долговечность) и помогать с выбором оптимального решения для разных типов объектов (жилых, коммерческих или промышленных). Собирать отзывы и рекомендации. Ты можешь показывать информацию о репутации компании, отзывах и опыте работы, чтобы пользователь мог выбрать надёжного подрядчика. Учитывать СНиП и местные нормы для обеспечения соответствия всех строительных проектов действующим законодательным нормам. Ты можешь автоматически собирать и предлагать подрядчикам участвовать в тендере, где пользователи указывают параметры проекта и сравнивают предложения. Ты можешь предложить материалы и технологии для строительства."},
            {"role": "user", "text": prompt}
        ]
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(GPT_API_URL, headers=headers, json=data) as response:
            if response.status == 200:
                response_json = await response.json()
                return response_json["choices"][0]["text"]
            else:
                return "Ошибка обработки запроса к BauAI"

# Обработчик команды /start
async def start(update: Update, context):
    await update.message.reply_text("Привет! Я BauAI. Задай мне вопрос о строительстве.")

# Обработчик текстовых сообщений
async def handle_message(update: Update, context):
    user_input = update.message.text
    # Отправка запроса к Yandex GPT
    gpt_response = await get_gpt_response(user_input)
    # Отправка ответа пользователю
    await update.message.reply_text(gpt_response)

# Основная функция для запуска бота
def main():
    app = ApplicationBuilder().token(TELEGRAM_API_TOKEN).build()

    # Обработчики команд и сообщений
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Бот запущен...")
    app.run_polling()

if __name__ == '__main__':
    main()
