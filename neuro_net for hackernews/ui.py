from bottle import redirect, route, run, template, request, post 
from db import *
from init import *

@route('/')
@route('/news')
def news_list():
    rows = s.query(News).filter(News.label == None).all()
    return template('news_template', rows=rows)

@route('/add_label/')

def add_label():
    # 1. Получить значения параметров label и id из GET-запроса + 
    label = request.query.get("label")
    id = request.query.get("id")
    # 2. Получить запись из БД с соответствующим id (такая запись только одна!) 
    return "{label} {id}".format(label=label, id=id)
    
    
    # 3. Изменить значение метки записи на значение label
    # 4. Сохранить результат в БД
    redirect('/news')

@route('/update_news')
def update_news():
    get_news('https://news.ycombinator.com/newest',1)
    # 1. Получить данные с новостного сайта
    # 2. Проверить, каких новостей еще нет в БД. Будем считать,
    #    что каждая новость может быть уникально идентифицирована
    #    по совокупности двух значений: заголовка и автора
    # 3. Сохранить в БД те новости, которых там нет
    redirect('/news')

