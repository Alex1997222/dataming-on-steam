from sqlPool import sqlPoolConfig as config
from dbutils.pooled_db import PooledDB

class MyConnectionPool(object):
    __pool = None

    # def __init__(self):
    #     self.conn = self.__getConn()
    #     self.cursor = self.conn.cursor()

    # construct dataset connection and cursor
    def __enter__(self):
        self.conn = self.__getconn()
        self.cursor = self.conn.cursor()

    # construct connection pool
    def __getconn(self):
        if self.__pool is None:
            self.__pool = PooledDB(
                creator=config.DB_CREATOR,
                mincached=config.DB_MIN_CACHED,
                maxcached=config.DB_MAX_CACHED,
                maxshared=config.DB_MAX_SHARED,
                maxconnections=config.DB_MAX_CONNECYIONS,
                blocking=config.DB_BLOCKING,
                maxusage=config.DB_MAX_USAGE,
                setsession=config.DB_SET_SESSION,
                host=config.DB_TEST_HOST,
                port=config.DB_TEST_PORT,
                user=config.DB_TEST_USER,
                passwd=config.DB_TEST_PASSWORD,
                db=config.DB_TEST_DBNAME,
                use_unicode=False,
                charset=config.DB_CHARSET
            )
        return self.__pool.connection()

    # relase resource
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cursor.close()
        self.conn.close()

    # get connection from pool
    def getconn(self):
        conn = self.__getconn()
        cursor = conn.cursor()
        return cursor, conn


# get connection instance
def get_my_connection():
    return MyConnectionPool()