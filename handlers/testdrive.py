from Registration_functions.functions import fetch_name,fetch_name_and_phone_number, register_testdrive, check_registered

from aiogram import F, types, Router
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from aiogram.types import (
    InlineKeyboardButton, CallbackQuery, Message, InlineKeyboardMarkup
)
from aiogram.filters.callback_data import CallbackData

from aiogram_calendar import SimpleCalendar , SimpleCalendarCallback, get_user_locale
from datetime import date, datetime
from utils.utils import TestDrive
from config_reader import COMMENTS

router = Router()

@router.callback_query(F.data == "test_drive")
async def process_test_drive(callback: CallbackQuery , state:FSMContext):
    await callback.answer() #Clicked Test Drive

    name , phone = fetch_name_and_phone_number(callback.from_user.id)
    await state.update_data(name= name , phone_number = phone)

    car_list = ["Toyota Camry 1" , "Toyota Camry 2" , "Toyota Camry 3" , "Toyota Camry 4" ,"Toyota Camry 5" ,"Toyota Camry 6" ,"Toyota Camry 7" , "Toyota Camry 8","Toyota Camry 9", "Toyota Camry 10"]

    kb = []
    for i in car_list:
        kb.append(InlineKeyboardButton(text=i , callback_data=f"Test:{i}"))
    
    rows = []
    for i in range(0, len(kb), 3):
        rows.append(kb[i:i+3])
        
    keyboard = InlineKeyboardMarkup(inline_keyboard= rows)
    
    await callback.message.answer(f"Thanks for selecting TajMotors! We will use name and phone number from registration form you filled!Plase fill the from for test drive.🚗\n"
                                  f"<b>Name:</b> {name}\n<b>Phone:</b> {phone}\n" 
                                  f"Please select vehicle you want to <b>drive test</b>:",
                                  parse_mode=ParseMode.HTML,
                                  reply_markup=keyboard)
    
    await state.set_state(TestDrive.car_model)
    
@router.callback_query(TestDrive.car_model , F.data.startswith("Test:"))
async def process_test_drive_car(callback: CallbackQuery , state: FSMContext):
    await callback.answer()
    
    selected = callback.data.split(":")[-1]
    await state.update_data(car_model = selected)
    
    await callback.message.edit_text(f"Great choice! We saved your choice:<b>{selected}</b>",
                                     parse_mode=ParseMode.HTML
                                     )
    
    calendar = SimpleCalendar(
        locale= await get_user_locale(callback.from_user),
        show_alerts= True
    )
    
    await callback.message.answer(
        "Select date for Test Drive:",
        reply_markup= await calendar.start_calendar()
    )
    
    await callback.answer()

@router.callback_query(SimpleCalendarCallback.filter())
async def process_simple_calendar(callback_query:CallbackQuery , callback_data: CallbackData, state: FSMContext):
    calendar = SimpleCalendar(
        locale = await get_user_locale(callback_query.from_user), 
        show_alerts = True
    )
    
    calendar.set_dates_range(datetime.today() , datetime(2030 , 12 , 31))
    
    selected, data = await calendar.process_selection(callback_query, callback_data)
    if selected:
        if data > datetime.today():
            await callback_query.message.edit_text(
                f'You selected this date - <b>{data.strftime("%d/%m/%Y")}</b>.\n\n'
                f'Now, please enter a convenient time (e.g., 14:30).',
                parse_mode=ParseMode.HTML
            )
            
            await state.update_data(test_date = data.strftime("%d/%m%Y"))
            await state.update_data(userid = callback_query.from_user.id)
           
            time_slots = ["09:00", "09:30" , "10:00" , "10:30", "11:00" , "11:30", "14:00" , "14:30", "15:00" , "15:30", "16:00", "16:30"]
            buttons = []
            for slots in time_slots:
                buttons.append(
                    InlineKeyboardButton(
                        text=slots,
                        callback_data=f"Chosen test time-{slots}"
                    )
                )
            kb = []
            for i in range( 0 , len(time_slots) , 3):
                kb.append(buttons[i:i+3])
            
            keyboard = InlineKeyboardMarkup(inline_keyboard=kb)
            await callback_query.message.answer(text="Select time for test drive:",
                                                reply_markup = keyboard
                                                )            

            await state.set_state(TestDrive.time)
        
        else:
            
            await callback_query.answer("You cannot select a date in the past. Please choose again.", show_alert=True)
            
            await callback_query.message.edit_reply_markup(text = "You cannot select a date in the past. Please choose again.",
                                                           reply_markup= await calendar.start_calendar()
                                                           )
            
        
@router.callback_query(TestDrive.time , F.data.startswith("Chosen test time-"))
async def process_testdrive_time(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()
    
    chosen_time = callback_query.data.split("-")[-1]
    
    await state.update_data(registration_time = datetime.today().strftime("%Y-%m-%d %H:%M:%S"))
    await state.update_data(time = chosen_time)
    
    info = await state.get_data()
    
    await callback_query.message.edit_text(text=f"You selected date on <b>{info["date"]} at {info["time"]}</b>.\n\n" + COMMENTS,
                                           parse_mode=ParseMode.HTML)
    
    await state.set_state(TestDrive.comments)
    

@router.message(TestDrive.comments)
async def process_testdrive_comments(message: Message, state: FSMContext):
    
    await state.update_data(comments = message.text)
    
    info = state.get_data()
    
    register_testdrive(user_id= info["userid"],
                       fullname= info["name"],
                       contact_number= info["phone"],
                       auto_model = info["car model"],
                       test_date=info["test_date"],
                       time=info["time"],
                       comments=info["comments"],
                       registration_time=info["registration_time"]
                       )

    await message.answer(
        f"Thank you! Your appointment request is complete and has been registered.\n"
        f"We recevied your request.<b>Our manager will contact you soon!</b>" + COMMENTS,
        parse_mode=ParseMode.HTML
    )
    
    await state.clear()
    
