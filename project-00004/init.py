import requests
from ui import *
from db import *
from bs4 import BeautifulSoup

news_list = []
data = {}

def get_data(url='https://news.ycombinator.com/newest'):
    # dump all datas from page
    print('Parsing from ' + url)
    r = requests.get(url)
    page = BeautifulSoup(r.text, 'html.parser')
    tbl_list = page.table.find('table', {'class': 'itemlist'})
    storyTitle = tbl_list.findAll('a', {'class': 'storylink'})
    storyAuthor = tbl_list.findAll('a', {'class': 'hnuser'})
    storyPoints = tbl_list.findAll('span', {'class': 'score'})
    storyComments = tbl_list.findAll('td', {'class': 'subtext'})
    # for changes next url 
    get_link(url)
    for i in range(len(storyTitle)):
        tempCom = storyComments[i].findAll('a')
        tempCom = tempCom[len(tempCom)-1].text
        if(tempCom == 'discuss'):
            tempCom = int(0)
        else:
            tempCom = int(tempCom.replace(u'\xa0', ' ').split(' ')[0])
        tempPoi = storyPoints[i].text
        tempPoi = int(tempPoi.replace('&nbsp;', '').split(' ')[0])
        data['author'] = storyAuthor[i].text
        data['comments'] = tempCom
        data['points'] = tempPoi
        data['title'] = storyTitle[i].text
        data['url'] = storyTitle[i].get('href')

        news_list.append({
            'author': data['author'],
            'comments': data['comments'],
            'points': data['points'],
            'title': data['title'],
            'url': data['url']
        })
    return news_list


def get_link(url):
    global url_global
    #cath others pages
    r = requests.get(url)
    page = BeautifulSoup(r.text, 'html.parser')
    tbl_list = page.table.find('table', {'class': 'itemlist'})
    moreLink = tbl_list.findAll('a', {'class': 'morelink'})
    url_global = url[:35]+moreLink[0].get('href').replace('newest', '')


def get_news(url, pages=1):
    data = []
    for i in range(pages):
        if(i==0):
            news_list.append(get_data(url))
        else:
            news_list.append(get_data(url_global))
    #fail - kill recursion in the last at the end of list data
    del news_list[len(news_list)-1]
    print('Was received ',len(news_list),' elements')
    
    for i in range(len(news_list)):
        #form data for querry 
        news = News(title = news_list[i]['title'], 
                author = news_list[i]['author'],
                url = news_list[i]['url'],
                comments = news_list[i]['comments'],
                points = news_list[i]['points'])
        #add changes in querry
        s.add(news)
        #commit changes
        s.commit()
    
    return news_list
    
if __name__ == '__main__':
    run(host='localhost', port=8888)

