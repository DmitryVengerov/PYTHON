import requests
import re
from bs4 import BeautifulSoup




def get_news(url='https://news.ycombinator.com/newest'):

    news_list = []
    data = {}
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
        tempPoi = int(tempPoi.replace('&nbsp;','').split(' ')[0])
        
        data['author'] = storyAuthor[i].text
        data['comments'] = tempCom
        data['points'] = tempPoi
        data['title'] = storyTitle[i].text
        data['url'] = storyTitle[i].get('href')

        news_list.append({

            'author':data['author'],
            'comments':data['comments'],
            'points':data['points'],
            'title':data['title'],
            'url':data['url']

            })
    print(news_list[:3])
    


if __name__ == '__main__':
    get_news()
