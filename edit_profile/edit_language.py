from aiogram import F, types, Router
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery, ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
)
from aiogram.filters.callback_data import CallbackData
# from aiogram.fsm.state import State
from utils.utils import EditProfile

import logging 
import re
from handlers.registration import show_new_menu_2
from Registration_functions.functions import change_language
from utils.edit_profile_constants import EDIT_LANGUAGE, EDIT_LANGUAGE_REPLY

router = Router()

@router.message(F.text.startswith("🌐"))
async def division_lang(message: Message, state: FSMContext):
    
    kb = [
        [InlineKeyboardButton(text="🇹🇯 Тоҷикӣ", callback_data="Language:TJ"),
         InlineKeyboardButton(text="🇷🇺 Русский", callback_data="Language:RU"),
         InlineKeyboardButton(text="🇺🇸 English", callback_data="Language:EN")]
    ]

    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)

    await message.answer(
            f"Здравствуйте, Выберите язык для общения с ботом.", 
            reply_markup=keyboard    
        )
    
    await state.set_state(EditProfile.change_language_end)

@router.callback_query(EditProfile.change_language_end, F.data.startswith('Language:'))
async def lang_changed(callback: CallbackQuery , state: FSMContext):
    
    language = callback.data.split(":")[-1]
    print(callback.from_user.id, language)
    change_language(callback.from_user.id, new_language= language)
    
    await callback.answer(
        text=EDIT_LANGUAGE_REPLY[language],
        parse_mode = ParseMode.HTML
    )
    
    await show_new_menu_2(callback.message)