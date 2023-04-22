from aiogram import Bot, Dispatcher, executor, types
import pymongo
from pymongo import MongoClient
from google.oauth2.service_account import Credentials
import gspread
from gspread_formatting import *
from gspread_formatting import Color
client = MongoClient('mongodb+srv://akmaral:aktolkyn2018@clusterarkabot.obnb02f.mongodb.net/test')
# выбор базы данных и коллекции
db = client.Clients_applications_DB
collection = db.applications_collection

# добавление новой записи
for i in range(10):
    post = {"author": f"ChatGPT{i+1}", "text": "Hello, MongoDB!"}
    post_id = collection.insert_one(post).inserted_id

# Подключение к Google Sheets
scope = ["https://www.googleapis.com/auth/drive", "https://www.googleapis.com/auth/spreadsheets"]
creds = Credentials.from_service_account_file("./fluted-union-384407-f6335f10cab3.json", scopes=scope)
client = gspread.authorize(creds)
sheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1YXVuFm9O1qhuZQiBoEEI2ns3vfm_prh4rgI0LK6sMMw/edit?usp=sharing").sheet1

# sheet.format('A1:B1', {'textFormat': {'bold': True}})
# Чтение данных из MongoDB и запись их в Google Sheets
data = []
for post in collection.find():
    data.append([post["author"], post["text"]])


for element in data:
    sheet.insert_row(element)    

sheet.insert_rows(data)

# вывод всех записей в коллекции
for post in collection.find():
    print(post)