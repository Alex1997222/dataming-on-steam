from sqlPool.dbDbUtilsInit import get_my_connection

class MySqLHelper(object):
    def __init__(self):
        self.db = get_my_connection()  # 从数据池中获取连接

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'inst'):  # 单例
            cls.inst = super(MySqLHelper, cls).__new__(cls, *args, **kwargs)
        return cls.inst

    def close(self, cursor, conn):
        cursor.close()
        conn.close()

    def execute(self, sql, param=None, autoclose=False):
        cursor, conn = self.db.getconn()  # 从连接池获取连接
        count = 0
        try:
            if param:
                count = cursor.execute(sql, param)  # count : 为改变的数据条数
            else:
                count = cursor.execute(sql)
            conn.commit()
            if autoclose:
                self.close(cursor, conn)
        except Exception as e:
            pass
        return cursor, conn, count

    def insertOneInfo(self,sql,param):
        try:
            cursor, conn, count = self.execute(sql, param)
            conn.commit()
            self.close(cursor, conn)
            print("insert success:")
            print(param)
            return count
        except Exception as e:
            print("insert failed:")
            print(e)
            conn.rollback()
            self.close(cursor, conn)
            return count
    #查询所有
    def selectall(self, sql, param=None):
        try:
            cursor, conn, count = self.execute(sql, param)
            res = cursor.fetchall()
            return res
        except Exception as e:
            print("query failed:")
            print(e)
            self.close(cursor, conn)
            return count