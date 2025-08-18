from aiogram import F, types, Router
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery, ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
)
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.state import State

import logging 
import re
import config_reader as config
from utils.utils import Registration
from datetime import datetime
from config_reader import BUTTON_EP

# logger = logging.getLogger(__name__)
router = Router()

@router.message(F.text.in_(BUTTON_EP.values()))
async def start_ep(message: Message, state: FSMContext):
    """
    This handler is triggered when the user presses the 'Edit Profile' ReplyKeyboardButton.
    """
    pass