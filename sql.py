import sqlite3
from datetime import datetime
#数据库操作

class DBControl:
    def __init__(self):
        # 初始化数据链接操作
        self.conn = sqlite3.connect('test.db')
    def reviewWord(self):
        '''搜索需要复习的单词,返回一个列表，列表中有信息的元组'''
        # 寻找需要复习的的单词 1、2、4、7、15天后复习
        cur = self.conn.cursor()
        cur.execute("select * from Word")
        data = cur.fetchall()
        datas=[]
        nowTime = datetime.now()
        for x in data:
            addTime=datetime.strptime(str(x[4]),"%Y-%m-%d %H:%M:%S.%f")
            reviewTime=(nowTime-addTime).days
            if(reviewTime==0 or reviewTime==1 or reviewTime==2 or reviewTime==4 or reviewTime==7 or reviewTime==15):
                datas.append(x)
        self.conn.commit()#提交事务
        return datas
    def addWord(self,e,c):
        '''增加单词'''
        try:
            cur = self.conn.cursor()
            a=datetime.now()
            t=a
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
    def updateReview(self,reviewId):
        '''更新复习单词'''
        now =str(datetime.now())
        cur=self.conn.cursor()
        sql = "update Word set time = :t where id=:id"
        for x in reviewId:
            cur.execute(sql,{"t":now,"id":int(x)})
        self.conn.commit()

