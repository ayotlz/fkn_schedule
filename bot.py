import telebot
from config import token

bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start', 'schedule'])
def menu(message):
    if message.text == '/start' or message.text == '/schedule':
        get_year(message)


def get_year(message):
    bot.send_message(message.chat.id, 'Курс', reply_markup=years_keyboard())


def years_keyboard():
    keyboard = telebot.types.InlineKeyboardMarkup()
    for i in range(5):
        keyboard.row(telebot.types.InlineKeyboardButton(text=str(i + 1), callback_data="year_" + str(i + 1)))
    return keyboard


def get_group(message, year):
    bot.send_message(message.chat.id, 'Группа', reply_markup=groups_keyboard(year))


def groups_keyboard(year):
    keyboard = telebot.types.InlineKeyboardMarkup()
    if year == '1':
        keyboard.row(telebot.types.InlineKeyboardButton(text='СБС-101-О-01', callback_data="group_СБС-101-О-01"))
        keyboard.row(telebot.types.InlineKeyboardButton(text='СБС-102-О-01', callback_data="group_СБС-102-О-01"))
        keyboard.row(telebot.types.InlineKeyboardButton(text='СББ-101-О-01', callback_data="group_СББ-101-О-01"))
        keyboard.row(telebot.types.InlineKeyboardButton(text='СМБ-101-О-01', callback_data="group_СМБ-101-О-01"))
        keyboard.row(telebot.types.InlineKeyboardButton(text='СИБ-101-О-01', callback_data="group_СИБ-101-О-01"))
        keyboard.row(telebot.types.InlineKeyboardButton(text='СПБ-101-О-01', callback_data="group_СПБ-101-О-01"))
    if year == '2':
        keyboard.row(telebot.types.InlineKeyboardButton(text='СБС-001-О-01', callback_data="group_СБС-001-О-01"))
        keyboard.row(telebot.types.InlineKeyboardButton(text='СБС-002-О-01', callback_data="group_СБС-002-О-01"))
        keyboard.row(telebot.types.InlineKeyboardButton(text='СББ-001-О-01', callback_data="group_СББ-001-О-01"))
        keyboard.row(telebot.types.InlineKeyboardButton(text='СМБ-001-О-01', callback_data="group_СМБ-001-О-01"))
        keyboard.row(telebot.types.InlineKeyboardButton(text='СИБ-001-О-01', callback_data="group_СИБ-001-О-01"))
        keyboard.row(telebot.types.InlineKeyboardButton(text='СПБ-001-О-01', callback_data="group_СПБ-001-О-01"))
    if year == '3':
        keyboard.row(telebot.types.InlineKeyboardButton(text='СБС-901-О-01', callback_data="group_СБС-901-О-01"))
        keyboard.row(telebot.types.InlineKeyboardButton(text='СББ-901-О-01', callback_data="group_СББ-901-О-01"))
        keyboard.row(telebot.types.InlineKeyboardButton(text='СМБ-901-О-01', callback_data="group_СМБ-901-О-01"))
        keyboard.row(telebot.types.InlineKeyboardButton(text='СИБ-901-О-01', callback_data="group_СИБ-901-О-01"))
        keyboard.row(telebot.types.InlineKeyboardButton(text='СПБ-901-О-01', callback_data="group_СПБ-901-О-01"))
    if year == '4':
        keyboard.row(telebot.types.InlineKeyboardButton(text='СБС-801-О-01', callback_data="group_СБС-801-О-01"))
        keyboard.row(telebot.types.InlineKeyboardButton(text='СББ-801-О-01', callback_data="group_СББ-801-О-01"))
        keyboard.row(telebot.types.InlineKeyboardButton(text='СМБ-801-О-01', callback_data="group_СМБ-801-О-01"))
        keyboard.row(telebot.types.InlineKeyboardButton(text='СИБ-801-О-01', callback_data="group_СИБ-801-О-01"))
        keyboard.row(telebot.types.InlineKeyboardButton(text='СПБ-801-О-01', callback_data="group_СПБ-801-О-01"))
    if year == '5':
        keyboard.row(telebot.types.InlineKeyboardButton(text='СБС-701-О-01', callback_data="group_СБС-701-О-01"))
    return keyboard


def get_day(message, group):
    bot.send_message(message.chat.id, group)


@bot.callback_query_handler(func=lambda message: True)
def handle(message):
    if message.data.startswith('year_'):
        get_group(message.message, message.data.split('year_')[1])
    if message.data.startswith('group_'):
        get_day(message.message, message.data.split('group_')[1])


if __name__ == '__main__':
    bot.infinity_polling()
