import sqlite3
import time
#数据库操作

class DBControl:
    def __init__(self):
        # 初始化数据链接操作
        self.conn = sqlite3.connect('test.db')
    def reviewWord(self):
        '''搜索需要复习的单词,返回一个列表，列表中有信息的元组'''
        cur = self.conn.cursor()
        cur.execute("select * from Word")
        data = cur.fetchall()
        self.conn.commit()#提交事务
        return data
    def addWord(self,e,c):
        '''增加单词'''
        try:
            cur = self.conn.cursor()
            t=time.time()
            cur.execute("insert into Word(english,chinese,time) values(:e,:c,:t)",{"e":e,"c":c,"t":str(t)})
            self.conn.commit()
            return True
        except BaseException:
            return False