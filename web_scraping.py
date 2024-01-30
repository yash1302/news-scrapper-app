import json
import bs4
import requests
import pandas as pd
import re
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import logging
import threading
import time
from urllib.request import HTTPError

class jsonInputData:
    title = []
    heading = []
    link = []
    days = []
    date = []
    search_eng = []
    search_string = []

     # Create log file
    logging.basicConfig(level=logging.DEBUG, filename='logs.log', format='%(asctime)s %(levelname)s:%(message)s') 

    def __init__(self,config_file):
        self.config_file = config_file
        # Logs added to logs.log file
        logging.info("Start of program execution") 
    
# Reads input from json file and gives inputList as output
    def read_config(self):
        with open(f"{self.config_file}","r") as file:
            jsonData = json.load(file)

        inputList = [[i,j,k] for i in jsonData['input'].get('company') for j in jsonData['input'].get('keywords') for k in range(0, jsonData['input'].get('TotalPages'))]

        # Logs added to logs.log file
        logging.debug("Input list created")

        search_engines = []
        search_engines.append(jsonData['search_engines'].get('google'))
        search_engines.append(jsonData['search_engines'].get('yahoo'))
        search_engines.append(jsonData['search_engines'].get('bing'))


        return inputList, search_engines

# Take input from inputList and config file for formatting the url of Yahoo Search Engine
# Title, media, date, link, search engine name, search string is scraped
# and stored to lists defined in the class
    def yahoo(self): 
        inputList, search_engines = self.read_config()

        try:
            for company,keyword,pageno in inputList:
                input_search_string =f'{company} and {keyword}'
                # Get information related to the news based on company and keywords
                response = requests.get(f"{search_engines[1]}{company}+{keyword}&b={pageno}1&pz=10&xargs=0") 
                soup = bs4.BeautifulSoup(response.text, 'lxml')
            
                news = soup.find_all('div',attrs={'class':"dd NewsArticle"})

                for i in news:
                    self.title.append(i.find('h4', attrs={'class':'s-title fz-16 lh-20'}).text) 
                    self.heading.append(i.find('span',attrs={'class':'s-source mr-5 cite-co'}).text) 
                    self.days.append(i.find('span',attrs={'class':'fc-2nd s-time mr-8'}).text) 
                    self.link.append(i.find('h4', class_={'s-title fz-16 lh-20'}).a['href']) 
                    self.search_eng.append('Yahoo') 
                    self.search_string.append(input_search_string) 
                
                # Logs added to logs.log file
                logging.debug("Data has been scraped in stored in list") 
                print("Yahoo")
            return self.title, self.heading, self.days, self.link, self.search_eng, self.search_string

        except HTTPError as he:
            #print(he)
            logging.error(f"{he} Error has occured")

        except ConnectionError as ce:
            #print(ce)
            logging.error(f"{ce} Error has occured")

        except Exception as e:
            #print(e)
            logging.error("Error has occured")

# Take input from inputList and config file for formatting the url of Google Search Engine
# Title, media, date, link, search engine name, search string is scraped
# and stored to lists defined in the class
    def google(self):
        inputList, search_engines = self.read_config()

        try:
            for company,keyword,pageno in inputList:
                input_search_string =f'{company} and {keyword}'
                # Get information related to the news based on company and keywords
                result = requests.get(f"{search_engines[0]}{company}+{keyword}&tbm=nws&start={pageno}0") 
                soup = bs4.BeautifulSoup(result.text,"lxml")

                news_1 = soup.find_all('div', attrs={'class':'Gx5Zad fP1Qef xpd EtOod pkphOe'})
                news_2 = soup.find_all('a', attrs={'class':'tHmfQe'})

                for i in news_1:
                    self.title.append(i.find('h3', attrs={'class':'zBAuLc l97dzf'}).text) 
                    self.heading.append(i.find('div', attrs={'class':'BNeawe UPmit AP7Wnd lRVwie'}).text) 
                    self.days.append(i.find('span', attrs={'class':'r0bn4c rQMQod'}).text) 
                    self.link.append(i.a['href']) 
                    self.search_eng.append('Google') 
                    self.search_string.append(input_search_string) 

                for i in news_2:
                    self.title.append(i.find('h3', attrs={'class':'zBAuLc l97dzf'}).text) 
                    self.heading.append(i.find('span', attrs={'class':'rQMQod aJyiOc'}).text) 
                    self.days.append(i.find('span', attrs={'class':'r0bn4c rQMQod'}).text) 
                    self.link.append(i['href']) 
                    self.search_eng.append('Google') 
                    self.search_string.append(input_search_string)

                # Logs added to logs.log file 
                logging.debug("Data has been scraped in stored in list")   
                print("google")
            return self.title, self.heading, self.days, self.link, self.search_eng, self.search_string
        
        except HTTPError as he:
            #print(he)
            logging.error(f"{he} Error has occured")

        except ConnectionError as ce:
            #print(ce)
            logging.error(f"{ce} Error has occured")

        except Exception as e:
            #print(e)
            logging.error("Error has occured")
        
# Take input from inputList and config file for formatting the url of Bing Search Engine
# Title, media, date, link, search engine name, search string is scraped
# and stored to lists defined in the class
    def bing(self):
        inputList, search_engines = self.read_config()

        try:
            for company,keyword,pageno in inputList:
                input_search_string =f'{company} and {keyword}'
                 # Get information related to the news based on company and keywords
                response = requests.get(f"{search_engines[2]}{company}+{keyword}urlnews/infinitescrollajax?page={pageno}")
                soup = bs4.BeautifulSoup(response.text, 'lxml')
                        
                news = soup.find_all('div',attrs={'class':"caption"})

                for i in news:
                    self.title.append(i.find('a', attrs={'class':'title'}).text) 
                    self.heading.append(i.find('div',attrs={'class':'source set_top'}).text) 
                    self.days.append(i.find('span',attrs={'tabindex':'0'}).text) 
                    self.link.append(i.find('a', class_='title').get('href')) 
                    self.search_eng.append('Bing') 
                    self.search_string.append(input_search_string)

                # Logs added to logs.log file
                logging.debug("Data has been scraped and stored in list") 
                print("Bing")
            return self.title, self.heading, self.days, self.link, self.search_eng, self.search_string

        except HTTPError as he:
            #print(he)
            logging.error(f"{he} Error has occured")

        except ConnectionError as ce:
            #print(ce)
            logging.error(f"{ce} Error has occured")

        except Exception as e:
            #print(e)
            logging.error("Error has occured")



    # Convert days list containing information about which hour/day/month/year article was published into datetime
    def convert_to_date(self): 

        for i in self.days:
            if 'mins' in i or 'min' in i or 'm' in i:
                j = int(re.search(r'\d+', i).group())
                self.date.append(str(datetime.now() - timedelta(minutes= j)))
            elif 'hours' in i or 'hour' in i or 'h' in i:
                j = int(re.search(r'\d+', i).group())
                self.date.append(str(datetime.now() - timedelta(hours= j)))
            elif 'days' in i or 'day' in i or 'd' in i:
                j = int(re.search(r'\d+', i).group())
                self.date.append(str(datetime.now() - timedelta(days= j)))
            elif 'month' in i or 'months' in i or 'mon' in i:
                j = int(re.search(r'\d+', i).group())
                self.date.append(str(datetime.now() - relativedelta(months= j)))
            elif 'year' in i or 'years' in i or 'y' in i:
                j = int(re.search(r'\d+', i).group())
                self.date.append(str(datetime.now() - relativedelta(years= j)))
        # Logs added to logs.log file
        logging.debug("Date conversion has been implemented successfully") 

        return self.date

    # Create dataframe and export it to csv file
    # Dataframe containing search_string, title, heading, link, date, search_eng is created
    def dataframe(self): 
        self.date = self.convert_to_date()

        df = pd.DataFrame(list(zip(self.search_string, self.title, self.heading, self.link, self.date, self.search_eng)), columns=['Search String', 'Title', 'Media', 'Link', 'Date', 'Search Engine'])
        df.to_csv('main.csv')
        print(df.head())
        # Logs added to logs.log file
        logging.debug("Dataframe created and exported to csv")

        return df

# Call the methods of class here
# Multithreading is implemented to reduce time required for implementation
def main(): 
    scrapping = jsonInputData("c:\\Users\\yashvardhan_Jadhav\\Desktop\\config.json")

    p1 = threading.Thread(target=scrapping.yahoo)
    p2 = threading.Thread(target=scrapping.google)
    p3 = threading.Thread(target=scrapping.bing)
    p1.start()
    p2.start()
    p3.start()
    p1.join()
    p2.join()
    p3.join()
    scrapping.dataframe()

if __name__ == "__main__":
    time_start = time.time()
    main()
    time_end = time.time()
    print(f"Time difference: {time_end - time_start}")
