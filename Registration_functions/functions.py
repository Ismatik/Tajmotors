"""Functions to register users or reading files"""

import pandas as pd
import config_reader as config

REGISTRATION_FILE = config.EXCEL_FILE
TEST_DRIVE_LIST = config.TEST_DRIVE_LIST
SERVICE_LIST = config.SERVICE_LIST



def check_registered(user_id) -> bool:
    """Enter User_ID to check, if he was registered already. 
    To proceed for further steps.
    
    _summary_

    Returns:
        _type_: _description_
    """
    try: 
        
        #Reading excel file using pd.read_excel
        df = pd.read_excel(REGISTRATION_FILE)

        return user_id in df["User_ID"].tolist() or user_id == df["User_ID"].values
    
    except FileNotFoundError:
        return False
    
def fetch_users()->list:
    """

    Returns:
        list: list of users
    """
    
    return pd.read_excel(REGISTRATION_FILE)


def register_user(user_id , name , phone, email, username,language) -> None:
    """Enter User_ID , Name, Phone  and Email to register user, after you have fetched all the info.
    As he finished registration, initialize the function."""
        
        
    new_df = pd.DataFrame([{
        'User_ID':user_id,
        'Name': name,
        'Phone' : phone,
        'Email' : email,
        'Username' : username,
        'Language' : language
        }])
    try: 
        ex_df = pd.read_excel(REGISTRATION_FILE)
        
        updated_df = pd.concat([ex_df, new_df], ignore_index=True)
        updated_df.to_excel(REGISTRATION_FILE, index=False)

    except FileNotFoundError:
        
        new_df.to_excel(REGISTRATION_FILE , index=False)

def fetch_name(user_id)-> str:
    """_summary_

    Args:
        user_id (_type_): _description_

    Returns:
        str: _description_
    """
    
    try:
        df = pd.read_excel(REGISTRATION_FILE)
        print(df)
        print(user_id)
        # 1. Filter the DataFrame to find the row(s) matching the user_id
        user_row = df[df["User_ID"] == user_id]
        print(user_row) 
        
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
    
def fetch_language(user_id)-> str:
    """_summary_

    Args:
        user_id (_type_): _description_

    Returns:
        str: _description_
    """
    
    try:
        df = pd.read_excel(REGISTRATION_FILE)
        # 1. Filter the DataFrame to find the row(s) matching the user_id
         
        user_row = df[df["User_ID"] == user_id]
        
        # 2. Check if any rows were found. .empty is the correct way to do this.
        if not user_row.empty:
            # 3. Get the value from the 'Name' column of the found row.
            # .item() is perfect for extracting a single value from a Series.
            return user_row["Language"].item()
        else:
            # 4. Nothing found, no such user
            return None
            
    except FileExistsError:
        return None

def change_email(user_id , new_email):
    """_summary_

    Args:
        user_id (_type_): _description_
        new_email (_type_): _description_

    Returns:
        _type_: _description_

    Finds a user by their ID in the Excel file and updates their email address.

    Args:
        user_id (int): The unique ID of the user to update.
        new_email (str): The new email address to set.

    Returns:
        bool: True if the user was found and updated, False otherwise.
    """
    
    try:
        df = pd.read_excel(REGISTRATION_FILE)
        
        user_mask = df["User_ID"] == user_id
        
        if user_mask.any():
            df.loc[user_mask , "Email"] = new_email
            df.to_excel(REGISTRATION_FILE, index=False)
        else:
            return False
        
    except FileExistsError:
        return None

def change_language(user_id , new_language):
    """_summary_

    Args:
        user_id (_type_): _description_
        new_email (_type_): _description_

    Returns:
        _type_: _description_

    Finds a user by their ID in the Excel file and updates their email address.

    Args:
        user_id (int): The unique ID of the user to update.
        new_email (str): The new email address to set.

    Returns:
        bool: True if the user was found and updated, False otherwise.
    """
    
    try:
        df = pd.read_excel(REGISTRATION_FILE)
        
        user_mask = df["User_ID"] == user_id
        print(user_mask)
        if user_mask.any():
            df.loc[user_mask , "Language"] = new_language
            df.to_excel(REGISTRATION_FILE, index=False)
        else:
            return False
        
    except FileExistsError:
        return None

def change_name(user_id , new_name):
    """_summary_

    Args:
        user_id (_type_): _description_
        new_name (_type_): _description_

    Returns:
        _type_: _description_

    Finds a user by their ID in the Excel file and updates their name.

    Args:
        user_id (int): The unique ID of the user to update.
        new_email (str): The new email address to set.

    Returns:
        bool: True if the user was found and updated, False otherwise.
    """
    
    try:
        df = pd.read_excel(REGISTRATION_FILE)
        
        user_mask = df["User_ID"] == user_id
        
        if user_mask.any():
            df.loc[user_mask , "Name"] = new_name
            df.to_excel(REGISTRATION_FILE, index=False)
        else:
            return False
        
    except FileExistsError:
        return None

def fetch_name_and_phone_number(user_id):
    """_summary_

    Args:
        user_id (_type_): _description_

    Returns:
        _type_: _description_
    """
    try:
        df = pd.read_excel(REGISTRATION_FILE)
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

def register_service(user_id , fullname , contact_number, VIN, auto_model, service, date_service, registration_time,time_service, comments):
    """
        ◦ ФИО. - fullname\n 
        ◦ Контактный телефон. - contact_number\n
        ◦ Госномер или VIN-код автомобиля. - VIN\n
        ◦ Модель автомобиля. - auto_model\n
        ◦ Тип необходимой услуги (выбор из списка, который редактируется в админ-панели). - service\n
        ◦ Желаемая дата. - date_service\n
        ◦ Желаемое время. - time_service\n
        ◦ Дата и время регистрации. - registration_time\n
        ◦ ID Пользователя
    """
    new_df = pd.DataFrame([{
        'User_ID':user_id,
        'Full name': fullname,
        'Phone/Contact number' : contact_number,
        'VIN' : VIN,
        'Auto Model' : auto_model,
        'Service Type' : service,
        'Service Datetime' : date_service,
        'Registration time' : registration_time,
        'Time Service' : time_service,
        'Comments' : comments
        }])
    
    
    try:
        ex_df = pd.read_excel(SERVICE_LIST)
        
        updated_df = pd.concat([ex_df, new_df], ignore_index=True)
        updated_df.to_excel(SERVICE_LIST, index=False)

    except FileNotFoundError:
        new_df.to_excel(SERVICE_LIST , index=False)
        
def register_testdrive(user_id , fullname , contact_number, auto_model, test_date, time, comments, registration_time):
    
    """
    ◦ ФИО. - fullname\n 
    ◦ Контактный телефон. - contact_number\n
    ◦ Модель автомобиля. - auto_model\n
    ◦ Выбор машины(выбор из списка, который редактируется в админ-панели). - service\n
    ◦ Желаемая дата. - date_service\n
    ◦ Желаемое время. - time_service\n
    ◦ Дата и время регистрации. - registration_time\n
    ◦ ID Пользователя
    """

    new_df = pd.DataFrame([{
        'User_ID':user_id,
        'Full name': fullname,
        'Phone/Contact number' : contact_number,
        'Auto Model' : auto_model,
        'Test date' : test_date,
        'Registration time' : registration_time,
        'Time Service' : time,
        'Comments' : comments
        }])
    
    
    try:
        ex_df = pd.read_excel(TEST_DRIVE_LIST)
        
        updated_df = pd.concat([ex_df, new_df], ignore_index=True)
        updated_df.to_excel(TEST_DRIVE_LIST, index=False)

    except FileNotFoundError:
        new_df.to_excel(TEST_DRIVE_LIST , index=False)
        
        
