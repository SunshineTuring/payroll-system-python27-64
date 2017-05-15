#coding=gbk
import wx

from panel import emPanel
from panel import wtPanel
from panel import wiPanel


class MainWindow(wx.Frame):
    '''
    ��������ά�������ڵ���ʾ�Լ��¼����������˵�����״̬������Panel���ά����
    ��Panel�������ݵ���ʾ����ӦPanel�����ദ��
    '''
    def __init__(self, parent, title):
        '''
        version20170513
        �����ڳ�ʼ��������
        ״̬������1��3�ı�����Ϊ�������֣��ұߵ���ʵ��ǰλ��
        �˵����������ļ������ߺͰ���������
            �ļ���1.���ݵ���������ǰҳ������ݵ���Ϊexcell��񣬴�ʵ�֡�
                  2.��ӡ����ӡ��ǰҳ����ʵ�֡�
            ���ߣ�ά����Panel����ͼ������Ա����Ϣ����͹�����Ϣ����
            ������1.�����������ĵ�����ʵ�֣�2.���ڣ���ʾ�汾��Ϣ
        :param parent:
        :param title:
        '''
        self.version = "�汾���ڣ� 2017-05-15"
        self.dirname = ''
        wx.Frame.__init__(self, parent, title=title,size=(820, 400))

        # ����״̬��
        self.statusbar = self.CreateStatusBar()
        self.statusbar.SetFieldsCount(2)
        self.statusbar.SetStatusWidths([-3, -1])
        self.statusbar.SetStatusText(u"��ǰλ�ã�Ա����Ϣ", 1)

        #�����˵����Ĳ˵���
        filemenu = wx.Menu()
        menuForward = filemenu.Append(wx.ID_FORWARD, u"���ݵ���", u"������ǰҳ������")
        menuPrint = filemenu.Append(wx.ID_PRINT, u"��ӡ", u"��ӡ��ǰҳ��")
        menuExit = filemenu.Append(wx.ID_EXIT, u"�˳�", u"�˳�����")

        toolMenu = wx.Menu()
        menuEI = toolMenu.Append(wx.ID_VIEW_DETAILS,u"&Ա������",u"Ա���������",kind=wx.ITEM_RADIO)
        menuWT = toolMenu.Append(wx.ID_VIEW_LARGEICONS, u"&���ֹ���", u"���ֹ������",kind=wx.ITEM_RADIO)
        menuWI = toolMenu.Append(wx.ID_VIEW_LIST, u"&������¼����", u"������¼����", kind=wx.ITEM_RADIO)

        helpMenu = wx.Menu()
        menuHelp = helpMenu.Append(wx.ID_HELP, u"����", u"����")
        menuAbout = helpMenu.Append(wx.ID_HELP, u"����", u"����")

        # �����˵���
        menuBar = wx.MenuBar()
        menuBar.Append(filemenu, u"�ļ�")
        menuBar.Append(toolMenu, u"����")
        menuBar.Append(helpMenu, u"����")
        self.SetMenuBar(menuBar)

        #�󶨲˵����¼�
        self.Bind(wx.EVT_MENU,self.OnForward,menuForward)
        self.Bind(wx.EVT_MENU, self.OnPrint, menuPrint)
        self.Bind(wx.EVT_MENU, self.OnExit, menuExit)

        self.Bind(wx.EVT_MENU, self.OnEM, menuEI)
        self.Bind(wx.EVT_MENU, self.OnWT, menuWT)
        self.Bind(wx.EVT_MENU, self.OnWI, menuWI)

        self.Bind(wx.EVT_MENU, self.OnAbout, menuHelp)
        self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)

        #��ʼ����Panel������
        self.employeePanelControl = emPanel.emPanel(self)
        self.workTypePanelControl = wtPanel.wtPanel(self)
        self.workInfoPanelControl = wiPanel.wiPanel(self)

        #��ʼ����Panel
        self.location = "em" #��־Ŀǰλ��
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
        ��Panel��ʾԱ����Ϣ��
        1.�ı�״̬����ʾ
        2.����ԭ��Panel
        3.������ʾԱ����Ϣ��Panel
        :param e:
        :return:
        '''
        self.statusbar.SetStatusText(u"��ǰλ�ã�Ա����Ϣ", 1)
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
        ��Panel��ʾԱ����Ϣ��
        1.�ı�״̬����ʾ
        2.����ԭ��Panel
        3.������ʾԱ����Ϣ��Panel
        :param e:
        :return:
        '''
        self.statusbar.SetStatusText(u"��ǰλ�ã�������Ϣ",1)
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
        dlg = wx.MessageDialog(self, self.version, u"���ǿƼ�")
        dlg.ShowModal()
        dlg.Destroy()

    def OnHelp(self):
        pass

    def showEM(self):
        self.employeePanelControl.showEM()

    def showWT(self):
        self.workTypePanelControl.showWT()


app = wx.App(False)
frame = MainWindow(None, u"���ʹ���ϵͳ")
app.MainLoop()