from aiogram.fsm.state import State, StatesGroup


class Registration(StatesGroup):
    waiting_for_email = State()
    email = State()
    phone = State()
    name = State()
    username = State()
    iduser = State()
    language = State()
    end = State()

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
    registration_time = State()
    userid = State()
    comments = State()

