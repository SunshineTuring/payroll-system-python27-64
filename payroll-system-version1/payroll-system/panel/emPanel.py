#coding=gbk
import sys

import wx

sys.path.append("..")
import gridData
import operateEmployee


class emPanel(object):
    '''
    员工信息Panle管理类，负责主窗口中主Panel的显示管理以及员工信息管理。
    '''
    def __init__(self,frame):
        self.colLabels = (u"员工ID", u"员工姓名", u"员工性别", u"员工联系电话")
        self.opEmployee = operateEmployee.operateEmployee()
        self.frame = frame

    def showEM(self):
        '''
        负责员工管理信息Panel的管理以及事件绑定
        1.创建以及布局Panel
        2.绑定员工管理事件
        3.返回布局完的Panel，交给Frame处理
        :return: self.bkg
        '''
        #创建Panel
        self.bkg = wx.Panel(self.frame)

        #布局Panel
        panel1 = wx.Panel(self.bkg,style=wx.BORDER_THEME)
        addButton = wx.Button(panel1, label=u"添加员工信息")
        addButton.Bind(wx.EVT_BUTTON, self.onAdd)
        deleteButton = wx.Button(panel1, label=u"删除员工信息")
        deleteButton.Bind(wx.EVT_BUTTON, self.onDelete)
        modifyButton = wx.Button(panel1, label=u"修改员工信息")
        modifyButton.Bind(wx.EVT_BUTTON, self.onModify)

        hbox = wx.BoxSizer()
        hbox.Add(addButton, proportion=0, flag=wx.LEFT, border=5)
        hbox.Add(deleteButton, proportion=0, flag=wx.LEFT, border=5)
        hbox.Add(modifyButton, proportion=0, flag=wx.LEFT, border=5)
        panel1.SetSizer(hbox)

        Info = self.opEmployee.emGetAll()
        if Info == 0:
            count = 0
        else:
            count = len(Info)
        rowLabels = range(1, count + 1)
        WIGrid = wx.grid.Grid(self.bkg)
        tableBase = gridData.GenericTable(Info, rowLabels, self.colLabels)
        WIGrid.SetTable(tableBase)

        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(panel1, proportion=0, flag=wx.EXPAND, border=5)
        vbox.Add(WIGrid, proportion=1, flag=wx.EXPAND | wx.LEFT | wx.BOTTOM | wx.RIGHT,border=5)
        self.bkg.SetSizer(vbox)
        return self.bkg

    def onAdd(self,e):

        self.UI1(self.Add)
        self.dlg.ShowModal()

    def onDelete(self,e):
        Info = self.opEmployee.emGetAll()
        listInfo = []
        if Info == 0:
            return 1
        for i in Info:
            tempOne = []
            for v in i:
                if isinstance(v,(int, float)):
                    v = str(v)
                tempOne.append(v)
            listInfo.append(u"，".join(tempOne))

        dlg = wx.SingleChoiceDialog(self.frame, u"请选择删除的员工信息:", u"删除员工信息",
                                    listInfo)
        if dlg.ShowModal() == wx.ID_OK:
            message = dlg.GetStringSelection()  # 获取选择的内容
            dlg_tip = wx.MessageDialog(dlg, u"确认删除："+message+u"？", u"请确认", wx.OK | wx.ICON_INFORMATION | wx.CANCEL)
            if dlg_tip.ShowModal() == wx.ID_OK:
                emDelete= message.split(u"，")
                emID = emDelete[0]
                self.Delete(emID)
            dlg_tip.Destroy()
        dlg.Destroy()
        self.frame.employeePanel.Destroy()
        self.frame.employeePanel = self.frame.employeePanelControl.showEM()
        self.frame.sizer.Add(self.frame.employeePanel, 1, wx.EXPAND)
        self.frame.Layout()

    def onModify(self,e):
        emInfo = self.opEmployee.emGetAll()
        if emInfo == 0:
            return 1
        listInfo = []
        for i in emInfo:
            tempOne = []
            for v in i:
                if isinstance(v, (int, float)):
                    v = str(v)
                tempOne.append(v)
            listInfo.append(u"，".join(tempOne))

        self.Modifydlg = wx.SingleChoiceDialog(self.frame, u"请选择修改的员工信息:", u"修改员工信息",
                                    listInfo)
        if self.Modifydlg.ShowModal() == wx.ID_OK:
            message = self.Modifydlg.GetStringSelection()  # 获取选择的内容
            emModify = message.split(u"，")
            self.UI1(self.Modify)
            self.oriEmID =  emModify[0]
            self.ID.SetValue(emModify[0])
            self.Name.SetValue(emModify[1])
            self.Sex.SetValue(emModify[2])
            self.Phone.SetValue(emModify[3])
            self.dlg.ShowModal()


    def Add(self,e):
        '''
        往后端数据库添加表项，并更新主Panel的显示
        :param e:
        :return:
        '''
        if self.ID.GetValue()!="" and self.Name.GetValue()!="":
            if 0 ==self.opEmployee.emAdd(self.ID.GetValue(),self.Name.GetValue(),self.Sex.GetValue(),self.Phone.GetValue()):
                wx.MessageBox("添加失败", u"添加失败", wx.OK | wx.ICON_INFORMATION)
        else:
            wx.MessageBox("添加失败", u"添加失败", wx.OK | wx.ICON_INFORMATION)

        self.dlg.Destroy()
        self.frame.employeePanel.Destroy()
        self.frame.employeePanel = self.frame.employeePanelControl.showEM()
        self.frame.sizer.Add(self.frame.employeePanel, 1, wx.EXPAND)
        self.frame.Layout()

    def Delete(self,emID):
        self.opEmployee.emDelete(emID)


    def Modify(self,e):
        if self.ID.GetValue()!="" and self.Name.GetValue()!="":
            if 0 == self.opEmployee.emModify( self.oriEmID,self.ID.GetValue(),self.Name.GetValue(),self.Sex.GetValue(),self.Phone.GetValue()):
                wx.MessageBox("修改失败", u"修改失败", wx.OK | wx.ICON_INFORMATION)
        else:
            wx.MessageBox("修改失败", u"修改失败", wx.OK | wx.ICON_INFORMATION)
        self.Modifydlg.Destroy()
        self.dlg.Destroy()
        self.frame.employeePanel.Destroy()
        self.frame.employeePanel = self.frame.employeePanelControl.showEM()
        self.frame.sizer.Add(self.frame.employeePanel, 1, wx.EXPAND)
        self.frame.Layout()

    def UI1(self,AddFunction):
        '''
        创建并布局添加对话框
        :param AddFunction:
        :return:
        '''
        self.dlg = wx.Dialog(self.frame, -1, u'添加/修改员工信息',size=(400,200))

        self.ID = wx.TextCtrl(self.dlg)
        self.Name = wx.TextCtrl(self.dlg)
        self.Sex = wx.TextCtrl(self.dlg)
        self.Phone = wx.TextCtrl(self.dlg)

        IDtext = wx.StaticText(self.dlg, label=u"员工ID：")
        Nametext = wx.StaticText(self.dlg, label=u"员工姓名：")
        Sextext = wx.StaticText(self.dlg, label=u"员工性别：")
        Phonetext = wx.StaticText(self.dlg, label=u"员工电话：")

        EMaddButton = wx.Button(self.dlg, label=u"确定")
        EMaddButton.Bind(wx.EVT_BUTTON, AddFunction)

        EMexitButton = wx.Button(self.dlg, label=u"退出")
        EMexitButton.Bind(wx.EVT_BUTTON, self.Exit)

        vbox1 = wx.BoxSizer(wx.VERTICAL)
        vbox2 = wx.BoxSizer(wx.VERTICAL)
        vbox3 = wx.BoxSizer(wx.VERTICAL)
        vbox4 = wx.BoxSizer(wx.VERTICAL)
        vbox5 = wx.BoxSizer(wx.VERTICAL)
        vbox6 = wx.BoxSizer(wx.VERTICAL)
        hbox1 = wx.BoxSizer()

        vbox1.Add(IDtext, proportion=0)
        vbox1.Add((10, 10))
        vbox1.Add(Sextext, proportion=0)

        vbox2.Add(self.ID, proportion=1)
        vbox2.Add(self.Sex, proportion=1)

        vbox3.Add(Nametext, proportion=0)
        vbox3.Add((10, 10))
        vbox3.Add(Phonetext, proportion=0)

        vbox4.Add(self.Name, proportion=1)
        vbox4.Add(self.Phone, proportion=1)

        hbox1.Add(vbox1, proportion=0)
        hbox1.Add(vbox2, proportion=0)
        hbox1.Add((10, 10))
        hbox1.Add(vbox3, proportion=0)
        hbox1.Add(vbox4, proportion=0)

        vbox6.Add(EMaddButton, proportion=0)
        vbox6.Add(EMexitButton, proportion=0)

        vbox5.Add(hbox1, proportion=0, flag=wx.LEFT | wx.RIGHT | wx.UP, border=30)
        vbox5.Add((10,10))
        vbox5.Add(vbox6, proportion=0, flag=wx.LEFT, border=290)

        self.dlg.SetSizer(vbox5)
        # dlg.Show()
    def Exit(self,e):
        self.dlg.Destroy()


