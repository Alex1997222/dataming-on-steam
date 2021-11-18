import redis
import json

class RedisUtil(object):
    __friend_redis_pool = None
    __owned_game_redis_pool = None
    __user_list_redis_pool = None
    __game_brief_redis_pool = None
    __review_redis_pool = None
    _instance = None
    _user_friend_ship = 5
    _user_owned_game = 6
    _game_brief_list = 7
    _user_list = 8
    _review_list = 9

    #For Singleton
    def __new__(cls, *args, **kw):
        if cls._instance is None:
            cls._instance = object.__new__(cls, *args, **kw)
        return cls._instance

    #initial connect pool
    def __init__(self):
        self.__friend_redis_pool = redis.ConnectionPool(host='127.0.0.1', port=6379, db=self._user_friend_ship)
        self.__owned_game_redis_pool = redis.ConnectionPool(host='127.0.0.1', port=6379, db=self._user_owned_game)
        self.__user_list_redis_pool = redis.ConnectionPool(host='127.0.0.1', port=6379, db=self._user_list)
        self.__game_brief_redis_pool = redis.ConnectionPool(host='127.0.0.1', port=6379, db=self._game_brief_list)
        self.__review_redis_pool = redis.ConnectionPool(host='127.0.0.1', port=6379, db=self._review_list)

    def checkReviewExist(self, appid):
        redis_conn = redis.Redis(connection_pool=self.__review_redis_pool)
        test = None
        try:
            test = redis_conn.get(appid)
        except Exception as e:
            print(e)
        return test != None

    def getReviewList(self, appid):
        redis_conn = redis.Redis(connection_pool=self.__review_redis_pool)
        result = None
        try:
            result_str = redis_conn.get(appid)
            result = json.loads(result_str)
        except Exception as e:
            print(e)
        return result

    def setReviews(self, appid, reviews):
        redis_conn = redis.Redis(connection_pool=self.__review_redis_pool)
        try:
            redis_conn.set(appid, json.dumps(reviews))
        except Exception as e:
            print(e)


    def checkGameExist(self, appid):
        redis_conn = redis.Redis(connection_pool=self.__game_brief_redis_pool)
        test = None
        try:
            test = redis_conn.get(appid)
        except Exception as e:
            print(e)
        return test != None

    def setGameExist(self, appid):
        redis_conn = redis.Redis(connection_pool=self.__game_brief_redis_pool)
        try:
            redis_conn.set(appid, 'exist')
        except Exception as e:
            print(e)

    def setGame(self, appid, gamaBrief):
        redis_conn = redis.Redis(connection_pool=self.__game_brief_redis_pool)
        try:
            redis_conn.set(appid,json.dumps(gamaBrief))
        except Exception as e:
            print("save game brief ERROR->",appid,gamaBrief)
            print(e)

    def checkUserExist(self, steamid):
        redis_conn = redis.Redis(connection_pool=self.__user_list_redis_pool)
        test = None
        try:
            test = redis_conn.get(steamid)
        except Exception as e:
            print(e)
        return test != None

    def setUser(self, steamid, id, name):
        redis_conn = redis.Redis(connection_pool=self.__user_list_redis_pool)
        try:
            user_info_str = json.dumps({"id":id,"name":name})
            redis_conn.set(steamid, user_info_str)
        except Exception as e:
            print(e)

    def setUserFriendship(self,steamid,friendList):
        redis_conn = redis.Redis(connection_pool=self.__friend_redis_pool)
        try:
            redis_conn.set(steamid,json.dumps(friendList))
        except Exception as e:
            print("save user friendship ERROR->",steamid,friendList)
            print(e)

    def setUserOwnedGames(self,steamid,gameList):
        redis_conn = redis.Redis(connection_pool=self.__owned_game_redis_pool)
        if gameList == []:
            return
        try:
            redis_conn.set(steamid,json.dumps(gameList))
        except Exception as e:
            print("set user owned games ERROR->",steamid,gameList)
            print(e)

    def getUserFriendship(self,steamid):
        redis_conn = redis.Redis(connection_pool=self.__friend_redis_pool)
        re_json = ''
        try:
            re_json = redis_conn.get(steamid)
        except Exception as e:
            print("get user friendship ERROR->", steamid)
            print(e)
            return None
        re = None
        if re_json != None:
            try:
                re = json.loads(re_json)
            except Exception as e:
                print("get user friendship json ERROR->", re_json)
                print(e)
        return re

    def getUserOwnedGames(self,steamid):
        redis_conn = redis.Redis(connection_pool=self.__owned_game_redis_pool)
        re_json = ''
        try:
            re_json = redis_conn.get(steamid)
        except Exception as e:
            print("get user owned game ERROR->", steamid)
            print(e)
            return []
        re = None
        if re_json != None:
            try:
                re = json.loads(re_json)
            except Exception as e:
                print("get user owned game json ERROR->", re_json)
                print(e)
        return re


if __name__ == '__main__':
    r = RedisUtil()
    print(r.checkUserExist('10'))