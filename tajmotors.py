# =================================================================================
# 1. IMPORTS
# =================================================================================
import asyncio
import logging
import re
from Registration_functions import functions

from aiogram import Bot, Dispatcher, F, types
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (
    InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton,
    Message, ReplyKeyboardMarkup, ReplyKeyboardRemove, CallbackQuery
)
from aiogram.filters.callback_data import CallbackData

from aiogram_calendar import SimpleCalendar , SimpleCalendarCallback, get_user_locale, DialogCalendar
from datetime import date, datetime

from config_reader import config

# =================================================================================
# 2. CONFIGURATION AND INITIALIZATION
# =================================================================================

logging.basicConfig(level=logging.INFO)

BOT_DESCRIPTION = (
    "ООО «Тадж Моторс» — современный 3S комплекс, построенный в соответствии со всеми стандартами TOYOTA MOTOR CORPORATION\nКомпания ООО «Тадж Моторс» является официальным дилером компании TOYOTA MOTOR CORPORATION в Республики Таджикистан с 05 июля 2013 года."
)

# Initialize bot, dispatcher
bot = Bot(token=config.bot_token.get_secret_value())
dp = Dispatcher()
# dp.include_router(service.router)

# =================================================================================
# 3. FSM (FINITE STATE MACHINE) STATES
# =================================================================================
# States should represent what the bot is WAITING FOR, not data it has stored.
class Registration(StatesGroup):
    waiting_for_email = State()
    email = State()
    phone = State()
    name = State()
    username = State()
    iduser = State()
    
class Service(StatesGroup):
    name = State()
    phone_number = State()
    VIN = State()
    auto_model = State()
    action_list = State()
    date = State()
    time = State()
    registration_time = State()
    userid = State()
    comments = State()

class TestDrive(StatesGroup):
    car_model = State()
    name=State()
    phone = State()
    test_date = State()
    time = State()
    comments = State()

# =================================================================================
# 6. HANDLERS FOR REGISTRATION
# =================================================================================
# --- Main Menu and Entry Point ---

#/start handler to ask the number
@dp.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    await state.set_state(Registration.phone)
    #Checking if he was registered
    if functions.check_registered(message.chat.id):
        await show_new_menu(message)
    
    else:
        await state.set_state(Registration.iduser)
        but = [
            [InlineKeyboardButton(text="▶️ Begin Registration" , callback_data="start_registration")]
        ]
        
        keyboard = InlineKeyboardMarkup(inline_keyboard = but)
        
        await state.update_data(iduser = message.chat.id)

        await message.answer(
            f"Hello, Please register before you start. We will need your phone number,name and " 
            f"email.\nClick 'Share My Phone Number', we will fetch automatically",
            reply_markup=keyboard    
        )
        

@dp.callback_query(F.data == "start_registration")
async def start_register(callback: types.CallbackQuery , state: State):
    # First, acknowledge the button press to remove the "loading" icon
    await callback.answer()
    
    # Now, send the Reply Keyboard with the contact request button.
    but = [
        [KeyboardButton(text="Share phone number", request_contact=True)]
    ]
    
    # Send the message asking for the contact
    # We use callback.message.answer to reply in the same chat
    keyboard = ReplyKeyboardMarkup(keyboard=but , resize_keyboard=True, one_time_keyboard=True)
    await callback.message.answer(
        "To start, please share your phone number by pressing the button below.",
        reply_markup=keyboard
    )
    
    await state.set_state(Registration.phone)    
    
    
#--------------Handler to catch the contact of user--------------------------------
@dp.message(Registration.phone)
async def contact_handler(message: Message , state: FSMContext):

    await state.update_data(phone = message.contact.phone_number)
    contact_name = (str(message.contact.first_name) + str(message.contact.last_name))
    contact_name = contact_name.replace("None" , "")
    await state.update_data(username = (str(message.contact.first_name) + " " + str(message.contact.last_name)))
    
    data = await state.get_data()
    #Here we remove the Reply Keyboard after fetching
    await message.answer(
        f"Thank you for sharing number!I've received this info:\n\nPhone number:{data['phone']}",
        reply_markup= ReplyKeyboardRemove()        
    )
    
    # Now we ask for the email and set the state, so in case he goes to /start we do not make it work
    await message.answer(f"Great! Now, please enter your full name(Example: Gulmurod Gulmurodov).")
    
    await state.set_state(Registration.name)
    
    
#------------------------------- This handler will only work when the bot is in the 'waiting_for_email' state-------------------------------

@dp.message(Registration.name)
async def name_handler(message:Message , state:FSMContext):
    await state.set_state(Registration.name)
    valid = message.text
    if " " not in valid:
        await message.reply("Please enter FULL Name.")
        return
    
    await state.update_data(name = message.text)
    
    await message.answer(f"Wonderful! Please enter your email address.")
    
    await state.set_state(Registration.waiting_for_email)


#------------------------------- This handler will only work when the bot is in the 'waiting_for_email' state-------------------------------
@dp.message(Registration.waiting_for_email)
async def email_handler(message: Message, state:FSMContext):
    
    # await state.set_state(Registration.email)
    #Need to make a validation for email entry
    valid = re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$' , message.text)
    if not valid:
        await message.reply("This doesn't look like e-mail, please check again.")
        return
    
    await state.update_data(email = message.text)
    
    # Retrieve all the stored data
    data = await state.get_data()

    functions.register_user(user_id=data['iduser'] , name=data['name'] , phone=data["phone"] , email = data["email"], username= data['username'])
    
    await message.answer(
        "Registration complete! Thanks for providing information.\n\n"
        f"<b>Phone</b>: {data['phone']}\n"
        f"<b>Email</b>: {data['email']}\n"
        f"<b>Name</b>: {data['name']}",
        parse_mode=ParseMode.HTML
    )
    
    #Registration of user
    await state.clear() #End the FSM Session

    #Start showind the menu with orders
    await show_new_menu(message)


async def show_new_menu(message: Message):

    name = functions.fetch_name(message.from_user.id)
    
    if name:
        content = f"Hello, <b>{name}</b>, Welcome to TajMotors Bot!\n"
    else:
        content = f"Hello, <b>{message.from_user.full_name}</b>, Welcome to TajMotors Bot!\n"
    content =  content + BOT_DESCRIPTION
    
    #Adding a callback data - it helps to know which button is clicked.
    kb = [
        [InlineKeyboardButton(text = "Catalogue" , callback_data = "Catalogue") , InlineKeyboardButton(text="Operator" , callback_data="Operator")],
        [InlineKeyboardButton(text = "Test Drive" , callback_data = "Test_Drive") , InlineKeyboardButton(text = "Service" , callback_data="Service")],
        [InlineKeyboardButton(text = "Contact/Address" , callback_data="Contact/Address" , url = "https://tjm.toyota-centralasia.com/about/dealerships?trade_source=menu")],
        [InlineKeyboardButton(text = "About us" , callback_data="AboutUs" , url = "https://tjm.toyota-centralasia.com/")]
    ]
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)

    await message.answer(
        text=content, 
        reply_markup=keyboard,
        parse_mode=ParseMode.HTML
    )
    
    # dp.include_router(service.router)

# =================================================================================
# 6.1 HANDLERS/CALLBACK QUERIES FOR MAIN MENU PART
# ================================================================================= 


# ==========================           SERVICE        ============================= 
@dp.callback_query(F.data == "Service")
async def process_service(callback: types.CallbackQuery , state:FSMContext):
    await callback.answer() #Service was clicked
    
    name , phone = functions.fetch_name_and_phone_number(callback.from_user.id)
    await state.update_data(name= name , phone_number = phone)

    
    await callback.message.answer(f"Thanks for selecting TajMotors! We will use name and phone number from registration form you filled!Plase fill the from for service of your car 🚗\n"
                                  f"<b>Name:</b> {name}\n<b>Phone:</b> {phone}\n" 
                                  f"Please enter state registration number or VIN code of the vehicle.",
                                  parse_mode=ParseMode.HTML)
    
    await state.set_state(Service.VIN)
    
@dp.message(Service.VIN)
async def process_service_VIN(message: Message, state: FSMContext):
    if len(message.text) != 17:
        await message.reply("Please enter correct VIN.")
        return
    
    await state.update_data(VIN = message.text)
    
    await message.answer("Thank you! Now, please enter the car model (e.g., Toyota Camry):")
    
    # Set the state to wait for the model
    await state.set_state(Service.auto_model)
    
@dp.message(Service.auto_model)
async def process_service_auto(message: Message , state: FSMContext):

    await state.update_data(auto_model = message.text)
    
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

    await state.set_state(Service.action_list)
    
@dp.callback_query(Service.action_list, F.data.startswith("chosen_service:"))
async def process_service_choice(callback: types.CallbackQuery, state: FSMContext):

    # await callback.answer()
    
    chose = callback.data.split(":")[-1]
    
    await state.update_data(action_list = chose)    
    
    await callback.message.edit_text(f"You have selected: <b>{chose}</b>." ,
                                     parse_mode=ParseMode.HTML)
    
    calendar = SimpleCalendar(
        locale=await get_user_locale(callback.from_user), 
        show_alerts=True
    )
    
    await callback.message.answer(
        "Great! Now, please select a convenient date:",
        reply_markup=await calendar.start_calendar()
    )
    await callback.answer()

@dp.callback_query(SimpleCalendarCallback.filter())
async def process_simple_calendar(callback_query: CallbackQuery, callback_data: CallbackData, state:FSMContext):
    calendar = SimpleCalendar(
        locale=await get_user_locale(callback_query.from_user), show_alerts=True
    )
    
    # calendar.set_dates_range(datetime(2022, 1, 1), datetime(2025, 12, 31))
    
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
            await callback_query.message.answer(text="Select your convenient time:",
                                                reply_markup = keyboard
                                                )            

            await state.set_state(Service.time)
            
         
        else:
            await callback_query.answer("You cannot select a date in the past. Please choose again.", show_alert=True)
            
            # Optional: You can re-send the calendar if you want them to immediately try again.
            # Note: This can feel a bit clunky to the user.
            await callback_query.message.edit_reply_markup(
                reply_markup=await calendar.start_calendar()
                
            )

@dp.callback_query(Service.time , F.data.startswith("Chosen-"))
async def process_time_service(callback_query: types.CallbackQuery , state:FSMContext):
    await callback_query.answer()
    
    chosen_time = callback_query.data.split("-")[-1]
    
    await state.update_data(registration_time = datetime.today().strftime("%Y-%m-%d %H:%M:%S"))
    await state.update_data(userid = callback_query.message.from_user.id)
    await state.update_data(time = chosen_time)
    info = await state.get_data()
    
    await callback_query.message.edit_text(text=f"You selected date on <b>{info["date"]} at {info["time"]}</b>.\n\n"
                                                f"Great. If you have any <b>additional comments</b> or requests for the mechanic, please enter them now. Please add contact number in case if we would not be able to reach you with number you registered with.\n\n"
                                                f"If you have no comments, just send a dash (-) to finish filling request form.",
                                           parse_mode=ParseMode.HTML)
    
    await state.set_state(Service.comments)
    
@dp.message(Service.comments)
async def process_test_drive_comments(message: Message, state:FSMContext):
    
    await state.update_data(comments = message.text)
    
    info = await state.get_data()
    functions.register_service(user_id=info["userid"] , 
                        fullname=info["name"],
                        contact_number = info["phone_number"],
                        VIN=info["VIN"] , 
                        auto_model=info["auto_model"], 
                        service=info["action_list"], 
                        date_service=info["date"],
                        registration_time=info["registration_time"],
                        time_service=info["time"],
                        comments = info["comments"])
    
    await message.answer(
        f"Thank you! Your appointment request is complete and has been registered.\n"
        f"Our manager will contact you soon."
        f"We recevied your request.<b>Our manager will contact you soon!</b>",
        parse_mode=ParseMode.HTML
    )
    
    await state.clear()
    
# =================================================================================

# =================================================================================
# 6.2 HANDLERS/CALLBACK QUERIES FOR MAIN MENU PART
# ================================================================================= 


@dp.callback_query(F.data == "Test Drive")
async def process_test_drive(callback: CallbackQuery , state:FSMContext):
    await callback.answer() #Clicked Test Drive

    name , phone = functions.fetch_name_and_phone_number(callback.from_user.id)
    await state.update_data(name= name , phone_number = phone)

    car_list = ["Toyota Camry 1" , "Toyota Camry 2" , "Toyota Camry 3" , "Toyota Camry 4" ,"Toyota Camry 5" ,"Toyota Camry 6" ,"Toyota Camry 7" "Toyota Camry 8","Toyota Camry 9", "Toyota Camry 10"]

    kb = []
    for i in car_list:
        kb.append(InlineKeyboardButton)
    
    await callback.message.answer(f"Thanks for selecting TajMotors! We will use name and phone number from registration form you filled!Plase fill the from for test drive.🚗\n"
                                  f"<b>Name:</b> {name}\n<b>Phone:</b> {phone}\n" 
                                  f"Please select vehicle you want to <b>drive test</b>:",
                                  parse_mode=ParseMode.HTML)
    
    await state.set_state(TestDrive.car_model)
    


# =================================================================================
# MAIN EXECUTION BLOCK
# =================================================================================

async def main():
    await dp.start_polling(bot)
    
if __name__ == "__main__":
    asyncio.run(main())
        
