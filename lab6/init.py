import requests
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
    # cath others pages
    r = requests.get(url)
    page = BeautifulSoup(r.text, 'html.parser')
    tbl_list = page.table.find('table', {'class': 'itemlist'})
    moreLink = tbl_list.findAll('a', {'class': 'morelink'})
    nextPage = url[:35]+moreLink[0].get('href').replace('newest', '')

    return nextPage


def get_news(url, pages=1):
    # controller for requesting
    '''
    
    if(pages == 1):
        data = get_data(url)
    else:'''
    i = 1
    while i <= pages:
        get_data(url)
        get_data(get_link(url))
        get_data(get_link(get_link(url)))
        i += 1
            
    # return data


if __name__ == '__main__':
    get_news('https://news.ycombinator.com/newest', 3)
