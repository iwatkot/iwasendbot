`reserved for code climate bade`

## Overview
This telegram bot uses `short.io API` for URL shortening in `caller.py` script. The bot is built on `aiogram` with `asyncio`.<br>
By design this's a private bot, which using `ALLOWED_IDS` list from an extrenal file (which is not presented in the repo). `ALLOWED_IDS` should contain a string with unique telegram ids separated by whitespaces. The external file also should contain telegram bot `TOKEN` along with short.ai `API_KEY` and `DOMAIN` which contains your own domain, which should be used for URL shortening.<br>
The directory `templates` contains `messages.json` file, which stores message templates for bot to send to the users.

## Commands
There's only one initial command available:<br>
`/start` - when user first interactes with bot
In other cases the bot expects to recieve a valid URL adress.

## Behavior
The bot reading `user_id` from `message.from_user` and checking if this ID is presented in the `ALLOWED_IDS`. If not, the bot will send `DENIED_MSG` from message templates. Otherwise the bot will be expecting message, which contains **valid public URL**. If it's not (module responsible for checking is `validators.url`), the bot will reply with `INVALID_MSG` template. If the URL is correct, the bot will launch `caller.py` scripts and will send the shortened URL to the user.