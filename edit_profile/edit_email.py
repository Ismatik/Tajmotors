from aiogram import F, types, Router
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery, ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
)

# from aiogram.fsm.state import State
from utils.utils import EditProfile

import logging 
import re
from handlers.registration import show_new_menu_2
from config_reader import WRONG_EMAIL
from Registration_functions.functions import fetch_language, change_email
from utils.edit_profile_constants import EDIT_EMAIL , EDIT_BACK_SIGN
from utils.edit_profile_constants import EDIT_EMAIL_TEXT, EDIT_EMAIL_REPLY

router = Router()

@router.message(F.text.in_(EDIT_EMAIL.values()))
async def division_email(message: Message, state:FSMContext):
    await state.set_state(EditProfile.change_email)
        
    lang = fetch_language(message.chat.id)
    await message.answer(
        text = EDIT_EMAIL_TEXT[lang],
        pare_smode=ParseMode.HTML
    )
    
    await state.set_state(EditProfile.change_email_end)
    
@router.message(EditProfile.change_email_end)
async def email_changed(message: Message, state: FSMContext):
    if message.text in EDIT_BACK_SIGN.values():
        await show_new_menu_2(message)
        return
    
    language = fetch_language(message.chat.id)
    valid = re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$' , message.text)
    if not valid:
        await message.reply(WRONG_EMAIL[language],
                            parse_mode=ParseMode.HTML)
        return

        
    change_email(message.chat.id , message.text)
    
    await message.answer(
        text= EDIT_EMAIL_REPLY[language]
    )    
    
    await show_new_menu_2(message)