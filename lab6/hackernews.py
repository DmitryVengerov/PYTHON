import requests
import re
from bs4 import BeautifulSoup



'''
Example json 
{'author': 'evo_9',
  'comments': 0,
  'points': 1,
  'title': 'Daily Action – Sign Up to Join the Resistance',
  'url': 'https://dailyaction.org/'}

'''


def get_news(url='https://news.ycombinator.com/newest'):

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
    	tempPoi = storyPoints[i].text
    	
    	#tempPoi = re.findall('(\d+)',tempPoi)
    	print(
    		"name: " + 
    		storyTitle[i].text + 
    		"\nauthor: " +
    		storyAuthor[i].text +
    		"\nlikes: " +
			tempPoi +
    		"\ncomments: " +
    		tempCom +
    		"\n"
    		)
	


if __name__ == '__main__':
    get_news()
