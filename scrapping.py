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
    

def main():
    a = jsonInputData("c:\\Users\\yashvardhan_Jadhav\\Desktop\\config.json")
    yahoo=a.yahoo()
    print(title)
    print(heading)
    print(days)
    print(link)

     

if __name__ == "__main__":
    main()




