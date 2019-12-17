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
    def findWord(self,k):
        '''根据关键字查询单词列表'''
        cur = self.conn.cursor()
        str="select * from Word where english like '"+k+"%';"
        cur.execute(str)
        data = cur.fetchall()
        self.conn.commit()
        return data
    def updateWord(self,data):
        '''更新单词列表'''
        cur = self.conn.cursor()
        for item in data:
            if(item[1].strip()!="" and item[2].strip()!=""):
                sql="update Word set english =:e,chinese =:c where id=:i;"
                cur.execute(sql,{"e":item[1],"c":item[2],"i":item[0]})
            else:
                sql="delete from Word where id=:i"
                cur.execute(sql,{"i":item[0]})
        self.conn.commit()
