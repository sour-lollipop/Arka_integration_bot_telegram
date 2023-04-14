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


@dp.message_handler(commands=['start'])
async def start_command(msg: types.Message):
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
    if n == 1:
        file_name = f"{data['client_name']} {data['client_id']}.txt" 
    else:
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
        file.writelines(f"{data['client_name']}//{data['client_msg_date']}//{data['client_id']}//T{n}")  
    await state.finish()

# @dp.message_handler(commands = ['clients'], chat_type = 'privates')
# def cpec_notifications(msg: types.Message,):
#     if 



notifications_KB = InlineKeyboardMarkup(row_width = 1)

@dp.callback_query_handler(lambda c: c.data == '1C')
async def save_information(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.edit_message_reply_markup(
        chat_id=callback_query.from_user.id,
        message_id=callback_query.message.message_id, 
        reply_markup=None
    )
    await  callback_query.message.answer('Вы выбрали 1C\n Находиться в разработке')



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates = True)