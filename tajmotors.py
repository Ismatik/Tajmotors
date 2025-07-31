import asyncio
import logging

from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command

#Turn on logging, not to miss important messages
logging.basicConfig(level=logging.INFO)

#Bot as an object(hide token#)
bot = Bot(token= "8138074349:AAF-e1wcIaO0TEOCkkj070Eb1Tnts02Loiw")

# The dispatcher receives updates from Telegram, which can include various types of interactions like messages, commands, or other events.
#Dispatcher
dp = Dispatcher()

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
    
@dp.message(Command("dice"))
async def cmd_dice(message: types.Message):
    await message.answer_dice(emoji="🎲")
    
if __name__ == "__main__":
    asyncio.run(main())
    
