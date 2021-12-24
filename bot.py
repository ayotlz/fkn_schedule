import telebot
from config import token
import db
# import socks
import feedparser
import distributing
from threading import Thread

bot = telebot.TeleBot(token)
Thread(target=distributing.launch, args=(bot,)).start()
db.init_db()

groups = {'1': ['СБС-101-О-01', 'СБС-102-О-01', 'СББ-101-О-01', 'СМБ-101-О-01', 'СИБ-101-О-01', 'СПБ-101-О-01'],
          '2': ['СБС-001-О-01', 'СБС-002-О-01', 'СББ-001-О-01', 'СМБ-001-О-01', 'СИБ-001-О-01', 'СПБ-001-О-01'],
          '3': ['СБС-901-О-01', 'СББ-901-О-01', 'СМБ-901-О-01', 'СИБ-901-О-01', 'СПБ-901-О-01'],
          '4': ['СБС-801-О-01', 'СББ-801-О-01', 'СМБ-801-О-01', 'СИБ-801-О-01', 'СПБ-801-О-01'],
          '5': ['СБС-701-О-01']
          }


@bot.message_handler(commands=['start', 'schedule', 'feed', 'add_reminder'])
def menu(message):
    if message.text == '/start' or message.text == '/schedule':
        schedule(message)
    if message.text == '/feed':
        proxy_feed(message)
    if message.text == '/add_reminder':
        reminder(message)


def proxy_feed(message):
    news = feedparser.parse(
        'https://rssbridge.blyat.org/?action=display&bridge=Vk&u=fkn_news&hide_reposts=on&format=atom')
    for post in news.entries:
        bot.send_message(message.chat.id, post.link)


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
        for i in groups[year]:
            keyboard.add(telebot.types.KeyboardButton(i))
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


def reminder(message):
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
        bot.register_next_step_handler(msg, get_time)

    def groups_keyboard(year):
        keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        for i in groups[year]:
            keyboard.add(telebot.types.KeyboardButton(i))
        return keyboard

    def get_time(msg):
        group = msg.text
        msg = bot.send_message(message.chat.id, 'Время в формате hh:mm',
                               reply_markup=telebot.types.ReplyKeyboardRemove())
        bot.register_next_step_handler(msg, add_reminder, group)

    def add_reminder(msg, group):
        db.add_reminder(tg_id=message.chat.id, group=group, time=msg.text)
        bot.send_message(message.chat.id, 'Успешно')

    get_year()


if __name__ == '__main__':
    bot.infinity_polling()
