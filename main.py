import asyncio
import json
import logging
import sys

from aiogram import Bot, Dispatcher, executor, types
from decouple import config
from validators import url as url_check

from caller import short_url

LOG_FILE = 'logs/main_log.txt'
MESSAGES_FILE = 'templates/messages.json'
TOKEN = config('TOKEN')
ALLOWED_IDS = list(map(int, config('ALLOWED_IDS').split()))

logging.basicConfig(level=logging.INFO, filename=LOG_FILE, filemode='a',
                    format="%(asctime)s %(levelname)s %(message)s")
logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))

with open(MESSAGES_FILE, encoding='utf8') as json_f:
    messages = json.load(json_f)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot)


@dp.message_handler(commands=["start"])
async def start_handler(message: types.Message):
    # Handles the '/start' command.
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    logging.info(f"{user_id}: {message['text']}")
    if user_id not in ALLOWED_IDS:
        logging.warning(f"{user_id} not in ALLOWED_IDS: {ALLOWED_IDS}")
        await message.reply(messages['DENIED_MSG'].format(user_name))
    else:
        logging.info(f"{user_id} is in ALLOWED_IDS: {ALLOWED_IDS}")
        await message.reply(messages['WELCOME_MSG'].format(user_name))
        await asyncio.sleep(2)
        await bot.send_message(user_id, messages['HOWTO_MSG'])


@dp.message_handler()
async def message_handler(message: types.Message):
    # Handles every message without specified command.
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    logging.info(f"{user_id}: {message['text']}")
    # Checking if user is allowed to use private bot.
    if user_id not in ALLOWED_IDS:
        await message.reply(messages['DENIED_MSG'].format(user_name))
    else:
        # Checking if the message from user contains valid URL adress.
        if url_check(message.text, public=True):
            url = short_url(message.text)
            logging.info(f"{user_id}: {url}")
            await message.reply(messages['SHORT_URL'].format(url))
        else:
            logging.warning(f"{user_id}: ivalid URL.")
            await message.reply(messages['INVALID_URL'])


if __name__ == "__main__":
    executor.start_polling(dp)
