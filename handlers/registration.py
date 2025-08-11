from Registration_functions.functions import fetch_name,register_user,check_registered

from aiogram import F, types, Router
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery, ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
)
from aiogram.fsm.state import State

import logging as lg
import re
import config_reader as config
from utils.utils import Registration
from datetime import datetime

BOT_DESCRIPTION = config.BOT_DESCRIPTION

router = Router()

#/start handler to ask the number
@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    await state.set_state(Registration.phone)
    user = message.from_user
    lg.info(f"{user.full_name} clicked button /start | {user.id} | {datetime.today().strftime("%Y-%m-%d %H:%M:%S")}")
    #Checking if he was registered
    if check_registered(message.chat.id):
        await show_new_menu(message)
    
    else:
        await state.set_state(Registration.iduser)
        but = [
            [InlineKeyboardButton(text="▶️ Begin Registration" , callback_data="start_registration")]
        ]
        
        keyboard = InlineKeyboardMarkup(inline_keyboard = but)
        
        await state.update_data(iduser = message.chat.id)

        await message.answer(
            f"Hello, Please register before you start. We will need your phone number,name and " 
            f"email.\nClick 'Share My Phone Number', we will fetch automatically",
            reply_markup=keyboard    
        )
        
        

@router.callback_query(F.data == "start_registration")
async def start_register(callback: types.CallbackQuery , state: State):
    # First, acknowledge the button press to remove the "loading" icon
    user = callback.from_user
    lg.info(f"{user.full_name} REGISTRATION begun | {user.id} | {datetime.today().strftime("%Y-%m-%d %H:%M:%S")}")
    await callback.answer()
    
    # Now, send the Reply Keyboard with the contact request button.
    but = [
        [KeyboardButton(text="Share phone number", request_contact=True)]
    ]
    
    # Send the message asking for the contact
    # We use callback.message.answer to reply in the same chat
    keyboard = ReplyKeyboardMarkup(keyboard=but , resize_keyboard=True, one_time_keyboard=True)
    await callback.message.answer(
        "To start, please share your phone number by pressing the button below.",
        reply_markup=keyboard
    )
    
    await state.set_state(Registration.phone)    
    
    
#--------------Handler to catch the contact of user--------------------------------
@router.message(Registration.phone)
async def contact_handler(message: Message , state: FSMContext):

    await state.update_data(phone = message.contact.phone_number)
    contact_name = (str(message.contact.first_name) + str(message.contact.last_name))
    contact_name = contact_name.replace("None" , "")
    await state.update_data(username = (str(message.contact.first_name) + " " + str(message.contact.last_name)))
    
    data = await state.get_data()
    #Here we remove the Reply Keyboard after fetching
    user = message.from_user
    lg.info(f"{user.full_name}'s NUMBER received | {user.id} | {datetime.today().strftime("%Y-%m-%d %H:%M:%S")}")

    await message.answer(
        f"Thank you for sharing number!I've received this info:\n\nPhone number:{data['phone']}",
        reply_markup= ReplyKeyboardRemove()        
    )
    
    # Now we ask for the email and set the state, so in case he goes to /start we do not make it work
    await message.answer(f"Great! Now, please enter your full name(Example: Gulmurod Gulmurodov).")
    
    await state.set_state(Registration.name)
    
    
#------------------------------- This handler will only work when the bot is in the 'waiting_for_email' state-------------------------------

@router.message(Registration.name)
async def name_handler(message:Message , state:FSMContext):
    await state.set_state(Registration.name)
    valid = message.text
    if " " not in valid:
        await message.reply("Please enter FULL Name.")
        return

    user = message.from_user
    lg.info(f"{message.text} - NAME fetched | {user.id} | {datetime.today().strftime("%Y-%m-%d %H:%M:%S")}")
   
    await state.update_data(name = message.text)
    
    await message.answer(f"Wonderful! Please enter your email address.")
    
    await state.set_state(Registration.waiting_for_email)


#------------------------------- This handler will only work when the bot is in the 'waiting_for_email' state-------------------------------
@router.message(Registration.waiting_for_email)
async def email_handler(message: Message, state:FSMContext):
    
    user = message.from_user
    lg.info(f"{message.text} - EMAIL fetched | {user.id} | {datetime.today().strftime("%Y-%m-%d %H:%M:%S")}")
    # await state.set_state(Registration.email)
    #Need to make a validation for email entry
    valid = re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$' , message.text)
    if not valid:
        await message.reply("This doesn't look like e-mail, please check again.")
        return
    
    await state.update_data(email = message.text)
    
    # Retrieve all the stored data
    data = await state.get_data()

    register_user(user_id=data['iduser'] , name=data['name'] , phone=data["phone"] , email = data["email"], username= data['username'])
    
    await message.answer(
        "Registration complete! Thanks for providing information.\n\n"
        f"<b>Phone</b>: {data['phone']}\n"
        f"<b>Email</b>: {data['email']}\n"
        f"<b>Name</b>: {data['name']}",
        parse_mode=ParseMode.HTML
    )
    
    #Registration of user
    await state.clear() #End the FSM Session
    lg.info(f"{user.full_name} Registration COMPLETE FSM Session CLOSED | {user.id} | {datetime.today().strftime("%Y-%m-%d %H:%M:%S")}")

    #Start showind the menu with orders
    await show_new_menu(message)


async def show_new_menu(message: Message):

    user = message.from_user
    lg.info(f"{message.text}'s - MAIN MENU SHOW | {user.id} | {datetime.today().strftime("%Y-%m-%d %H:%M:%S")}")
    
    name = fetch_name(message.from_user.id)
    
    if name:
        content = f"Hello, <b>{name}</b>, Welcome to TajMotors Bot!\n"
    else:
        content = f"Hello, <b>{message.from_user.full_name}</b>, Welcome to TajMotors Bot!\n"
    content =  content + BOT_DESCRIPTION

    lg.info(f"{message.text}'s - MAIN MENU SHOWED | {user.id} | {datetime.today().strftime("%Y-%m-%d %H:%M:%S")}")    
    
    #Adding a callback data - it helps to know which button is clicked.
    kb = [
        [InlineKeyboardButton(text = "Catalogue" , callback_data = "Catalogue") , InlineKeyboardButton(text="Operator" , callback_data="Operator")],
        [InlineKeyboardButton(text = "Test Drive" , callback_data = "test_drive") , InlineKeyboardButton(text = "Service" , callback_data="Service")],
        [InlineKeyboardButton(text = "Contact/Address" , callback_data="Contact/Address" , url = "https://tjm.toyota-centralasia.com/about/dealerships?trade_source=menu")],
        [InlineKeyboardButton(text = "About us" , callback_data="AboutUs" , url = "https://tjm.toyota-centralasia.com/")]
    ]
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)

    await message.answer(
        text=content, 
        reply_markup=keyboard,
        parse_mode=ParseMode.HTML
    )

