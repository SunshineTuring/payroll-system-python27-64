#coding=gbk
import sys

import wx

sys.path.append("..")
import gridData
import operateWorkType


class wtPanel(object):
    def __init__(self,frame):
        self.colLabels = (u"����ID", u"������", u"���ֵ���")
        self.opWorkType = operateWorkType.operateWorkType()
        self.frame = frame

    def showWT(self):
        self.bkg = wx.Panel(self.frame)

        panel1 = wx.Panel(self.bkg,style=wx.BORDER_THEME)
        addButton = wx.Button(panel1, label=u"��ӹ�����Ϣ")
        addButton.Bind(wx.EVT_BUTTON, self.onAdd)
        deleteButton = wx.Button(panel1, label=u"ɾ��������Ϣ")
        deleteButton.Bind(wx.EVT_BUTTON, self.onDelete)
        modifyButton = wx.Button(panel1, label=u"�޸Ĺ�����Ϣ")
        modifyButton.Bind(wx.EVT_BUTTON, self.onModify)

        hbox = wx.BoxSizer()
        hbox.Add(addButton, proportion=0, flag=wx.LEFT, border=5)
        hbox.Add(deleteButton, proportion=0, flag=wx.LEFT, border=5)
        hbox.Add(modifyButton, proportion=0, flag=wx.LEFT, border=5)
        panel1.SetSizer(hbox)

        Info = self.opWorkType.wtGetAll()
        if Info==0:
            count=0
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
        Info = self.opWorkType.wtGetAll()
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

        dlg = wx.SingleChoiceDialog(self.frame, u"��ѡ��ɾ���Ĺ�����Ϣ:", u"ɾ��������Ϣ",
                                    listInfo)
        if dlg.ShowModal() == wx.ID_OK:
            message = dlg.GetStringSelection()  # ��ȡѡ�������
            dlg_tip = wx.MessageDialog(dlg, u"ȷ��ɾ����"+message+u"��", u"��ȷ��", wx.OK | wx.ICON_INFORMATION | wx.CANCEL)
            if dlg_tip.ShowModal() == wx.ID_OK:
                wtDelete= message.split(u"��")
                wtID = wtDelete[0]
                self.Delete(wtID)
            dlg_tip.Destroy()
        dlg.Destroy()
        self.frame.workTypePanel.Destroy()
        self.frame.workTypePanel = self.frame.workTypePanelControl.showWT()
        self.frame.sizer.Add(self.frame.workTypePanel, 1, wx.EXPAND)
        self.frame.Layout()

    def onModify(self,e):
        emInfo = self.opWorkType.wtGetAll()
        listInfo = []
        if emInfo == 0:
            return 1
        for i in emInfo:
            tempOne = []
            for v in i:
                if isinstance(v, (int, float)):
                    v = str(v)
                tempOne.append(v)
            listInfo.append(u"��".join(tempOne))

        self.Modifydlg = wx.SingleChoiceDialog(self.frame, u"��ѡ���޸ĵĹ�����Ϣ:", u"�޸Ĺ�����Ϣ",
                                    listInfo)
        if self.Modifydlg.ShowModal() == wx.ID_OK:
            message = self.Modifydlg.GetStringSelection()  # ��ȡѡ�������
            emModify = message.split(u"��")
            self.UI1(self.Modify)
            self.oriEmID =  emModify[0]
            self.ID.SetValue(emModify[0])
            self.Name.SetValue(emModify[1])
            self.UnitPrice.SetValue(emModify[2])
            self.dlg.ShowModal()


    def Add(self,e):
        if self.ID.GetValue()!="" and self.Name.GetValue()!="" and self.UnitPrice!="":
            if 0 == self.opWorkType.wtAdd(self.ID.GetValue(),self.Name.GetValue(),float(self.UnitPrice.GetValue())):
                wx.MessageBox("���ʧ��", u"���ʧ��", wx.OK | wx.ICON_INFORMATION)
        else:
            wx.MessageBox("���ʧ��", u"���ʧ��", wx.OK | wx.ICON_INFORMATION)
        self.dlg.Destroy()
        self.frame.workTypePanel.Destroy()
        self.frame.workTypePanel = self.frame.workTypePanelControl.showWT()
        self.frame.sizer.Add(self.frame.workTypePanel, 1, wx.EXPAND)
        self.frame.Layout()

    def Delete(self,emID):

        if 0 == self.opWorkType.wtDelete(emID):
            wx.MessageBox("ɾ��ʧ��", u"ɾ��ʧ��", wx.OK | wx.ICON_INFORMATION)


    def Modify(self,e):
        if self.ID.GetValue()!="" and self.Name.GetValue()!="":
            if 0 == self.opWorkType.wtModify( self.oriEmID,self.ID.GetValue(),self.Name.GetValue(),float(self.UnitPrice.GetValue())):
                wx.MessageBox("�޸�ʧ��", u"�޸�ʧ��", wx.OK | wx.ICON_INFORMATION)
        else:
            wx.MessageBox("�޸�ʧ��", u"�޸�ʧ��", wx.OK | wx.ICON_INFORMATION)
        self.Modifydlg.Destroy()
        self.dlg.Destroy()
        self.frame.workTypePanel.Destroy()
        self.frame.workTypePanel = self.frame.workTypePanelControl.showWT()
        self.frame.sizer.Add(self.frame.workTypePanel, 1, wx.EXPAND)
        self.frame.Layout()

    def UI1(self,AddFunction):
        self.dlg = wx.Dialog(self.frame, -1, u'���/�޸Ĺ�����Ϣ',size=(550,150))

        self.ID = wx.TextCtrl(self.dlg)
        self.Name = wx.TextCtrl(self.dlg)
        self.UnitPrice = wx.TextCtrl(self.dlg)

        IDtext = wx.StaticText(self.dlg, label=u"����ID��")
        Nametext = wx.StaticText(self.dlg, label=u"��������")
        UnitPricetext = wx.StaticText(self.dlg, label=u"���ֵ��ۣ�")


        EMaddButton = wx.Button(self.dlg, label=u"ȷ��")
        EMaddButton.Bind(wx.EVT_BUTTON, AddFunction)

        EMexitButton = wx.Button(self.dlg, label=u"�˳�")
        EMexitButton.Bind(wx.EVT_BUTTON, self.Exit)

        hbox1 = wx.BoxSizer()
        vbox1 = wx.BoxSizer(wx.VERTICAL)
        vbox2 = wx.BoxSizer(wx.VERTICAL)

        hbox1.Add(IDtext, proportion=0)
        hbox1.Add(self.ID, proportion=1)
        hbox1.Add(Nametext, proportion=0)
        hbox1.Add(self.Name, proportion=1)
        hbox1.Add(UnitPricetext, proportion=0)
        hbox1.Add(self.UnitPrice , proportion=1)

        vbox2.Add(EMaddButton, proportion=0)
        vbox2.Add(EMexitButton, proportion=0)

        vbox1.Add(hbox1, proportion=0, flag=wx.CENTER | wx.UP, border=30)
        vbox1.Add((10,10))
        vbox1.Add(vbox2, proportion=0, flag=wx.LEFT, border=430)

        self.dlg.SetSizer(vbox1)
    def Exit(self):
        self.dlg.Destroy()



