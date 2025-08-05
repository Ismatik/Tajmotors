# =================================================================================
# 1. IMPORTS
# =================================================================================
import asyncio
import logging
import datetime
import re
import pandas as pd

from aiogram import Bot, Dispatcher, F, types
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (
    InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton,
    Message, ReplyKeyboardMarkup, ReplyKeyboardRemove
)

from config_reader import config


# =================================================================================
# 2. CONFIGURATION AND INITIALIZATION
# =================================================================================

logging.basicConfig(level=logging.INFO)

EXCEL_FILE = 'Registered_users.xlsx'
BOT_DESCRIPTION = (
    "ООО «Тадж Моторс» — современный 3S комплекс, построенный в соответствии со всеми стандартами TOYOTA MOTOR CORPORATION\nКомпания ООО «Тадж Моторс» является официальным дилером компании TOYOTA MOTOR CORPORATION в Республики Таджикистан с 05 июля 2013 года."
)
TEST_DRIVE_LIST = 'Test_drive_list.xlsx'

# Initialize bot, dispatcher
bot = Bot(token=config.bot_token.get_secret_value())
dp = Dispatcher()


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
    
class TestDrive(StatesGroup):
    name = State()
    phone_number = State()
    VIN = State()
    auto_model = State()
    action_list = State()
    date_and_time = State()

def check_registered(user_id) -> bool:
    """Enter User_ID to check, if he was registered already. 
    To proceed for further steps."""
    try: 
        
        #Reading excel file using pd.read_excel
        df = pd.read_excel(EXCEL_FILE)

        return user_id in df["User_ID"].tolist()
    
    except FileNotFoundError:
        return False
    

def register_user(user_id , name , phone, email, username,) -> None:
    """Enter User_ID , Name, Phone  and Email to register user, after you have fetched all the info.
    As he finished registration, initialize the function."""
    
    try:
        df = pd.read_excel(EXCEL_FILE)
    except FileNotFoundError:
        df = pd.DataFrame(
            columns=['User_ID' , 'Name' , 'Phone' , 'Email', 'Username']
        )
        
    new_df = pd.DataFrame([{
        'User_ID':user_id,
        'Name': name,
        'Phone' : phone,
        'Email' : email,
        'Username' : username
        }])
    
    #Append new user to the existing DataFrame, fetching from excel file.
    df = pd.concat([df , new_df] , ignore_index=True)
    
    #Save the updated 
    df.to_excel(EXCEL_FILE , index=False)


def fetch_name(user_id)-> str:
    
    try:
        df = pd.read_excel(EXCEL_FILE)
        # 1. Filter the DataFrame to find the row(s) matching the user_id
         
        user_row = df[df["User_ID"] == user_id]
        
        # 2. Check if any rows were found. .empty is the correct way to do this.
        if not user_row.empty:
            # 3. Get the value from the 'Name' column of the found row.
            # .item() is perfect for extracting a single value from a Series.
            return user_row["Name"].item()
        else:
            # 4. Nothing found, no such user
            return None
            
    except FileExistsError:
        return None

def fetch_name_and_phone_number(user_id):
    try:
        df = pd.read_excel(EXCEL_FILE)
        # 1. Filter the DataFrame to find the row(s) matching the user_id
         
        user_row = df[df["User_ID"] == user_id]
        
        # 2. Check if any rows were found. .empty is the correct way to do this.
        if not user_row.empty:
            # 3. Get the value from the 'Name' column of the found row.
            # .item() is perfect for extracting a single value from a Series.
            return user_row["Name"].item(), user_row["Phone"].item()
        else:
            # 4. Nothing found, no such user
            return None
            
    except FileExistsError:
        return None

def register_testdrive(fullname , contact_number, VIN, auto_model, service, date_and_time_service):
    """
        ◦ ФИО. - fullname\n 
        ◦ Контактный телефон. - contact_number\n
        ◦ Госномер или VIN-код автомобиля. - VIN\n
        ◦ Модель автомобиля. - auto_model\n
        ◦ Тип необходимой услуги (выбор из списка, который редактируется в админ-панели). - service\n
        ◦ Желаемая дата и время. - date_and_time_service\n
    """
    pass

# =================================================================================
# 6. HANDLERS FOR REGISTRATION
# =================================================================================
# --- Main Menu and Entry Point ---

#/start handler to ask the number
@dp.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    await state.set_state(Registration.phone)
    #Checking if he was registered
    if check_registered(message.chat.id):
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
    await state.update_data(username = (message.contact.first_name + message.contact.last_name))
       
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

    register_user(user_id=data['iduser'] , name=data['name'] , phone=data["phone"] , email = data["email"], username= data['username'])
    
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

    name = fetch_name(message.from_user.id)
    
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
   
# =================================================================================
# 6. HANDLERS/CALLBACK QUERIES FOR MAIN MENU PART
# ================================================================================= 

@dp.callback_query(F.data == "Service")
async def process_test_drive(callback: types.CallbackQuery , state:FSMContext):
    
    name , phone = fetch_name_and_phone_number(callback.from_user.id)
    await state.update_data(name= name)
    await state.update_data(phone = phone)
    data = await state.get_data()
    
    await callback.message.answer(f"Thanks for selecting TajMotors! We will use name and phone number from registration form you filled!Plase fill the from for service of your car 🚗\n"
                                  f"Name: {name}\n"
                                  f"Phone: {phone}\n" 
                                  f"Please enter state registration number or VIN code of the vehicle.")
    
    await state.update_data(VIN = callback.message.text)
    await state.set_state(TestDrive.auto_model)
    await callback.answer()
    
@dp.message(TestDrive.auto_model)
async def process_service_auto(message: Message , state: FSMContext):
    await message.answer("We received your VIN! Enter Car Model of yours:")

    await state.update_data(auto_model = message.text)
    
    await state.set_state(TestDrive.action_list)

@dp.message(TestDrive.action_list)
async def process_service_list(message: Message , state:FSMContext):
    await message.answer(text="We noted your car model.")
    
    #list as for now
    service_list = [InlineKeyboardButton(text= "Service 1" , callback_data= "Service 1") , InlineKeyboardButton(text= "Service 2" , callback_data= "Service 2") ,
                    InlineKeyboardButton(text= "Service 3" , callback_data= "Service 3") , InlineKeyboardButton(text= "Service 4" , callback_data= "Service 4") ,
                    InlineKeyboardButton(text= "Service 5" , callback_data= "Service 5")]
    kb = []
    for i in range(0 , len(service_list) , 2):
        kb.append(service_list[i: i+2])
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)

    await message.answer( 
        text="Please select what service you require:",
        reply_markup=keyboard,
        parse_mode=ParseMode.HTML
    )
    await state.update_data(action_list = "")
    await state.set_state(TestDrive.date_and_time)
    
@dp.message(TestDrive.date_and_time)
async def process_service_dateandtime(message: Message , state: FSMContext):
    print("YAAAAAAAAAAAAAAAA")
    
    
# @dp.callback_query(F.data == "service")
# async def process_service(callback: types.CallbackQuery):
#     await callback.message.answer("You chose 'Service'. What do you need help with?")
#     await callback.answer()

# @dp.callback_query(F.data == "about_us")
# async def process_about_us(callback: types.CallbackQuery):
#     await callback.message.answer("TajMotors is a premier dealership for luxury vehicles.")
#     await callback.answer()

# =================================================================================
# MAIN EXECUTION BLOCK
# =================================================================================

async def main():
    await dp.start_polling(bot )
    
if __name__ == "__main__":
    asyncio.run(main())
        
