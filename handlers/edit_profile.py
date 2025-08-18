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

@router.callback_query(F.data == "Edit Profile")
async def start_ep(callback: CallbackQuery):
    print(callback)