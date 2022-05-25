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
    statick_keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    buttons = ['Так', 'Ні']
    statick_keyboard.add(*buttons)
    return statick_keyboard


def error_in_questionary():
    statik_keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    button = ["Змінити анкету"]
    statik_keyboard.add(*button)
    return statik_keyboard


def correct_answers():
    statick_keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    buttons = ['1', '2', '3', '4', '5']
    statick_keyboard.add(*buttons)
    return statick_keyboard