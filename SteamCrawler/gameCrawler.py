import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import properties
from utils.sqlUtils import dbconnector
from userCrawler import user_crawler
import socket
import urllib
import urllib.request
from contextlib import closing
from time import sleep


class GameCrawler:
    def __init__(self):
        self.headers = properties.headers
        self.game_conn = dbconnector()
    #get game's name
    def getGameName(self,soup):
        try:
            name = soup.find(class_="apphub_AppName")
            name = str(name.string)
        except:
            name = soup.find(class_="apphub_AppName")
            name = str(name.text)
        return name

    def getGamePrice(self,soup):
        try:
            price = soup.findAll(class_="discount_original_price")
            for i in price:
                if re.search('¥|free|免费', str(i), re.IGNORECASE):
                    price = i
            price = str(price.string).replace('	', '').replace('\n', '').replace('\r', '').replace(' ', '')
            price = price.replace('¥','')
        except:
            price = soup.findAll(class_="game_purchase_price price")
            for i in price:
                if re.search('¥|free|免费', str(i), re.IGNORECASE):
                    price = i
            price = str(price.string).replace('	', '').replace('\n', '').replace('\r', '').replace(' ', '')
            price = price.replace('¥', '')
        return int(price)

    #get game's label
    def getNameLabel(self,soup):
        label_list = []
        tag = soup.find_all(class_="app_tag")
        for i in tag:
            label = str(i.string).replace('	', '').replace('\n', '').replace('\r', '')
            if label == '+':
                pass
            else:
                label_list.append(label)
        label_list = str(','.join(label_list))
        return label_list

    #get game's decription
    def getGameDescription(self,soup):
        description = soup.find(class_="game_description_snippet")
        description = str(description.string).replace('	', '').replace('\n', '').replace('\r', '')
        return description

    #get game's rate
    def getGameEvaluate(self,soup):
        eva = soup.find(class_="summary column")
        try:
            eva = str(eva.span.string)
        except:
            eva = str(eva.text)
        return eva

    #Get game's information and save the data to dataset
    def infoSave(self,id,link):
        try:
            response = requests.get(link, headers=properties.headers, timeout=10)
        except:
            print('server no response')
        try:
            soup = BeautifulSoup(response.text, 'lxml')
            name = self.getGameName(soup)
            price = self.getGamePrice(soup)
            label = self.getNameLabel(soup)
            description = self.getGameDescription(soup)
            GameEvaluate = self.getGameEvaluate(soup)
            # print(name)
            self.game_conn.writeGameInfo(id,name,price,label,description,GameEvaluate)
            print('save success!')
        except Exception as e:
            print('info save failed!')   #Rated R Games need to crawl by another method, currently, we save the game in the database
            self.game_conn.WriteLimitedGameInfo(id,link)

            #get user information and comment of the game
        usercrawer = user_crawler()
        nameList,commentList,timeList,rateList = usercrawer.userInfoGet(id)
        for name,comment,tim,rate in zip(nameList,commentList,timeList,rateList):
            self.game_conn.WriteUserTable(name,id,comment,tim,rate)

    def download_page(self, url, maxretries, timeout, pause):
        tries = 0
        htmlpage = None
        while tries < maxretries and htmlpage is None:
            try:
                with closing(urllib.request.urlopen(url, timeout=timeout)) as f:
                    htmlpage = f.read()
                    sleep(pause)
            except (urllib.error.URLError, socket.timeout, socket.error):
                tries += 1
        return htmlpage






















