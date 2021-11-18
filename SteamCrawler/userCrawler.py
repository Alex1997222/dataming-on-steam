import requests
from bs4 import BeautifulSoup
import re
import properties

class user_crawler:
    def __init__(self):
        self.headers = properties.headers

    # 提取用户评论
    def getCommentList(self,comments):
        commentList = []
        for comment in comments:
            comment = re.sub('<(.*?)>', '', str(comment), 0)
            comment = comment.replace(r'\t', '').replace(r'\r', '').replace(r'\n', '')
            commentList.append(comment)
        return commentList

    #提取用户名
    def getpersonNamesList(self,personNames):
        nameList = []
        for name in personNames:
            name = re.sub('<(.*?)>', '', str(name), 0)
            nameList.append(name)
        return nameList

    #提取用户评论
    def gettimeAndRatesList(self,timeAndRates):
        timeList = []
        rateList = []
        for info in timeAndRates:
            rate = re.findall(r">(.*?)</div>", info)
            tim = re.findall(r"(\d.+)", info)
            rateList.extend(rate)
            timeList.extend(tim)
        return timeList,rateList

    #将用户信息,评论,评分等整合后返回
    def userInfoGet(self,id):
        url = 'https://store.steampowered.com/appreviews/'+str(id)
        nameList = []
        commentList = []
        timeList= []
        rateList = []
        try:
            response = requests.get(url, headers=properties.headers, timeout=10)
            soup = BeautifulSoup(response.text,'lxml')
            comments = soup.findAll(class_=r'\"content\"')
            personNames = soup.findAll(class_=r'\"persona_name\"')
            timeAndRates = re.findall(r"ellipsis(.*?) hrs",str(soup))

            nameList = self.getpersonNamesList(personNames)
            commentList = self.getCommentList(comments)
            timeList,rateList = self.gettimeAndRatesList(timeAndRates)
        except:
            pass

        return nameList,commentList,timeList,rateList


