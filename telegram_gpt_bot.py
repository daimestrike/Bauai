import aiohttp
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

TELEGRAM_API_TOKEN = "YOUR_TELEGRAM_TOKEN"
GPT_API_URL = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
GPT_API_KEY = "YOUR_YANDEX_API_KEY"

async def get_gpt_response(prompt):
    headers = {
        'Authorization': f'Api-Key {GPT_API_KEY}',
        'Content-Type': 'application/json',
        'x-folder-id': 'b1g1nh4208ekvnfp0nrv',
    }
    data = {
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
            {"role": "user", "text": prompt}
        ]
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(GPT_API_URL, headers=headers, json=data) as response:
            response_text = await response.text()
            if response.status == 200:
                response_json = await response.json()
                return response_json.get("choices", [{}])[0].get("text", "Нет ответа")
            else:
                return f"Ошибка обработки запроса к BauAI: {response.status} - {response_text}"

# Остальной код без изменений...

async def start(update: Update, context):
    await update.message.reply_text("Привет! Я BauAI. Задай мне вопрос о строительстве.")

async def handle_message(update: Update, context):
    user_input = update.message.text
    gpt_response = await get_gpt_response(user_input)
    await update.message.reply_text(gpt_response)

def main():
    app = ApplicationBuilder().token(TELEGRAM_API_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Бот запущен...")
    app.run_polling()

if __name__ == '__main__':
    main()
