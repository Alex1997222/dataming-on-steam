# from multiprocessing import Process, Queue
from queue import Queue
import threading
from crawler.reviewCrawler import ReviewCrawler
from crawler.userCrawler import UserCrawler
import json
from GameListCrawler import getGameList

import time
from utils.redisUtis import RedisUtil
from utils.sqlUtils import dbconnector
from gameCrawler import GameCrawler
import requests
import properties

game_queue = Queue()
user_queue = Queue()
review_queue = Queue()

def game_consumer(game_queue,user_queue,review_queue):
    while True:
        game_info_str = game_queue.get(block=True)
        try:
            game_info = json.loads(game_info_str)
            game_helper(game_queue = game_queue,user_queue = user_queue,review_queue = review_queue,id = game_info['id'], url = game_info['url'])
        except Exception as e:
            print("game_consumer_error:",game_info_str)
        time.sleep(1)

def game_helper(game_queue,user_queue,review_queue,id, url):
    # crawler review
    review_queue.put(id)
    redisUtil = RedisUtil()
    if redisUtil.checkGameExist(id):
        print("exist game"+str(id))
        return
    gameCrawler = GameCrawler()
    gameCrawler.infoSave(id,url)
    redisUtil.setGameExist(id)

def review_consumer(game_queue,user_queue,review_queue):
    while True:
        appid = review_queue.get(block=True)
        try:
            review_helper(game_queue = game_queue,user_queue = user_queue,review_queue = review_queue,appid = appid)
        except Exception as e:
            print("review_consumer_error:",appid)
        time.sleep(1)

def review_helper(game_queue,user_queue,review_queue,appid):
    rc = ReviewCrawler(appid)
    reviews = rc.requestReview()
    rc.saveReview()
    for review in reviews:
        steamid = review['steamid']
        user_queue.put(steamid)


def user_consumer(game_queue,user_queue,review_queue):
    while True:
        steamid = user_queue.get(block=True)
        try:
            user_helper(game_queue = game_queue,user_queue = user_queue,review_queue = review_queue, steamid = steamid)
        except Exception as e:
            print("user_consumer_error:",steamid)
        time.sleep(1)

def user_helper(game_queue,user_queue,review_queue,steamid):
    uc = UserCrawler(steamid)
    friendList = uc.requestFriendList()
    uc.saveFriendList()
    if friendList != None:
        for friend in friendList:
            user_queue.put(friend['steamid'])
    ownedGameList = uc.requestOwnedGames()
    uc.saveOwnedGames()
    # put game task
    if ownedGameList != None:
        for game in ownedGameList:
            url = "https://store.steampowered.com/app/" + str(game['appid'])
            try:
                response = requests.get(url, headers=properties.headers, timeout=10)
            except Exception as e:
                print("add owned game to gamelist error: no response and",e)
            game_queue.put(json.dumps({"id": game['appid'], "url": url}))

def provider(game_queue):
    sql = dbconnector()
    start_games =[{"id":"10","url":"https://store.steampowered.com/app/10/CounterStrike/"},{"id":"20","url":"https://store.steampowered.com/app/20/Team_Fortress_Classic/"}]
    for item in start_games:
        game_info_str = json.dumps(item)
        game_queue.put(game_info_str)

if __name__ == '__main__':

    # redisUtil = RedisUtil()
    game_consumer_num = 5
    review_consumer_num = 5
    user_consumer_num = 5

    game_consumer_list = []
    review_consumer_list = []
    user_consumer_list = []

    game_list_provider_threading = threading.Thread(target=getGameList, args=(game_queue,))
    game_list_provider_threading.start()

    print("start allocating threading")
    for i in range(game_consumer_num):
        game_consumer_process = threading.Thread(target=game_consumer, args=(game_queue, user_queue, review_queue,))
        game_consumer_list.append(game_consumer_process)
        game_consumer_process.start()
    for i in range(user_consumer_num):
        user_consumer_process = threading.Thread(target=user_consumer, args=(game_queue, user_queue, review_queue,))
        user_consumer_list.append(user_consumer_process)
        user_consumer_process.start()
    for i in range(review_consumer_num):
        reveiw_consumer_process = threading.Thread(target=review_consumer, args=(game_queue, user_queue, review_queue,))
        review_consumer_list.append(reveiw_consumer_process)
        reveiw_consumer_process.start()

