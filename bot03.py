import logging
from aiogram import Bot,Dispatcher,executor,types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import os
import locale
from google.oauth2.service_account import Credentials
import gspread
from pymongo import MongoClient

client = MongoClient('mongodb+srv://akmaral:aktolkyn2018@clusterarkabot.obnb02f.mongodb.net/test')
db = client.Clients_applications_DB
collection = db.applications_collection

scope = ["https://www.googleapis.com/auth/drive", "https://www.googleapis.com/auth/spreadsheets"]
creds = Credentials.from_service_account_file("./fluted-union-384407-f6335f10cab3.json", scopes=scope)
client = gspread.authorize(creds)
sheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1YXVuFm9O1qhuZQiBoEEI2ns3vfm_prh4rgI0LK6sMMw/edit?usp=sharing").sheet1


locale.setlocale(locale.LC_ALL, '')
'ru_RU.utf8'
# Configure logging
logging.basicConfig(level = logging.INFO)
# Initialize bot and storage
bot = Bot(token = '5924382439:AAGLwM6sUPbY_cVxmOKzT_xf3b-PaUesZPs')
dp = Dispatcher(bot, storage = MemoryStorage())
# остановить все процессы
stop = InlineKeyboardButton("стоп", callback_data='stop')
aboute = InlineKeyboardButton("о боте", callback_data='about')
base_KB = InlineKeyboardMarkup(row_width=1).row(aboute, stop)
# Кнопки для клиентов, чтоб выбирали куда заявку писать
button_iiko = InlineKeyboardButton('Iiko', callback_data='Iiko')
button_1c = InlineKeyboardButton('1C', callback_data='1C')
choose_iiko_1c_KB = InlineKeyboardMarkup(row_width=1).row(button_1c, button_iiko).row(stop,aboute)



# кнопки для специалистов, чтоб смотреть заявки
button_iiko_cpec = InlineKeyboardButton('Iiko', callback_data='Iiko_cpec')
button_1c_cpec = InlineKeyboardButton('1C', callback_data='1C_cpec')
choose_iiko_1c_for_cpec_KB = InlineKeyboardMarkup(row_width=1).row(button_iiko_cpec, button_1c_cpec)

# кнопки для специалистов, чтоб смотреть список специалистов и добавлять их 
list_of_spec = InlineKeyboardButton('Список специалистов',callback_data="list_of_spec")
add_spec = InlineKeyboardButton('Добавить специалиста',callback_data="add_spec")
spec_kb = InlineKeyboardMarkup(row_width=1).row(list_of_spec,add_spec)
# кнопки для специалистов, чтоб смотреть список принятых заявок
accec_iiko_tsak = InlineKeyboardButton('Iiko',callback_data="accec_iiko_tsak")
accec_1C_tsak = InlineKeyboardButton('1С',callback_data="accec_1C_tsak")
acceces_task = InlineKeyboardMarkup(row_width=1).row(accec_iiko_tsak,accec_1C_tsak)



# кнопки для принятия или отказа заявки
yes_iiko = InlineKeyboardButton(text="YES", callback_data="iiko_btn_Yes")
no_iiko = InlineKeyboardButton(text="NO", callback_data="iiko_btn_No")    
option_for_iiko_KB = InlineKeyboardMarkup(row_width=1).add(yes_iiko, no_iiko)

yes_1C = InlineKeyboardButton(text="YES", callback_data="1C_btn_Yes")
no_1C = InlineKeyboardButton(text="NO", callback_data="1C_btn_No")    
option_for_1C_KB = InlineKeyboardMarkup(row_width=1).add(yes_1C, no_1C)


class Clients_States(StatesGroup):
    fio_client_state = State()
    contact_number_client_state = State()
    organization_name_client_state = State()
    version_iiko_client_state = State()
    conf_client_state = State()
    count_cass_client_state = State()
    contact_client_state = State()
    contact_client_phone_state = State()
    adress_client_state = State()
    date_client_state = State()

class Specialist_States(StatesGroup):
    add_spec_state = State()
    comment_state = State()
    comment_state_1C = State()
   

# @dp.message_handler(content_types=['new_chat_members'])
# async def new_members(msg):
#     for i in range(len(msg.new_chat_members)):
#         name = msg.new_chat_members[i].first_name
#         await bot.send_message(msg.chat.id, f"Добро пожаловать, @{name}! \n"\
#                             "Что бы отправить заявку, пишите мне в директ(лс)")
        
@dp.message_handler(commands=['start'], state='*')
async def start_command(msg: types.Message, state: FSMContext):
    await state.finish()
    # кнопки для специалистов
    if str(msg.from_user.id) in cpecialist_list():
        await bot.send_message(msg.from_user.id,
                        text=f'Добро пожаловать {msg.from_user.first_name}!\n'+ 
                                ' Выберите свое направление, и появится список заявок.',
                        reply_markup=choose_iiko_1c_for_cpec_KB
                        )
        await bot.send_message(msg.from_user.id,
                               text='Выберете свое направление и понему появится список принятых заявок:',
                               reply_markup=acceces_task)
        await bot.send_message(msg.from_user.id,
                        text=f'Вы можете просмотреть список специалистов или добавить специалиста\n', 
                        reply_markup= spec_kb
                        )

    else:    
    # кнопки для клиентов   
        await bot.send_message(msg.from_user.id,
                                text=f'Добро пожаловать {msg.from_user.first_name}!\n'+ 
                                        'Создать заявку для интеграции'
                                ,reply_markup=choose_iiko_1c_KB
                                )
        
@dp.callback_query_handler(lambda c: c.data == 'stop')
async def stop_process(callback_query: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await  callback_query.message.answer('Вы остановили все процессы')

@dp.message_handler(commands=['stop'], state='*')
async def stop_command(msg: types.Message, state: FSMContext):
    await state.finish()

@dp.callback_query_handler(lambda c: c.data == 'about')
async def stop_process(callback_query: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await  callback_query.message.answer('В данном боте вы можете создать заявки'+
                                         ' для интеграции 1С или Iiko. Для этого'+
                                         ' вам всего лишь нужно ответить на несколько вопросов'
                                         )

@dp.callback_query_handler(lambda c: c.data == 'Iiko')
async def Start_to_create_Iiko(callback_query: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await state.update_data(client_choose = 1)
    await  callback_query.message.answer('Напишите ФИО менеджера арки')
    await Clients_States.fio_client_state.set()

@dp.callback_query_handler(lambda c: c.data == '1C')
async def Start_to_create_1C(callback_query: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await state.update_data(client_choose = 2)
    await  callback_query.message.answer('Напишите ФИО менеджера арки')
    await Clients_States.fio_client_state.set()

@dp.message_handler(content_types=['text'], state= Clients_States.fio_client_state)
async def save_date_fio(msg: types.Message, state: FSMContext):
    await state.update_data(client_name = msg.from_user.first_name,
                            client_id = msg.from_user.id,
                            client_fio = msg.text,
                            client_msg_date = msg.date.strftime('%w %B %H:%M')
                            )
    await bot.send_message(msg.from_user.id,
                           'Напишите контактный номер менеджера арки'
                           )
    await Clients_States.contact_number_client_state.set()

@dp.message_handler(content_types=['text'], state= Clients_States.contact_number_client_state)
async def save_date_contact_number(msg: types.Message, state: FSMContext):
    await state.update_data(client_contact_number = msg.text)

    await bot.send_message(msg.from_user.id,'Напишите имя организации')
    await Clients_States.organization_name_client_state.set()


@dp.message_handler(content_types=['text'], state= Clients_States.organization_name_client_state)
async def save_date_organization(msg: types.Message, state: FSMContext):
    await state.update_data(client_organization_name = msg.text)
    data = await state.get_data()
    if data['client_choose'] == 1:
        await  bot.send_message(msg.from_user.id,'Введите версию Iiko\n'+
                                'Например: Iiko v 1.2.734')
        await Clients_States.version_iiko_client_state.set()
    else:
        await  bot.send_message(msg.from_user.id,'Какая у вас конфигурация данных?'+
                                '(версия, редакцию, типовая или доработанная)\n'+
                                'Например: Управление торговлей, редакция 11.4.8')
        await Clients_States.conf_client_state.set()



@dp.message_handler(content_types=['text'], state=Clients_States.version_iiko_client_state)
async def save_version_iiko(msg: types.Message, state: FSMContext):
    await state.update_data(client_version_iiko = msg.text)
    await bot.send_message(msg.from_user.id,
                        'Напишите ФИО клиента'
                        )
    await Clients_States.contact_client_state.set()


@dp.message_handler(content_types=['text'], state=Clients_States.conf_client_state)
async def save_date_conf_client(msg: types.Message, state: FSMContext):
    await state.update_data(client_conf = msg.text,)

    await bot.send_message(msg.from_user.id,
                            'Напишите количество касс'
                            )
    await Clients_States.count_cass_client_state.set()

@dp.message_handler(content_types=['text'], state=Clients_States.count_cass_client_state)
async def save_date_conf_client(msg: types.Message, state: FSMContext):
    await state.update_data(count_cass_client_state = msg.text,)

    await bot.send_message(msg.from_user.id,
                            'Напишите ФИО клиента'
                            )
    await Clients_States.contact_client_state.set()

@dp.message_handler(content_types=['text'], state=Clients_States.contact_client_state)
async def save_contact_client(msg: types.Message, state: FSMContext):
    await state.update_data(client_contact_client = msg.text)
    await bot.send_message(msg.from_user.id,
                                'Напишите номер клиента'
                                )
    await Clients_States.contact_client_phone_state.set()

@dp.message_handler(content_types=['text'], state=Clients_States.contact_client_phone_state)
async def save_contact_client(msg: types.Message, state: FSMContext):
    await state.update_data(contact_client_phone_state = msg.text)
    
    data = await state.get_data()
    if data['client_choose'] == 1:
        await bot.send_message(msg.from_user.id,
                            'Напишите адрес\n'+
                            'Например: страна Казахстан, город Алматы, улица Таугуль, дом 33б'
                            )
        await Clients_States.adress_client_state.set()
    else:
        n = 1
        for file in os.listdir():
            if f"{data['client_name']} {data['client_id']}" in file:
                n+=1
        file_name = f"{data['client_name']} {data['client_id']} C{n}.txt" 

        save_data( file_name = file_name, 
                    client_name = data['client_name'],
                    client_id = data['client_id'],
                    client_fio = data['client_fio'],
                    client_contact_number = data['client_contact_number'],
                    client_client_organization_name = data['client_organization_name'],
                    client_choose = data['client_choose'], 
                    client_contact_client =data['client_contact_client'] ,
                    contact_client_phone_state = data['contact_client_phone_state'],
                    count_cass_client_state = data['count_cass_client_state'],
                    client_msg_date = data['client_msg_date'],
                    client_conf = data['client_conf'] 
                )
        await bot.send_message(chat_id = group_chat_id , 
                           text="Появилась заявка для 1C интеграции"
                           )
        with open('notifications_1C.txt','a',encoding='utf-8') as file:
            file.writelines(f"{data['client_name']}//{data['client_msg_date']}//{data['client_id']}//C{n}\n") 

        await bot.send_message(msg.from_user.id,
                        'Ваша заявка отправлена\n'+
                        'Скоро вам придет ответ специалиста'
                        )
        # View task 
        with open(f"{file_name}", encoding='utf-8') as file:
            file_text = file.readlines()
        task = ''
        for i in range(len(file_text)):
            if i != 0:
                task += file_text[i]
        await bot.send_message(chat_id = group_chat_id , 
                            text=task
                            )
        await state.finish()

@dp.message_handler(content_types=['text'], state=Clients_States.adress_client_state)
async def save_adress(msg: types.Message, state: FSMContext):
    await state.update_data(client_adress = msg.text)
    await bot.send_message(msg.from_user.id,
                        'Напишите дату установки\n'+
                        'Например: 28.11.2023 18:00 UTC+6'
                        )
    await Clients_States.date_client_state.set()
# ********************************************
# ********************************************************
# ********************************************************

def save_data( file_name, 
                    client_name,
                    client_id,
                    client_fio,
                    client_contact_number,
                    client_client_organization_name, 
                    client_choose,
                    client_contact_client,
                    contact_client_phone_state,
                    client_msg_date,
                    client_date= 'None',
                    client_adress= 'None',
                    client_version_iiko = 'None',
                    client_conf = 'None',
                    count_cass_client_state = 'None'
                  ):
    with open(f"{file_name}",'w', encoding='utf-8') as file:
          file.writelines(f"Ник и id клиента:: {client_name} {client_id}\n")
          file.writelines(f"ФИО менаджера:: {client_fio}\n")
          file.writelines(f"Контактный номер менеджера:: {client_contact_number}\n")
          file.writelines(f"Имя организации:: {client_client_organization_name}\n")


    if client_choose == 1:
      with open(f"{file_name}",'a', encoding='utf-8') as file:
        file.writelines(f"Версия Iiko:: {client_version_iiko}\n")
        file.writelines(f"Время установки:: {client_date}\n")
        file.writelines(f"Адрес установки:: {client_adress}\n")
    elif client_choose == 2:
        with open(f"{file_name}",'a', encoding='utf-8') as file:
            file.writelines(f"Конфигурация данных:: {client_conf}\n")
            file.writelines(f"Количество касс:: {count_cass_client_state}\n")

    with open(f"{file_name}",'a', encoding='utf-8') as file:
          file.writelines(f"Имя клиента:: {client_contact_client}\n")
          file.writelines(f"Контактный номер телефона:: {contact_client_phone_state}\n")
          file.writelines(f"Данная заявка была отправлена:: {client_msg_date}\n")

group_chat_id = -1001840340665
@dp.message_handler(content_types=['text'], state=Clients_States.date_client_state)
async def save_dates(msg: types.Message, state: FSMContext):
    data = await state.get_data()
    if data['client_choose'] == 1:
        await state.update_data(client_date = msg.text.lower())
    data = await state.get_data()
    n = 1
    for file in os.listdir():
        if f"{data['client_name']} {data['client_id']}" in file:
            n+=1
    group_chat_id = -1001840340665

    file_name = f"{data['client_name']} {data['client_id']} I{n}.txt" 

    save_data( file_name = file_name, 
                client_name = data['client_name'],
                client_id = data['client_id'],
                client_fio = data['client_fio'],
                client_contact_number = data['client_contact_number'],
                client_client_organization_name = data['client_organization_name'],
                client_choose = data['client_choose'], 
                client_contact_client =data['client_contact_client'] ,
                contact_client_phone_state = data['contact_client_phone_state'],
                client_date = data['client_date'],
                client_adress = data['client_adress'],
                client_msg_date = data['client_msg_date'],
                client_version_iiko = data['client_version_iiko'] 
            )
    await bot.send_message(chat_id = group_chat_id , 
                        text="Появилась заявка для Iiko интеграции"
                        )
    with open('notifications_Iiko.txt','a',encoding='utf-8') as file:
        file.writelines(f"{data['client_name']}//{data['client_msg_date']}//{data['client_id']}//I{n}\n")  
    
    await bot.send_message(msg.from_user.id,
                        'Ваша заявка отправлена\n'+
                        'Скоро вам придет ответ специалиста'
                        )
    # View task 
    with open(f"{file_name}", encoding='utf-8') as file:
        file_text = file.readlines()
    task = ''
    for i in range(len(file_text)):
        if i != 0:
            task += file_text[i]
    await bot.send_message(chat_id = group_chat_id , 
                           text=task
                           )
    await state.finish()
# *************************************
# *************************************
# *************************************

# Просмотреть id чат
@dp.message_handler(commands=['id'])
async def send_welcome(message: types.Message):    
    await message.reply(message.chat.id)
# *******************************************************
# *******************************************************
# *******************************************************
# составить список специалистов
def cpecialist_list():
    with open('./specialist_list.txt',encoding='utf-8') as file:
        specialist_list = file.readlines()
    # specialist_list = open('./specialist_list.txt',encoding='utf-8').readlines()
    cpecs = []
    for spec in specialist_list:
        for el in spec.split():
            cpecs.append(el)
    return cpecs
# добавить специалистов
@dp.callback_query_handler(lambda c: c.data == 'add_spec')
async def instruction_for_add(callback_query: types.CallbackQuery):
        await callback_query.message.answer(text =  f'Ввидите id и имя специалиста,'+ 
                                            'которого хотите добавить\n'+
                                            'например: 123456789 Сергей'
                                            )
        await Specialist_States.add_spec_state.set()

@dp.message_handler(content_types=['text'], state=Specialist_States.add_spec_state)
async def update_spec(msg=types.Message, state=FSMContext):
    with open(f'./specialist_list.txt', 'a', encoding='utf-8') as file:
        file.writelines(f'{msg.text}\n')
    
    await bot.send_message(chat_id=msg.from_user.id, 
                           text= f'Вы успешно добавили специалиста:\n{msg.text}'
                            )
    await state.finish()
# Просмотр список специалистов
@dp.callback_query_handler(lambda c: c.data == 'list_of_spec')
async def list_of_spec(callback_query: types.CallbackQuery):
    
        cpec_list = ''
        period = 0
        for cpec in cpecialist_list():
            period += 1
            cpec_list+= f"{cpec} "
            if period%2 == 0:
                cpec_list+='\n'
            
        await callback_query.message.answer( f'Список специалистов:\n {cpec_list}')
# ******************************************        
# ******************************************        
# ******************************************        
# Просмотр заявок для интеграции Iiko
@dp.callback_query_handler(lambda c: c.data == 'Iiko_cpec')
async def iiko_notifications(callback_query: types.CallbackQuery, state: FSMContext):

    nots_iiko_KB = InlineKeyboardMarkup(row_width=1)

    with open ('./notifications_Iiko.txt',encoding='utf-8') as file:
        notifications_list = file.readlines()

    for line in notifications_list:
        notification =  f"{line.split('//')[0]} {line.split('//')[1]} {line.split('//')[3]}"
        notification_id = f"notification_iiko_{line.split('//')[2]}_{line.split('//')[3]}"
        nots_iiko_KB.add(InlineKeyboardButton(text=notification,
                                                 callback_data=notification_id
                                                 ))
    await callback_query.message.answer('Список заявок:',
                                        reply_markup=nots_iiko_KB
                                        )
   

# Call button iiko task 
@dp.callback_query_handler(lambda c: c.data and c.data.startswith('notification_iiko'))
async def iiko_notification(callback_query: types.CallbackQuery, state: FSMContext):

    notification = f"{callback_query.data.split('_')[2]} {callback_query.data.split('_')[3]}"
    print('Notification:', notification)
    task_text = ''
    k = 0
    for file in os.listdir():
        print(file)
        if ((notification.split()[0] in file) and (notification.split()[1] in file)) and 'YESI' not in file:
            k+=1
            with open(file, encoding='utf-8')as task_file:
                task = task_file.readlines()
            for line in task:
                task_text += line
            await callback_query.message.answer(task_text)

            await state.update_data(client_task = task_text,
                                    client_task_number = notification.split()[1],
                                    client_id = notification.split()[0],
                                    client_file = file,
                                    client_name = file.split()[0],
                                    db_menedjer_name = f"{task[1].split('::')[1]}" ,
                                    db_menedjer_phone = f"{task[2].split('::')[1]}" ,
                                    db_organization = f"{task[3].split('::')[1]}" ,
                                    db_client_name = f"{task[7].split('::')[1]}" ,
                                    db_client_phone = f"{task[8].split('::')[1]}" ,
                                    db_task_date = f"{task[9].split('::')[1]}" ,
                                    db_type_in = 'Iiko'
                                    )
            await callback_query.message.answer('Принять заявку?', 
                                                reply_markup=option_for_iiko_KB
                                                )
    if k == 0:
        await callback_query.message.answer('Данной заявки уже нет')

@dp.callback_query_handler(lambda c: c.data == 'iiko_btn_Yes')
async def receive_task(callback_query: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await bot.edit_message_reply_markup(
        chat_id=callback_query.from_user.id,
        message_id=callback_query.message.message_id, 
        reply_markup=None
    )
    await callback_query.message.answer("Принято")
    await bot.send_message(int(data["client_id"]), 'Ваша заявка принята')
    await bot.send_message(int(data["client_id"]), 'Заявка:')
    await bot.send_message(int(data["client_id"]), data['client_task'])


    await bot.send_message(group_chat_id, 'Данная заявка была принята')
    await bot.send_message(group_chat_id, data['client_task'])

    os.remove(f'./{data["client_file"]}')
    with open(f"YESI {data['client_file']}", 'w', encoding='utf-8') as file:
        for line in data['client_task']:
            file.writelines(line)

    with open('./notifications_Iiko.txt', encoding='utf-8') as file:
        notifications = file.readlines()
    for line in notifications:
        if data["client_id"] in line and  data['client_task_number'] in line:
            notifications.remove(line)
    with open('./notifications_Iiko.txt','w', encoding='utf-8') as file:
        for line in notifications:
            file.writelines(line)

    print(data["client_file"])
    print(data["client_id"])
    print(data["client_name"])
    print(data["client_task_number"])
    await state.finish()

# *************************************
# *************************************
# *************************************

@dp.callback_query_handler(lambda c: c.data == 'iiko_btn_No')
async def receive_task(callback_query: types.CallbackQuery, state: FSMContext):
    
    await bot.edit_message_reply_markup(
        chat_id=callback_query.from_user.id,
        message_id=callback_query.message.message_id, 
        reply_markup=None
    )
    data = await state.get_data()

    await callback_query.message.answer("Отказано")
    os.remove(f'./{data["client_file"]}')
    await callback_query.message.answer("Напишите причину отказа")
    await Specialist_States.comment_state.set()

@dp.message_handler(content_types=['text'],state=Specialist_States.comment_state)
async def send_comment(msg: types.Message, state: FSMContext):
    data = await state.get_data()
    await bot.send_message(int(data["client_id"]), 'Ваша заявка не принята')
    await bot.send_message(int(data["client_id"]), 'Заявка:')
    await bot.send_message(int(data["client_id"]), data['client_task'])
    await bot.send_message(int(data["client_id"]), f'Комментарий специалиста\n{msg.text}')


    await bot.send_message(group_chat_id, 'Данная заявка не принято:')
    await bot.send_message(group_chat_id, data['client_task'])
    await bot.send_message(group_chat_id, f'Причина:\n{msg.text}')

    post = {"manager_name": f"{data['db_menedjer_name']}",
            "manager_phone": f"{data['db_menedjer_phone']}",
            "organization": f"{data['db_organization']}",
            "client_name": f"{data['db_client_name']}",
            "client_phone": f"{data['db_client_phone']}",
            "type": f"{data['db_type_in']}",
            "task_date": f"{data['db_task_date']}",
            "status": "Отказано",
            }
    post_id = collection.insert_one(post).inserted_id
    datadb = []
    datadb.append([post["manager_name"], 
                    post["manager_phone"],
                    post["organization"],
                    post["client_name"],
                    post["type"],
                    post["task_date"],
                    post["status"]
                ])
    sheet.insert_rows(datadb)

    with open('./notifications_Iiko.txt', encoding='utf-8') as file:
        notifications = file.readlines()
    for line in notifications:
        if data["client_id"] in line and  data['client_task_number'] in line:
            notifications.remove(line)
    with open('./notifications_Iiko.txt','w', encoding='utf-8') as file:
        for line in notifications:
            file.writelines(line)
    await state.finish()

@dp.callback_query_handler(lambda c: c.data == 'accec_iiko_tsak')
async def view_accepted_task(callback_query: types.CallbackQuery, state: FSMContext):
        task_iiko_accepted_KB = InlineKeyboardMarkup(row_width=1)
        numeration = 0
        for file in os.listdir():
            if "YESI" in file:
                task_iiko_accepted_KB.add(InlineKeyboardButton(text=file, callback_data=f'{file}//{numeration}'))
                numeration += 1
        await callback_query.message.answer("Список принятых заявок Iiko",
                               reply_markup=task_iiko_accepted_KB)

@dp.callback_query_handler(lambda c: c.data and c.data.startswith('YESI'))
async def iiko_accepted_task(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.edit_message_reply_markup(
                                        chat_id=callback_query.from_user.id,
                                        message_id=callback_query.message.message_id, 
                                        reply_markup=None
                                        )
    task = callback_query.data.split('//')[0]
    print(task)
    task_text = ''

    with open(task, encoding='utf-8') as file:
        text = file.readlines()
    for line in text:
        task_text += line
    await state.update_data(db_menedjer_name = f"{text[1].split('::')[1]}" ,
                            db_menedjer_phone = f"{text[2].split('::')[1]}" ,
                            db_organization = f"{text[3].split('::')[1]}" ,
                            db_client_name = f"{text[7].split('::')[1]}" ,
                            db_client_phone = f"{text[8].split('::')[1]}" ,
                            db_task_date = f"{text[9].split('::')[1]}" ,
                            db_type_in = 'Iiko',
                            file_name = task
                            )
    await callback_query.message.answer(task_text, reply_markup=save_db_kb)

closed_btn = InlineKeyboardButton('Закрыть', callback_data='closed_tasks')
regected_btn = InlineKeyboardButton('Отменить', callback_data='regected_tasks')
save_db_kb = InlineKeyboardMarkup(row_width=1).row(closed_btn, regected_btn)

@dp.callback_query_handler(lambda c: c.data == 'closed_tasks')
async def save_db_closed_tasks(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.edit_message_reply_markup(
        chat_id=callback_query.from_user.id,
        message_id=callback_query.message.message_id, 
        reply_markup=None
    )
    data = await state.get_data()
    os.remove(data['file_name'])
    post = {"manager_name": f"{data['db_menedjer_name']}",
        "manager_phone": f"{data['db_menedjer_phone']}",
        "organization": f"{data['db_organization']}",
        "client_name": f"{data['db_client_name']}",
        "client_phone": f"{data['db_client_phone']}",
        "type": f"{data['db_type_in']}",
        "task_date": f"{data['db_task_date']}",
        "status": "Закрыто(Выполнено)"
        }
    datadb = []
    post_id = collection.insert_one(post).inserted_id
    datadb.append([post["manager_name"], 
                    post["manager_phone"],
                    post["organization"],
                    post["client_name"],
                    post["type"],
                    post["task_date"],
                    post["status"]
                    ])
    sheet.insert_rows(datadb)
    await callback_query.message.answer('Данная заявка была закрыта(завершена)')

@dp.callback_query_handler(lambda c: c.data == 'regected_tasks')
async def save_db_regected_tasks(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.edit_message_reply_markup(
        chat_id=callback_query.from_user.id,
        message_id=callback_query.message.message_id, 
        reply_markup=None
    )
    data = await state.get_data()
    os.remove(data['file_name'])
    post = {"manager_name": f"{data['db_menedjer_name']}",
        "manager_phone": f"{data['db_menedjer_phone']}",
        "organization": f"{data['db_organization']}",
        "client_name": f"{data['db_client_name']}",
        "client_phone": f"{data['db_client_phone']}",
        "type": f"{data['db_type_in']}",
        "task_date": f"{data['db_task_date']}",
        "status": "Отменено"
        }
    datadb = []
    post_id = collection.insert_one(post).inserted_id
    datadb.append([post["manager_name"], 
                    post["manager_phone"],
                    post["organization"],
                    post["client_name"],
                    post["type"],
                    post["task_date"],
                    post["status"]
                    ])
    sheet.insert_rows(datadb)
    await callback_query.message.answer('Данная заявка была отменена')

# ******************************************        
# ******************************************        
# ******************************************        
# Просмотр заявок для интеграции 1C
@dp.callback_query_handler(lambda c: c.data == '1C_cpec')
async def notifications_1C(callback_query: types.CallbackQuery, state: FSMContext):
    nots_1C_KB = InlineKeyboardMarkup(row_width=1)

    with open ('./notifications_1C.txt',encoding='utf-8') as file:
        notifications_list = file.readlines()

    for line in notifications_list:
        notification =  f"{line.split('//')[0]} {line.split('//')[1]} {line.split('//')[3]}"
        notification_id = f"notifications_1C_{line.split('//')[2]}_{line.split('//')[3]}"
        nots_1C_KB.add(InlineKeyboardButton(text=notification,
                                                 callback_data=notification_id
                                                 ))
    await callback_query.message.answer('Список заявок:',
                                        reply_markup=nots_1C_KB
                                        )

# Call button 1C task 
@dp.callback_query_handler(lambda c: c.data and c.data.startswith('notifications_1C'))
async def notification_1C(callback_query: types.CallbackQuery, state: FSMContext):

    notification = f"{callback_query.data.split('_')[2]} {callback_query.data.split('_')[3]}"
    print('Notification:', notification)
    task_text = ''
    k = 0
    for file in os.listdir():
        print(file)
        if ((notification.split()[0] in file) and (notification.split()[1] in file)) and 'YESC' not in file:
            k+=1
            with open(file, encoding='utf-8')as task_file:
                task = task_file.readlines()
            for line in task:
                task_text += line
            await callback_query.message.answer(task_text)

            
            
            await state.update_data(client_task = task_text,
                                    client_task_number = notification.split()[1],
                                    client_id = notification.split()[0],
                                    client_file = file,
                                    client_name = file.split()[0],
                                    db_menedjer_name = f"{task[1].split('::')[1]}",
                                    db_menedjer_phone = f"{task[2].split('::')[1]}",
                                    db_organization = f"{task[3].split('::')[1]}",
                                    db_client_name = f"{task[6].split('::')[1]}",
                                    db_client_phone = f"{task[7].split('::')[1]}",
                                    db_task_date = f"{task[8].split('::')[1]}" ,
                                    db_type_in = '1C'
                                    )
            await callback_query.message.answer('Принять заявку?', 
                                                reply_markup=option_for_1C_KB
                                                )
    if k == 0:
        await callback_query.message.answer('Данной заявки уже нет')

@dp.callback_query_handler(lambda c: c.data == '1C_btn_Yes')
async def receive_task_1C(callback_query: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await bot.edit_message_reply_markup(
        chat_id=callback_query.from_user.id,
        message_id=callback_query.message.message_id, 
        reply_markup=None
    )
    await callback_query.message.answer("Принято")
    await bot.send_message(int(data["client_id"]), 'Ваша заявка принята')
    await bot.send_message(int(data["client_id"]), 'Заявка:')
    await bot.send_message(int(data["client_id"]), data['client_task'])
    
    await bot.send_message(group_chat_id, 'Данная заявка была принята')
    await bot.send_message(group_chat_id, data['client_task'])

    os.remove(f'./{data["client_file"]}')
    with open(f"YESC {data['client_file']}", 'w', encoding='utf-8') as file:
        for line in data['client_task']:
            file.writelines(line)

    with open('./notifications_1C.txt', encoding='utf-8') as file:
        notifications = file.readlines()
    for line in notifications:
        if data["client_id"] in line and  data['client_task_number'] in line:
            notifications.remove(line)
    with open('./notifications_1C.txt','w', encoding='utf-8') as file:
        for line in notifications:
            file.writelines(line)

    print(data["client_file"])
    print(data["client_id"])
    print(data["client_name"])
    print(data["client_task_number"])
    await state.finish()


@dp.callback_query_handler(lambda c: c.data == '1C_btn_No')
async def receive_task_1C(callback_query: types.CallbackQuery, state: FSMContext):
    
    await bot.edit_message_reply_markup(
        chat_id=callback_query.from_user.id,
        message_id=callback_query.message.message_id, 
        reply_markup=None
    )
    data = await state.get_data()
    
    await callback_query.message.answer("Отказано")
    os.remove(f'./{data["client_file"]}')
    await callback_query.message.answer("Напишите причину отказа")
    await Specialist_States.comment_state_1C.set()

@dp.message_handler(content_types=['text'],state=Specialist_States.comment_state_1C)
async def send_comment_1C(msg: types.Message, state: FSMContext):
    data = await state.get_data()
    await bot.send_message(int(data["client_id"]), 'Ваша заявка не принята')
    await bot.send_message(int(data["client_id"]), 'Заявка:')
    await bot.send_message(int(data["client_id"]), data['client_task'])
    await bot.send_message(int(data["client_id"]), f'Комментарий специалиста\n{msg.text}')

    await bot.send_message(group_chat_id, 'Данная заявка не принято:')
    await bot.send_message(group_chat_id, data['client_task'])
    await bot.send_message(group_chat_id, f'Причина:\n{msg.text}')

    post = {"manager_name": f"{data['db_menedjer_name']}",
            "manager_phone": f"{data['db_menedjer_phone']}",
            "organization": f"{data['db_organization']}",
            "client_name": f"{data['db_client_name']}",
            "client_phone": f"{data['db_client_phone']}",
            "type": f"{data['db_type_in']}",
            "task_date": f"{data['db_task_date']}",
            "status": "Отказано",
            }
    post_id = collection.insert_one(post).inserted_id
    datadb = []
    datadb.append([post["manager_name"], 
                    post["manager_phone"],
                    post["organization"],
                    post["client_name"],
                    post["type"],
                    post["task_date"],
                    post["status"]
                    ])
    sheet.insert_rows(datadb)
    with open('./notifications_1C.txt', encoding='utf-8') as file:
        notifications = file.readlines()
    for line in notifications:
        if data["client_id"] in line and  data['client_task_number'] in line:
            notifications.remove(line)
    with open('./notifications_1C.txt','w', encoding='utf-8') as file:
        for line in notifications:
            file.writelines(line)
    await state.finish()

@dp.callback_query_handler(lambda c: c.data == 'accec_1C_tsak')
async def view_accepted_task_1C(callback_query: types.CallbackQuery, state: FSMContext):
        task_1C_accepted_KB = InlineKeyboardMarkup(row_width=1)
        numeration = 0
        for file in os.listdir():
            if "YESC" in file:
                task_1C_accepted_KB.add(InlineKeyboardButton(text=file, callback_data=f'{file}//{numeration}'))
                numeration += 1
        await callback_query.message.answer("Список принятых заявок 1C",
                               reply_markup=task_1C_accepted_KB)
        
@dp.callback_query_handler(lambda c: c.data and c.data.startswith('YESC'))
async def accepted_task_1C(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.edit_message_reply_markup(
                                        chat_id=callback_query.from_user.id,
                                        message_id=callback_query.message.message_id, 
                                        reply_markup=None
                                        )
    task = callback_query.data.split('//')[0]
    print(task)
    task_text = ''
    with open(task, encoding='utf-8') as file:
        text = file.readlines()
    for line in text:
        task_text += line
    await state.update_data(db_menedjer_name = f"{text[1].split('::')[1]}",
                            db_menedjer_phone = f"{text[2].split('::')[1]}",
                            db_organization = f"{text[3].split('::')[1]}",
                            db_client_name = f"{text[6].split('::')[1]}",
                            db_client_phone = f"{text[7].split('::')[1]}",
                            db_task_date = f"{text[8].split('::')[1]}" ,
                            db_type_in = '1C',
                            file_name = task
                            )
    await callback_query.message.answer(task_text, reply_markup=save_db_kb)
    

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates = True)

# q w e r t y u i o p a s d f g h j k l z x c v b n m