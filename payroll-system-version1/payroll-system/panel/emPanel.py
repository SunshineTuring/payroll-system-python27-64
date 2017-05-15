#coding=gbk
import sys

import wx

sys.path.append("..")
import gridData
import operateEmployee


class emPanel(object):
    '''
    Ա����ϢPanle�����࣬��������������Panel����ʾ�����Լ�Ա����Ϣ����
    '''
    def __init__(self,frame):
        self.colLabels = (u"Ա��ID", u"Ա������", u"Ա���Ա�", u"Ա����ϵ�绰")
        self.opEmployee = operateEmployee.operateEmployee()
        self.frame = frame

    def showEM(self):
        '''
        ����Ա��������ϢPanel�Ĺ����Լ��¼���
        1.�����Լ�����Panel
        2.��Ա�������¼�
        3.���ز������Panel������Frame����
        :return: self.bkg
        '''
        #����Panel
        self.bkg = wx.Panel(self.frame)

        #����Panel
        panel1 = wx.Panel(self.bkg,style=wx.BORDER_THEME)
        addButton = wx.Button(panel1, label=u"���Ա����Ϣ")
        addButton.Bind(wx.EVT_BUTTON, self.onAdd)
        deleteButton = wx.Button(panel1, label=u"ɾ��Ա����Ϣ")
        deleteButton.Bind(wx.EVT_BUTTON, self.onDelete)
        modifyButton = wx.Button(panel1, label=u"�޸�Ա����Ϣ")
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
            listInfo.append(u"��".join(tempOne))

        dlg = wx.SingleChoiceDialog(self.frame, u"��ѡ��ɾ����Ա����Ϣ:", u"ɾ��Ա����Ϣ",
                                    listInfo)
        if dlg.ShowModal() == wx.ID_OK:
            message = dlg.GetStringSelection()  # ��ȡѡ�������
            dlg_tip = wx.MessageDialog(dlg, u"ȷ��ɾ����"+message+u"��", u"��ȷ��", wx.OK | wx.ICON_INFORMATION | wx.CANCEL)
            if dlg_tip.ShowModal() == wx.ID_OK:
                emDelete= message.split(u"��")
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
            listInfo.append(u"��".join(tempOne))

        self.Modifydlg = wx.SingleChoiceDialog(self.frame, u"��ѡ���޸ĵ�Ա����Ϣ:", u"�޸�Ա����Ϣ",
                                    listInfo)
        if self.Modifydlg.ShowModal() == wx.ID_OK:
            message = self.Modifydlg.GetStringSelection()  # ��ȡѡ�������
            emModify = message.split(u"��")
            self.UI1(self.Modify)
            self.oriEmID =  emModify[0]
            self.ID.SetValue(emModify[0])
            self.Name.SetValue(emModify[1])
            self.Sex.SetValue(emModify[2])
            self.Phone.SetValue(emModify[3])
            self.dlg.ShowModal()


    def Add(self,e):
        '''
        ��������ݿ���ӱ����������Panel����ʾ
        :param e:
        :return:
        '''
        if self.ID.GetValue()!="" and self.Name.GetValue()!="":
            if 0 ==self.opEmployee.emAdd(self.ID.GetValue(),self.Name.GetValue(),self.Sex.GetValue(),self.Phone.GetValue()):
                wx.MessageBox("���ʧ��", u"���ʧ��", wx.OK | wx.ICON_INFORMATION)
        else:
            wx.MessageBox("���ʧ��", u"���ʧ��", wx.OK | wx.ICON_INFORMATION)

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
                wx.MessageBox("�޸�ʧ��", u"�޸�ʧ��", wx.OK | wx.ICON_INFORMATION)
        else:
            wx.MessageBox("�޸�ʧ��", u"�޸�ʧ��", wx.OK | wx.ICON_INFORMATION)
        self.Modifydlg.Destroy()
        self.dlg.Destroy()
        self.frame.employeePanel.Destroy()
        self.frame.employeePanel = self.frame.employeePanelControl.showEM()
        self.frame.sizer.Add(self.frame.employeePanel, 1, wx.EXPAND)
        self.frame.Layout()

    def UI1(self,AddFunction):
        '''
        ������������ӶԻ���
        :param AddFunction:
        :return:
        '''
        self.dlg = wx.Dialog(self.frame, -1, u'���/�޸�Ա����Ϣ',size=(400,200))

        self.ID = wx.TextCtrl(self.dlg)
        self.Name = wx.TextCtrl(self.dlg)
        self.Sex = wx.TextCtrl(self.dlg)
        self.Phone = wx.TextCtrl(self.dlg)

        IDtext = wx.StaticText(self.dlg, label=u"Ա��ID��")
        Nametext = wx.StaticText(self.dlg, label=u"Ա��������")
        Sextext = wx.StaticText(self.dlg, label=u"Ա���Ա�")
        Phonetext = wx.StaticText(self.dlg, label=u"Ա���绰��")

        EMaddButton = wx.Button(self.dlg, label=u"ȷ��")
        EMaddButton.Bind(wx.EVT_BUTTON, AddFunction)

        EMexitButton = wx.Button(self.dlg, label=u"�˳�")
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


