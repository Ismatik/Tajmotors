from aiogram import F, Router
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    Message, ReplyKeyboardMarkup, KeyboardButton
)

from utils.utils import EditProfile

import logging 
import re
from handlers.registration import show_new_menu_2
from config_reader import WRONG_EMAIL
from Registration_functions.functions import fetch_language, change_email
from config_reader import BUTTON_EP
from utils.edit_profile_constants import EDIT_EMAIL, EDIT_BACK_SIGN, EDIT_LANGUAGE ,EDIT_NAME

# logger = logging.getLogger(__name__)
router = Router()

@router.message(F.text.in_(BUTTON_EP.values()))
async def start_ep(message: Message, state: FSMContext):
    await state.set_state(EditProfile.choice)
    """
    This handler is triggered when the user presses the 'Edit Profile' ReplyKeyboardButton.
    """
    language = fetch_language(message.chat.id)
    
    kb = [
        [KeyboardButton(text=EDIT_NAME[language]), KeyboardButton(text=EDIT_EMAIL[language])],
        [KeyboardButton(text=EDIT_BACK_SIGN[language]), KeyboardButton(text=EDIT_LANGUAGE[language])]
    ]
    
    keyboard = ReplyKeyboardMarkup(keyboard=kb , resize_keyboard=True, one_time_keyboard=True)
    
    content = {"EN" : "Select <b>information</b> you want to edit:",
               "RU" : "Выберите <b>информацию</b>, которую вы хотите изменить:",
               "TJ" : "Информасияи <b>таърифшуда</b>-ро интихоб кунед:"}
    
    await message.answer(
        text=content[language],
        reply_markup=keyboard,
        parse_mode=ParseMode.HTML
    )
    


