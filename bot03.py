import logging
from aiogram import Bot,Dispatcher,executor,types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
import markups as nav
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from translations import _
import os
import locale
from google.oauth2.service_account import Credentials
import gspread
from pymongo import MongoClient
import phonenumbers


client = MongoClient('mongodb+srv://akmaral:aktolkyn2018@clusterarkabot.obnb02f.mongodb.net/test')
db = client.Clients_applications_DB
collection = db.applications_collection
users_collection = db.users_collection

scope = ["https://www.googleapis.com/auth/drive", "https://www.googleapis.com/auth/spreadsheets"]
creds = Credentials.from_service_account_file("./fluted-union-384407-f6335f10cab3.json", scopes=scope)
client = gspread.authorize(creds)
sheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1YXVuFm9O1qhuZQiBoEEI2ns3vfm_prh4rgI0LK6sMMw/edit?usp=sharing").sheet1


locale.setlocale(locale.LC_ALL, '')
'ru_RU.utf8'
# Configure logging
logging.basicConfig(level = logging.INFO)
# Initialize bot and storage
# bot = Bot(token = '5924382439:AAGLwM6sUPbY_cVxmOKzT_xf3b-PaUesZPs')
# test bot token
bot = Bot(token="6027542967:AAH634BtIzZSQiYOIn33WcV1-RQ_9v7bfk0")
dp = Dispatcher(bot, storage = MemoryStorage())

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
    retry_number_arka = State()
    retry_number_client = State()
class Specialist_States(StatesGroup):
    add_spec_state = State()
    drop_spec_state = State()
    edit_spec_state = State()
    comment_state = State()
    comment_state_1C = State()
    change_group_chat_id_state = State()
   

# @dp.message_handler(content_types=['new_chat_members'])
# async def new_members(msg):
#     for i in range(len(msg.new_chat_members)):
#         name = msg.new_chat_members[i].first_name
#         await bot.send_message(msg.chat.id, f"Добро пожаловать, @{name}! \n"\
#                             "Что бы отправить заявку, пишите мне в директ(лс)")
        
@dp.message_handler(commands=['start'], state='*')
async def start_command(msg: types.Message, state: FSMContext):
    await state.finish()
    # насроийки языка
    # кнопки для специалистов
    
    if  users_collection.find_one({'user_id':f'{msg.from_user.id}'}):
        lang = users_collection.find_one({'user_id':f'{msg.from_user.id}'})['language']
        if str(msg.from_user.id) in cpecialist_list():
            await bot.send_message(msg.from_user.id,
                            text=f'{_("Добро пожаловать",lang)} {msg.from_user.first_name}!\n'+ 
                                    _("Выберите свое направление, и появится список заявок.", lang),
                            reply_markup=nav.choose_iiko_1c_(lang)
                            )
            await bot.send_message(msg.from_user.id,
                                text=_('Выберете свое направление и появится список принятых заявок',lang),
                                reply_markup=nav.acceces_task_KB)
            await bot.send_message(msg.from_user.id,
                            text=_("Вы можете просмотреть список специалистов, добавить специалиста или его удалить. Также вы можете поменять свое имя как специалиста(по умолчанию используется имя вашего аккаунта)",lang),
                            reply_markup= nav.spec_(lang)
                            )
            await bot.send_message(msg.from_user.id,
                            text=_("Поменять язык: ", lang),
                            reply_markup=nav.lang_KB
                            )
        
        else:    
        # кнопки для клиентов   
            text1 = _('Добро пожаловать', lang) 
            text2 = _('Создать заявку для интеграции',lang)
            await bot.send_message(msg.from_user.id,
                                    text=f'{text1} {msg.from_user.first_name}!\n {text2}'
                                    ,reply_markup=nav.choose_iiko_1c_(lang)
                                    )
            await bot.send_message(msg.from_user.id,
                            text=_('Поменять язык: ',lang),
                            reply_markup=nav.lang_KB
                            )

    else:
        await bot.send_message(msg.from_user.id,
                        text='Choose language:',
                        reply_markup=nav.lang_KB
                        )


@dp.callback_query_handler(lambda c: c.data and c.data.startswith('lang'))
async def choose_lang(callback_query: types.CallbackQuery):
    language = callback_query.data.split('_')[1]
    print(language)
    if  users_collection.find_one({'user_id':f'{callback_query.from_user.id}'}):
        users_collection.update_one({'user_id': f'{callback_query.from_user.id}'}, {'$set': {'language': language}})
    else:
        user = {
            'username': f'{callback_query.from_user.first_name}',
            'user_id': f'{callback_query.from_user.id}',
            'language': language
        }
        users_collection.insert_one(user)
    await callback_query.message.answer(_('Вы успешно поменяли язык на русский.',language))
    await callback_query.message.answer(_('Отправье команду /start еще раз.',language))
    

@dp.callback_query_handler(lambda c: c.data == 'stop', state='*')
async def stop_process(callback_query: types.CallbackQuery, state: FSMContext):
    await state.finish()
    lang = users_collection.find_one({'user_id':f'{callback_query.from_user.id}'})['language']
    await  callback_query.message.answer(_("Вы остановили все процессы", lang))

@dp.message_handler(commands=['stop'], state='*')
async def stop_command(msg: types.Message, state: FSMContext):
    lang = users_collection.find_one({'user_id':f'{msg.from_user.id}'})['language']
    await  bot.send_message(msg.from_user.id, _("Вы остановили все процессы", lang))
    await state.finish()

@dp.callback_query_handler(lambda c: c.data == 'about')
async def stop_process(callback_query: types.CallbackQuery, state: FSMContext):
    lang = users_collection.find_one({'user_id':f'{callback_query.from_user.id}'})['language']
    await state.finish()
    await  callback_query.message.answer(
    _("В данном боте вы можете создать заявки для интеграции 1С или Iiko. Для этого вам всего лишь нужно ответить на несколько вопросов",lang)        
                                         )

@dp.callback_query_handler(lambda c: c.data == 'Iiko')
async def Start_to_create_Iiko(callback_query: types.CallbackQuery, state: FSMContext):
    lang = users_collection.find_one({'user_id':f'{callback_query.from_user.id}'})['language']
    await state.finish()
    await state.update_data(client_choose = 1)
    await  callback_query.message.answer(_("Напишите ФИО менеджера арки",lang))
    await Clients_States.fio_client_state.set()

@dp.callback_query_handler(lambda c: c.data == '1C')
async def Start_to_create_1C(callback_query: types.CallbackQuery, state: FSMContext):
    lang = users_collection.find_one({'user_id':f'{callback_query.from_user.id}'})['language']
    await state.finish()
    await state.update_data(client_choose = 2)
    await  callback_query.message.answer(_("Напишите ФИО менеджера арки",lang))
    await Clients_States.fio_client_state.set()

@dp.message_handler(content_types=['text'], state= Clients_States.fio_client_state)
async def save_date_fio(msg: types.Message, state: FSMContext):
    lang = users_collection.find_one({'user_id':f'{msg.from_user.id}'})['language']

    await state.update_data(client_name = msg.from_user.first_name,
                            client_id = msg.from_user.id,
                            client_fio = msg.text,
                            client_msg_date = msg.date.strftime('%d %B %H:%M')
                            )
    await bot.send_message(msg.from_user.id,
    _("Напишите контактный номер менеджера арки\n Например: +998 71 200 0000" , lang)
                           )
    await Clients_States.contact_number_client_state.set()

 

@dp.message_handler(content_types=['text'], state= Clients_States.contact_number_client_state)
async def save_date_contact_number(msg: types.Message, state: FSMContext):
    lang = users_collection.find_one({'user_id':f'{msg.from_user.id}'})['language']
    try:
        phone =  phonenumbers.format_number(phonenumbers.parse(msg.text, None), phonenumbers.PhoneNumberFormat.INTERNATIONAL)
        await state.update_data(client_contact_number = phone)
        await bot.send_message(msg.from_user.id,_('Наименование организации', lang))
        await Clients_States.organization_name_client_state.set()
    except:
        await bot.send_message(msg.from_user.id, _("Неправильно введен номер", lang))
        await bot.send_message(msg.from_user.id,
                           _("Напишите контактный номер менеджера арки\n Например: +998 71 200 0000", lang)
                           )
        await Clients_States.contact_number_client_state.set()




@dp.message_handler(content_types=['text'], state= Clients_States.organization_name_client_state)
async def save_date_organization(msg: types.Message, state: FSMContext):
    lang = users_collection.find_one({'user_id':f'{msg.from_user.id}'})['language']
    await state.update_data(client_organization_name = msg.text)
    data = await state.get_data()
    if data['client_choose'] == 1:
        await  bot.send_message(msg.from_user.id, f'{_("Введите версию Iiko",lang)}\n'+
                                f'{_("Например: Iiko v 1.2.734", lang)}')
        await Clients_States.version_iiko_client_state.set()
    else:
        await  bot.send_message(msg.from_user.id,
                                f'{_("Какая у вас конфигурация данных(версия, редакцию, типовая или доработанная)?", lang)}\n' +
                                f'{_("Например: Управление торговлей, редакция 11.4.8", lang)}')
        await Clients_States.conf_client_state.set()



@dp.message_handler(content_types=['text'], state=Clients_States.version_iiko_client_state)
async def save_version_iiko(msg: types.Message, state: FSMContext):
    lang = users_collection.find_one({'user_id':f'{msg.from_user.id}'})['language']
    await state.update_data(client_version_iiko = msg.text)
    await bot.send_message(msg.from_user.id,
                        _("Фио контактного лица клиента", lang)
                        )
    await Clients_States.contact_client_state.set()


@dp.message_handler(content_types=['text'], state=Clients_States.conf_client_state)
async def save_date_conf_client(msg: types.Message, state: FSMContext):
    lang = users_collection.find_one({'user_id':f'{msg.from_user.id}'})['language']
    await state.update_data(client_conf = msg.text,)

    await bot.send_message(msg.from_user.id,
                            _("Напишите количество касс", lang)
                            )
    await Clients_States.count_cass_client_state.set()

@dp.message_handler(content_types=['text'], state=Clients_States.count_cass_client_state)
async def save_date_conf_client(msg: types.Message, state: FSMContext):
    lang = users_collection.find_one({'user_id':f'{msg.from_user.id}'})['language']
    await state.update_data(count_cass_client_state = msg.text,)

    await bot.send_message(msg.from_user.id,
                            _("Фио контактного лица клиента", lang)
                            )
    await Clients_States.contact_client_state.set()

@dp.message_handler(content_types=['text'], state=Clients_States.contact_client_state)
async def save_contact_client(msg: types.Message, state: FSMContext):
    lang = users_collection.find_one({'user_id':f'{msg.from_user.id}'})['language']
    await state.update_data(client_contact_client = msg.text)
    await bot.send_message(msg.from_user.id,
                                _("Напишите номер телефона клиента\n Например: +998 71 200 0000", lang)
                                )
    await Clients_States.contact_client_phone_state.set()

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
          file.writelines(f"ФИО менеджера:: {client_fio}\n")
          file.writelines(f"Контактный номер менеджера:: {client_contact_number}\n")
          file.writelines(f"Имя организации:: {client_client_organization_name}\n")
    task = {
        'username': client_name,
        'userid': client_id,
        'fio_menedjer': client_fio,
        'contact_number_menedjer': client_contact_number,
        'organization_name' : client_client_organization_name,
        'fio_client': client_contact_client,
        'contact_number_client' : contact_client_phone_state
    }

    if client_choose == 1:
        with open(f"{file_name}",'a', encoding='utf-8') as file:
            file.writelines(f"Версия Iiko:: {client_version_iiko}\n")
            file.writelines(f"Время установки:: {client_date}\n")
            file.writelines(f"Адрес установки:: {client_adress}\n")
        task['task_type'] = 'Iiko'
        task['Iiko_version'] = client_version_iiko
        task['install_date'] = client_date
        task['adress_install_date'] = client_adress


    elif client_choose == 2:
        with open(f"{file_name}",'a', encoding='utf-8') as file:
            file.writelines(f"Конфигурация данных:: {client_conf}\n")
            file.writelines(f"Количество касс:: {count_cass_client_state}\n")
        task['task_type'] = '1C'
        task['data_config'] = client_conf
        task['cass_count'] = count_cass_client_state

    with open(f"{file_name}",'a', encoding='utf-8') as file:
          file.writelines(f"Имя клиента:: {client_contact_client}\n")
          file.writelines(f"Контактный номер клиента:: {contact_client_phone_state}\n")
          file.writelines(f"Данная заявка была отправлена:: {client_msg_date}\n")
    task['task_date'] = client_msg_date
    task['status'] = 'holver'
    collection.insert_one(task)

@dp.message_handler(content_types=['text'], state=Clients_States.contact_client_phone_state)
async def save_contact_client(msg: types.Message, state: FSMContext):
    lang = users_collection.find_one({'user_id':f'{msg.from_user.id}'})['language']
    try:
        formatted_num = phonenumbers.format_number(phonenumbers.parse(msg.text, None), phonenumbers.PhoneNumberFormat.INTERNATIONAL)
    

        await state.update_data(contact_client_phone_state = formatted_num)
        
        data = await state.get_data()
        if data['client_choose'] == 1:
            await bot.send_message(msg.from_user.id,
                                f'{_("Напишите адрес", lang)}\n'+
                                f'{_("Например: страна Казахстан, город Алматы, улица Таугуль, дом 33б", lang)}'
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
                            text=_("Появилась заявка для 1C интеграции", lang)
                            )
            with open('notifications_1C.txt','a',encoding='utf-8') as file:
                file.writelines(f"{data['client_name']}//{data['client_msg_date']}//{data['client_id']}//C{n}\n") 

            await bot.send_message(msg.from_user.id,
                            f'{_("Ваша заявка отправлена", lang)}\n'+
                            _("Скоро вам придет ответ специалиста", lang)
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
    except:
        await bot.send_message(msg.from_user.id, _("Неправильно введен номер", lang))
        await bot.send_message(msg.from_user.id,
                           _("Напишите номер телефона клиента\n Например: +998 71 200 0000", lang)
                           )
        await Clients_States.contact_client_phone_state.set()

@dp.message_handler(content_types=['text'], state=Clients_States.adress_client_state)
async def save_adress(msg: types.Message, state: FSMContext):
    lang = users_collection.find_one({'user_id':f'{msg.from_user.id}'})['language']
    await state.update_data(client_adress = msg.text)
    await bot.send_message(msg.from_user.id,
                        f'{_("Напишите дату установки", lang)}\n'+
                        f'{_("Например: 28.11.2023 18:00 UTC+6", lang)}'
                        )
    await Clients_States.date_client_state.set()
# ********************************************
# ********************************************************
# ********************************************************


@dp.message_handler(content_types=['text'], state=Clients_States.date_client_state)
async def save_dates(msg: types.Message, state: FSMContext):
    lang = users_collection.find_one({'user_id':f'{msg.from_user.id}'})['language']
    data = await state.get_data()
    if data['client_choose'] == 1:
        await state.update_data(client_date = msg.text.lower())
    data = await state.get_data()
    n = 1
    for file in os.listdir():
        if f"{data['client_name']} {data['client_id']}" in file:
            n+=1
    group_chat_id = -910221550

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
                        text=_("Появилась заявка для Iiko интеграции", lang)
                        )
    with open('notifications_Iiko.txt','a',encoding='utf-8') as file:
        file.writelines(f"{data['client_name']}//{data['client_msg_date']}//{data['client_id']}//I{n}\n")  
    
    await bot.send_message(msg.from_user.id,
                        f'{_("Ваша заявка отправлена", lang)}\n'+
                        f'{_("Скоро вам придет ответ специалиста", lang)}'
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
# Config commands
# Просмотреть id чат
@dp.message_handler(commands=['id'])
async def send_welcome(message: types.Message):    
    await message.reply(message.chat.id)

group_chat_id = -910221550

@dp.message_handler(commands=['change_group_chat_id'])
async def change_group_chat_id(msg: types.Message):    
    if str(msg.from_user.id) in cpecialist_list():
        await msg.reply('Please write the ID of the group to which the notifications will be sent.')
        await Specialist_States.change_group_chat_id_state.set()
    else:
        await msg.reply("You do not have access.")

@dp.message_handler(content_types=['text'], state=Specialist_States.change_group_chat_id_state)
async def update_spec(msg=types.Message, state=FSMContext):
    
    try:
        await bot.send_message(chat_id=int(msg.text), 
                           text= "This group will receive notifications."
                            )
        global group_chat_id 
        group_chat_id = msg.text
    except:
        await msg.reply("Its ID does not exist.")
    await state.finish()
@dp.message_handler(commands=['all_comands'])
async def change_group_chat_id(msg: types.Message):    
    await msg.reply(
        '/id - view the ID\n'+
        '/change_group_chat_id - change the ID of the group where notifications will be sent\n'+
        '/start - start working with the bot\n'+
        '/stop - stop all processes\n'+
        '/all_commands - view existing commands\n'
        )

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
    lang = users_collection.find_one({'user_id':f'{callback_query.from_user.id}'})['language']
    await callback_query.message.answer(text =  f'Введите id и имя специалиста,'+ 
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
    lang = users_collection.find_one({'user_id':f'{msg.from_user.id}'})['language']

    cpec_list = ''
    period = 0
    for cpec in cpecialist_list():
        period += 1
        cpec_list+= f"{cpec} "
        if period%2 == 0:
            cpec_list+='\n'
        
    await callback_query.message.answer( f'Список специалистов:\n {cpec_list}')
# удалить специалистов
@dp.callback_query_handler(lambda c: c.data == 'drop_spec')
async def instruction_for_add(callback_query: types.CallbackQuery):
    lang = users_collection.find_one({'user_id':f'{msg.from_user.id}'})['language']
    await callback_query.message.answer(text =  f'Введите id специалиста'+ 
                                        'которого хотите удалить\n'+
                                        'например: 123456789 '
                                        )
    await Specialist_States.drop_spec_state.set()

@dp.message_handler(content_types=['text'], state=Specialist_States.drop_spec_state)
async def update_spec(msg=types.Message, state=FSMContext):
    with open('./specialist_list.txt', encoding='utf-8') as file:
        specialist_list = file.readlines()
    drop = '1'
    for line in specialist_list:
        if f'{msg.text}'  in line:
            drop = line
            specialist_list.remove(line)
           
        
    print(specialist_list)
    with open('./specialist_list.txt','w', encoding='utf-8') as file:
        for line in specialist_list:
            file.writelines(line)
    if drop == '1':
        await bot.send_message(chat_id=msg.from_user.id, 
                           text= f'Нет такого специалиста: {msg.text}' 
                            )
    else:
        await bot.send_message(chat_id=msg.from_user.id, 
                            text= f'Вы успешно удалили специалиста:\n{drop}'
                                )
    await state.finish()
# удалит специалистов
@dp.callback_query_handler(lambda c: c.data == 'edit_spec')
async def instruction_for_add(callback_query: types.CallbackQuery):
    lang = users_collection.find_one({'user_id':f'{msg.from_user.id}'})['language']
    await callback_query.message.answer(text =  f'Введите новое имя')
    await Specialist_States.edit_spec_state.set()

@dp.message_handler(content_types=['text'], state=Specialist_States.edit_spec_state)
async def update_spec(msg=types.Message, state=FSMContext):
    await state.update_data(cpec_name_new = msg.text )
    
    await bot.send_message(chat_id=msg.from_user.id, 
                           text= f'Вы успешно поменяли свое имя на:\n{msg.text}'
                            )
    await state.finish()
# ******************************************        
# ******************************************        
# ******************************************        
# Просмотр заявок для интеграции Iiko
@dp.callback_query_handler(lambda c: c.data == 'Iiko_cpec')
async def iiko_notifications(callback_query: types.CallbackQuery, state: FSMContext):

    lang = users_collection.find_one({'user_id':f'{msg.from_user.id}'})['language']
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

    lang = users_collection.find_one({'user_id':f'{msg.from_user.id}'})['language']
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
                                                reply_markup=nav.option_for_iiko_KB
                                                )
    if k == 0:
        await callback_query.message.answer('Данной заявки уже нет')

@dp.callback_query_handler(lambda c: c.data == 'iiko_btn_Yes')
async def receive_task(callback_query: types.CallbackQuery, state: FSMContext):
    lang = users_collection.find_one({'user_id':f'{msg.from_user.id}'})['language']
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

    try:
        name = data['cpec_name_new']
    except:
        name = callback_query.from_user.first_name
    await bot.send_message(group_chat_id, f"{name}: Данная заявка была принята")
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
    
    lang = users_collection.find_one({'user_id':f'{msg.from_user.id}'})['language']
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
    lang = users_collection.find_one({'user_id':f'{msg.from_user.id}'})['language']
    data = await state.get_data()
    await bot.send_message(int(data["client_id"]), 'Ваша заявка не принята')
    await bot.send_message(int(data["client_id"]), 'Заявка:')
    await bot.send_message(int(data["client_id"]), data['client_task'])
    await bot.send_message(int(data["client_id"]), f'Комментарий специалиста\n{msg.text}')

    try:
        name = data['cpec_name_new']
    except:
        name = msg.from_user.first_name
    await bot.send_message(group_chat_id, f'{name}: Данная заявка не принята:')
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
                    post["client_phone"],
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
    lang = users_collection.find_one({'user_id':f'{msg.from_user.id}'})['language']
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
    lang = users_collection.find_one({'user_id':f'{msg.from_user.id}'})['language']
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
    await callback_query.message.answer(task_text, reply_markup=nav.save_db_kb)


@dp.callback_query_handler(lambda c: c.data == 'closed_tasks')
async def save_db_closed_tasks(callback_query: types.CallbackQuery, state: FSMContext):
    lang = users_collection.find_one({'user_id':f'{msg.from_user.id}'})['language']
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
                    post["client_phone"],
                    post["type"],
                    post["task_date"],
                    post["status"]
                    ])
    sheet.insert_rows(datadb)
    await callback_query.message.answer('Данная заявка была закрыта(завершена)')

@dp.callback_query_handler(lambda c: c.data == 'regected_tasks')
async def save_db_regected_tasks(callback_query: types.CallbackQuery, state: FSMContext):
    lang = users_collection.find_one({'user_id':f'{msg.from_user.id}'})['language']
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
                    post["client_phone"],
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
    lang = users_collection.find_one({'user_id':f'{msg.from_user.id}'})['language']
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
    lang = users_collection.find_one({'user_id':f'{msg.from_user.id}'})['language']

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
                                                reply_markup=nav.option_for_1C_KB
                                                )
    if k == 0:
        await callback_query.message.answer('Данной заявки уже нет')

@dp.callback_query_handler(lambda c: c.data == '1C_btn_Yes')
async def receive_task_1C(callback_query: types.CallbackQuery, state: FSMContext):
    lang = users_collection.find_one({'user_id':f'{msg.from_user.id}'})['language']
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
    
    try:
        name = data['cpec_name_new']
    except:
        name = callback_query.from_user.first_name
    await bot.send_message(group_chat_id, f'{name}: Данная заявка была принята')
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

    await state.finish()


@dp.callback_query_handler(lambda c: c.data == '1C_btn_No')
async def receive_task_1C(callback_query: types.CallbackQuery, state: FSMContext):
    
    lang = users_collection.find_one({'user_id':f'{callback_query.from_user.id}'})['language']
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
    lang = users_collection.find_one({'user_id':f'{msg.from_user.id}'})['language']
    data = await state.get_data()
    await bot.send_message(int(data["client_id"]), 'Ваша заявка не принята')
    await bot.send_message(int(data["client_id"]), 'Заявка:')
    await bot.send_message(int(data["client_id"]), data['client_task'])
    await bot.send_message(int(data["client_id"]), f'Комментарий специалиста\n{msg.text}')

    try:
        name = data['cpec_name_new']
    except:
        name = msg.from_user.first_name
    await bot.send_message(group_chat_id, f'{name}: Данная заявка не принята:')
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
                    post["client_phone"],
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
    lang = users_collection.find_one({'user_id':f'{msg.from_user.id}'})['language']
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
    lang = users_collection.find_one({'user_id':f'{msg.from_user.id}'})['language']
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
    await callback_query.message.answer(task_text, reply_markup=nav.save_db_kb)
    

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates = True)

# q w e r t y u i o p a s d f g h j k l z x c v b n m