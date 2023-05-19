from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from translations import _

# Кнопки дляч смены языка
ru = InlineKeyboardButton(text='русский', callback_data = 'lang_ru')
uz = InlineKeyboardButton(text='oʻzbek tili', callback_data = 'lang_uz')
lang_KB = InlineKeyboardMarkup(row_width=1).row(ru, uz)

# кнопки для специалистов, чтоб смотреть заявки
button_iiko_cpec = InlineKeyboardButton('Iiko', callback_data='Iiko_cpec')
button_1c_cpec = InlineKeyboardButton('1C', callback_data='1C_cpec')
choose_iiko_1c_for_cpec_KB = InlineKeyboardMarkup(row_width=1).row(button_iiko_cpec, button_1c_cpec)

# кнопки для специалистов, чтоб смотреть список принятых заявок
accec_iiko_tsak = InlineKeyboardButton('Iiko',callback_data="accec_iiko_tsak")
accec_1C_tsak = InlineKeyboardButton('1С',callback_data="accec_1C_tsak")
acceces_task_KB = InlineKeyboardMarkup(row_width=1).row(accec_iiko_tsak,accec_1C_tsak)

# остановить все процессы
def base_(lang):
    stop = InlineKeyboardButton(_("стоп",lang), callback_data='stop')
    aboute = InlineKeyboardButton(_("о боте",lang), callback_data='about')
    base_KB = InlineKeyboardMarkup(row_width=1).row(aboute, stop)
    return base_KB

# Кнопки для клиентов, чтоб выбирали куда заявку писать
def choose_iiko_1c_(lang):
    stop = InlineKeyboardButton(_("стоп",lang), callback_data='stop')
    aboute = InlineKeyboardButton(_("о боте",lang), callback_data='about')
    button_iiko = InlineKeyboardButton('Iiko', callback_data='Iiko')
    button_1c = InlineKeyboardButton('1C', callback_data='1C')
    choose_iiko_1c_KB = InlineKeyboardMarkup(row_width=1).row(button_1c, button_iiko).row(stop,aboute)
    return choose_iiko_1c_KB
def view_tasks(lang):
    return InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(_("Отправленные заявки", lang), callback_data='my_tasks'))
# кнопки для специалистов, чтоб смотреть список специалистов и добавлять их 
def spec_(lang):
    list_of_spec = InlineKeyboardButton(_('Список специалистов', lang),callback_data="list_of_spec")
    add_spec = InlineKeyboardButton(_('Добавить специалиста', lang),callback_data="add_spec")
    drop_spec = InlineKeyboardButton(_('Удалить специалиста', lang),callback_data="drop_spec")
    edit_spec = InlineKeyboardButton(_('Поменять свое имя', lang),callback_data="edit_spec")
    spec_kb = InlineKeyboardMarkup(row_width=1).row(list_of_spec,add_spec).row(edit_spec,drop_spec)
    return spec_kb
# кнопки для принятия или отказа заявки
def operation_(lang):
    yes_iiko = InlineKeyboardButton(text=_("Принять", lang), callback_data="task_btn_Yes")
    no_iiko = InlineKeyboardButton(text=_("Отклонить", lang), callback_data="task_btn_No")    
    option_for_iiko_KB = InlineKeyboardMarkup(row_width=1).row(yes_iiko, no_iiko)
    return option_for_iiko_KB
# кнопки для принятия или отказа заявки со стороны айко
def option_for_iiko_(lang):
    yes_iiko = InlineKeyboardButton(text=_("Принять", lang), callback_data="iiko_btn_Yes")
    no_iiko = InlineKeyboardButton(text=_("Отклонить", lang), callback_data="iiko_btn_No")    
    option_for_iiko_KB = InlineKeyboardMarkup(row_width=1).row(yes_iiko, no_iiko)
    return option_for_iiko_KB

# кнопки для принятия или отказа заявки со стороны 1С
def option_for_1C_(lang):
    yes_1C = InlineKeyboardButton(text=_("Принять", lang), callback_data="1C_btn_Yes")
    no_1C = InlineKeyboardButton(text=_("Отклонить", lang), callback_data="1C_btn_No")    
    option_for_1C_KB = InlineKeyboardMarkup(row_width=1).row(yes_1C, no_1C)
    return option_for_1C_KB

# Кнопки для закрытия или отменвы заявки , при этом они сохроняются в бд
def save_db_(lang):
    closed_btn = InlineKeyboardButton(_('Закрыть', lang), callback_data='closed_tasks')
    regected_btn = InlineKeyboardButton(_('Отменить', lang), callback_data='regected_tasks')
    save_db_kb = InlineKeyboardMarkup(row_width=1).row(closed_btn, regected_btn)
    return save_db_kb
