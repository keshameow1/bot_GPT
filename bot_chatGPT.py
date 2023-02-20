import os
import aiogram
import openai
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
bot_token = os.getenv("BOT_TOKEN")

bot = aiogram.Bot(token=bot_token)
dp = aiogram.Dispatcher(bot)

async def on_startup(_):
    print('Bot start')


@dp.message_handler()
async def handle_message(message: aiogram.types.Message):
    # Проверяем, что сообщение пришло не от бота
    if message.from_user.is_bot:
        return

    # Создаем промпт на основе входящего сообщения
    prompt = f"You: {message.text}\nFriend:"

    # Генерируем ответ на основе промпта
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=1.0,
        max_tokens=2048,
        top_p=1.0,
        frequency_penalty=0.5,
        presence_penalty=0.0,
        stop=["You:"]
    )

    # Отправляем сгенерированный ответ пользователю
    await bot.send_message(chat_id=message.chat.id, text=response.choices[0].text)


if __name__ == '__main__':
    aiogram.executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
