import db
from datetime import datetime

week = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота']


def launch(bot):
    hour = datetime.today().hour
    minute = datetime.today().minute
    updated = True
    while True:
        if hour != datetime.today().hour or minute != datetime.today().minute:
            hour = datetime.today().hour
            minute = datetime.today().minute
            updated = True

        if updated is True:
            for users in db.get_all_reminders():
                if int(users[2].split(':')[0]) == hour and int(users[2].split(':')[1]) == minute:
                    bot.send_message(users[0], 'Расписание на сегодня:\n\n' + db.get_lessons(group=users[1], day=week[
                        datetime.today().weekday()]))
            updated = False
