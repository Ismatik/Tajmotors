from aiogram import F, Router
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    Message
)
from aiogram.filters.callback_data import CallbackData
# from aiogram.fsm.state import State
from utils.utils import EditProfile

import logging 
import re
from handlers.registration import show_new_menu_2
from config_reader import FULL_NAME, CONTAIN_NUMBER
from Registration_functions.functions import fetch_language, change_name
from utils.edit_profile_constants import EDIT_NAME, EDIT_BACK_SIGN
from utils.edit_profile_constants import EDIT_NAME_TEXT, EDIT_NAME_REPLY

router = Router()

@router.message(F.text.in_(EDIT_NAME.values()))
async def division_name(message: Message, state: FSMContext):
    await state.set_state(EditProfile.change_name)
    
    lang = fetch_language(message.chat.id)
    await message.answer(
        text= EDIT_NAME_TEXT[lang],
        parse_mode=ParseMode.HTML
    )
    
    await state.set_state(EditProfile.change_name_end)
    
@router.message(EditProfile.change_name_end)
async def name_changed(message: Message , state:FSMContext):
    valid = message.text
    lang = fetch_language(message.chat.id)
    
    if valid in EDIT_BACK_SIGN.values():
        await show_new_menu_2(message)
        return
        
    if " " not in valid:
        await message.reply(FULL_NAME[lang])
        return
    
    if re.search(r'\d+', valid):
        await message.reply(CONTAIN_NUMBER[lang])
        return

    change_name(message.chat.id , message.text)
    
    await message.answer(
        text = EDIT_NAME_REPLY[lang]
    )
    
    await show_new_menu_2(message)