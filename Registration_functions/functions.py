"""Functions to register users or reading files"""

import pandas as pd

EXCEL_FILE = '/home/ikki/Desktop/Koinot/Tajmotors/Registration files/Registered_users.xlsx'
TEST_DRIVE_LIST = '/home/ikki/Desktop/Koinot/Tajmotors/Registration files/Test_drive_list.xlsx'





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
        
    new_df = pd.DataFrame([{
        'User_ID':user_id,
        'Name': name,
        'Phone' : phone,
        'Email' : email,
        'Username' : username
        }])
    try: 
        ex_df = pd.read_excel(EXCEL_FILE)
        
        updated_df = pd.concat([ex_df, new_df], ignore_index=True)
        updated_df.to_excel(EXCEL_FILE, index=False)

    except FileNotFoundError:
        
        new_df.to_excel(EXCEL_FILE , index=False)


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
        ex_df = pd.read_excel(TEST_DRIVE_LIST)
        
        updated_df = pd.concat([ex_df, new_df], ignore_index=True)
        updated_df.to_excel(TEST_DRIVE_LIST, index=False)

    except FileNotFoundError:
        new_df.to_excel(TEST_DRIVE_LIST , index=False)
        

def register_testdrive(user_id , fullname , contact_number, auto_model, test_date, time, comments):
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
