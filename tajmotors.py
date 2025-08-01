import asyncio
import logging
from config_reader import config

from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command

from datetime import datetime

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
dp["started_at"] = datetime.now().strftime("%Y/%m/%d, %H:%M:%S")

#Handler for command /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Welcome to TajMotors Bot! Please select option you would like to have:")
    
#Start process of polling new proccesses
async def main():
    await dp.start_polling(bot)
    
    
#Test1 Handler
@dp.message(Command("test1"))
async def cmd_test1(message: types.Message):
    await message.reply("Test 1")
    
#Test2 Handler
@dp.message(Command("test2"))
async def cmd_test2(message: types.Message):
    await message.answer("Test2")
    
#Dice to play    
@dp.message(Command("dice"))
async def cmd_dice(message: types.Message):
    await message.answer_dice(emoji='🎲')
    
#Registration time
@dp.message(Command("register"))
async def cmd_register(message: types.Message, info_list: list[str]):
    pass


if __name__ == "__main__":
    asyncio.run(main())
    
