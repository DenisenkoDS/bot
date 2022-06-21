import os
import logging
import transliterate

from aiogram import Bot, Dispatcher, executor, types
from transliterate import translit

from Token import TOKEN
# TOKEN = os.getenv('TOKEN')

logging.basicConfig(filename='textsave.txt', 
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
                    datefmt='%Y-%m-%d:%H:%M:%S',
                    level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    user_name = message.from_user.full_name
    user_id = message.from_user.id
    text = f'Привет {user_name}, напиши свои ФИО на кириллице.'
    logging.info(f"{user_name=} {user_id=} sent message: {message.text}")
    await message.reply(text)

@dp.message_handler(content_types=['text'])
async def send_translation(message: types.Message):
    user_name = message.from_user.full_name
    user_id = message.from_user.id
    text = message.text.upper().replace('Ь', '').replace('-', '').replace('Я', 'ИА').replace('Ю', 'ИУ')
    text = (translit(text, language_code='ru', reversed=True)).upper()
    logging.info(f"{user_name=} {user_id=} sent message: {text}")
    await bot.send_message (message.chat.id, text)

if __name__ == '__main__':
    executor.start_polling(dp)