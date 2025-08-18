from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr

EXCEL_FILE = '/home/ikki/Desktop/Koinot/Tajmotors/Registration files/Registered_users.xlsx'
TEST_DRIVE_LIST = '/home/ikki/Desktop/Koinot/Tajmotors/Registration files/Test_drive_list.xlsx'
SERVICE_LIST = '/home/ikki/Desktop/Koinot/Tajmotors/Registration files/Service_list.xlsx'
USER_ACTIVITY_LOG_FILE = '/home/ikki/Desktop/Koinot/Tajmotors/user_activity.log'
#Registration Text Selection
START_MESSAGE = {"RU" : f"Здравствуйте! Пожалуйста, зарегистрируйтесь, прежде чем начать. Нам понадобится ваш номер телефона, имя и адрес электронной почты.\nНажмите «Начать регистрацию», чтобы начать регистрацию.",
                 "EN" : f"Hello, Please register before you start. We will need your phone number,name and email.\nClick 'Begin Registration', to start registration",
                 "TJ" : f"Салом, Лутфан пеш аз оғоз шудан сабти ном шавед. Ба мо рақами телефон, ном ва почтаи электронии шумо лозим аст.\nБарои оғози сабти ном 'Оғози бақайдгирӣ' -ро клик кунед."}

PHONE_NUMBER = {"EN" : f"To start, please share your phone number by pressing the button below.",
                "RU" : f"Для начала, пожалуйста, поделитесь своим номером телефона, нажав кнопку ниже.",
                "TJ" : f"Барои оғоз кардан, лутфан рақами телефони худро бо пахш кардани тугмаи зер мубодила кунед."}

BEGIN_REGISTR = {"EN" : "▶️Begin Registration",
                 "RU" : "▶️Начать регистрацию",
                 "TJ" : "▶️Бақайдгирӣ оғоз кунед"}

SHARE_PHONE_NUMBER = {"EN" : "Share phone number",
                      "RU" : "Поделиться номером телефона",
                      "TJ" : "Рақами телефонро мубодила кунед"}

PHONE_NUMBER_REPLY = {"EN" : f"Thank you for sharing number!I've received this info:\n\nPhone number:",
                      "RU" : f"Спасибо, что поделились номером! Я получил эту информацию:\n\nНомер телефона:",
                      "TJ" : f"Ташаккур барои мубодилаи рақам! Ман ин маълумотро гирифтам:\n\nРақами телефон:"}

NAME_FETCH = {"EN" : f"Great! Now, please enter your full name(Example: Gulmurod Gulmurodov).",
              "RU" : f"Отлично! Теперь введите своё полное имя (пример: Гулмурод Гулмуродов).",
              "TJ" : f"Аҷоиб! Акнун, лутфан номи пурраи худро ворид кунед (Масалан: Гулмурод Гулмуродов)."}

FULL_NAME = {"EN" : "Please enter FULL Name.",
             "RU" : "Пожалуйста, введите ПОЛНОЕ имя.",
             "TJ" : "Лутфан номи ПУРРА ворид кунед."}

CONTAIN_NUMBER = {"EN" : "Name can not contain number.",
                  "RU" : "Имя не может содержать цифры.",
                  "TJ" : "Ном наметавонад рақамро дар бар гирад."}

EMAIL = {"EN" : "Wonderful! Please enter your email address.",
         "RU" : "Замечательно! Пожалуйста, введите свой адрес электронной почты.",
         "TJ" : "Аҷоиб! Лутфан суроғаи почтаи электронии худро ворид кунед."}

WRONG_EMAIL = {"EN" : "This doesn't look like e-mail, please check your e-mail again.",
               "RU" : "Это не похоже на электронную почту.Пожалуйста, проверьте почту еще раз",
               "TJ" : "Ин ба почтаи электронӣ монанд нест, лутфан почтаи электронии худро бори дигар тафтиш кунед."}

REGISTRATION_OVER = {"EN" : "Registration complete! Thanks for providing information.\n\n",
                     "RU" : "Регистрация завершена! Спасибо за предоставленную информацию.",
                     "TJ" : "Бақайдгирӣ анҷом ёфт! Ташаккур барои пешниҳоди маълумот."}

BUTTON_EP = {"EN" : "👤 Edit Profile",
             "RU" : "👤 Изменить Профиль",
             "TJ" : "👤 Таҳрири Профил"}
BUTTON_TDH = {"EN" : "🚗 Test Drive History",
              "RU" : "🚗 История Тест-драйв Запросов",
              "TJ" : "🚗 Таърихи Драйви Озмоишӣ"}
BUTTON_SH = {"EN" : "⚙️ Service History",
             "RU" : "⚙️ История обслуживания",
             "TJ" : "⚙️ Таърихи хидмат"}
BUTTON_CS = {"EN" : "📞 Contact Support",
             "RU" : "📞 Обратиться В Службу Поддержки",
             "TJ" : "📞 Бо Дастгирии Тамос"}

BUTTONS_TEXT = {"EN" : "Use the buttons below for quick navigation.",
                "RU" : "Для быстрой навигации используйте кнопки ниже.",
                "TJ" : "Барои паймоиши зуд тугмаҳои зерро истифода баред."}

BUTTON_LANGUAGE = {"EN" : "🌐 Change language",
                   "RU" : "🌐 Изменить Язык",
                   "TJ" : "🌐 Забонро Иваз Кардан"}

BOT_DESCRIPTION = {"RU" : "ООО «Тадж Моторс» — современный 3S комплекс, построенный в соответствии со всеми стандартами TOYOTA MOTOR CORPORATION\nКомпания ООО «Тадж Моторс» является официальным дилером компании TOYOTA MOTOR CORPORATION в Республики Таджикистан с 05 июля 2013 года.",
                   "EN" : "Taj Motors LLC is a modern 3S complex built in accordance with all TOYOTA MOTOR CORPORATION standards\nTaj Motors LLC is the official dealer of TOYOTA MOTOR CORPORATION in the Republic of Tajikistan since July 5, 2013.",
                   "TJ" : 'ҶДММ "Таҷ Моторс" як маҷмааи замонавии 3S мебошад, ки бо тамоми стандартҳои TOYOTA MOTOR CORPORATION сохта шудааст.\nҶДММ Тоҷ Моторс дилери расмии TOYOTA MOTOR CORPORATION дар Ҷумҳурии Тоҷикистон аз 5 июли соли 2013 мебошад.'}

CATALOGUE = {"EN" : "Catalogue",
             "RU" : "Каталог",
             "TJ" : "Феҳрист"}
OPERATOR = {"EN" : "Operator",
            "RU" : "Оператор",
            "TJ" : "Мутахассис"}
TEST_DRIVE = {"EN" : "Test Drive",
              "RU" : "Тест Драйв",
              "TJ" : "Ронандагии озмоишӣ"}
SERVICE = {"EN" : "Service",
           "RU" : "Сервис",
           "TJ" : "Хизматрасонӣ"}
ABOUT_US = {"EN" : "Contact/Address/About Us",
            "RU" : "Контакты/Адрес/О нас",
            "TJ" : "Тамосҳо/Суроға"}

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
