import asyncio
import logging
from config_reader import config

from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.utils.formatting import Bold, Text,Italic

from datetime import datetime

from aiogram import F
#Added Inline buttons and Markups
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters import Command
from aiogram.enums import ParseMode 

from aiogram import html

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
    # Create the text content for the message
    content = f"Hello, <b>{message.from_user.full_name}</b>, Welcome to TajMotors Bot!"
    # content = Text(
    #     "Hello, " , 
    #     Bold(message.from_user.full_name) ,
    #     " ,Welcome to ",
    #     Bold(Italic("TajMotors"))
    # )
    
    #Adding a callback data - it helps to know whic button is clicked.
    kb = [
        [InlineKeyboardButton(text = "Test Drive" , callback_data = "Test Drive" , url="https://tjm.toyota-centralasia.com/")],
        [InlineKeyboardButton(text="Service" , callback_data="Service" , url="https://tjm.toyota-centralasia.com/vladeltsam/service?trade_source=menu")],
        [InlineKeyboardButton(text = "About us" , callback_data="About us" , url = "https://tjm.toyota-centralasia.com/about/dealerships?trade_source=menu")]
    ]
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)
    
    await message.answer(
        text=content, 
        reply_markup=keyboard,
        parse_mode=ParseMode.HTML
    )
    print(content)

    # the **content.as_kwargs() construct will return the text, 
    # entities, parse_mode arguments and substitute them into the answer() call.

    # await message.answer(
    #     **content.as_kwargs()
    # )

@dp.callback_query(F.data == "test_drive")
async def process_test_drive(callback: types.CallbackQuery):
    await callback.message.answer("You chose 'Test Drive'. When are you available?")
    await callback.answer() # Acknowledge the button press

@dp.callback_query(F.data == "service")
async def process_service(callback: types.CallbackQuery):
    await callback.message.answer("You chose 'Service'. What do you need help with?")
    await callback.answer()

@dp.callback_query(F.data == "about_us")
async def process_about_us(callback: types.CallbackQuery):
    await callback.message.answer("TajMotors is a premier dealership for luxury vehicles.")
    await callback.answer()

async def main():
    await dp.start_polling(bot)
    
if __name__ == "__main__":
    asyncio.run(main())
        

    # await message.answer(
    #     f"Hello, welcome to *TajMotors*\!",
    #     parse_mode=ParseMode.MARKDOWN_V2
    # )
    
#Start process of polling new proccesses



#Using entities to fetch info of user
# @dp.message(F.text)
# async def extract_data(message: Message):
#     data = {
#         "name" : "N/A",
#         "phone" : "N/A",
#         "email" : "N/A"
#     }    
#     entities = message.entities or []
#     for item in entities:
#         if item.type in data.keys():
#             data[item.type] = item.extract_from(message.text)
    
#     await message.reply(
#         "Found this\n"
#         f"Name: {html.quote(data['name'])}\n",
#         f"Phone: {html.quote(data['phone'])}\n",
#         f"E-mail: {html.quote(data['email'])}"
#     )
    
# #Handler for command /start
# @dp.message(Command("start"))
# async def cmd_start(message: types.Message):
#     await message.answer("Welcome to TajMotors Bot! Please select option you would like to have:")

