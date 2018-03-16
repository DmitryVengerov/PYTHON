import requests
import ui
from  db  import *
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
    # cath others pages
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
    len_news = len(news_list)
    print('Was received ',len_news,' elements')
    news = News(title='Lab 7', 
                author='dementiy',
                url='https://dementiy.gitbooks.io/-python/content/lab7.html',
                comments=0,
                points=0)

    s.add_all(news)
    s.comit()
    
    return news_list
    
if __name__ == '__main__':
    get_news('https://news.ycombinator.com/newest',2)
    

