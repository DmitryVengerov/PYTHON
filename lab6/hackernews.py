import requests
from bs4 import BeautifulSoup

news_list = []
data = {}

def get_news(url='https://news.ycombinator.com/newest', pageCount=1):
    r = requests.get(url)
    page = BeautifulSoup(r.text, 'html.parser')
    tbl_list = page.table.find('table', {'class': 'itemlist'})
    storyTitle = tbl_list.findAll('a', {'class': 'storylink'})
    storyAuthor = tbl_list.findAll('a', {'class': 'hnuser'})
    storyPoints = tbl_list.findAll('span', {'class': 'score'})
    storyComments = tbl_list.findAll('td', {'class': 'subtext'})

    # catch get url for other pages
    moreLink = tbl_list.findAll('a', {'class': 'morelink'})
    nextPage = url+moreLink[0].get('href').replace('newest', '') 

    print(nextPage)

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

def next_page(url,page):
    return url

if __name__ == '__main__':
    print(get_news())
    #print(get_news('https://news.ycombinator.com/newest?next=16513818&n=31'))
    #print(get_news('https://news.ycombinator.com/newest?next=16513229&n=61'))

    
