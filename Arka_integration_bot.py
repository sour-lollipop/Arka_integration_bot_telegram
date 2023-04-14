import logging
from aiogram import Bot,Dispatcher,executor,types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import os
import locale
locale.setlocale(locale.LC_ALL, '')
'ru_RU.utf8'
# Configure logging
logging.basicConfig(level = logging.INFO)
# Initialize bot and storage
bot = Bot(token = '5924382439:AAGLwM6sUPbY_cVxmOKzT_xf3b-PaUesZPs')
dp = Dispatcher(bot, storage = MemoryStorage())

button_iiko = InlineKeyboardButton('Iiko', callback_data='Iiko')
button_1c = InlineKeyboardButton('1C', callback_data='1C')
choose_iiko_1c_KB = InlineKeyboardMarkup(row_width=1).add(button_iiko, button_1c)

button_iiko_cpec = InlineKeyboardButton('Iiko', callback_data='Iiko_cpec')
button_1c_cpec = InlineKeyboardButton('1C', callback_data='1C_cpec')
choose_iiko_1c_for_cpec_KB = InlineKeyboardMarkup(row_width=1).add(button_iiko_cpec, button_1c_cpec)
@dp.message_handler(content_types=['new_chat_members'])
async def new_members(msg):
    for i in range(len(msg.new_chat_members)):
        name = msg.new_chat_members[i].first_name
        await bot.send_message(msg.chat.id, f"Добро пожаловать, @{name}! \n"\
                            "Что бы отправить заявку, пишите мне в директ(лс)")
        

@dp.message_handler(commands=['start'], chat_type = 'private')
async def start_command(msg: types.Message):
    if str(msg.from_user.id) in cpecialist_list():
        await bot.send_message(msg.from_user.id,
                           text=f'Добро пожаловать {msg.from_user.first_name}!\n'+ 
                                'Выберете свое направление:',
                           reply_markup=choose_iiko_1c_for_cpec_KB
                           )
    else:    
        await bot.send_message(msg.from_user.id,
                            text=f'Добро пожаловать {msg.from_user.first_name}!\n'+ 
                                    'Выберете с чем вы хотите работать:',
                            reply_markup=choose_iiko_1c_KB
                            )

class Iiko_States(StatesGroup):
    date_time_state = State()
    ip_state = State()
    adress_state = State()
    access_state = State()
    iiko_front_IP_state = State()
    iiko_front_auth_state = State()
    iiko_office_IP_state = State()
    iiko_office_auth_state = State()
    test_state = State()

class Specialist_States(StatesGroup):
    add_spec_state = State()
    comment_state = State()
   
@dp.callback_query_handler(lambda c: c.data == 'Iiko')
async def save_information(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.edit_message_reply_markup(
        chat_id=callback_query.from_user.id,
        message_id=callback_query.message.message_id, 
        reply_markup=None
    )
    await  callback_query.message.answer('Вы выбрали Iiko')
    await  callback_query.message.answer('Введите время установки\n'+
                                         'Например: 28.11.2023 18:00 UTC+6 '
                                         )
    await Iiko_States.date_time_state.set()

@dp.message_handler(content_types=['text'], state=Iiko_States.date_time_state)
async def save_date(msg: types.Message, state: FSMContext):
    await state.update_data(client_name = msg.from_user.first_name,
                            client_id = msg.from_user.id,
                            client_date = msg.text,
                            client_msg_date = msg.date.strftime('%w %B %H:%M')
                            )
    await bot.send_message(msg.from_user.id,
                           'Напишите полное названиеИП'
                           )
    await Iiko_States.ip_state.set()

@dp.message_handler(content_types=['text'], state=Iiko_States.ip_state)
async def save_date(msg: types.Message, state: FSMContext):
    await state.update_data(client_SP = msg.text)
    await bot.send_message(msg.from_user.id,
                           'Напишите адресс, где устанавливать плагин\n'+
                           'Например: страна Казахстан, город Алматы, улица Таугуль, дом 33б'
                           )
    await Iiko_States.adress_state.set()
    
@dp.message_handler(content_types=['text'], state=Iiko_States.adress_state)
async def save_date(msg: types.Message, state: FSMContext):
    await state.update_data(client_adress = msg.text)
    await bot.send_message(msg.from_user.id,
                        'Дадите ли вы доступ(пароль, логин) к IikoFront, IikoOffice?\n'+
                        'Ответ должен быть ДА или НЕТ'
                        )
    await Iiko_States.access_state.set()

@dp.message_handler(content_types=['text'], state=Iiko_States.access_state)
async def save_date(msg: types.Message, state: FSMContext):
    await state.update_data(client_access = msg.text.lower())
    await bot.send_message(msg.from_user.id,
                           'Напишите IP Anydesk, где рассположен Iiko Front'
                            )
    await Iiko_States.iiko_front_IP_state.set()

# ********************************************
@dp.message_handler(content_types=['text'], state=Iiko_States.iiko_front_IP_state)
async def save_date(msg: types.Message, state: FSMContext):
    await state.update_data(client_iiko_front_IP = msg.text)
    data = await state.get_data()
    if 'нет' in data['client_access']: 
        await bot.send_message(msg.from_user.id,
                           'Протестировать плагин?\n'+
                           'Ответ должен быть ДА или НЕТ'
                           )
        await Iiko_States.test_state.set()
    else:
        await bot.send_message(msg.from_user.id,
                            'Напишите пароль Iiko Front\n'+
                            'Например: Pa$$W0Rd123'
                            )
        await Iiko_States.iiko_front_auth_state.set()

@dp.message_handler(content_types=['text'], state=Iiko_States.iiko_front_auth_state)
async def save_date(msg: types.Message, state: FSMContext):
    await state.update_data(client_iiko_front_auth = msg.text)
    await bot.send_message(msg.from_user.id,
                        'Напишите IP Anydesk, где рассположен Iiko Office'
                        )
    await Iiko_States.iiko_office_IP_state.set()
# ********************************************************
@dp.message_handler(content_types=['text'], state=Iiko_States.iiko_office_IP_state)
async def save_date(msg: types.Message, state: FSMContext):
    await state.update_data(client_iiko_office_IP = msg.text)
    data = await state.get_data()
    await bot.send_message(msg.from_user.id,
                            'Напишите логин и пароль Iiko Office\n'+
                            'Например: UsEr123 Pa$$W0Rd123'
                            )
    await Iiko_States.iiko_office_auth_state.set()

@dp.message_handler(content_types=['text'], state=Iiko_States.iiko_office_auth_state)
async def save_date(msg: types.Message, state: FSMContext):
    await state.update_data(client_iiko_office_auth = msg.text)
    await bot.send_message(msg.from_user.id,
                           'Протестировать плагин?\n'+
                           'Ответ должен быть ДА или НЕТ'
                           )
    await Iiko_States.test_state.set()
# ********************************************************

def save_data( file_name, 
                    client_name,
                    client_id,
                    client_SP,
                    client_date,
                    client_adress,
                    client_access, 
                    client_iiko_front_IP,
                    client_test,
                    client_msg_date,
                    client_iiko_front_auth = 'None',
                    client_iiko_office_IP = 'None',
                    client_iiko_office_auth = 'None'
                  ):
  with open(f"{file_name}",'w', encoding='utf-8') as file:
          file.writelines(f"Имя и id клиента:: {client_name} {client_id}\n")
          file.writelines(f"Ип:: {client_SP}\n")
          file.writelines(f"Время установки:: {client_date}\n")
          file.writelines(f"Адресс установки:: {client_adress}\n")
          file.writelines(f"Доступ к IP:: {client_access}\n")
          file.writelines(f"IP Iiko Front:: {client_iiko_front_IP}\n")

  if 'да'in client_access:
      with open(f"{file_name}",'a', encoding='utf-8') as file:
          file.writelines(f"Iiko Front пароль:: {client_iiko_front_auth}\n")
          file.writelines(f"IP Iiko Office:: {client_iiko_office_IP}\n")
          file.writelines(f"Iiko Office логин,пароль:: {client_iiko_office_auth}\n")

  with open(f"{file_name}",'a', encoding='utf-8') as file:
          file.writelines(f"Разрешение на тестирование:: {client_test}\n")
          file.writelines(f"Данная заявка была отправлена:: {client_msg_date}\n")

@dp.message_handler(content_types=['text'], state=Iiko_States.test_state)
async def save_date(msg: types.Message, state: FSMContext):
    await state.update_data(client_test = msg.text.lower())
    data = await state.get_data()
    n = 1
    for file in os.listdir():
        if f"{data['client_name']} {data['client_id']}" in file:
            n+=1
   
    file_name = f"{data['client_name']} {data['client_id']} T{n}.txt" 
    if 'да'in data['client_access']:
        save_data( file_name = file_name, 
                    client_name = data['client_name'],
                    client_id = data['client_id'],
                    client_SP = data['client_SP'],
                    client_date = data['client_date'],
                    client_adress = data['client_adress'],
                    client_access = data['client_access'], 
                    client_iiko_front_IP =data['client_iiko_office_IP'] ,
                    client_iiko_front_auth = data['client_iiko_front_auth'],
                    client_iiko_office_IP = data['client_iiko_office_IP'],
                    client_iiko_office_auth = data['client_iiko_office_auth'],
                    client_test = data['client_test'],
                    client_msg_date = data['client_msg_date'] 
                )
    else:
        save_data( file_name = file_name, 
                    client_name = data['client_name'],
                    client_id = data['client_id'],
                    client_SP = data['client_SP'],
                    client_date = data['client_date'],
                    client_adress = data['client_adress'],
                    client_access = data['client_access'], 
                    client_iiko_front_IP = data['client_iiko_front_IP'] ,
                    client_test = data['client_test'],
                    client_msg_date = data['client_msg_date'] 
                )

    await bot.send_message(msg.from_user.id,
                        'Ваша заявка отправлена\n'+
                        'Скоро вам придет ответ специалиста'
                        )
    with open('notifications.txt','a',encoding='utf-8') as file:
        file.writelines(f"{data['client_name']}//{data['client_msg_date']}//{data['client_id']}//T{n}\n")  
    await state.finish()

# *******************************************************
# *******************************************************
# *******************************************************
def cpecialist_list():
    with open('./specialist_list.txt',encoding='utf-8') as file:
        specialist_list = file.readlines()
    # specialist_list = open('./specialist_list.txt',encoding='utf-8').readlines()
    cpecs = []
    for spec in specialist_list:
        for el in spec.split():
            cpecs.append(el)
    return cpecs

@dp.message_handler(commands=['add_spec'], chat_type = 'private')
async def instruction_for_add(msg: types.Message):
    if str(msg.from_user.id) in cpecialist_list():
        await bot.send_message(chat_id = msg.from_user.id, 
                                text =  f'Ввидите id и имя специалиста, которого хотите добавить\n'+
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

@dp.message_handler(commands=['view_spec'], chat_type = 'private')
async def instruction_for_add(msg: types.Message):
    if str(msg.from_user.id) in cpecialist_list():
        cpec_list = ''
        period = 0
        for cpec in cpecialist_list():
            period += 1
            cpec_list+= f"{cpec} "
            if period%2 == 0:
                cpec_list+='\n'
            
        await bot.send_message(chat_id = msg.from_user.id, 
                                text =  f'Список специалистов:\n'+
                                f'{cpec_list}'
                                )

@dp.callback_query_handler(lambda c: c.data == 'Iiko_cpec')
async def iiko_notifications(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.edit_message_reply_markup(
        chat_id=callback_query.from_user.id,
        message_id=callback_query.message.message_id, 
        reply_markup=None
    )

    nots_iiko_KB = InlineKeyboardMarkup(row_width=1)

    with open ('./notifications.txt',encoding='utf-8') as file:
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
    await bot.delete_message(chat_id=callback_query.message.chat.id, 
                             message_id=callback_query.message.message_id
                             )
yes_iiko = InlineKeyboardButton(text="YES", callback_data="iiko_btn_Yes")
no_iiko = InlineKeyboardButton(text="NO", callback_data="iiko_btn_No")    
option_for_iiko_KB = InlineKeyboardMarkup(row_width=1).add(yes_iiko, no_iiko)

@dp.callback_query_handler(lambda c: c.data and c.data.startswith('notification_iiko'))
async def iiko_notification(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.edit_message_reply_markup(
            chat_id=callback_query.from_user.id,
            message_id=callback_query.message.message_id, 
            reply_markup=None
        )
    notification = f"{callback_query.data.split('_')[2]} {callback_query.data.split('_')[3]}"
    print('Notification:', notification)
    task_text = ''
    k = 0
    for file in os.listdir():
        print(file)
        if ((notification.split()[0] in file) and (notification.split()[1] in file)) and 'YES' not in file:
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
                                    client_name = file.split()[0]
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
    os.remove(f'./{data["client_file"]}')
    with open(f"YES {data['client_file']}", 'w', encoding='utf-8') as file:
        for line in data['client_task']:
            file.writelines(line)

    with open('./notifications.txt', encoding='utf-8') as file:
        notifications = file.readlines()
    for line in notifications:
        if data["client_id"] in line and  data['client_task_number'] in line:
            notifications.remove(line)
    with open('./notifications.txt','w', encoding='utf-8') as file:
        for line in notifications:
            file.writelines(line)

    print(data["client_file"])
    print(data["client_id"])
    print(data["client_name"])

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
    with open('./notifications.txt', encoding='utf-8') as file:
        notifications = file.readlines()
    for line in notifications:
        if data["client_id"] in line and  data['client_task_number'] in line:
            notifications.remove(line)
    with open('./notifications.txt','w', encoding='utf-8') as file:
        for line in notifications:
            file.writelines(line)
    await state.finish()


@dp.callback_query_handler(lambda c: c.data == '1C_cpec')
async def notifications_1C(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.edit_message_reply_markup(
        chat_id=callback_query.from_user.id,
        message_id=callback_query.message.message_id, 
        reply_markup=None
    )
    await  callback_query.message.answer('Вы выбрали 1C\n В разработке')
# @dp.message_handler(commands = ['clients'], chat_type = 'private')
# def cpec_notifications(msg: types.Message,):
#     if 



@dp.callback_query_handler(lambda c: c.data == '1C')
async def save_information_1C(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.edit_message_reply_markup(
        chat_id=callback_query.from_user.id,
        message_id=callback_query.message.message_id, 
        reply_markup=None
    )
    await  callback_query.message.answer('Вы выбрали 1C\n Находиться в разработке')



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates = True)