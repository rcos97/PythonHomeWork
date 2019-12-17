import wx
import wx.grid
import sql
class GridFrame(wx.Frame):
    def __init__(self, parent,content):
        wx.Frame.__init__(self, parent,title="单词表 关闭即可保存修改",size=(300,200))

        # Create a wxGrid object
        grid = wx.grid.Grid(self, -1)

        # 数据库操作
        db=sql.DBControl()
        data = db.findWord(content)
        # 渲染表格
        grid.CreateGrid(len(data), 3)
        # id号不可编辑
        for i in range(len(data)):
            grid.SetReadOnly(i, 0, isReadOnly=True)
        for i in range(len(data)):
                grid.SetCellValue(i,0,str(data[i][0]))
                grid.SetCellValue(i,1,data[i][1])
                grid.SetCellValue(i,2, data[i][2])
        that = self
        def OnClose(self):
            r = wx.MessageBox("保存修改？", "确认", wx.CANCEL | wx.OK | wx.ICON_QUESTION)
            if r == wx.OK:
                reviseData=[]
                for i in range(len(data)):
                        reviseData.append((int(grid.GetCellValue(i,0)),grid.GetCellValue(i,1),grid.GetCellValue(i,2)))
                # 与原数据比较是否有更改
                subData=[]
                for x in reviseData:
                    flag = 1
                    for y in data:
                        if x[1] == y[1] and x[2] == y[2]:
                            flag = 0
                            break
                    if(flag == 1):
                        subData.append(x)
                db.updateWord(subData)
                that.Show(False)
            else:
                that.Show(False)
        self.Bind(wx.EVT_CLOSE, OnClose)
        self.Show()


if __name__ == '__main__':

    app = wx.App(0)
    frame = GridFrame(None)
    app.MainLoop()
