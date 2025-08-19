import pandas as pd
EXCEL_FILE = '/home/ikki/Desktop/Koinot/Tajmotors/Registration files/Registered_users.xlsx'

user_id = 631886740

df = pd.read_excel(EXCEL_FILE)
ser_row = df[df["User_ID"] == user_id]
print(ser_row)