from aiogram import F, Router
from aiogram.types import Message
# from aiogram.fsm.state import State


import logging 
from handlers.registration import show_new_menu_2
from utils.edit_profile_constants import EDIT_BACK_SIGN

router = Router()

@router.message(F.text.in_(EDIT_BACK_SIGN.values()))
async def division_back(message: Message):
     
    await show_new_menu_2(message)