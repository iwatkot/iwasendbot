<a href="https://codeclimate.com/github/iwatkot/iwasendbot/maintainability"><img src="https://api.codeclimate.com/v1/badges/fd0932ad1fd4cfd1dcd2/maintainability" /></a>
## To-Do
1. Change the logic for `ALLOWED_IDS` to be stored in an external file (txt or JSON) instead of `.env` fle.

## Overview
This telegram bot uses short.io API for URL shortening in **caller.py** script. The bot is built on **aiogram** with **asyncio**.<br>
By design this's a private bot, which using `ALLOWED_IDS` list from an extrenal file (which is not presented in the repo). `ALLOWED_IDS` should contain a string with unique telegram ids separated by whitespaces. The external file also should contain telegram bot `TOKEN` along with short.ai `API_KEY` and `DOMAIN` which contains your own domain that you're going to use for URL shortening.<br>
The directory **templates** contains `messages.json` and `whitelist.json`. The first one is serves for storing message templates, which bot uses to reply to the users. The second file doesn't appear in the repo and should contain the list of IDs, which are have permission to use the bot.

## Commands
There's only one initial command available for an ordinary user. And admin user can use two more commands.<br>
`/start` - when user first interactes with bot<br>
`/showusers` - **admin command**, which shows users, allowed to use the bot (from the whitelist)<br>
`/edituser` - **admin command**, which allows to edit the whitelist (add or remove users)<br>
In other cases the bot expects to recieve a valid URL adress.

## Behavior
The bot reading `user_id` from **message.from_user** and checking if this ID is presented in the `ALLOWED_IDS`. If not, the bot will send **DENIED_MSG** from message templates. Otherwise the bot will be expecting message, which contains **valid public URL**. If it's not (module responsible for checking is `validators.url`), the bot will reply with **INVALID_MSG** template. If the URL is correct, the bot will launch `caller.py` scripts and will send the shortened URL to the user.

## Changelog
**2023/01/17** Added admin commands and changed the way bot stores the list with users, allowed to use it.<br>
**2023/01/12** Added logging to `stdout`, should be working with `docker logs` too.