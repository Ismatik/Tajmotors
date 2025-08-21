import pandas as pd
from numpy import ndarray
EXCEL_FILE = '/home/ikki/Desktop/Koinot/Tajmotors/Registration files/Registered_users.xlsx'
TEST_DRIVE_LIST = '/home/ikki/Desktop/Koinot/Tajmotors/Registration files/Test_drive_list.xlsx'


user_id = 631886740

df = pd.read_excel(TEST_DRIVE_LIST)
info = df[df["User_ID"] == user_id]

content = []
# for i in info.values:
#     content.append(i)
# return i
# for i,j,k in ser_row['Auto Model'] , ser_row['Test date'],ser_row['Registration time']:
#     print(i,j,k)

# def return_tdh(user_id):
#     try:
#         df = pd.DataFrame(TEST_DRIVE_LIST)
#         info = df[df["User_ID"] == user_id]
        
#         if not info.empty:
#             # return info[""]
#             pass
#     except:
#         pass