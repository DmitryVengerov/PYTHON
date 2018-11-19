# telegramm bot

import telebot
import datetime
import sys
import requests
import time
import webbrowser

from telebot import types
from bs4 import BeautifulSoup
# token gives you from botfather
access_token = '5'
bot = telebot.TeleBot(access_token)

def get_page(group, week=''):
    if week:
        week = str(week) + '/'

    url = '{domain}/{group}/{week}raspisanie_zanyatiy_{group}.htm'.format(
        domain="http://www.ifmo.ru/ru/schedule/0",
        week=week,
        group=group)
    print(url)
    response = requests.get(url)
    print(response.status_code)
    print(response.history)

    web_page = response.text
    web_page_len = len(web_page)
    if web_page_len <= 58286:
        web_page = 'error'
        print(web_page)
    return web_page

def get_schedule(web_page, day):
    schedule_table = ''
    soup = BeautifulSoup(web_page, "html5lib")
    try:
        if day == '/monday':
            schedule_table = soup.find("table", attrs={"id": "1day"})

        if day == '/tuesday':
            schedule_table = soup.find("table", attrs={"id": "2day"})

        if day == '/wednesday':
            schedule_table = soup.find("table", attrs={"id": "3day"})

        if day == '/thursday':
            schedule_table = soup.find("table", attrs={"id": "4day"})

        if day == '/friday':
            schedule_table = soup.find("table", attrs={"id": "5day"})

        if day == '/saturday':
            schedule_table = soup.find("table", attrs={"id": "6day"})


    # Время проведения занятий
        times_list = schedule_table.find_all("td", attrs={"class": "time"})
        times_list = [time.span.text for time in times_list]

    # Место проведения занятий
        locations_list = schedule_table.find_all("td", attrs={"class": "room"})
        locations_list = [room.span.text for room in locations_list]

    # Название дисциплин и имена преподавателей
        lessons_list = schedule_table.find_all("td", attrs={"class": "lesson"})
        lessons_list = [lesson.text.split('\n\n') for lesson in lessons_list]
        lessons_list = [', '.join([info for info in lesson_info if info]) for lesson_info in lessons_list]

    # Номер аудитории
        room_number = schedule_table.find_all("td", attrs={"class": "room"})
        room_number = [room.dd.text for room in room_number]
    except:
        times_list = ''
        locations_list = ''
        lessons_list = ''
        room_number = ''
    return times_list, locations_list, lessons_list, room_number

#@bot.message_handler(commands=['monday'])
#def get_monday(message):
#    _, group = message.text.split()
#    web_page = get_page(group)
#   times_lst, locations_lst, lessons_lst = get_schedule(web_page)
#    resp = ''
#    for time, location, lession in zip(times_lst, locations_lst, lessons_lst):
#        resp += '<b>{}</b>, {}, {}\n'.format(time, location, lession)

#    bot.send_message(message.chat.id, resp, parse_mode='HTML')

@bot.message_handler(commands=['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'all'])
def get_command(message, idd=''):
    if idd == '':
        idd = message.chat.id
    try:
        day, group, week = message.text.split()
    except:
        try:
            day, group = message.text.split()
            week = ''
        except:
            try:
                day, group, week = message.split()
            except:
                try:
                    day, group = message.split()
                    week = ''
                except:
                    return bot.send_message(idd, 'Error', parse_mode='HTML')


    web_page = get_page(group, week)
    resp = ''
    if day == '/all':
        get_command('/monday %(group)s %(week)s' % {"group": group, "week": week}, idd)
        get_command('/tuesday %(group)s %(week)s' % {"group": group, "week": week}, idd)
        get_command('/wednesday %(group)s %(week)s' % {"group": group, "week": week}, idd)
        get_command('/thursday %(group)s %(week)s' % {"group": group, "week": week}, idd)
        get_command('/friday %(group)s %(week)s' % {"group": group, "week": week}, idd)
        get_command('/saturday %(group)s %(week)s' % {"group": group, "week": week}, idd)
        return resp
    times_lst, locations_lst, lessons_lst, room_number = get_schedule(web_page, day)
    if times_lst or locations_lst or lessons_lst or room_number != '':
        for time, location, lession, room in zip(times_lst, locations_lst, lessons_lst, room_number):
            resp += '{}, <b>{}</b>, {}, {}, {}'.format(day, time, location, lession, room)
        resp = prettufy_mode(resp)
        bot.send_message(idd, resp, parse_mode='HTML')
    if web_page == 'error':
        bot.send_message(idd, "error", parse_mode='HTML')

@bot.message_handler(commands=['exit'])
def leave_now(message):
    bot.send_message(message.chat.id, 'We remember', parse_mode='HTML')
    print('exit')
    exit()

@bot.message_handler(commands=['tomorrow'])
def not_today(message):
    idd = message.chat.id
    _, group = message.text.split()
    now = datetime.datetime.now()
    ar = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']
    for i in range(5):
        if now.strftime("%A").lower() == ar[i]:
            get_command('/%(day)s %(group)s' % {"day": ar[i+1], "group": group}, idd)
        elif now.strftime("%A").lower() == 'saturday':
            get_command('/monday %(group)s' % {"group": group}, idd)
            break

@bot.message_handler(commands=['near_lesson'])
def not_today(message):
    idd = message.chat.id
    _, group = message.text.split()
    now = datetime.datetime.now()
    nowtime = datetime.datetime.time(datetime.datetime.now())
    nowtime = str(nowtime.hour)+':'+str(nowtime.minute)
    web_page = get_page(group, '')

    url = '{domain}/{group}/raspisanie_zanyatiy_{group}.htm'.format(
        domain="http://www.ifmo.ru/ru/schedule/0", group=group)
    response = requests.get(url)
    web_page = response.text
    soup = BeautifulSoup(web_page, "html.parser")
    weeknum = soup.find("h2", attrs={"class": "schedule-week"})
    weeknum = weeknum.get_text()

    if "Нечетная" in weeknum:
        week = 2
    else:
        week = 1

    day = '/'+now.strftime("%A").lower()
    web_page = get_page(group, week)
    times_lst, locations_lst, lessons_lst, room_number = get_schedule(web_page, day)

    ar = ['/monday', '/tuesday', '/wednesday', '/thursday', '/friday', '/saturday']
    for i in range(len(ar)):
        if day == ar[i]:
            dday = ar[0]

    for i in range(len(times_lst)):
        gg = str(times_lst[i])
        if nowtime < gg[0:gg.find('-')]:
            resp = str(times_lst[i]+" "+lessons_lst[i]+" "+locations_lst[i]+" "+room_number[i])
            break
        elif i == len(times_lst)-1:
            if day != '/saturday':
                times_lst, locations_lst, lessons_lst, room_number = get_schedule(web_page, dday)
                resp = str(times_lst[0]+" "+lessons_lst[0]+" "+locations_lst[0]+" "+room_number[0]+' tomorrow')
            else:
                times_lst, locations_lst, lessons_lst, room_number = get_schedule(web_page, "/monday")
                resp = str(times_lst[0]+" "+lessons_lst[0]+" "+locations_lst[0]+" "+room_number[0]+' monday')
    resp = prettufy_mode(resp)
    bot.send_message(idd, resp, parse_mode='HTML')

def prettufy_mode(resp):
        # delete all trush
        resp = resp.replace('\t', '')
        resp = resp.replace('\n', '')
            # make this better
        resp = resp.replace('./','.\n/')
        resp = resp.replace(', /','.\n/')
            # for kirrilic symbols
        resp = resp.replace('/monday,','<i>Понедельник</i>\n')
        resp = resp.replace('/tuesday,','<i>Вторник</i>\n')
        resp = resp.replace('/wednesday,','<i>Среда</i>\n')
        resp = resp.replace('/thursday,','<i>Четверг</i>\n')
        resp = resp.replace('/friday,','<i>Пятница-развратница</i>\n')
        resp = resp.replace('/saturday,','<i>Суббота</i>\n')
        print(len(resp))
        print(resp)
        return resp


if __name__ == '__main__':
   bot.polling(none_stop=True)
