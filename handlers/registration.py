from Registration_functions.functions import fetch_name,register_user,check_registered, fetch_language

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
from config_reader import START_MESSAGE, PHONE_NUMBER, PHONE_NUMBER_REPLY, NAME_FETCH, FULL_NAME, CONTAIN_NUMBER, EMAIL, WRONG_EMAIL, REGISTRATION_OVER,BEGIN_REGISTR
from config_reader import BUTTON_EP, BUTTON_TDH, BUTTON_SH, BUTTON_CS, BUTTONS_TEXT, CATALOGUE, OPERATOR, TEST_DRIVE, SERVICE, ABOUT_US, SHARE_PHONE_NUMBER
from utils.utils import Registration
from datetime import datetime

BOT_DESCRIPTION = config.BOT_DESCRIPTION

router = Router()

#/start handler to ask the number
@router.message(Command("start"))
async def cmd_language(message:Message , state: FSMContext):
    await state.set_state(Registration.language)
    user = message
    lg.info(f"{user.from_user.full_name} clicked button /start | {user.from_user.id} | {datetime.today().strftime("%Y-%m-%d %H:%M:%S")}")
    if check_registered(message.chat.id):
        await show_new_menu_2(message)
    else:
        
        kb = [
            [InlineKeyboardButton(text="🇹🇯 TJ", callback_data="Language:TJ"),InlineKeyboardButton(text="🇷🇺 RU", callback_data="Language:RU"),InlineKeyboardButton(text="🇺🇸 EN", callback_data="Language:EN")]
        ]

        keyboard = InlineKeyboardMarkup(inline_keyboard=kb)

        await message.answer(
                f"Здравствуйте, Выберите язык для общения с ботом.", 
                reply_markup=keyboard    
            )

@router.callback_query(Registration.language , F.data.startswith('Language:'))
async def cmd_start(callback: CallbackQuery , state: FSMContext):
    await callback.answer() #Button clicked
    language = callback.data.split(":")[-1]
    await state.update_data(language = language)
    
    await state.set_state(Registration.phone)
    
    #Checking if he was registered
    if check_registered(callback.message.chat.id):
        await show_new_menu(callback.message)
    else:
        await state.set_state(Registration.iduser)
        data = await state.get_data()
        language = data['language']
        but = [
            [InlineKeyboardButton(text=BEGIN_REGISTR[language] , callback_data="start_registration")]
        ]
        
        keyboard = InlineKeyboardMarkup(inline_keyboard = but)
        
        await state.update_data(iduser = callback.message.chat.id)
        content = START_MESSAGE[language]
        await callback.message.answer(
            text=content,
            reply_markup=keyboard    
        )
        
        

@router.callback_query(F.data == "start_registration")
async def start_register(callback: types.CallbackQuery , state: State):
    # First, acknowledge the button press to remove the "loading" icon
    user = callback.from_user
    lg.info(f"{user.full_name} REGISTRATION begun | {user.id} | {datetime.today().strftime("%Y-%m-%d %H:%M:%S")}")
    await callback.answer()
    data = await state.get_data()
    language = data['language']
    # Now, send the Reply Keyboard with the contact request button.
    but = [
        [KeyboardButton(text=SHARE_PHONE_NUMBER[language], request_contact=True)]
    ]
    
    # Send the message asking for the contact
    # We use callback.message.answer to reply in the same chat
    keyboard = ReplyKeyboardMarkup(keyboard=but , resize_keyboard=True, one_time_keyboard=True)
    # data = await state.get_data()
    content = PHONE_NUMBER[language]
    await callback.message.answer(
        text=content,
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
    
    #Here we remove the Reply Keyboard after fetching
    user = message.from_user
    lg.info(f"{user.full_name}'s NUMBER received | {user.id} | {datetime.today().strftime("%Y-%m-%d %H:%M:%S")}")
    data = await state.get_data()
    content = PHONE_NUMBER_REPLY[data['language']]
    await message.answer(
        text = content + f"{data['phone']}",
        reply_markup= ReplyKeyboardRemove()        
    )
    
    content = NAME_FETCH[data['language']]
    await message.answer(content)
    
    await state.set_state(Registration.name)
    
    
#------------------------------- This handler will only work when the bot is in the 'waiting_for_email' state-------------------------------

@router.message(Registration.name)
async def name_handler(message:Message , state:FSMContext):
    await state.set_state(Registration.name)
    data = await state.get_data()
    valid = message.text
    if " " not in valid:
        await message.reply(FULL_NAME[data['language']])
        return
    
    if re.search(r'\d+', valid):
        await message.reply(CONTAIN_NUMBER[data['language']])
        return

    user = message.from_user
    lg.info(f"{message.text} - NAME fetched | {user.id} | {datetime.today().strftime("%Y-%m-%d %H:%M:%S")}")
   
    await state.update_data(name = message.text)
    
    await message.answer(EMAIL[data["language"]])
    
    await state.set_state(Registration.waiting_for_email)


#------------------------------- This handler will only work when the bot is in the 'waiting_for_email' state-------------------------------
@router.message(Registration.waiting_for_email)
async def email_handler(message: Message, state:FSMContext):
    data1 = await state.get_data()
    user = message.from_user

    language = data1['language']
    #Need to make a validation for email entry
    valid = re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$' , message.text)
    if not valid:
        await message.reply(WRONG_EMAIL[language])
        return
    
    await state.update_data(email = message.text)
    lg.info(f"{message.text} - EMAIL shall be updated in STATE | {user.id} | {datetime.today().strftime("%Y-%m-%d %H:%M:%S")}")
    data = await state.get_data()
    
    register_user(user_id=data['iduser'] , name=data['name'] , phone=data['phone'] , email = data['email'], username= data['username'], language=data['language'])
    
    await message.answer(
        REGISTRATION_OVER[language],
        # f"<b>Phone</b>: {data['phone']}\n"
        # f"<b>Email</b>: {data['email']}\n"
        # f"<b>Name</b>: {data['name']}",
        parse_mode=ParseMode.HTML
    )
    
    #Registration of user
    lg.info(f"{user.full_name} Registration COMPLETE FSM Session CLOSED | {user.id} | {datetime.today().strftime("%Y-%m-%d %H:%M:%S")}")

    await state.clear()
    #Start showind the menu with orders
    await show_new_menu(message)


async def show_new_menu(message: Message):

    language = fetch_language(message.chat.id)

    reply_kb = [
        [KeyboardButton(text=BUTTON_EP[language])],
        [KeyboardButton(text=BUTTON_TDH[language] ,callback_data = "TH"), KeyboardButton(text=BUTTON_SH[language], callback_data="SH")],
        [KeyboardButton(text=BUTTON_CS[language])]
    ]
    reply_keyboard = ReplyKeyboardMarkup(
        keyboard=reply_kb,
        resize_keyboard=True
    )
    # Send a message with real text to introduce the new keyboard.
    await message.answer(
        BUTTONS_TEXT[language],
        reply_markup=reply_keyboard
    )
    
    user = message.from_user
    lg.info(f"{message.text}'s - MAIN MENU SHOW | {user.id} | {datetime.today().strftime("%Y-%m-%d %H:%M:%S")}")
    
    name = fetch_name(message.from_user.id)

    content =  {"EN" : f"Hello, <b>{name}</b>, Welcome to TajMotors Bot!\n" + BOT_DESCRIPTION[language],
                "RU" : f"Здравствуйте, <b>{name}</b>, Добро пожаловать в Тадж Моторс Бот!\n" + BOT_DESCRIPTION[language],
                "TJ" : f"Салом, <b>{name}</b>, Хуш омадед ба TajMotors Bot!\n" + BOT_DESCRIPTION[language]}

    lg.info(f"{message.text}'s - MAIN MENU SHOWED | {user.id} | {datetime.today().strftime("%Y-%m-%d %H:%M:%S")}")    
    
    #Adding a callback data - it helps to know which button is clicked.
    kb = [
        [InlineKeyboardButton(text = CATALOGUE[language] , callback_data = "Catalogue") , InlineKeyboardButton(text=OPERATOR[language] , callback_data="Operator")],
        [InlineKeyboardButton(text = TEST_DRIVE[language] , callback_data = "test_drive") , InlineKeyboardButton(text = SERVICE[language] , callback_data="Service")],
        [InlineKeyboardButton(text = ABOUT_US[language] , callback_data="Contact/Address" , url = "https://tjm.toyota-centralasia.com/about/dealerships?trade_source=menu")]
    ]
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)

    await message.answer(
        text=content[language], 
        reply_markup=keyboard,
        parse_mode=ParseMode.HTML
    )
    
async def show_new_menu_2(message: Message):

    language = fetch_language(message.chat.id)

    reply_kb = [
        [KeyboardButton(text=BUTTON_EP[language])],
        [KeyboardButton(text=BUTTON_TDH[language] ,callback_data = "TH"), KeyboardButton(text=BUTTON_SH[language], callback_data="SH")],
        [KeyboardButton(text=BUTTON_CS[language])]
    ]
    reply_keyboard = ReplyKeyboardMarkup(
        keyboard=reply_kb,
        resize_keyboard=True
    )
    # Send a message with real text to introduce the new keyboard.
    await message.answer(
        BUTTONS_TEXT[language],
        reply_markup=reply_keyboard
    )
    
    user = message.from_user
    # lg.info(f"{message.text}'s - MAIN MENU SHOW | {user.id} | {datetime.today().strftime("%Y-%m-%d %H:%M:%S")}")
    
    name = fetch_name(message.chat.id)
    print(f'NAME REgistered: {message}')
    content =  {"EN" : f"Welcome back, <b>{name}</b>, to TajMotors Bot!\n",
                "RU" : f"Добро пожаловать, <b>{name}</b>, в Тадж Моторс Бот!\n",
                "TJ" : f"Хуш омадед, <b>{name}</b>, ба TajMotors Bot!\n"}

    # lg.info(f"{message.text}'s - MAIN MENU SHOWED | {user.id} | {datetime.today().strftime("%Y-%m-%d %H:%M:%S")}")    
    
    #Adding a callback data - it helps to know which button is clicked.
    kb = [
        [InlineKeyboardButton(text = CATALOGUE[language] , callback_data = "Catalogue") , InlineKeyboardButton(text=OPERATOR[language] , callback_data="Operator")],
        [InlineKeyboardButton(text = TEST_DRIVE[language] , callback_data = "test_drive") , InlineKeyboardButton(text = SERVICE[language] , callback_data="Service")],
        [InlineKeyboardButton(text = ABOUT_US[language] , callback_data="Contact/Address" , url = "https://tjm.toyota-centralasia.com/about/dealerships?trade_source=menu")]
    ]
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)

    await message.answer(
        text=content[language], 
        reply_markup=keyboard,
        parse_mode=ParseMode.HTML
    )