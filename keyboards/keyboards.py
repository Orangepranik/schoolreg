from importi.importi import *
def start_keyboard():
    static_info_keyboard = types.ReplyKeyboardMarkup()
    buttons = ['Подати заявку на вступ', 'Інформація про школу', 'Профіль']
    static_info_keyboard.add(*buttons)
    return static_info_keyboard
def returntomenu():
    statick_keyboard = types.ReplyKeyboardMarkup()
    buttons = ['Повернутися назад']
    statick_keyboard.add(*buttons)
    return statick_keyboard
def yesornorequest():
    statick_keyboard = types.ReplyKeyboardMarkup()
    buttons = ['Так', 'Ні']
    statick_keyboard.add(*buttons)
    return statick_keyboard