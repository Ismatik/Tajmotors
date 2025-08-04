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

#Adding info to Excel(for now)
import pandas as pd

#Library for validating email
import re

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

EXCEL_FILE = 'Registered_users.xlsx'

class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

#Turn on logging, not to miss important messages
logging.basicConfig(level=logging.INFO)

class Registration(StatesGroup):
    waiting_for_email = State()
    email = State()
    phone = State()
    name = State()
    username = State()
    iduser = State()

    
bot = Bot(token= config.bot_token.get_secret_value())


dp = Dispatcher()

def check_registered(user_id) -> bool:
    """Enter User_ID to check, if he was registered already. 
    To proceed for further steps."""
    try: 
        
        #Reading excel file using pd.read_excel
        df = pd.read_excel(EXCEL_FILE)

        return user_id in df["User_ID"].tolist()
    
    except FileNotFoundError:
        return False
    

def register_user(user_id , name , phone, email) -> None:
    """Enter User_ID , Name, Phone  and Email to register user, after you have fetched all the info.
    As he finished registration, initialize the function."""
    
    try:
        df = pd.read_excel(EXCEL_FILE)
    except FileNotFoundError:
        df = pd.DataFrame(
            columns=['User_ID' , 'Name' , 'Phone' , 'Email']
        )
        
    new_df = pd.DataFrame([{
        'User_ID':user_id,
        'Name': name,
        'Phone' : phone,
        'Email' : email
        }])
    
    #Append new user to the existing DataFrame, fetching from excel file.
    df = pd.concat([df , new_df] , ignore_index=True)
    
    #Save the updated 
    df.to_excel(EXCEL_FILE , index=False)


#/start handler to ask the number
@dp.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    await state.set_state(Registration.phone)
    #Checking if he was registered
    if check_registered(message.chat.id):
        await show_new_menu(message)
    
    else:
        but = [
            [KeyboardButton(text="Share My Phone Number" , callback_data = "Fetch phone number",request_contact=True)]
        ]
        
        await state.update_data(iduser = message.chat.id)
        
        keyboard = ReplyKeyboardMarkup(
            keyboard=but,
            resize_keyboard=True, # Makes the keyboard smaller
            one_time_keyboard=True # Hides the keyboard after a button is pressed
        )

        await message.answer(
            f"Hello, Please register before you start. We will need your phone number,name and " 
            f"email.\nClick 'Share My Phone Number', we will fetch automatically",
            reply_markup=keyboard    
        )
        
        # await state.set_state(Registration.waiting_for_email)
    
#--------------Handler to catch the contact of user--------------------------------
@dp.message(F.contact)
async def contact_handler(message: Message , state: FSMContext):

    await state.update_data(phone = message.contact.phone_number)        
    #Fetching info of the user
    contact = message.contact
    
    await state.update_data(username = (contact.first_name + contact.last_name))
    await state.update_data(phone = contact.phone_number)
    
    #Save the phone number in the bot's memory for this user
    # await state.update_data(phone_number = contact.phone_number)
    
    data = await state.get_data()
    #Here we remove the Reply Keyboard after fetching
    await message.answer(
        f"Thank you for sharing number!I've received this info:\nYour username:{data['username']}\nPhone number:{data['phone']}",
        reply_markup=ReplyKeyboardRemove()        
    )
    
    # Now we ask for the email and set the state, so in case he goes to /start we do not make it work
    await message.answer("Great! Now, please enter your name.")
    
    await state.set_state(Registration.name)
    
#------------------------------- This handler will only work when the bot is in the 'waiting_for_email' state-------------------------------

@dp.message(Registration.name)
async def name_handler(message:Message , state:FSMContext):
    await state.set_state(Registration.name)
    
    await state.update_data(name = message.text)
    
    await message.answer("Great! Now, please enter your email address.")
    
    await state.set_state(Registration.waiting_for_email)


#------------------------------- This handler will only work when the bot is in the 'waiting_for_email' state-------------------------------
@dp.message(Registration.waiting_for_email)
async def email_handler(message: Message, state:FSMContext):
    
    await state.set_state(Registration.email)
    #Need to make a validation for email entry
    valid = re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$' , message.text)
    if not valid:
        await message.reply("This doesn't look like e-mail, please check again.")
        return
    
    await state.update_data(email = message.text)
    
    # Retrieve all the stored data
    data = await state.get_data()
    
    await message.answer(
        "Registration complete! Thanks for providing information.\n\n"
        f"<b>Phone</b>:{data['phone']}\n"
        f"<b>Email</b>:{data['email']}\n"
        f"<b>Name</b>:{data['username']}",
        parse_mode=ParseMode.HTML
    )
    
    #Registration of user
    register_user(user_id=message.chat.id , name=data['name'] , phone=data["phone"] , email = data["email"])
    await state.clear() #End the FSM Session

    #Start showind the menu with orders
    await show_new_menu(message)


async def show_new_menu(message: Message):
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
        
