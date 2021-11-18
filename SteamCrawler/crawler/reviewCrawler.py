import socket
import time
import urllib
import urllib.request
from contextlib import closing
from time import sleep
import re
from bs4 import BeautifulSoup
import datetime
import json
import string
import requests
import properties
from utils.redisUtis import RedisUtil


class ReviewCrawler:
    maxretries = 3
    timeout = 180
    pause = 0.5
    reviewList = None
    appid = None

    def __init__(self):
        pass

    def __init__(self, appid, maxretries=3, timeout=10, pause=0.5):
        self.maxretries = maxretries
        self.timeout = timeout
        self.pause = pause
        self.appid = str(appid)
        self.getReview()

    def sendGetRequset(self, url,param):
        tries = 0
        req = None
        while tries < self.maxretries and req is None:
            try:
                req = requests.get(url,params=param,timeout=self.timeout,headers=properties.headers)
                sleep(self.pause)
            except Exception as e:
                tries += 1
        time.sleep(self.pause * 2)
        return req

    def reviewExtrator(self, soup):
        helpfulre = re.compile(r'([0-9]+) [a-z]+? found this review helpful')
        funnyre = re.compile(r'([0-9]+) [a-z]+? found this review funny')
        ownedre = re.compile(r'([0-9]+) product')
        revre = re.compile(r'([0-9]+) review')
        timere = re.compile(r'([0-9.]+) hrs on record')
        postedre = re.compile(r'Posted: (.+)')
        yearre = re.compile(r'.* [0-9][0-9][0-9][0-9]$')
        userre = re.compile(r'/(profiles|id)/(.+?)/')
        resultList = []

        for reviewdiv in soup.findAll('div', attrs={'class': 'review_box'}):
            helpful = 0
            funny = 0
            elem = reviewdiv.find('div', attrs={'class': 'vote_info'})
            if elem:
                m = helpfulre.search(elem.text)
                if m:
                    helpful = m.group(1)
                m = funnyre.search(elem.text)
                if m:
                    funny = m.group(1)
            username = '__anon__'
            elem = reviewdiv.find('div', attrs={'class': 'persona_name'})
            if elem:
                m = elem.a
                if m:
                    username = m.text
            steamid = '_____'
            elem = (reviewdiv.find('div', attrs={'class': 'persona_name'}).a)
            if elem:
                useridre = re.compile('https://steamcommunity.com/(profiles|id)/(.*?)/')
                m = useridre.search(elem['href'])
                if m:
                    steamid = m.group(2)
            owned = 0
            elem = reviewdiv.find('div', attrs={'class': 'num_owned_games'})
            if elem:
                m = ownedre.search(elem.text)
                if m:
                    owned = m.group(1)
            numrev = 0
            elem = reviewdiv.find('div', attrs={'class': 'num_reviews'})
            if elem:
                m = revre.search(elem.text)
                if m:
                    numrev = m.group(1)
            recco = 0
            elem = reviewdiv.find('div', attrs={'class': 'title ellipsis'})
            if elem:
                if elem.text == 'Recommended':
                    recco = 1
                else:
                    recco = -1
            time = 0
            elem = reviewdiv.find('div', attrs={'class': 'hours ellipsis'})
            if elem:
                m = timere.search(elem.text)
                if m:
                    time = m.group(1)
            posted = 0
            elem = reviewdiv.find('div', attrs={'class': 'postedDate'})
            if elem:
                m = postedre.search(elem.text)
                if m:
                    posted = m.group(1).strip()
                    if not yearre.match(posted):
                        posted = posted + ", %s" % datetime.date.today().year
            content = ''
            elem = reviewdiv.find('div', attrs={'class': 'content'})
            if elem:
                content = elem.text.strip()
            resultList.append({"helpful": helpful,
                               "funny": funny,
                               "username": username,
                               "steamid": steamid,
                               "owned": owned,
                               "numrev": numrev,
                               "recco": recco,
                               "time": time,
                               "posted": posted,
                               "content": content})
        return resultList

    # get all review of the given game
    # params: appId->String-> game id
    # if request exist in database, it will return [] while check = True
    def requestReview(self, max_page=-1, check=True):
        if self.appid == None:
            return
        if self.reviewList != None and check == True:
            return []
        print("getting reviews of " + str(self.appid))
        base_url = "https://store.steampowered.com/appreviews/"+str(self.appid)
        param = {"cursor":"*","filter":"recent","language":"english"}
        endre = re.compile(r'no_more_reviews')
        page = 1
        maxError = 10
        errorCount = 0
        self.reviewList = None
        while True:
            response = self.sendGetRequset(base_url, param)

            if response is None:
                sleep(self.pause * 3)
                errorCount += 1
                if errorCount >= maxError:
                    print('Max error!')
                    break
            else:
                # requset_json = json.loads(request.text)
                # if requset_json['success'] != 1:
                #     break
                response_json = ''
                soup = None
                try:
                    response_json = json.loads(response.text)
                    if response_json['success'] != 1:
                        break
                    if endre.search(response_json['html']) != None:
                        break
                    soup = BeautifulSoup(response_json['html'], "html.parser")
                except ValueError:
                    print('error ')
                if soup == None:
                    break
                reviews = self.reviewExtrator(soup)

                if self.reviewList == None:
                    self.reviewList = reviews
                else:
                    self.reviewList.extend(reviews)
                page = page + 1
                param['cursor'] = response_json['cursor']
            if max_page >= 1 and page >= max_page:
                break
        print(self.reviewList)
        return self.reviewList

    def saveReview(self):
        if self.appid == '' or self.reviewList==None:
            return
        redisUtil = RedisUtil()
        try:
            redisUtil.setReviews(self.appid,self.reviewList)
        except Exception as e:
            print("save reviews of"+ self.appid+" error!")

    def getReview(self):
        if self.appid == None:
            return
        if self.reviewList != None:
            return self.reviewList
        redisUtil = RedisUtil()
        try:
            self.reviewList = redisUtil.getReviews(self.appid, self.reviewList)
        except Exception as e:
            print("get reviews of" + self.appid + " error!")
        return self.reviewList

# Test
if __name__ == '__main__':
    rc = ReviewCrawler()
    xs = rc.requestReview('1172470')
    print (xs)
    # sql = dbconnector()
    # sql.writeReviewList('1172470',xs)
    # print(xs)
    pass
