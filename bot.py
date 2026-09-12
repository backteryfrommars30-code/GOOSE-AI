import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from google import genai

# Ваши ключи
BOT_TOKEN = "8419211060:AAE68d2WxeS_KZIIU43dt43MdBhP3NSZpjE"
GEMINI_API_KEY = "AQ.Ab8RN6Lj1ZwwQ8gdG_hGUn1GiqRGXnQ02FeUPN9wE_ZYUXiAww"

# Инициализация Gemini и Telegram
ai_client = genai.Client(api_key=GEMINI_API_KEY)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def start_handler(message: types.Message):
    await message.answer("Привет! Я готов отвечать на твои вопросы с помощью Gemini!")

@dp.message()
async def generate_response(message: types.Message):
    # Показываем статус "печатает..."
    await bot.send_chat_action(chat_id=message.chat.id, action="typing")
    
    try:
        # Отправка запроса к Gemini 2.5 Flash
        response = ai_client.models.generate_content(
            model="gemini-2.5-flash",
            contents=message.text,
        )
        
        if response.text:
            await message.reply(response.text)
        else:
            await message.reply("Не удалось получить текст ответа.")
            
    except Exception as e:
        logging.error(f"Ошибка: {e}")
        await message.reply("Произошла ошибка при обращении к ИИ.")

async def main():
    logging.basicConfig(level=logging.INFO)
    print("Бот запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())