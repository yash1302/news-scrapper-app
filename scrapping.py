import json
import bs4
import requests
import pandas as pd
import re
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import logging

title = []
heading = []
link = []
days = []
date=[]

class jsonInputData:

    logging.basicConfig(level=logging.DEBUG, filename='logs.log', format='%(asctime)s %(levelname)s:%(message)s')

    def __init__(self,config_file):
        self.config_file = config_file
    
    def read_config(self):
        with open(f"{self.config_file}","r") as file:
            jsonData = json.load(file)

        inputList = [[i,j,k] for i in jsonData['input'].get('company') for j in jsonData['input'].get('keywords') for k in range(0,jsonData['input'].get('TotalPages'))]

        # print(inputList)
        return inputList

    def yahoo(self): 
        # title = []
        # heading = []
        # link = []
        # days = []
        search_eng = []
        inputList = self.read_config()
        global title
        global heading
        global link
        global days

        try:
            for i,j,k in inputList:
            
                response = requests.get('https://in.news.search.yahoo.com/search;_ylt=AwrPrHDa8bFlRA4EagfAHAx.;_ylu=Y29sbwNzZzMEcG9zAzEEdnRpZAMEc2VjA3BhZ2luYXRpb24-?q={i}+{j}&b={k}1&pz=10&xargs=0')
                soup = bs4.BeautifulSoup(response.text, 'lxml')
            
                news = soup.find_all('div',attrs={'class':"dd NewsArticle"})

                for i in news:
                    title.append(i.find('h4', attrs={'class':'s-title fz-16 lh-20'}).text)
                    heading.append(i.find('span',attrs={'class':'s-source mr-5 cite-co'}).text)
                    days.append(i.find('span',attrs={'class':'fc-2nd s-time mr-8'}).text)
                    link.append(i.find('h4', class_={'s-title fz-16 lh-20'}).a['href'])
                print("hello")
        

        except:
            logging.error("Error has occured")
        
        return title,heading,days,link

    def google(self):
        search_eng = []
        inputList = self.read_config()
        global title
        global heading
        global link
        global days

        try:
            for i,j,k in inputList:
                result = requests.get(f"https://www.google.com/search?q='{i}'+'{j}'&sca_esv=600979061&rlz=1C1RXQR_enIN1092IN1092&tbm=nws&ei=v6uwZcfjKsOnvr0Pq5So4AQ&start={k}0&sa=N&ved=2ahUKEwiHv7fFsPWDAxXDk68BHSsKCkwQ8tMDegQIBBAE&biw=1318&bih=646&dpr=1")
                soup = bs4.BeautifulSoup(result.text,"lxml")

                news_1 = soup.find_all('div', attrs={'class':'Gx5Zad fP1Qef xpd EtOod pkphOe'})
                news_2 = soup.find_all('a', attrs={'class':'tHmfQe'})

                for i in news_1:
                    title.append(i.find('h3', attrs={'class':'zBAuLc l97dzf'}).text)
                    heading.append(i.find('div', attrs={'class':'BNeawe UPmit AP7Wnd lRVwie'}).text)
                    days.append(i.find('span', attrs={'class':'r0bn4c rQMQod'}).text)
                    link.append(i.a['href'])

                for i in news_2:
                    title.append(i.find('h3', attrs={'class':'zBAuLc l97dzf'}).text)
                    heading.append(i.find('span', attrs={'class':'rQMQod aJyiOc'}).text)
                    days.append(i.find('span', attrs={'class':'r0bn4c rQMQod'}).text)
                    link.append(i['href'])

        except:
            logging.error("Error has occured")
        
        return title,heading,days,link

    def bing(self):

    
        inputList = self.read_config()
        global title
        global heading
        global link
        global days
        
        try:
            for i,j,k in inputList:
                response = requests.get(f"https://www.bing.com/news/search?q={i}+{j}urlnews/infinitescrollajax?page={k}")
                soup = BeautifulSoup(response.text, 'lxml')
                        
                news = soup.find_all('div',attrs={'class':"caption"})

                

                for i in news:
                    title.append(i.find('a', attrs={'class':'title'}).text)
                    heading.append(i.find('div',attrs={'class':'source set_top'}).text)
                    days.append(i.find('span',attrs={'tabindex':'0'}).text)
                    link.append(i.find('a', class_='title').get('href'))
                    
        except :
            logging.error("Error has occured")

    def convert_to_date(self):
        global days
        global date

        for i in days:
            if 'hours' in i:
                j = int(re.search(r'\d+', i).group())
                date.append(str(datetime.now() - timedelta(hours= j)))
            elif 'days' in i:
                j = int(re.search(r'\d+', i).group())
                date.append(str(datetime.now() - timedelta(days= j)))
            elif 'month' or 'months' in i:
                j = int(re.search(r'\d+', i).group())
                date.append(str(datetime.now() - relativedelta(months= j)))
            elif 'year' or 'years' in i:
                j = int(re.search(r'\d+', i).group())
                date.append(str(datetime.now() - relativedelta(years= j)))

        return date



def main():
    a = jsonInputData("c:\\Users\\yashvardhan_Jadhav\\Desktop\\config.json")
    yahoo=a.yahoo()
    google = a.google()
    print(title)

     

if __name__ == "__main__":
    main()




