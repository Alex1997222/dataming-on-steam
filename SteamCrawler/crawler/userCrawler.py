import time

import requests
import json
import properties
from utils.redisUtis import RedisUtil
from time import sleep


class UserCrawler:
    _maxretries = 3
    _timeout = 180
    _pause = 0.5
    _key = properties.apikey
    steamid = None
    friendList = None
    ownedGameList = None

    def __init__(self):
        pass

    def __init__(self, steamid, maxretries=3, timeout=10,pause=0.5):
        self._maxretries = maxretries
        self._timeout = timeout
        self._pause = pause
        self.steamid = steamid
        self.getFriendList()
        self.getOwnedGames()

    def sendGetRequest(self, url, param):
        re = None
        tries = 0
        while tries < self._maxretries:
            try:
                re = requests.get(url, params=param, timeout=self._timeout)
                sleep(self._pause)
            except Exception as e:
                tries = tries + 1
                print(e)
                print("user request error", url, param)
            if re == None:
                tries = tries+1
            else:
                break
        time.sleep(1 * self._pause)
        return re

    def requestFriendList(self, check=True):
        if self.steamid == None:
            return
        if self.friendList != None and check == True:
            return []
        print("getting friends's list of "+str(self.steamid))
        param = {"key": self._key, "relationship": "friend", "steamid": self.steamid}
        tries = 0
        while tries < self._maxretries:
            re = self.sendGetRequest("http://api.steampowered.com/ISteamUser/GetFriendList/v0001", param)
            re_json = json.loads(re.content)
            if re.status_code == 200:
                break
            time.sleep(5*self._pause)
            tries = tries + 1
        if tries >= self._maxretries:
            return []
        try:
            self.friendList = re_json['friendslist']['friends']
        except Exception as e:
            print(e)
        print(self.ownedGameList)
        return self.friendList

    def saveFriendList(self):
        if self.steamid == None or self.friendList == None:
            return
        try:
            redisUtil = RedisUtil()
            redisUtil.setUserFriendship(self.steamid,self.friendList)
        except Exception as e:
            print("save friend list error! steamid:" + self.steamid)

    def getFriendList(self):
        if self.steamid == None:
            return
        if self.friendList != None:
            return self.friendList
        redisUtil = RedisUtil()
        try:
            self.friendList = redisUtil.getUserFriendship(self.steamid)
        except Exception as e:
            print("get friendList of" + self.steamid + " error!")
        return self.friendList

    def requestOwnedGames(self, include_appinfo=True, check=True):
        if self.steamid == None:
            return
        if self.ownedGameList != None and check == True:
            return []
        self.steamid = self.steamid
        print("get user owned games of "+str(self.steamid))
        param = {"key": self._key, "steamid": self.steamid, "format": "json"}
        if (include_appinfo is True):
            param["include_appinfo"] = "true"
        tries = 0
        while tries < self._maxretries:
            re = self.sendGetRequest("http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001", param)
            if re.status_code == 200:
                break
            time.sleep(5 * self._pause)
            tries = tries + 1
        if tries >= self._maxretries:
            return []
        try:
            self.ownedGameList = json.loads(re.content)['response'].get("games")
        except Exception as e:
            print("getOwnedGames error"+self.steamid)
            print(e)
        print(self.ownedGameList)
        return self.ownedGameList

    def saveOwnedGames(self):
        if self.steamid == None or self.ownedGameList == None:
            return
        try:
            redisUtil = RedisUtil()
            redisUtil.setUserOwnedGames(self.steamid,self.ownedGameList)
        except Exception as e:
            print("save owned game error! steamid:" + self.ownedGameList)

    def getOwnedGames(self):
        if self.steamid == None:
            return
        if self.ownedGameList != None:
            return self.ownedGameList
        redisUtil = RedisUtil()
        try:
            self.ownedGameList = redisUtil.getUserOwnedGames(self.steamid)
        except Exception as e:
            print("get user owned game of" + self.steamid + " error!")
        return self.ownedGameList

if __name__ == '__main__':
    uc = UserCrawler('76561198237972514')
    uc.requestFriendList()
    uc.requestOwnedGames()
    # xs = uc.getFriendList('76561198237972514')
    # sql = dbconnector()
    # sql.writeFriendRelationList('76561198237972514',xs)
    # redisUtil = RedisUtil()
    # redisUtil.saveUserFriendship('76561198237972514',xs)

    # xs = uc.getOwnedGames('thewalt')
    # redisUtil = RedisUtil()
    # redisUtil.setUserOwnedGames('thewalt',xs)

