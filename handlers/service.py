from Registration_functions.functions import fetch_name_and_phone_number, register_service

from aiogram import F, types, Router
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery
)
from aiogram.filters.callback_data import CallbackData

from aiogram_calendar import SimpleCalendar , SimpleCalendarCallback, get_user_locale
from datetime import date, datetime
from utils.utils import Service

from config_reader import COMMENTS
import logging

logger = logging.getLogger(__name__)
router = Router()

@router.callback_query(F.data == "Service")
async def process_service(callback: types.CallbackQuery , state:FSMContext):
    await callback.answer() #Service was clicked
    user = callback.from_user
    logger.info(f"{user.full_name} user {user.id}-id started the SERVICE flow | {datetime.today().strftime("%Y-%m-%d %H:%M:%S")}")
    
    name , phone = fetch_name_and_phone_number(callback.from_user.id)
    await state.update_data(name= name , phone_number = phone)
    logger.info(f"{user.full_name} user {user.id}-id MESSAGE for SERVICE flow | {datetime.today().strftime("%Y-%m-%d %H:%M:%S")}")    
    
    await callback.message.answer(f"Thanks for selecting TajMotors! We will use name and phone number from registration form you filled!Plase fill the from for service of your car 🚗\n"
                                  f"<b>Name:</b> {name}\n<b>Phone:</b> {phone}\n" 
                                  f"Please enter state registration number or VIN code of the vehicle.",
                                  parse_mode=ParseMode.HTML)
    
    await state.set_state(Service.VIN)
    
@router.message(Service.VIN)
async def process_service_VIN(message: Message, state: FSMContext):
    user = message.from_user
    if len(message.text) != 17:
        await message.reply("Please enter correct VIN.")
        logger.info(f"{user.full_name} user {user.id}-id WRONG VIN entered | {datetime.today().strftime("%Y-%m-%d %H:%M:%S")}")
        return
    
    await state.update_data(VIN = message.text)
    logger.info(f"{user.full_name} user {user.id}-id VIN ENTERED | {datetime.today().strftime("%Y-%m-%d %H:%M:%S")}")

    
    await message.answer("Thank you! Now, please enter the car model (e.g., Toyota Camry):")
    
    # Set the state to wait for the model
    await state.set_state(Service.auto_model)
    
@router.message(Service.auto_model)
async def process_service_auto(message: Message , state: FSMContext):
    user = message.from_user
    await state.update_data(auto_model = message.text)
    logger.info(f"{user.full_name} user {user.id}-id CAR MODEL entered | {datetime.today().strftime("%Y-%m-%d %H:%M:%S")}")
    
    await message.answer(text="We noted your car model.")
    
    #list as for now
    service_list = [
        InlineKeyboardButton(text="Service 1" , callback_data="chosen_service:Service 1"),
        InlineKeyboardButton(text="Service 2" , callback_data="chosen_service:Service 2"),
        InlineKeyboardButton(text="Service 3" , callback_data="chosen_service:Service 3"),
        InlineKeyboardButton(text="Service 4" , callback_data="chosen_service:Service 4"),
        InlineKeyboardButton(text="Service 5" , callback_data="chosen_service:Service 5")
    ]
    
    kb = []
    for i in range(0 , len(service_list) , 2):
        kb.append(service_list[i: i+2])
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)

    await message.answer( 
        text="Please select what service you require:",
        reply_markup=keyboard,
        parse_mode=ParseMode.HTML
    )
    logger.info(f"{user.full_name} user {user.id}-id SERVICE SELECTION | {datetime.today().strftime("%Y-%m-%d %H:%M:%S")}")


    await state.set_state(Service.action_list)
    
@router.callback_query(Service.action_list, F.data.startswith("chosen_service:"))
async def process_service_choice(callback: types.CallbackQuery, state: FSMContext):

    await callback.answer()
    user = callback.from_user
    logger.info(f"{user.full_name} user {user.id}-id SERVICE CHOSEN | {datetime.today().strftime("%Y-%m-%d %H:%M:%S")}")
    
    chose = callback.data.split(":")[-1]
    
    await state.update_data(action_list = chose)    
    
    await callback.message.edit_text(f"You have selected: <b>{chose}</b>." ,
                                     parse_mode=ParseMode.HTML)
    logger.info(f"{user.full_name} user {user.id}-id PRINTER CHOSEN service | {datetime.today().strftime("%Y-%m-%d %H:%M:%S")}")
    calendar = SimpleCalendar(
        locale=await get_user_locale(callback.from_user), 
        show_alerts=True
    )
    
    await callback.message.answer(
        "Great! Now, please select a convenient date:",
        reply_markup=await calendar.start_calendar()
    )
    logger.info(f"{user.full_name} user {user.id}-id DATE SELECTION PROCESS | {datetime.today().strftime("%Y-%m-%d %H:%M:%S")}")
    await callback.answer()
    await state.set_state(Service.date)

@router.callback_query(Service.date , SimpleCalendarCallback.filter())
async def process_simple_calendar(callback_query: CallbackQuery, callback_data: CallbackData, state:FSMContext):
    calendar = SimpleCalendar(
        locale=await get_user_locale(callback_query.from_user), show_alerts=True
    )
    user=callback_query.from_user
    logger.info(f"{user.full_name} user {user.id}-id SERVICE CALENDAR CREATION | {datetime.today().strftime("%Y-%m-%d %H:%M:%S")}")
    calendar.set_dates_range(datetime.today(), datetime(2030, 12, 31))# set from today
    selected, data = await calendar.process_selection(callback_query, callback_data)
    if selected:
        if data > datetime.today():
            await callback_query.message.edit_text(
                # f'You selected {data.strftime("%d/%m/%Y")}.\n\nWe recevied your request.<b>Our manager will contact you soon!</b>',
                f'You selected this date - <b>{data.strftime("%d/%m/%Y")}</b>.\n\n'
                f'Now, please enter a convenient time (e.g., 14:30).',
                parse_mode=ParseMode.HTML
            )
            
            await state.update_data(date = data.strftime("%d/%m/%Y"))
            await state.update_data(registration_time = date.today().strftime("%Y-%m-%d %H:%M:%S"))
            await state.update_data(userid = callback_query.message.from_user.id)
            logger.info(f"{user.full_name} user {user.id}-id SERVICE DATE UPDATED | {datetime.today().strftime("%Y-%m-%d %H:%M:%S")}")
            time_slots = ["09:00", "09:30" , "10:00" , "10:30", "11:00" , "11:30", "14:00" , "14:30", "15:00" , "15:30", "16:00", "16:30"]
            buttons = []
            for slots in time_slots:
                buttons.append(
                    InlineKeyboardButton(
                        text=slots,
                        callback_data=f"Chosen-{slots}"
                    )
                )
            kb = []
            for i in range( 0 , len(time_slots) , 3):
                kb.append(buttons[i:i+3])
            
            keyboard = InlineKeyboardMarkup(inline_keyboard=kb)
            await callback_query.message.answer(text="Select your convenient time for service:",
                                                reply_markup = keyboard
                                                )            
            logger.info(f"{user.full_name} user {user.id}-id SERVICE TIME SELECTION | {datetime.today().strftime("%Y-%m-%d %H:%M:%S")}")
            await state.set_state(Service.time)
            
         
        else:
            await callback_query.answer("You cannot select a date in the past. Please choose again.", show_alert=True)
            logger.info(f"{user.full_name} user {user.id}-id SERVICE TIME WRONG SELECTION | {datetime.today().strftime("%Y-%m-%d %H:%M:%S")}")
            # Optional: You can re-send the calendar if you want them to immediately try again.
            # Note: This can feel a bit clunky to the user.
            await callback_query.message.edit_reply_markup(
                reply_markup=await calendar.start_calendar()
                
            )

@router.callback_query(Service.time , F.data.startswith("Chosen-"))
async def process_time_service(callback_query: types.CallbackQuery , state:FSMContext):
    await callback_query.answer()
    user = callback_query.from_user
    logger.info(f"{user.full_name} user {user.id}-id SERVICE TIME CHOSEN | {datetime.today().strftime("%Y-%m-%d %H:%M:%S")}")
    chosen_time = callback_query.data.split("-")[-1]
    
    await state.update_data(registration_time = datetime.today().strftime("%Y-%m-%d %H:%M:%S"))
    await state.update_data(userid = callback_query.message.from_user.id)
    await state.update_data(time = chosen_time)
    info = await state.get_data()
    logger.info(f"{user.full_name} user {user.id}-id RESPONSE for date and time with COMMENTS| {datetime.today().strftime("%Y-%m-%d %H:%M:%S")}")
    await callback_query.message.edit_text(text=f"You selected date on <b>{info["date"]} at {info["time"]}</b>.\n\n{COMMENTS}",
                                           parse_mode=ParseMode.HTML)
    
    await state.set_state(Service.comments)
    
@router.message(Service.comments)
async def process_service_comments(message: Message, state:FSMContext):
    user = message.from_user
    logger.info(f"{user.full_name} user {user.id}-id SERVICE COMMENTS FETCHED | {datetime.today().strftime("%Y-%m-%d %H:%M:%S")}")
    await state.update_data(comments = message.text)
    
    info = await state.get_data()
    
    register_service(user_id=info["userid"] , 
                        fullname=info["name"],
                        contact_number = info["phone_number"],
                        VIN = info["VIN"] , 
                        auto_model=info["auto_model"], 
                        service=info["action_list"], 
                        date_service=info["date"],
                        registration_time=info["registration_time"],
                        time_service=info["time"],
                        comments = info["comments"])
    logger.info(f"{user.full_name} user {user.id}-id SERVICE COMMENTS added to FILE | {datetime.today().strftime("%Y-%m-%d %H:%M:%S")}")
    
    await message.answer(
        f"Thank you! Your appointment request is complete and has been registered.\n"
        f"We recevied your request for <b>Service</b>.\n<b>Our manager will contact you soon!</b>",
        parse_mode=ParseMode.HTML
    )
    
    await state.clear()
    logger.info(f"{user.full_name} user {user.id}-id SERVICE END | {datetime.today().strftime("%Y-%m-%d %H:%M:%S")}")
