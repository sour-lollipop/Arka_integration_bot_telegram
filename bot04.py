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
import re
from bson.objectid import ObjectId



client = MongoClient('mongodb+srv://akmaral:aktolkyn2018@clusterarkabot.obnb02f.mongodb.net/test')
db = client.Clients_applications_DB
collection = db.tasks_collection
users_collection = db.users_collection
specialist_collection = db.specialist_collection
group_chat_id_bd = db.group_chat_id
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
# test bot token
# bot = Bot(token="6027542967:AAH634BtIzZSQiYOIn33WcV1-RQ_9v7bfk0")
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
    
    if  users_collection.find_one({'user_id':msg.from_user.id}):
        lang = users_collection.find_one({'user_id':msg.from_user.id})['language']
        
        if msg.from_user.id in cpecialist_list():
            name = specialist_collection.find_one({'spec_id':msg.from_user.id})['spec_name']
            await bot.send_message(msg.from_user.id,
                            text=f'{_("Добро пожаловать",lang)} {name}!\n'+ 
                                    _("Выберите свое направление, и появится список заявок.", lang),
                            reply_markup=nav.choose_iiko_1c_for_cpec_KB
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
                                   text=_("Вы можете просмотреть свои отправленные заявки", lang),
                                   reply_markup=nav.view_tasks(lang)
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

# Config commands
# Просмотреть id чат
@dp.message_handler(commands=['id'])
async def send_welcome(message: types.Message):    
    await message.reply(message.chat.id)


# idd = group_chat_id_bd.find_one({'name': "group_chat"})["group_chat_id"]
group_chat_id = -1001803545201
@dp.message_handler(commands=['test_group_chat_id'])
async def test_group_chat_id(msg: types.Message):
    await bot.send_message(chat_id=group_chat_id, text="This group will receive notifications.")
    await msg.reply(f"Successful: {group_chat_id}")

@dp.message_handler(commands=['change_group_chat_id'])
async def change_group_chat_id(msg: types.Message):    
    if msg.from_user.id in cpecialist_list():
        await msg.reply('Please write the ID of the group to which the notifications will be sent.')
        await msg.reply('Before changing the group ID, make sure you have added the bot to the group and granted it all the necessary permissions.')
        await Specialist_States.change_group_chat_id_state.set()
    else:
        await msg.reply("You do not have access.")

@dp.message_handler(content_types=['text'], state=Specialist_States.change_group_chat_id_state)
async def update_group_id(msg=types.Message, state=FSMContext):
    match = re.search(r'[-+]?\d+', msg.text)
    print(int(match.group()))
    if match:
        try:
            global group_chat_id
            group_chat_id = int(match.group())
            print(group_chat_id)
            await bot.send_message(chat_id=group_chat_id, text="This group will receive notifications.")
            await msg.reply("Successful")
        except:
            await msg.reply("Its ID does not exist.")
            await msg.reply('Before changing the group ID, make sure you have added the bot to the group and granted it all the necessary permissions.')
    else:         
        await msg.reply("Its ID wrong format.")
    await state.finish()

@dp.message_handler(commands=['all_comands'])
async def change_group_chat_id(msg: types.Message):    
    await msg.reply(
        '/id - view the ID\n'+
        '/start - start working with the bot\n'+
        '/stop - stop all processes\n'+
        '/test_group_chat_id - test the ID of the group where notifications will be sent\n'+
        'change_group_chat_id - change the ID of the group where notifications will be sent\n'
        '/all_commands - view existing commands\n'
        )
    
# составить список специалистов
def cpecialist_list():
    speces_id = []
    spesec = specialist_collection.find()
    for spec in spesec :
        speces_id.append(spec['spec_id'])
    return speces_id
# добавить специалистов
@dp.callback_query_handler(lambda c: c.data == 'add_spec')
async def instruction_for_add(callback_query: types.CallbackQuery):
    lang = users_collection.find_one({'user_id':callback_query.from_user.id})['language']
    await callback_query.message.answer(text =  
                                        _("Введите id и имя специалиста, которого хотите добавить\n например: 123456789 Сергей", lang)
                                        )
    await Specialist_States.add_spec_state.set()

@dp.message_handler(content_types=['text'], state=Specialist_States.add_spec_state)
async def update_spec(msg=types.Message, state=FSMContext):
    lang = users_collection.find_one({'user_id':msg.from_user.id})['language']
    if msg.text.split()[0].isnumeric():
        try:
            if specialist_collection.find_one({'spec_id': int(msg.text.split()[0])}):
                await bot.send_message(chat_id=msg.from_user.id, 
                           text= f'{_("Такой специалист уже добавлен", lang)}'
                            )
            else:
                await bot.send_message(chat_id=int(msg.text.split()[0]), 
                           text= f'{_("Вы специалист в боте @Arka_intefration_bot", lang)}'
                            )
                await bot.send_message(chat_id=msg.from_user.id, 
                           text= f'{_("Вы успешно добавили специалиста", lang)}:\n{msg.text}'
                            )
                spec = {
                    'spec_id': int(msg.text.split()[0]),
                    'spec_name': ''.join(msg.text.split()[1:])
                }
                specialist_collection.insert_one(spec)
        except:
            await bot.send_message(chat_id=msg.from_user.id, 
                           text= _("Пользователь не найден. Возможно вы ввели неправильные данные.\nПовторите попытку еще раз.", lang)
                            )
    else:
        await bot.send_message(chat_id=msg.from_user.id, 
                           text= _("Пользователь не найден. Возможно вы ввели неправильные данные.\nПовторите попытку еще раз.", lang)
                              )

    await state.finish()

# Просмотр список специалистов
@dp.callback_query_handler(lambda c: c.data == 'list_of_spec')
async def list_of_spec(callback_query: types.CallbackQuery):
    lang = users_collection.find_one({'user_id':callback_query.from_user.id})['language']
    spec_list = ''
    spesec = specialist_collection.find()
    for spec in spesec :
        spec_list += f"{spec['spec_id']}: {spec['spec_name']}\n"    
    await callback_query.message.answer( f'{_("Список специалистов:", lang)}\n {spec_list}')
# удалить специалистов
@dp.callback_query_handler(lambda c: c.data == 'drop_spec')
async def instruction_for_add(callback_query: types.CallbackQuery):
    lang = users_collection.find_one({'user_id':callback_query.from_user.id})['language']
    await callback_query.message.answer(text =_("Введите id специалиста которого хотите удалить\n например: 123456789", lang))
    await Specialist_States.drop_spec_state.set()
# удалит специалистa
@dp.message_handler(content_types=['text'], state=Specialist_States.drop_spec_state)
async def update_spec(msg=types.Message, state=FSMContext):
    lang = users_collection.find_one({'user_id':msg.from_user.id})['language']
    if msg.text.split()[0].isnumeric():
        if specialist_collection.find_one({'spec_id': int(msg.text.split()[0])}):
            spec = specialist_collection.find_one({'spec_id': int(msg.text.split()[0])})
            drop = f"{spec['spec_id']}: {spec['spec_name']}"
            specialist_collection.delete_one({'spec_id': int(msg.text.split()[0])})
            await bot.send_message(chat_id=msg.from_user.id, 
                                text= f'{_("Вы успешно удалили специалиста:" , lang)}\n{drop}'
                                    )
        else:
            await bot.send_message(chat_id=msg.from_user.id,                            
                                   text= _("Пользователь не найден. Возможно вы ввели неправильные данные.\nПовторите попытку еще раз.", lang)

                        )
    else:
        await bot.send_message(chat_id=msg.from_user.id,                            
                               text= _("Пользователь не найден. Возможно вы ввели неправильные данные.\nПовторите попытку еще раз.", lang)

                                )
    await state.finish()
# изменить имя специалистa

@dp.callback_query_handler(lambda c: c.data == 'edit_spec')
async def instruction_for_add(callback_query: types.CallbackQuery):
    lang = users_collection.find_one({'user_id':callback_query.from_user.id})['language']
    await callback_query.message.answer(text =  _("Введите новое имя", lang))
    await Specialist_States.edit_spec_state.set()

@dp.message_handler(content_types=['text'], state=Specialist_States.edit_spec_state)
async def update_spec(msg=types.Message, state=FSMContext):
    lang = users_collection.find_one({'user_id':msg.from_user.id})['language']
    specialist_collection.update_one({"spec_id": msg.from_user.id}, {"$set":{"spec_name": msg.text}})
    await bot.send_message(chat_id=msg.from_user.id, 
                           text= f'{_("Вы успешно поменяли свое имя на:", lang)}\n{msg.text}'
                            )
    await state.finish()    

# *******************************************************
# *******************************************************
@dp.callback_query_handler(lambda c: c.data and c.data.startswith('lang'))
async def choose_lang(callback_query: types.CallbackQuery):
    language = callback_query.data.split('_')[1]
    print(language)
    if  users_collection.find_one({'user_id':callback_query.from_user.id}):
        users_collection.update_one({'user_id': callback_query.from_user.id}, {'$set': {'language': language}})
    else:
        user = {
            'username': f'{callback_query.from_user.first_name}',
            'user_id': callback_query.from_user.id,
            'language': language
        }
        users_collection.insert_one(user)
    await callback_query.message.answer(_('Вы успешно поменяли язык на русский.',language))
    await callback_query.message.answer(_('Отправьте команду /start еще раз.',language))
    

@dp.callback_query_handler(lambda c: c.data == 'stop', state='*')
async def stop_process(callback_query: types.CallbackQuery, state: FSMContext):
    await state.finish()
    lang = users_collection.find_one({'user_id':callback_query.from_user.id})['language']
    await  callback_query.message.answer(_("Вы остановили все процессы", lang))

@dp.message_handler(commands=['stop'], state='*')
async def stop_command(msg: types.Message, state: FSMContext):
    lang = users_collection.find_one({'user_id':msg.from_user.id})['language']
    await  bot.send_message(msg.from_user.id, _("Вы остановили все процессы", lang))
    await state.finish()

@dp.callback_query_handler(lambda c: c.data == 'about')
async def stop_process(callback_query: types.CallbackQuery, state: FSMContext):
    lang = users_collection.find_one({'user_id':callback_query.from_user.id})['language']
    await state.finish()
    await  callback_query.message.answer(
    _("В данном боте вы можете создать заявки для интеграции 1С или Iiko. Для этого вам всего лишь нужно ответить на несколько вопросов",lang)        
                                         )

@dp.callback_query_handler(lambda c: c.data == 'my_tasks')
async def view_my_tasks(callback_query: types.CallbackQuery):
    lang = users_collection.find_one({'user_id':callback_query.from_user.id})['language']
    if collection.find_one({"userid": callback_query.from_user.id}):
        for task in collection.find({"userid": callback_query.from_user.id}):
            task_text = f'{_("Заявка", lang)}:\n'
            task_text += f'task_type: {task["task_type"]}\n'
            task_text += f'user_name: {task["username"]}\n'
            task_text += f'user_id: {task["userid"]}\n'
            task_text += f'{_("ФИО менеджера", lang)}: {task["fio_menedjer"]}\n'
            task_text += f'{_("Контактный номер менеджера", lang)}: {task["contact_number_menedjer"]}\n'
            task_text += f'{_("Имя организации", lang)}: {task["organization_name"]}\n'
            task_text += f'{_("Имя клиента", lang)}: {task["fio_client"]}\n'
            task_text += f'{_("Контактный номер клиента", lang)}: {task["contact_number_client"]}\n'
            if task["task_type"] == "Iiko":
                task_text += f'{_("Версия Iiko", lang)}: {task["Iiko_version"]}\n'
                task_text += f'{_("Время установки", lang)}: {task["install_date"]}\n'
                task_text += f'{_("Адрес установки" , lang)}: {task["adress_install_date"]}\n'
            else:
                task_text += f'{_("Конфигурация данных", lang)}: {task["data_config"]}\n'
                task_text += f'{_("Количество касс", lang)}: {task["cass_count"]}\n'
            task_text += f'{_("Данная заявка была отправлена", lang)}: {task["task_date"]}\n'
            task_text += f'status: {task["status"]}'
            delete_kb = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton('DELETE', callback_data=f'DELETE_{task["_id"]}'))
            await  bot.send_message(callback_query.from_user.id, task_text, reply_markup=delete_kb)
    else:
        await  bot.send_message(callback_query.from_user.id, _('Ранее, вы не создавали заявки', lang))

@dp.callback_query_handler(lambda c: c.data and c.data.startswith('DELETE_')) 
async def delete_my_task(callback_query: types.CallbackQuery):
    await bot.edit_message_reply_markup(
        chat_id=callback_query.from_user.id,
        message_id=callback_query.message.message_id, 
        reply_markup=None
    )
    lang = users_collection.find_one({'user_id':callback_query.from_user.id})['language']
    collection.delete_one({"_id": ObjectId(callback_query.data.replace("DELETE_", ""))})
    await  callback_query.message.answer(_("Данная заявка удалена",lang)) 

@dp.callback_query_handler(lambda c: c.data == 'Iiko')
async def Start_to_create_Iiko(callback_query: types.CallbackQuery, state: FSMContext):
    lang = users_collection.find_one({'user_id':callback_query.from_user.id})['language']
    await state.finish()
    await state.update_data(client_choose = 2)
    await  callback_query.message.answer(_("Напишите ФИО менеджера арки",lang))
    await Clients_States.fio_client_state.set()

@dp.callback_query_handler(lambda c: c.data == '1C')
async def Start_to_create_1C(callback_query: types.CallbackQuery, state: FSMContext):
    lang = users_collection.find_one({'user_id':callback_query.from_user.id})['language']
    await state.finish()
    await state.update_data(client_choose = 1)
    await  callback_query.message.answer(_("Напишите ФИО менеджера арки",lang))
    await Clients_States.fio_client_state.set()

@dp.message_handler(content_types=['text'], state= Clients_States.fio_client_state)
async def save_date_fio(msg: types.Message, state: FSMContext):
    lang = users_collection.find_one({'user_id':msg.from_user.id})['language']

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
    lang = users_collection.find_one({'user_id':msg.from_user.id})['language']
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
    lang = users_collection.find_one({'user_id':msg.from_user.id})['language']
    await state.update_data(client_organization_name = msg.text)
    data = await state.get_data()
    if data['client_choose'] == 2:
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
    lang = users_collection.find_one({'user_id':msg.from_user.id})['language']
    await state.update_data(client_version_iiko = msg.text)
    await bot.send_message(msg.from_user.id,
                        _("Фио контактного лица клиента", lang)
                        )
    await Clients_States.contact_client_state.set()


@dp.message_handler(content_types=['text'], state=Clients_States.conf_client_state)
async def save_date_conf_client(msg: types.Message, state: FSMContext):
    lang = users_collection.find_one({'user_id':msg.from_user.id})['language']
    await state.update_data(client_conf = msg.text,)

    await bot.send_message(msg.from_user.id,
                            _("Напишите количество касс", lang)
                            )
    await Clients_States.count_cass_client_state.set()

@dp.message_handler(content_types=['text'], state=Clients_States.count_cass_client_state)
async def save_date_conf_client(msg: types.Message, state: FSMContext):
    lang = users_collection.find_one({'user_id':msg.from_user.id})['language']
    await state.update_data(count_cass_client_state = msg.text,)

    await bot.send_message(msg.from_user.id,
                            _("Фио контактного лица клиента", lang)
                            )
    await Clients_States.contact_client_state.set()

@dp.message_handler(content_types=['text'], state=Clients_States.contact_client_state)
async def save_contact_client(msg: types.Message, state: FSMContext):
    lang = users_collection.find_one({'user_id':msg.from_user.id})['language']
    await state.update_data(client_contact_client = msg.text)
    await bot.send_message(msg.from_user.id,
                                _("Напишите номер телефона клиента\n Например: +998 71 200 0000", lang)
                                )
    await Clients_States.contact_client_phone_state.set()

def save_data(  
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
        task['task_type'] = '1C'
        task['data_config'] = client_conf
        task['cass_count'] = count_cass_client_state

    elif client_choose == 2: 
        task['task_type'] = 'Iiko'
        task['Iiko_version'] = client_version_iiko
        task['install_date'] = client_date
        task['adress_install_date'] = client_adress
 
    task['task_date'] = client_msg_date
    task['status'] = 'holver'
    collection.insert_one(task)

@dp.message_handler(content_types=['text'], state=Clients_States.contact_client_phone_state)
async def save_contact_client(msg: types.Message, state: FSMContext):
    lang = users_collection.find_one({'user_id':msg.from_user.id})['language']
    try:
        formatted_num = phonenumbers.format_number(phonenumbers.parse(msg.text, None), phonenumbers.PhoneNumberFormat.INTERNATIONAL)
    
    except:
        await bot.send_message(msg.from_user.id, _("Неправильно введен номер", lang))
        await bot.send_message(msg.from_user.id,
                           _("Напишите номер телефона клиента\n Например: +998 71 200 0000", lang)
                           )
        await Clients_States.contact_client_phone_state.set()
    await state.update_data(contact_client_phone_state = formatted_num)
    
    data = await state.get_data()
    if data['client_choose'] == 1:
        
        save_data( 
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
        await bot.send_message(msg.from_user.id,
                        f'{_("Ваша заявка отправлена", lang)}\n'+
                        _("Скоро вам придет ответ специалиста", lang)
                        )
        # View task 
        if collection.find_one({'userid': data['client_id']}) and collection.find_one({'task_date': data['client_msg_date']}):
            task = collection.find_one({'userid': data['client_id']})

            await bot.send_message(chat_id = group_chat_id , 
                                text = f'{_("Ник и id клиента", lang)} : {task["username"]} {task["userid"]}\n' +
                                        f'{_("ФИО менеджера", lang)} : {task["fio_menedjer"]}\n' +
                                        f'{_("Контактный номер менеджера", lang)} : {task["contact_number_menedjer"]}\n' +
                                        f'{_("Имя организации", lang)} : {task["organization_name"] }\n' +
                                        f'{_("Имя клиента", lang)} : {task["fio_client"]}\n' +
                                        f'{_("Контактный номер клиента", lang)} : {task["contact_number_client"] }\n' +
                                        f'{_("Конфигурация данных", lang)} : {task["data_config"]}\n' +
                                        f'{_("Количество касс", lang)} : {task["cass_count"]}\n' +
                                        f'{_("Данная заявка была отправлена", lang)} : {task["task_date"] }\n' 
                                )
            await state.finish()
    else:
        await bot.send_message(msg.from_user.id,
                            f'{_("Напишите адрес", lang)}\n'+
                            f'{_("Например: страна Казахстан, город Алматы, улица Таугуль, дом 33б", lang)}'
                            )
        await Clients_States.adress_client_state.set()
    

@dp.message_handler(content_types=['text'], state=Clients_States.adress_client_state)
async def save_adress(msg: types.Message, state: FSMContext):
    lang = users_collection.find_one({'user_id':msg.from_user.id})['language']
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
    lang = users_collection.find_one({'user_id':msg.from_user.id})['language']
    data = await state.get_data()
    await state.update_data(client_date = msg.text.lower())
    data = await state.get_data()
    save_data( 
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
    
    await bot.send_message(msg.from_user.id,
                        f'{_("Ваша заявка отправлена", lang)}\n'+
                        f'{_("Скоро вам придет ответ специалиста", lang)}'
                        )
    # View task 
    if collection.find_one({'userid': data['client_id']}) and collection.find_one({'task_date': data['client_msg_date']}):
        task = collection.find_one({'userid': data['client_id']})

        await bot.send_message(chat_id = group_chat_id , 
                            text = f'{_("Ник и id клиента", lang)} : {task["username"]} {task["userid"]}\n' +
                                    f'{_("ФИО менеджера", lang)} : {task["fio_menedjer"]}\n' +
                                    f'{_("Контактный номер менеджера", lang)} : {task["contact_number_menedjer"]}\n' +
                                    f'{_("Имя организации", lang)} : {task["organization_name"] }\n' +
                                    f'{_("Имя клиента", lang)} : {task["fio_client"]}\n' +
                                    f'{_("Контактный номер клиента", lang)} : {task["contact_number_client"] }\n' +
                                    f'{_("Версия Iiko", lang)} : {task["Iiko_version"]}\n' +
                                    f'{_("Время установки", lang)} : {task["install_date"]}\n' +
                                    f'{_("Адрес установки", lang)} : {task["adress_install_date"]}\n' +
                                    f'{_("Данная заявка была отправлена", lang)} : {task["task_date"] }' 
                            )
  
    await state.finish()
# *************************************
# *************************************
# *************************************


# ******************************************        
# ******************************************        
# ******************************************        
# Просмотр заявок для интеграции Iiko
@dp.callback_query_handler(lambda c: c.data == 'Iiko_cpec')
async def iiko_notifications(callback_query: types.CallbackQuery, state: FSMContext):
    lang = users_collection.find_one({'user_id':callback_query.from_user.id})['language']
    nots_iiko_KB = InlineKeyboardMarkup(row_width=1)
    num = 0
    for task in collection.find({'status': 'holver'}):
        if task['task_type'] == 'Iiko': #task['task_type'] = 'Iiko'
            print(task)
            notification = f'{num}| {task["username"]} {task["task_date"]}' 
            notification_data = f'notification_iiko_{task["userid"]}_{task["task_date"]}_{num}'
            nots_iiko_KB.add(InlineKeyboardButton(text=notification,
                                                    callback_data=notification_data
                                                    ))
            num += 1
    await callback_query.message.answer(_("Список заявок:", lang),
                                        reply_markup=nots_iiko_KB
                                        )
   
# Просмотр заявок для интеграции 1C
@dp.callback_query_handler(lambda c: c.data == '1C_cpec')
async def notifications_1C(callback_query: types.CallbackQuery, state: FSMContext):
    lang = users_collection.find_one({'user_id':callback_query.from_user.id})['language']
    nots_1C_KB = InlineKeyboardMarkup(row_width=1)
    num = 0
    for task in collection.find({'status': 'holver'}):
        if task['task_type'] == '1C': #task['task_type'] = 'Iiko'
            print(task)
            notification = f'{num}| {task["username"]} {task["task_date"]}' 
            notification_data = f'notifications_1C_{task["userid"]}_{task["task_date"]}_{num}'
            nots_1C_KB.add(InlineKeyboardButton(text=notification,
                                                    callback_data=notification_data
                                                    ))
            num += 1
    await callback_query.message.answer(_("Список заявок:", lang),
                                        reply_markup=nots_1C_KB
                                        )
# Call button iiko task 
@dp.callback_query_handler(lambda c: c.data and c.data.startswith('notification_iiko_'))
async def iiko_notification(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.edit_message_reply_markup(
        chat_id=callback_query.from_user.id,
        message_id=callback_query.message.message_id, 
        reply_markup=None
    )
    k = 0
    lang = users_collection.find_one({'user_id':callback_query.from_user.id})['language']
    for task in collection.find({'status': 'holver'}):
        if task['task_type'] == 'Iiko' and task['userid'] == int(callback_query.data.split('_')[2]) and task["task_date"] == callback_query.data.split('_')[3]:
            task_data = task
            k += 1
    if k != 0:            
        task_text = f'{_("Заявка", lang)}:\n'
        task_text += f'user_name: {task_data["username"]}\n'
        task_text += f'user_id: {task_data["userid"]}\n'
        task_text += f'{_("ФИО менеджера", lang)}: {task_data["fio_menedjer"]}\n'
        task_text += f'{_("Контактный номер менеджера", lang)}: {task_data["contact_number_menedjer"]}\n'
        task_text += f'{_("Имя организации", lang)}: {task_data["organization_name"]}\n'
        task_text += f'{_("Имя клиента", lang)}: {task_data["fio_client"]}\n'
        task_text += f'{_("Контактный номер клиента", lang)}: {task_data["contact_number_client"]}\n'
        task_text += f'{_("Версия Iiko", lang)}: {task_data["Iiko_version"]}\n'
        task_text += f'{_("Время установки", lang)}: {task_data["install_date"]}\n'
        task_text += f'{_("Адрес установки" , lang)}: {task_data["adress_install_date"]}\n'
        task_text += f'{_("Данная заявка была отправлена", lang)}: {task_data["task_date"]}'
        await callback_query.message.answer(task_text)

        await state.update_data(client_task = task_text,
                                task_id = task_data['_id'],
                                task_data = task_data
                                )
        await callback_query.message.answer(_("Принять заявку?", lang), 
                                            reply_markup=nav.operation_(lang)
                                            )
    else:
        await callback_query.message.answer(_("Данной заявки уже нет", lang))

# Call button 1C task 
@dp.callback_query_handler(lambda c: c.data and c.data.startswith('notifications_1C'))
async def notification_1C(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.edit_message_reply_markup(
        chat_id=callback_query.from_user.id,
        message_id=callback_query.message.message_id, 
        reply_markup=None
    )
    lang = users_collection.find_one({'user_id':callback_query.from_user.id})['language']
    k = 0
    for task in collection.find({'status': 'holver'}):
        if task['task_type'] == '1C' and task['userid'] == int(callback_query.data.split('_')[2]) and task["task_date"] == callback_query.data.split('_')[3]:
            task_data = task
            k += 1
    if k != 0:            

        notification = f"{callback_query.data.split('_')[2]} {callback_query.data.split('_')[3]}"
        print('Notification:', notification)
        task_text = ''
        task_text = f'{_("Заявка", lang)}:\n'
        task_text += f'user_name: {task_data["username"]}\n'
        task_text += f'user_id: {task_data["userid"]}\n'
        task_text += f'{_("ФИО менеджера", lang)}: {task_data["fio_menedjer"]}\n'
        task_text += f'{_("Контактный номер менеджера", lang)}: {task_data["contact_number_menedjer"]}\n'
        task_text += f'{_("Имя организации", lang)}: {task_data["organization_name"]}\n'
        task_text += f'{_("Имя клиента", lang)}: {task_data["fio_client"]}\n'
        task_text += f'{_("Контактный номер клиента", lang)}: {task_data["contact_number_client"]}\n'
        task_text += f'{_("Конфигурация данных", lang)}: {task_data["data_config"]}\n'
        task_text += f'{_("Количество касс", lang)}: {task_data["cass_count"]}\n'
        task_text += f'{_("Данная заявка была отправлена", lang)}: {task_data["task_date"]}'

        await callback_query.message.answer(task_text)

        await state.update_data(client_task = task_text,
                                task_id = task_data['_id'],
                                task_data = task_data
                                )
        await callback_query.message.answer(_("Принять заявку?", lang),
                                            reply_markup=nav.operation_(lang)
                                            )
    else:
        await callback_query.message.answer(_("Данной заявки уже нет", lang))

# task accepted
@dp.callback_query_handler(lambda c: c.data == 'task_btn_Yes')
async def receive_task(callback_query: types.CallbackQuery, state: FSMContext):
    lang = users_collection.find_one({'user_id':callback_query.from_user.id})['language']
    data = await state.get_data()
    await bot.edit_message_reply_markup(
        chat_id=callback_query.from_user.id,
        message_id=callback_query.message.message_id, 
        reply_markup=None
    )
    collection.update_one({"_id": ObjectId(data["task_data"]["_id"])}, {"$set":{"status": "accepted"}})

    await callback_query.message.answer(_("Принято", lang))

    lang2 = users_collection.find_one({'user_id':int(data["task_data"]["userid"])})['language']
    task_text = f'{_("Заявка", lang2)}:\n'
    task_text += f'user_name: {data["task_data"]["username"]}\n'
    task_text += f'user_id: {data["task_data"]["userid"]}\n'
    task_text += f'{_("ФИО менеджера", lang2)}: {data["task_data"]["fio_menedjer"]}\n'
    task_text += f'{_("Контактный номер менеджера", lang2)}: {data["task_data"]["contact_number_menedjer"]}\n'
    task_text += f'{_("Имя организации", lang2)}: {data["task_data"]["organization_name"]}\n'
    task_text += f'{_("Имя клиента", lang2)}: {data["task_data"]["fio_client"]}\n'
    task_text += f'{_("Контактный номер клиента", lang2)}: {data["task_data"]["contact_number_client"]}\n'
    if data["task_data"]["task_type"] == '1C':
        task_text += f'{_("Конфигурация данных", lang2)}: {data["task_data"]["data_config"]}\n'
        task_text += f'{_("Количество касс", lang2)}: {data["task_data"]["cass_count"]}\n'
    else:
        task_text += f'{_("Версия Iiko", lang2)}: {data["task_data"]["Iiko_version"]}\n'
        task_text += f'{_("Время установки", lang2)}: {data["task_data"]["install_date"]}\n'
        task_text += f'{_("Адрес установки" , lang2)}: {data["task_data"]["adress_install_date"]}\n'
    task_text += f'{_("Данная заявка была отправлена", lang2)}: {data["task_data"]["task_date"]}'

    await bot.send_message(int(data["task_data"]["userid"]), _("Ваша заявка принята", lang2))
    await bot.send_message(int(data["task_data"]["userid"]), f'{_("Заявка", lang2)}:\n')
    await bot.send_message(int(data["task_data"]["userid"]), task_text)

    spec = specialist_collection.find_one({'spec_id': callback_query.from_user.id})
    name = spec['spec_name']
    await bot.send_message(group_chat_id, f"{name}: {_('Данная заявка была принята', lang)}")
    await bot.send_message(group_chat_id, data['client_task'])

    await state.finish()

# task not accepted
@dp.callback_query_handler(lambda c: c.data == 'task_btn_No')
async def receive_task(callback_query: types.CallbackQuery, state: FSMContext):
    
    lang = users_collection.find_one({'user_id':callback_query.from_user.id})['language']
    await bot.edit_message_reply_markup(
        chat_id=callback_query.from_user.id,
        message_id=callback_query.message.message_id, 
        reply_markup=None
    )
    data = await state.get_data()
    collection.update_one({"_id": ObjectId(data["task_data"]["_id"])}, {"$set":{"status": "not accepted"}})
    
    await callback_query.message.answer(_("Отказано", lang))
    
    await callback_query.message.answer(_("Напишите причину отказа", lang))
    await Specialist_States.comment_state.set()

@dp.message_handler(content_types=['text'],state=Specialist_States.comment_state)
async def send_comment(msg: types.Message, state: FSMContext):
    lang = users_collection.find_one({'user_id':msg.from_user.id})['language']
    data = await state.get_data()

    lang2 = users_collection.find_one({'user_id':int(data["task_data"]["userid"])})['language']
    task_text = f'{_("Заявка", lang2)}:\n'
    task_text += f'user_name: {data["task_data"]["username"]}\n'
    task_text += f'user_id: {data["task_data"]["userid"]}\n'
    task_text += f'{_("ФИО менеджера", lang)}: {data["task_data"]["fio_menedjer"]}\n'
    task_text += f'{_("Контактный номер менеджера", lang2)}: {data["task_data"]["contact_number_menedjer"]}\n'
    task_text += f'{_("Имя организации", lang2)}: {data["task_data"]["organization_name"]}\n'
    task_text += f'{_("Имя клиента", lang2)}: {data["task_data"]["fio_client"]}\n'
    task_text += f'{_("Контактный номер клиента", lang2)}: {data["task_data"]["contact_number_client"]}\n'
    if data["task_data"]["task_type"] == '1C':
        task_text += f'{_("Конфигурация данных", lang2)}: {data["task_data"]["data_config"]}\n'
        task_text += f'{_("Количество касс", lang2)}: {data["task_data"]["cass_count"]}\n'
    else:
        task_text += f'{_("Версия Iiko", lang2)}: {data["task_data"]["Iiko_version"]}\n'
        task_text += f'{_("Время установки", lang2)}: {data["task_data"]["install_date"]}\n'
        task_text += f'{_("Адрес установки" , lang2)}: {data["task_data"]["adress_install_date"]}\n'
    task_text += f'{_("Данная заявка была отправлена", lang2)}: {data["task_data"]["task_date"]}'

    await bot.send_message(int(data["task_data"]["userid"]), _("Ваша заявка не принята", lang2))
    await bot.send_message(int(data["task_data"]["userid"]), f'{_("Заявка", lang2)}:')
    await bot.send_message(int(data["task_data"]["userid"]), task_text)
    await bot.send_message(int(data["task_data"]["userid"]), f'{_("Комментарий специалиста", lang)}:\n{msg.text}')

    spec = specialist_collection.find_one({'spec_id': msg.from_user.id})
    name = spec['spec_name']
    await bot.send_message(group_chat_id, f'{name}: {_("Данная заявка не принята:", lang)}\n')
    await bot.send_message(group_chat_id, data['client_task'])
    await bot.send_message(group_chat_id, f'{_("Причина", lang)}:\n{msg.text}')

    post = {"manager_name": f"{data['task_data']['fio_menedjer']}",
            "manager_phone": f"{data['task_data']['contact_number_menedjer']}",
            "organization": f"{data['task_data']['organization_name']}",
            "client_name": f"{data['task_data']['fio_client']}",
            "client_phone": f"{data['task_data']['contact_number_client']}",
            "type": f"{data['task_data']['task_type']}",
            "task_date": f"{data['task_data']['task_date']}",
            "status": "not accepted",
            }
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
    await state.finish()
# list of notificationds accepted tasks Iiko
@dp.callback_query_handler(lambda c: c.data == 'accec_iiko_tsak')
async def view_accepted_task(callback_query: types.CallbackQuery, state: FSMContext):
    lang = users_collection.find_one({'user_id':callback_query.from_user.id})['language']
    task_iiko_accepted_KB = InlineKeyboardMarkup(row_width=1)
    num = 0
    for task in collection.find({'status': 'accepted'}):
        if task['task_type'] == 'Iiko': 
            print(task)
            notification = f'{num}| {task["username"]} {task["task_date"]}' 
            notification_data = f'accepted_tasks_iiko_{task["_id"]}'
            task_iiko_accepted_KB.add(InlineKeyboardButton(text=notification, callback_data=f'{notification_data}'))
            num += 1
    await callback_query.message.answer(_("Список принятых заявок Iiko", lang),
                            reply_markup=task_iiko_accepted_KB)

# list of notificationds accepted tasks 1C
@dp.callback_query_handler(lambda c: c.data == 'accec_1C_tsak')
async def view_accepted_task_1C(callback_query: types.CallbackQuery, state: FSMContext):
    lang = users_collection.find_one({'user_id':callback_query.from_user.id})['language']
    task_1C_accepted_KB = InlineKeyboardMarkup(row_width=1)
    num = 0
    for task in collection.find({'status': 'accepted'}):
        if task['task_type'] == '1C': 
            notification = f'{num}| {task["username"]} {task["task_date"]}' 
            notification_data = f'accepted_tasks_1c_{task["_id"]}'
            task_1C_accepted_KB.add(InlineKeyboardButton(text=notification, callback_data=f'{notification_data}'))
            num += 1
    await callback_query.message.answer(_("Список принятых заявок 1C", lang),
                            reply_markup=task_1C_accepted_KB)
    

@dp.callback_query_handler(lambda c: c.data and c.data.startswith('accepted_tasks_iiko_'))
async def iiko_accepted_task(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.edit_message_reply_markup(
        chat_id=callback_query.from_user.id,
        message_id=callback_query.message.message_id, 
        reply_markup=None
    )
    lang = users_collection.find_one({'user_id':callback_query.from_user.id})['language'] 
    task_data = collection.find_one({'_id': ObjectId(callback_query.data.split('_')[3])})
    task_text = f'{_("Заявка", lang)}:\n'
    task_text += f'user_name: {task_data["username"]}\n'
    task_text += f'user_id: {task_data["userid"]}\n'
    task_text += f'{_("ФИО менеджера", lang)}: {task_data["fio_menedjer"]}\n'
    task_text += f'{_("Контактный номер менеджера", lang)}: {task_data["contact_number_menedjer"]}\n'
    task_text += f'{_("Имя организации", lang)}: {task_data["organization_name"]}\n'
    task_text += f'{_("Имя клиента", lang)}: {task_data["fio_client"]}\n'
    task_text += f'{_("Контактный номер клиента", lang)}: {task_data["contact_number_client"]}\n'
    task_text += f'{_("Версия Iiko", lang)}: {task_data["Iiko_version"]}\n'
    task_text += f'{_("Время установки", lang)}: {task_data["install_date"]}\n'
    task_text += f'{_("Адрес установки" , lang)}: {task_data["adress_install_date"]}\n'
    task_text += f'{_("Данная заявка была отправлена", lang)}: {task_data["task_date"]}'

    await state.update_data(client_task = task_text,
                            task_id = task_data['_id'],
                            task_data = task_data
                            )
    await callback_query.message.answer(task_text, reply_markup=nav.save_db_(lang))

@dp.callback_query_handler(lambda c: c.data and c.data.startswith('accepted_tasks_1c_'))
async def accepted_task_1C(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.edit_message_reply_markup(
        chat_id=callback_query.from_user.id,
        message_id=callback_query.message.message_id, 
        reply_markup=None
    )
    lang = users_collection.find_one({'user_id':callback_query.from_user.id})['language'] 
    task_data = collection.find_one({'_id': ObjectId(callback_query.data.split('_')[3])})
    task_text = ''
    task_text = f'{_("Заявка", lang)}:\n'
    task_text += f'user_name: {task_data["username"]}\n'
    task_text += f'user_id: {task_data["userid"]}\n'
    task_text += f'{_("ФИО менеджера", lang)}: {task_data["fio_menedjer"]}\n'
    task_text += f'{_("Контактный номер менеджера", lang)}: {task_data["contact_number_menedjer"]}\n'
    task_text += f'{_("Имя организации", lang)}: {task_data["organization_name"]}\n'
    task_text += f'{_("Имя клиента", lang)}: {task_data["fio_client"]}\n'
    task_text += f'{_("Контактный номер клиента", lang)}: {task_data["contact_number_client"]}\n'
    task_text += f'{_("Конфигурация данных", lang)}: {task_data["data_config"]}\n'
    task_text += f'{_("Количество касс", lang)}: {task_data["cass_count"]}\n'
    task_text += f'{_("Данная заявка была отправлена", lang)}: {task_data["task_date"]}'

    await state.update_data(client_task = task_text,
                            task_id = task_data['_id'],
                            task_data = task_data
                            )
    await callback_query.message.answer(task_text, reply_markup=nav.save_db_(lang))


@dp.callback_query_handler(lambda c: c.data == 'closed_tasks')
async def save_db_closed_tasks(callback_query: types.CallbackQuery, state: FSMContext):
    lang = users_collection.find_one({'user_id':callback_query.from_user.id})['language']
    await bot.edit_message_reply_markup(
        chat_id=callback_query.from_user.id,
        message_id=callback_query.message.message_id, 
        reply_markup=None
    )
    data = await state.get_data()
    collection.update_one({"_id": ObjectId(data["task_data"]["_id"])}, {"$set":{"status": "closed"}})

    post = {"manager_name": f"{data['task_data']['fio_menedjer']}",
            "manager_phone": f"{data['task_data']['contact_number_menedjer']}",
            "organization": f"{data['task_data']['organization_name']}",
            "client_name": f"{data['task_data']['fio_client']}",
            "client_phone": f"{data['task_data']['contact_number_client']}",
            "type": f"{data['task_data']['task_type']}",
            "task_date": f"{data['task_data']['task_date']}",
            "status": "closed(finished)"
        }
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
    await callback_query.message.answer(_("Данная заявка была закрыта(завершена)", lang))

@dp.callback_query_handler(lambda c: c.data == 'regected_tasks')
async def save_db_regected_tasks(callback_query: types.CallbackQuery, state: FSMContext):
    lang = users_collection.find_one({'user_id':callback_query.from_user.id})['language']
    await bot.edit_message_reply_markup(
        chat_id=callback_query.from_user.id,
        message_id=callback_query.message.message_id, 
        reply_markup=None
    )
    data = await state.get_data()
    collection.update_one({"_id": ObjectId(data["task_data"]["_id"])}, {"$set":{"status": "regected"}})
    post = {"manager_name": f"{data['task_data']['fio_menedjer']}",
            "manager_phone": f"{data['task_data']['contact_number_menedjer']}",
            "organization": f"{data['task_data']['organization_name']}",
            "client_name": f"{data['task_data']['fio_client']}",
            "client_phone": f"{data['task_data']['contact_number_client']}",
            "type": f"{data['task_data']['task_type']}",
            "task_date": f"{data['task_data']['task_date']}",
            "status": "regected"
        }
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
    await callback_query.message.answer(_("Данная заявка была отменена", lang))


    

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates = True)

# q w e r t y u i o p a s d f g h j k l z x c v b n m