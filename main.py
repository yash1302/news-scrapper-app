# import necessary libraries
import requests
import bs4
import json
import pandas as pd
import re
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import logging

logging.basicConfig(level=logging.DEBUG, filename='logs.log', format='%(asctime)s %(levelname)s:%(message)s')

# json file reading
with open("C:\\Users\\yashvardhan_Jadhav\\Desktop\\config.json","r") as file:
    jsonData = json.load(file)

# list created for taking input from json files
companies= []
services = []
page_no = []

# fetching info from json file and adding in list
for infos in jsonData:
    companies.append(jsonData[infos].get("company"))
    services.append(jsonData[infos].get("keyword"))
    page_no.append(jsonData[infos].get("PageNo"))

# all the list are converted into single list for easy traversal
mixedList = [[i,j,k] for i in companies
                     for j in services
                     for k in range(0,page_no[0])]

# for scrapping news from google
def google():
# list for saving information from google 
    link = []
    title = []
    heading3 = []
    days = []
    # try block if code runs other wise in except block
    try:
        for i,j,k in mixedList:
            # result string formatted to search for each company and keyword and for page numbers
            result = requests.get(f"https://www.google.com/search?q='{i}'+'{j}'&sca_esv=600979061&rlz=1C1RXQR_enIN1092IN1092&tbm=nws&ei=v6uwZcfjKsOnvr0Pq5So4AQ&start={k}0&sa=N&ved=2ahUKEwiHv7fFsPWDAxXDk68BHSsKCkwQ8tMDegQIBBAE&biw=1318&bih=646&dpr=1")

            # converted into beautiful format
            soup = bs4.BeautifulSoup(result.text,"lxml")

                # block(news which comes in three news together) title
            for item in soup.find_all('span',attrs={'class':'rQMQod Xb5VRe'}):
                title.append(item.text)
                logging.debug(f"{len(title)} Titles has been appended")

                    # blog(seprate news) title
            for item in soup.find_all('div',attrs={'class':'BNeawe vvjwJb AP7Wnd'}):
                title.append(item.text)
                logging.debug(f"{len(title)} Titles has been appended")
                    # block heading
            for item in soup.find_all('span',attrs={'class':'rQMQod aJyiOc'}):
                heading3.append(item.text)
                logging.debug(f"{len(heading3)} Headings has been appended")
                        # print(item.text)
                    # block days
            for item in soup.find_all('span',attrs={'class':'r0bn4c rQMQod'}):
                days.append(item.text)
                logging.debug(f"{len(days)} Days has been appended")
                        # print(item.text)
                    # links
            for i in soup.select('div>a'):
                if i.text.endswith('ago'):
                            # print(i.get('href'))
                    link.append(i.get('href'))
                    logging.debug(f"{len(link)} Links has been appended")
                            # print(i.get('href'))
                    # blog heading
            for item in soup.find_all('div',attrs={'class':'BNeawe UPmit AP7Wnd lRVwie'}):
                heading3.append(item.text)
                logging.debug(f"{len(heading3)} Headings has been appended")
                        # print(item.text)
                    # blog days
            for item in soup.find_all('div',attrs={'span':'r0bn4c rQMQod'}):
                heading3.append(item.text)
                logging.debug(f"{len(heading3)} Headings has been appended")
                        # print(item.text)
                # search_eng list is to store from which we have searched the url
            search_eng = []

            for i in range(0,len(days)):
                search_eng.append("google")
                logging.debug(f"{len(search_eng)} Search Engines has been appended")
            # print("hello")
                
    except:
        logging.error("Error occured")

    return link,title,heading3,days,search_eng

# to scrape from news
def bing():
    # list to store news information
    link = []
    title = []
    heading4 = []
    days1 = []
    search_eng = []

    try:
        for i,j,k in mixedList:
            result = requests.get(f"https://www.bing.com/news/search?q={i}+{j}urlnews/infinitescrollajax?page={k}")

            soup = bs4.BeautifulSoup(result.text,"lxml")

            # block heading
            for i in soup.find_all("div", {"class": "source set_top"}):
                for anch in i.find_all('a'):
                    heading4.append(anch.text)
                    logging.debug(f"{len(heading4)} Headings has been appended")   
                    
            # # blof title
            for item in soup.find_all('a',attrs={'class':'title'}):
                title.append(item.text)
                logging.debug(f"{len(title)} Titles has been appended")
            # # block days
            for i in soup.find_all("div", {"class": "source set_top"}):
                for anch in i.find_all('span'):
                    days1.append(anch.text) 
                    logging.debug(f"{len(days1)} Days has been appended") 
            # # links
            for i in soup.find_all("a", {"class": "title"}):
                link.append(i.get('href'))
                logging.debug(f"{len(link)} Link has been appended")
            while("" in days1):
                days1.remove("")
            for i in range(0,len(days1)):
                search_eng.append("bing")
                logging.debug(f"{len(search_eng)} Search Engines has been appended")
            print("hello")

    except:
        logging.error("Error has occured")

    return link,title,heading4,days1,search_eng

def yahoo():
    # list to store news information
    title = []
    heading = []
    link = []
    days = []
    search_eng = []

    try:
        for i,j,k in mixedList:
        
            response = requests.get('https://in.news.search.yahoo.com/search;_ylt=AwrPrHDa8bFlRA4EagfAHAx.;_ylu=Y29sbwNzZzMEcG9zAzEEdnRpZAMEc2VjA3BhZ2luYXRpb24-?q={i}+{j}&b={k}1&pz=10&xargs=0')
            soup = bs4.BeautifulSoup(response.text, 'lxml')
        
            # this is for title
            for item in soup.find_all('h4',attrs={'class':'s-title fz-16 lh-20'}):
                title.append(item.text)
                logging.debug(f"{len(title)} Titles has been appended")
            for item in soup.find_all('span',attrs={'class':'s-source mr-5 cite-co'}):
                heading.append(item.text)
                logging.debug(f"{len(heading)} Headings has been appended")
            for item in soup.find_all('span',attrs={'class':'fc-2nd s-time mr-8'}):
                days.append(item.text)
                logging.debug(f"{len(days)} Days has been appended")
            for i in soup.find_all('h4', class_='s-title fz-16 lh-20'):
                link.append(i.a['href'])
                logging.debug(f"{len(link)} Links has been appended")
            for i in range(0,len(days)):
                search_eng.append("yahoo")
                logging.debug(f"{len(search_eng)} Search Engines has been appended")
            print("hello")

    except:
        logging.error("Error has occured")

    return title,heading,link,days,search_eng


# calling each function and storing them in variables
linkg,titleg,heading3g,daysg,search_engg = google()
linkb,titleb,heading4b,days1b,search_engb = bing()
titley,headingy,linky,daysy,search_engy = yahoo()


# creating final list which stores information
finalListTitle = []
finalListHeading = []
finalListDays = []
finalListLink = []
finalListEngine = []

# appending into final products from google
for i in range(len(linkg)):
    finalListLink.append(linkg[i])
    finalListTitle.append(titleg[i])
    finalListHeading.append(heading3g[i])
    finalListDays.append(daysg[i])
    finalListEngine.append(search_engg[i])


# appending into final products from bing
for i in range(len(linkb)):
    finalListLink.append(linkb[i])
    finalListTitle.append(titleb[i])
    finalListHeading.append(heading4b[i])
    finalListDays.append(days1b[i])
    finalListEngine.append(search_engb[i])


# appending into final products from yahoo
for i in range(len(linky)):
    finalListLink.append(linky[i])
    finalListTitle.append(titley[i])
    finalListHeading.append(headingy[i])
    finalListDays.append(daysy[i])
    finalListEngine.append(search_engy[i])

# converting days into date
for i in finalListDays:
    print(i)
# for i in finalListDays:
#     if 'hours' in i:
#         j = int(re.search(r'\d+', i).group())
#         finalListDate.append(str(datetime.now() - timedelta(hours= j)))
#     elif 'days' in i:
#         j = int(re.search(r'\d+', i).group())
#         finalListDate.append(str(datetime.now() - timedelta(days= j)))
#     elif 'month' or 'months' in i:
#         j = int(re.search(r'\d+', i).group())
#         finalListDate.append(str(datetime.now() - relativedelta(months= j)))
#     elif 'year' or 'years' in i:
#         j = int(re.search(r'\d+', i).group())
#         finalListDate.append(str(datetime.now() - relativedelta(years= j)))
# logging.debug(f"{len(finalListDate)} Dates has been appended")


# # entering into dataframes
# df = pd.DataFrame(list(zip(finalListTitle, finalListLink, finalListDate, finalListHeading,finalListEngine)), columns=['Title','Link', 'Date', 'Heading','Search Engine'])
# logging.info("DataFrame has been created")

# # making csv files
# df.to_csv('output.csv', sep = ',')
# logging.info("Output file has been created")
