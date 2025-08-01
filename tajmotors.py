import asyncio
import logging
from config_reader import config

from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command

from datetime import datetime

from aiogram import F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.enums import ParseMode 

#Turn on logging, not to miss important messages
logging.basicConfig(level=logging.INFO)

#Bot as an object(hide token#)
# For entries with type Secret* you need to
# call the get_secret_value() method,
# to get the real content instead of '*******'
bot = Bot(token= config.bot_token.get_secret_value())

# The dispatcher receives updates from Telegram, which can include various types of interactions like messages, commands, or other events.
#Dispatcher
dp = Dispatcher()
# dp["started_at"] = datetime.now().strftime("%Y/%m/%d, %H:%M:%S")
    
@dp.message(Command("start"))
async def any_message(message: Message):
    await message.answer(
        f"Hello, <b>{message.from_user.full_name}</b> , welcome to <em><b>TajMotors</b></em>!", 
        parse_mode=ParseMode.HTML
    )
    # await message.answer(
    #     f"Hello, welcome to *TajMotors*\!",
    #     parse_mode=ParseMode.MARKDOWN_V2
    # )
    
#Start process of polling new proccesses
async def main():
    await dp.start_polling(bot)
    
    
# #Handler for command /start
# @dp.message(Command("start"))
# async def cmd_start(message: types.Message):
#     await message.answer("Welcome to TajMotors Bot! Please select option you would like to have:")

if __name__ == "__main__":
    asyncio.run(main())
    
