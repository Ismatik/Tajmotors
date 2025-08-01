import asyncio
import logging
from config_reader import config

from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.utils.formatting import Bold, Text,Italic

from datetime import datetime

from aiogram import F
#Added Inline buttons and Markups
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
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


#/start handler to ask the number
@dp.message(Command("start"))
async def cmd_start(message: Message):

    but = [
        [KeyboardButton(text="Share My Phone Number" , callback_data = "Fetch phone number",request_contact=True)]
    ]
    
    keyboard = ReplyKeyboardMarkup(
        keyboard=but,
        resize_keyboard=True, # Makes the keyboard smaller
        one_time_keyboard=True # Hides the keyboard after a button is pressed
    )

    await message.answer(
        "Hello, Please register before you start. We will need your phone number and name.\nClick 'Share My Phone Number', we will fetch automatically",
        reply_markup=keyboard    
    )
    
#Handler to catch the contact of user
@dp.message(F.contact)
async def contact_handler(message: Message):
    contact = message.contact
    phone_number = contact.phone_number
    name = contact.first_name + contact.last_name
    user_id = contact.user_id
    
    await message.answer(
        f"Thank you for sharing number!I've received this info:\nYour name:{name}\nPhone number:{phone_number}",
        reply_markup=ReplyKeyboardRemove()        
    )    

@dp.message(Command("options"))
async def any_message(message: Message):
    # Create the text content for the message
    if message.from_user.full_name == "" or message.from_user.full_name == " ":
        content = f"Hello, Welcome to TajMotors Bot!"
    elif("<" in message.from_user.full_name or ">" in message.from_user.full_name):
        content = f"Hello, {message.from_user.full_name}, Welcome to TajMotors Bot!"
    else:
        content = f"Hello, <b>{message.from_user.full_name}</b>, Welcome to TajMotors Bot!"
    
    #Adding a callback data - it helps to know which button is clicked.
    kb = [
        [InlineKeyboardButton(text = "Test Drive" , callback_data = "Test Drive" , url="https://tjm.toyota-centralasia.com/") , InlineKeyboardButton(text="Service" , callback_data="Service" , url="https://tjm.toyota-centralasia.com/vladeltsam/service?trade_source=menu")],
        [InlineKeyboardButton(text = "About us" , callback_data="About us" , url = "https://tjm.toyota-centralasia.com/about/dealerships?trade_source=menu")]
    ]
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)
    
    await message.answer(
        text=content, 
        reply_markup=keyboard,
        parse_mode=ParseMode.HTML
    )

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
        
