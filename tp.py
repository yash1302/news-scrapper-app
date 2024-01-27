# mb-15 reg searchCenterMiddle

import json
import bs4
import requests

title = []
# heading = []
# link = []
# days = []

response = requests.get('https://in.news.search.yahoo.com/search;_ylt=AwrPrHDa8bFlRA4EagfAHAx.;_ylu=Y29sbwNzZzMEcG9zAzEEdnRpZAMEc2VjA3BhZ2luYXRpb24-?q=microsoft+AI&b=01&pz=10&xargs=0')
soup = bs4.BeautifulSoup(response.text, 'lxml')

# print(soup)

class tp:

    def appendNews():
        global title
        news = soup.find_all('div',attrs={'class':"dd NewsArticle"})
        for i in news:
            title.append(i.find('h4', attrs={'class':'s-title fz-16 lh-20'}).text)
            # heading.append(i.find('span',attrs={'class':'s-source mr-5 cite-co'}).text)
            # days.append(i.find('span',attrs={'class':'fc-2nd s-time mr-8'}).text)
            # link.append(i.find('h4', class_='s-title fz-16 lh-20').a['href'])

    appendNews()
    print(title)

# for i in link:
#     print(i)

    
