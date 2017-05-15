#coding=gbk
import wx

from panel import emPanel
from panel import wtPanel
from panel import wiPanel


class MainWindow(wx.Frame):
    '''
    该类用于维护主窗口的显示以及事件处理，包括菜单栏、状态栏和主Panel体的维护。
    主Panel具体内容的显示由相应Panel管理类处理。
    '''
    def __init__(self, parent, title):
        '''
        version20170513
        主窗口初始化操作：
        状态栏：以1：3的比例分为两个部分，右边的现实当前位置
        菜单栏：包括文件、工具和帮助三部分
            文件：1.数据导出：将当前页面的数据导出为excell表格，待实现。
                  2.打印：打印当前页，待实现。
            工具：维护主Panel体视图，包括员工信息界面和工种信息界面
            帮助：1.帮助：帮助文档，待实现；2.关于：显示版本信息
        :param parent:
        :param title:
        '''
        self.version = "版本日期： 2017-05-15"
        self.dirname = ''
        wx.Frame.__init__(self, parent, title=title,size=(820, 400))

        # 创建状态栏
        self.statusbar = self.CreateStatusBar()
        self.statusbar.SetFieldsCount(2)
        self.statusbar.SetStatusWidths([-3, -1])
        self.statusbar.SetStatusText(u"当前位置：员工信息", 1)

        #创建菜单栏的菜单项
        filemenu = wx.Menu()
        menuForward = filemenu.Append(wx.ID_FORWARD, u"数据导出", u"导出当前页面数据")
        menuPrint = filemenu.Append(wx.ID_PRINT, u"打印", u"打印当前页面")
        menuExit = filemenu.Append(wx.ID_EXIT, u"退出", u"退出程序")

        toolMenu = wx.Menu()
        menuEI = toolMenu.Append(wx.ID_VIEW_DETAILS,u"&员工管理",u"员工管理界面",kind=wx.ITEM_RADIO)
        menuWT = toolMenu.Append(wx.ID_VIEW_LARGEICONS, u"&工种管理", u"工种管理界面",kind=wx.ITEM_RADIO)
        menuWI = toolMenu.Append(wx.ID_VIEW_LIST, u"&工作记录管理", u"工作记录界面", kind=wx.ITEM_RADIO)

        helpMenu = wx.Menu()
        menuHelp = helpMenu.Append(wx.ID_HELP, u"帮助", u"帮助")
        menuAbout = helpMenu.Append(wx.ID_HELP, u"关于", u"关于")

        # 创建菜单栏
        menuBar = wx.MenuBar()
        menuBar.Append(filemenu, u"文件")
        menuBar.Append(toolMenu, u"工具")
        menuBar.Append(helpMenu, u"帮助")
        self.SetMenuBar(menuBar)

        #绑定菜单栏事件
        self.Bind(wx.EVT_MENU,self.OnForward,menuForward)
        self.Bind(wx.EVT_MENU, self.OnPrint, menuPrint)
        self.Bind(wx.EVT_MENU, self.OnExit, menuExit)

        self.Bind(wx.EVT_MENU, self.OnEM, menuEI)
        self.Bind(wx.EVT_MENU, self.OnWT, menuWT)
        self.Bind(wx.EVT_MENU, self.OnWI, menuWI)

        self.Bind(wx.EVT_MENU, self.OnAbout, menuHelp)
        self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)

        #初始化主Panel管理类
        self.employeePanelControl = emPanel.emPanel(self)
        self.workTypePanelControl = wtPanel.wtPanel(self)
        self.workInfoPanelControl = wiPanel.wiPanel(self)

        #初始化主Panel
        self.location = "em" #标志目前位置
        self.employeePanel = self.employeePanelControl.showEM()
        self.workTypePanel = None
        self.workInfoPanel = None
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.employeePanel,1,wx.EXPAND)
        self.SetSizer(self.sizer)

        # self.workTypePanel.showWT()
        self.Show()

    def OnForward(self, e):
        pass

    def OnPrint(self,e):
        pass

    def OnExit(self, e):
        self.Close()

    def OnEM(self, e):
        '''
        主Panel显示员工信息。
        1.改变状态栏显示
        2.销毁原主Panel
        3.创建显示员工信息的Panel
        :param e:
        :return:
        '''
        self.statusbar.SetStatusText(u"当前位置：员工信息", 1)
        if self.location == "wt":
            self.workTypePanel.Destroy()
        elif self.location == "wi":
            self.workInfoPanel.Destroy()
        self.location = "em"
        self.employeePanel = self.employeePanelControl.showEM()
        self.sizer.Add(self.employeePanel, 1, wx.EXPAND)
        self.Layout()

    def OnWT(self,e):
        '''
        主Panel显示员工信息。
        1.改变状态栏显示
        2.销毁原主Panel
        3.创建显示员工信息的Panel
        :param e:
        :return:
        '''
        self.statusbar.SetStatusText(u"当前位置：工种信息",1)
        if self.location == "em":
            self.employeePanel.Destroy()
        elif self.location == "wi":
            self.workInfoPanel.Destroy()
        self.location = "wt"
        self.workTypePanel = self.workTypePanelControl.showWT()
        self.sizer.Add(self.workTypePanel,1,wx.EXPAND)
        self.Layout()

    def OnWI(self,e):
        if self.location == "em":
            self.employeePanel.Destroy()
        elif self.location == "wt":
            self.workTypePanel.Destroy()
        self.location = "wi"
        self.workInfoPanel = self.workInfoPanelControl.showWI()
        self.sizer.Add(self.workInfoPanel,1,wx.EXPAND)
        self.Layout()

    def OnAbout(self, e):
        dlg = wx.MessageDialog(self, self.version, u"星星科技")
        dlg.ShowModal()
        dlg.Destroy()

    def OnHelp(self):
        pass

    def showEM(self):
        self.employeePanelControl.showEM()

    def showWT(self):
        self.workTypePanelControl.showWT()


app = wx.App(False)
frame = MainWindow(None, u"工资管理系统")
app.MainLoop()