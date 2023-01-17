import asyncio
import json
import logging
import sys

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from decouple import config
from validators import url as url_check

from caller import short_url

LOG_FILE = 'logs/main_log.txt'
MESSAGES_FILE = 'templates/messages.json'
WHITELIST_FILE = 'templates/whitelist.json'
TOKEN = config('TOKEN')
ADMIN = int(config('ADMIN'))
whitelist = json.load(open(WHITELIST_FILE))

logging.basicConfig(level=logging.INFO, filename=LOG_FILE, filemode='a',
                    format="%(asctime)s %(levelname)s %(message)s")
logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))

with open(MESSAGES_FILE, encoding='utf8') as json_f:
    MESSAGES = json.load(json_f)

# Preparing the storage for a dialog (/edituser command).
storage = MemoryStorage()
bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot, storage=storage)


# It will be needed for storing the answer after /edituser command.
class Form(StatesGroup):
    edituser = State()


@dp.message_handler(commands=["start"])
async def start_handler(message: types.Message):
    # Handles the '/start' command.
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    logging.info(f"{user_id}: {message['text']}")
    if user_id not in whitelist:
        # Checking if the user is allowed to use the bot.
        logging.warning(f"{user_id} not in the whitelist: {whitelist}.")
        await message.reply(MESSAGES['DENIED_MSG'].format(user_name))
    else:
        # Responding to the user, if he's in the whitelist.
        logging.info(f"{user_id} is in the WHITELIST: {whitelist}")
        await message.reply(MESSAGES['WELCOME_MSG'].format(user_name))
        await asyncio.sleep(2)
        await bot.send_message(user_id, MESSAGES['HOWTO_MSG'])


@dp.message_handler(commands=["showusers"])
async def showusers_handler(message: types.Message):
    # Handles the '/showusers' command.
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    logging.info(f"{user_id}: {message['text']}")
    if user_id != ADMIN:
        # Checking if the user is an administrator.
        logging.warning(f"{user_id} is not an ADMIN.")
        await message.reply(MESSAGES['NOT_ADMIN'].format(user_name))
    else:
        await message.reply(
            f"The list of users in the whitelist: {whitelist}.")


@dp.message_handler(commands=["edituser"])
async def edituser_handler(message: types.Message):
    # Handles the '/edituser' command.
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    logging.info(f"{user_id}: {message['text']}")
    if user_id != ADMIN:
        # Checking if the user is an administrator.
        logging.warning(f"{user_id} is not an ADMIN.")
        await message.reply(MESSAGES['NOT_ADMIN'].format(user_name))
    else:
        await Form.edituser.set()
        await message.reply(MESSAGES['EDIT_USER'])


@dp.message_handler(state='*', commands=['cancel'])
async def cancel_handler(message: types.Message, state: FSMContext):
    # Handles the '/cancel' command.
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    logging.info(f"{user_id}: {message['text']}")
    if user_id != ADMIN:
        logging.warning(f"{user_id} is not an ADMIN.")
        await message.reply(MESSAGES['NOT_ADMIN'].format(user_name))
    else:
        current_state = await state.get_state()
        if current_state is None:
            return
        await state.finish()
        await message.reply(MESSAGES['CANCELLED'])


@dp.message_handler(state=Form.edituser)
async def process_name(message: types.Message, state: FSMContext):
    # Catching the answer for the /edituser command.
    await state.finish()
    user_id = message.from_user.id
    logging.info(f"{user_id}: {message['text']}")
    try:
        # Checking if the answer contains only int value.
        editing_user = int(message.text)
        if editing_user in whitelist:
            # Checking if the ID already in the list.
            whitelist.remove(editing_user)
            await message.reply(MESSAGES['DELETED_FROM_WL'])
        elif editing_user not in whitelist:
            whitelist.append(editing_user)
            await message.reply(MESSAGES['ADDED_TO_WL'])
        json.dump(whitelist, open(WHITELIST_FILE, 'w'))
    except ValueError:
        # Send an error message if the input was incorrect.
        await message.reply(MESSAGES['WRONG_ID_INPUT'])


@dp.message_handler()
async def message_handler(message: types.Message):
    # Handles every message without specified command.
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    logging.info(f"{user_id}: {message['text']}")
    # Checking if user is allowed to use private bot.
    if user_id not in whitelist:
        await message.reply(MESSAGES['DENIED_MSG'].format(user_name))
    else:
        # Checking if the message from user contains valid URL adress.
        if url_check(message.text, public=True):
            url = short_url(message.text)
            logging.info(f"{user_id}: {url}")
            await message.reply(MESSAGES['SHORT_URL'].format(url))
        else:
            logging.warning(f"{user_id}: ivalid URL.")
            await message.reply(MESSAGES['INVALID_URL'])


if __name__ == "__main__":
    executor.start_polling(dp)
