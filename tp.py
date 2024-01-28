import requests
import bs4 
import json
import logging
import re
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import pandas as pd

# title = []
# heading = []
# link = []
# days = []
# date=[]



class scrapper:
    title = []
    heading = []
    link = []
    days = []
    date=[]
    logging.basicConfig(level=logging.DEBUG, filename='logs.log', format='%(asctime)s %(levelname)s:%(message)s')

    def __init__(self,config_file):
        self.config_file = config_file


    def read_config(self):
        with open(f"{self.config_file}","r") as file:
            jsonData = json.load(file)

        inputList = [[i,j,k] for i in jsonData['input'].get('company') for j in jsonData['input'].get('keywords') for k in range(0,jsonData['input'].get('TotalPages'))]

        return inputList 

    def bing(self):

    
        inputList = self.read_config()
        # global title
        # global heading
        # global link
        # global days
        
        try:
            for i,j,k in inputList:
                response = requests.get(f"https://www.bing.com/news/search?q='{i}'+'{j}'urlnews/infinitescrollajax?page={k}")
                soup = bs4.BeautifulSoup(response.text, 'lxml')
                        
                news = soup.find_all('div',attrs={'class':"caption"})

                

                for i in news:
                    self.title.append(i.find('a', attrs={'class':'title'}).text)
                    self.heading.append(i.find('div',attrs={'class':'source set_top'}).text)
                    self.days.append(i.find('span',attrs={'tabindex':'0'}).text)
                    self.link.append(i.find('a', class_='title').get('href'))
                print("bing")
        except :
            logging.error("Error has occured")

    def convert_to_date(self):
        # global days
        # global date

        for i in self.days:
            if 'hours' in i:
                j = int(re.search(r'\d+', i).group())
                self.date.append(str(datetime.now() - timedelta(hours= j)))
            elif 'days' in i:
                j = int(re.search(r'\d+', i).group())
                self.date.append(str(datetime.now() - timedelta(days= j)))
            elif 'month' or 'months' in i:
                j = int(re.search(r'\d+', i).group())
                self.date.append(str(datetime.now() - relativedelta(months= j)))
            elif 'year' or 'years' in i:
                j = int(re.search(r'\d+', i).group())
                self.date.append(str(datetime.now() - relativedelta(years= j)))

        return self.date
    

    def dataframe(self):
        date = self.convert_to_date()

        df = pd.DataFrame(list(zip(self.title, self.heading, self.link, date)), columns=[ 'Title', 'Heading', 'Link', 'Date'])
        df.to_csv('yash1.csv')
        print(df.head())

        # return df
        

 
def main():
    scrapping = scrapper("c:\\Users\\yashvardhan_Jadhav\\Desktop\\config.json")
    # scrapping.google()
    scrapping.bing()
    scrapping.dataframe()





    # print((len(scrapping.title)))
    # print((len(scrapping.heading)))
    # print((len(scrapping.link)))
    # print((len(scrapping.days)))

     
    # scrapping.read_config()
    # print(yahoo)


if __name__ == "__main__":
    main()

