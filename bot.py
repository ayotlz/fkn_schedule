import telebot
from config import token
import db

bot = telebot.TeleBot(token)
db.init_db()


@bot.message_handler(commands=['start', 'schedule'])
def menu(message):
    if message.text == '/start' or message.text == '/schedule':
        schedule(message)


def schedule(message):
    def get_year():
        msg = bot.send_message(message.chat.id, 'Курс', reply_markup=years_keyboard())
        bot.register_next_step_handler(msg, get_group)

    def years_keyboard():
        keyboard = telebot.types.ReplyKeyboardMarkup()
        for i in range(5):
            keyboard.add(telebot.types.KeyboardButton(str(i + 1)))
        return keyboard

    def get_group(msg):
        msg = bot.send_message(message.chat.id, 'Группа', reply_markup=groups_keyboard(msg.text))
        bot.register_next_step_handler(msg, get_day)

    def groups_keyboard(year):
        keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        if year == '1':
            keyboard.add(telebot.types.KeyboardButton('СБС-101-О-01'))
            keyboard.add(telebot.types.KeyboardButton('СБС-102-О-01'))
            keyboard.add(telebot.types.KeyboardButton('СББ-101-О-01'))
            keyboard.add(telebot.types.KeyboardButton('СМБ-101-О-01'))
            keyboard.add(telebot.types.KeyboardButton('СИБ-101-О-01'))
            keyboard.add(telebot.types.KeyboardButton('СПБ-101-О-01'))
        if year == '2':
            keyboard.add(telebot.types.KeyboardButton('СБС-001-О-01'))
            keyboard.add(telebot.types.KeyboardButton('СБС-002-О-01'))
            keyboard.add(telebot.types.KeyboardButton('СББ-001-О-01'))
            keyboard.add(telebot.types.KeyboardButton('СМБ-001-О-01'))
            keyboard.add(telebot.types.KeyboardButton('СИБ-001-О-01'))
            keyboard.add(telebot.types.KeyboardButton('СПБ-001-О-01'))
        if year == '3':
            keyboard.add(telebot.types.KeyboardButton('СБС-901-О-01'))
            keyboard.add(telebot.types.KeyboardButton('СББ-901-О-01'))
            keyboard.add(telebot.types.KeyboardButton('СМБ-901-О-01'))
            keyboard.add(telebot.types.KeyboardButton('СИБ-901-О-01'))
            keyboard.add(telebot.types.KeyboardButton('СПБ-901-О-01'))
        if year == '4':
            keyboard.add(telebot.types.KeyboardButton('СБС-801-О-01'))
            keyboard.add(telebot.types.KeyboardButton('СББ-801-О-01'))
            keyboard.add(telebot.types.KeyboardButton('СМБ-801-О-01'))
            keyboard.add(telebot.types.KeyboardButton('СИБ-801-О-01'))
            keyboard.add(telebot.types.KeyboardButton('СПБ-801-О-01'))
        if year == '5':
            keyboard.add(telebot.types.KeyboardButton('СБС-701-О-01'))
        return keyboard

    def get_day(msg):
        group = msg.text
        msg = bot.send_message(message.chat.id, 'День недели', reply_markup=days_keyboard())
        bot.register_next_step_handler(msg, get_schedule, group)

    def days_keyboard():
        days = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота']
        keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        for day in days:
            keyboard.add(telebot.types.KeyboardButton(day))
        return keyboard

    def get_schedule(msg, group):
        bot.send_message(message.chat.id, db.get_lessons(group=group, day=msg.text),
                         reply_markup=telebot.types.ReplyKeyboardRemove())

    get_year()


if __name__ == '__main__':
    bot.infinity_polling()
