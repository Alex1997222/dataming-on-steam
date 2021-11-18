import pymysql
import properties
import traceback
from sqlPool.sqlHelper import MySqLHelper

class dbconnector:
    def __init__(self):
        self.game_db = MySqLHelper()

    #insert game information into database
    def writeGameInfo(self,id,name,price,label,description,GameEvaluate):
        sql = "INSERT INTO game_table(game_id,game_title,game_price,game_label,game_description,game_evaluate) VALUES(%s,%s,%s,%s,%s,%s)"
        self.game_db.insertOneInfo(sql,(id,name,price,label,description,GameEvaluate))

    #insert Rated R Games information
    def WriteLimitedGameInfo(self,gid,glink):
        sql = "INSERT INTO limited_game_table(g_id,g_link) VALUES(%s,%s)"
        self.game_db.insertOneInfo(sql,(gid,glink))

    #insert user comment into database
    def WriteUserTable(self,name,id,comment,hours,rate):
        sql = "INSERT INTO user_table(user_name,user_id,user_comment,user_hours,user_rate) VALUES(%s,%s,%s,%s,%s)"
        self.game_db.insertOneInfo(sql,(name,id,comment,hours,rate))

    def writeGameBriefList(self,gameList):
        sql = "INSERT INTO game_brief(`type`,id, name) VALUES(%s,%s,%s)"
        for type, id, name in gameList:
            self.game_db.insertOneInfo(sql,(type,id,name))

    def writeGameBrief(self,id, name, type = None):
        if type == None:
            type = 'NULL'
        sql = "INSERT INTO game_brief(`type`,id, name) VALUES(%s,%s,%s)"
        self.game_db.insertOneInfo(sql, (type, id, name))


    def writeFriendRelationList(self,steamid,friendRelationList):
        sql = "INSERT INTO friend_relation(steamid, friend_id, relationship, friend_since) VALUES(%s,%s,%s,%s)"
        for item in friendRelationList:
            self.game_db.insertOneInfo(sql, (steamid, item["steamid"], item["relationship"], item["friend_since"]))


    def writeReviewList(self,appid,reviewList):
        sql = "INSERT INTO review(appid, helpful, funny, username, steamid, owned, numrev, recco, `time`, posted, content) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        for item in reviewList:
            self.game_db.insertOneInfo(sql, (appid,item['helpful'], item['funny'], item['username'], item['steamid'], item['owned'], item['numrev'],item['recco'], item['time'], item['posted'], item['content']))


    def selectAllGameBrief(self):
        sql = "SELECT * FROM game_brief"
        re = self.game_db.selectall(sql)
        return re

