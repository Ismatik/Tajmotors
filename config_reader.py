from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr

EXCEL_FILE = '/home/ikki/Desktop/Koinot/Tajmotors/Registration files/Registered_users.xlsx'
TEST_DRIVE_LIST = '/home/ikki/Desktop/Koinot/Tajmotors/Registration files/Test_drive_list.xlsx'
SERVICE_LIST = '/home/ikki/Desktop/Koinot/Tajmotors/Registration files/Service_list.xlsx'

BOT_DESCRIPTION = ("ООО «Тадж Моторс» — современный 3S комплекс, построенный в соответствии со всеми стандартами TOYOTA MOTOR CORPORATION\nКомпания ООО «Тадж Моторс» является официальным дилером компании TOYOTA MOTOR CORPORATION в Республики Таджикистан с 05 июля 2013 года.")

COMMENTS = f"Great. If you have any <b>additional comments</b> or requests, please enter them. Please add contact number in case if we would not be able to reach you with number you registered with.\n\nIf you have no comments, just send a dash (-) to finish filling request form."

class Settings(BaseSettings):
    #Hide token as SecretStr not Str
    bot_token: SecretStr
    
    #Setting configuration using model_config
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')
    

# When importing a file, a config object will be immediately created
# and validated,
# which can then be imported from different places
config = Settings()
    