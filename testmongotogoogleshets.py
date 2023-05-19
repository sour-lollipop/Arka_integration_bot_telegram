from aiogram import Bot, Dispatcher, executor, types
import pymongo
from pymongo import MongoClient
# from google.oauth2.service_account import Credentials
# import gspread
# from gspread_formatting import *
# from gspread_formatting import Color
client = MongoClient('mongodb+srv://akmaral:aktolkyn2018@clusterarkabot.obnb02f.mongodb.net/test')
# выбор базы данных и коллекции
db = client.Clients_applications_DB
specialist_collection = db.specialist_collection
collection = db.applications_collection
group_chat_id_bd = db.group_chat_id

group = {
        "name":"group_chat",
        "group_chat_id" : 910221550
}
group_chat_id_bd.insert_one(group)

group_chat_id_bd.update_one({"name": "group_chat"}, {"$set":{"group_chat_id": 5446}})
idd = group_chat_id_bd.find_one({'name': "group_chat"})["group_chat_id"]
# msg = "1198133863 Черный"
# spec = {
#     'spec_id': int(msg.split()[0]),
#     'spec_name': ''.join(msg.split()[1:])
# }
# specialist_collection.insert_one(spec)
# spec = specialist_collection.find_one({'spec_id': 1198133863})
# specialist_collection.update_one({"spec_id": spec["spec_id"]}, {"$set":{"spec_name": "Nikita"}})

# for task in collection.find({'status': 'Отказано'}):
#      print(task['_id'])

# users_collection = db.users_collection

# user = {
#             'username': 'Akma',
#             'user_id': '836047649',
#             'language': 'uz'
#         }
# users_collection.insert_one(user)
# if  users_collection.find_one({'user_id':'836047649'}):
#     print('YES')
#     user = users_collection.find_one({'user_id':'836047649'})
#     lang = user['language'] 
# else:
#     print('NO')
# # добавление новой записи
# for i in range(10):
#     post = {"author": f"ChatGPT{i+1}", "text": "Hello, MongoDB!"}
#     # post_id = collection.insert_one(post).inserted_id

# # Подключение к Google Sheets
# scope = ["https://www.googleapis.com/auth/drive", "https://www.googleapis.com/auth/spreadsheets"]
# creds = Credentials.from_service_account_file("./fluted-union-384407-f6335f10cab3.json", scopes=scope)
# client = gspread.authorize(creds)
# sheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1FaLQeTl6fob_cgkEjUeklDIp58lOpc7OU_0dX9lCklM/edit?usp=sharing").sheet1

# column_1 = sheet.get('A1:A')
# values_column_1 = [cell[0] for cell in column_1]
# t = 0
# while t < 3:
#     print(values_column_1[t])
#     t += 1

# # Чтение данных из второго столбца (столбец B)
# column_2 = sheet.get('B1:B')
# values_column_2 = [cell[0] for cell in column_2]
# k = 0
# while k < 3:
#     print(values_column_2[k])
#     k += 1
# with open('./translationsdata.txt','w', encoding='utf-8') as file:
#     for i in range(len(values_column_1)):
#         line = f'"{values_column_1[i]}" : "{values_column_2[i]}",\n'
        # file.writelines(line)
# # sheet.format('A1:B1', {'textFormat': {'bold': True}})
# # Чтение данных из MongoDB и запись их в Google Sheets
# data = []
# # for post in collection.find():
# data.append([post["author"], post["text"]])


# # for element in data:
# #     sheet.insert_row(element)    

# sheet.insert_rows(data)

# # вывод всех записей в коллекции
# for post in collection.find():
#     print(post)