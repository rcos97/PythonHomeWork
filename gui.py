'''图形'''

import wx
import sql
import wx.grid
import tt

app = wx.App(False)  # 每一个wxPython应用程序都是wx.App这个类的一个实例,False”，意味着不重定向标准输出和错误输出到窗口上。
frame = wx.Frame(None, wx.ID_ANY, "大学英语词汇学习系统",size=(600,400))  # None代表没有父类,是一个顶级窗口
frame2 =wx.Frame(None,-1,"修改")
app.SetTopWindow(frame)
db = sql.DBControl()  # 初始化数据库
# 菜单
menuBar = wx.MenuBar()  # 菜单条
fileMenu = wx.Menu()  # 一级菜单
practiceMenu = wx.Menu()
explainMenu = wx.Menu()
openFile = fileMenu.Append(-1, "导入文件")
quitApp = fileMenu.Append(-1, "退出")
menuBar.Append(fileMenu, "开始")
menuBar.Append(practiceMenu, "测试")
menuBar.Append(explainMenu, "说明")
frame.SetMenuBar(menuBar)  # 框架设置菜单栏


# 初始主界面
def initGui():
    # 事件
    def onChecked(e):
        '''将review 存放了已经复习完的单词的id'''
        cb = e.GetEventObject()
        id = cb.GetLabel()[3::]
        if (cb.GetValue() == True):
            review.append(id)
        else:
            review.remove(id)

    def show(e):
        '''点击显示中文'''
        try:
            cb = e.GetEventObject()
            id = cb.GetLabel()[4::]
            cb.SetLabel(wordList[int(id)][2])
        except BaseException:
            return

    def update(e):  # 上传信息
        pass

    def addWord(e):
        '''提交新单词'''
        e=englistInput.GetValue()
        c=chinesInput.GetValue()
        flag = db.addWord(e,c)
        if(flag == True):
            wx.MessageBox("提交成功", "Message" ,wx.OK | wx.ICON_INFORMATION)
            englistInput.SetValue("")
            chinesInput.SetValue("")
        else:
            wx.MessageBox("提交失败", "Message", wx.OK | wx.ICON_INFORMATION)
    findWordFlag=1
    def findWord(e):
        '''查询单词'''
        content = findEInput.GetValue()
        print(content)
        sonGui()
        if(findWordFlag==1):
            frame2.Show(True)
            findWordFlag = 0
        else:
            frame2.Show(False)
            findWordFlag = 1
    #gui界面
    panel = wx.Panel(frame, -1)  # panel是窗口的容器，通常其大小与Frame一样，在其上放置各种控件
    # 左半边
    leftBox = wx.BoxSizer(wx.VERTICAL)
    font = wx.Font(20, wx.ROMAN, wx.ITALIC, wx.NORMAL)
    promptInfo = wx.StaticText(panel, -1, "今天应该复习")
    promptInfo.SetFont(font)
    leftBox.Add(promptInfo, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, border=20)
    # 需要复习的单词
    wordList = db.reviewWord()
    font2 = wx.Font(14, wx.DECORATIVE, wx.NORMAL, wx.NORMAL)
    listGrid = wx.GridSizer(len(wordList), 3, 0, 0)  # 按顺序自动填充
    review = []  # 已经复习了的单词
    j = 0
    for word in wordList:
        a = wx.StaticText(panel, -1, label=word[1])
        a.SetFont(font2)
        listGrid.Add(a, 2, wx.LEFT | wx.ALIGN_CENTER, 20)  # 不能直接填写字符串，应该wx的对象
        b = wx.StaticText(panel, -1, label="点击显示" + str(j))
        j = j + 1
        b.SetFont(font2)
        b.Bind(wx.EVT_LEFT_DOWN, show)
        listGrid.Add(b, 2, wx.LEFT | wx.ALIGN_CENTER, 20)
        c = wx.CheckBox(panel, -1, label="记住了" + str(word[0]))
        listGrid.Add(c, 1, wx.LEFT | wx.ALIGN_CENTER, 20)
        c.Bind(wx.EVT_CHECKBOX, onChecked)
    okButton = wx.Button(panel, -1, label="确定")
    okButton.Bind(wx.EVT_BUTTON, update)
    leftBox.Add(listGrid, 0, wx.ALIGN_CENTER, 20)
    leftBox.Add(okButton, 0, wx.TOP | wx.ALIGN_CENTER, 30)
    # 右半边
    rightBox = wx.BoxSizer(wx.VERTICAL)
    promptInfo2 = wx.StaticText(panel, -1, "修改单词库")
    promptInfo2.SetFont(font)
    rightBox.Add(promptInfo2, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, border=20)
    # 增
    addTitle = wx.StaticText(panel, -1, label="新单词")
    rightBox.Add(addTitle, 0, wx.BOTTOM | wx.ALIGN_CENTER_HORIZONTAL, border=20)
    # 英语
    englistBox = wx.BoxSizer(wx.HORIZONTAL)
    englistTitle = wx.StaticText(panel, -1, label="请输入英语:")
    englistInput = wx.TextCtrl(panel, -1)
    englistBox.Add(englistTitle, 0, wx.RIGHT | wx.ALIGN_CENTER, border=30)
    englistBox.Add(englistInput, 0, wx.ALIGN_CENTER, border=20)
    rightBox.Add(englistBox, 0, wx.BOTTOM | wx.ALIGN_CENTER_HORIZONTAL, border=20)
    # 汉语
    chinesBox = wx.BoxSizer(wx.HORIZONTAL)
    chinesTitle = wx.StaticText(panel, -1, label="请输入汉语:")
    chinesInput = wx.TextCtrl(panel, -1)
    chinesBox.Add(chinesTitle, 0, wx.RIGHT | wx.ALIGN_CENTER, border=30)
    chinesBox.Add(chinesInput, 0, wx.ALIGN_CENTER, border=20)
    rightBox.Add(chinesBox, 0, wx.BOTTOM | wx.ALIGN_CENTER_HORIZONTAL, border=20)
    #上交按钮
    addButton=wx.Button(panel, -1, label="确定")
    rightBox.Add(addButton,0,wx.BOTTOM | wx.ALIGN_CENTER_HORIZONTAL, border=20)
    addButton.Bind( wx.EVT_LEFT_DOWN, addWord)

    #查询与修改
    # 查找单词
    findTitle = wx.StaticText(panel, -1, label="查找单词(可模糊匹配)")
    rightBox.Add(findTitle, 0, wx.BOTTOM | wx.ALIGN_CENTER_HORIZONTAL, border=20)
    # 输入英文关键词
    findEBox=wx.BoxSizer(wx.HORIZONTAL)
    findETitle = wx.StaticText(panel, -1, label="请输入英语:")
    findEInput = wx.TextCtrl(panel, -1)
    findEBox.Add(findETitle,0, wx.RIGHT | wx.ALIGN_CENTER, border=30)
    findEBox.Add(findEInput,0, wx.ALIGN_CENTER, border=20)
    rightBox.Add(findEBox,0, wx.BOTTOM | wx.ALIGN_CENTER_HORIZONTAL, border=20)
    # 查询按钮
    findButton = wx.Button(panel, -1, label="查询")
    rightBox.Add(findButton, 0, wx.BOTTOM | wx.ALIGN_CENTER_HORIZONTAL, border=20)
    findButton.Bind(wx.EVT_LEFT_DOWN, findWord)
    # 整体布局
    mainBox = wx.BoxSizer(wx.HORIZONTAL)
    mainBox.Add(leftBox, 1)
    mainBox.Add(rightBox, 1)

    panel.SetSizer(mainBox)

# 修改单词的子界面
def sonGui():
    panel = wx.Panel(frame2, -1)
    obj = tt.GridFrame(None)
initGui()
frame.Show(True)  # 展示窗口
app.MainLoop()  # 监听事件
