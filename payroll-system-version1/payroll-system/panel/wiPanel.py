#coding=gbk
import sys

import wx

sys.path.append("..")
import gridData
import operateWorkInfo
import operateEmployee
import operateWorkType
import datetime



class wiPanel(object):
    '''
    员工信息Panle管理类，负责主窗口中主Panel的显示管理以及员工信息管理。
    '''
    def __init__(self,frame):
        self.colLabels = (u"员工ID", u"员工姓名", u"工种ID", u"工种名",u"数量",u"单价",u"总额",u"日期")
        self.opEmployee = operateEmployee.operateEmployee()
        self.opWorkType = operateWorkType.operateWorkType()
        self.opWorkInfo = operateWorkInfo.operateWorkInfo()
        self.frame = frame

    def showWI(self):
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
        addButton = wx.Button(panel1, label=u"添加工作记录")
        addButton.Bind(wx.EVT_BUTTON, self.onAdd)
        deleteButton = wx.Button(panel1, label=u"删除工作记录")
        deleteButton.Bind(wx.EVT_BUTTON, self.onDelete)
        modifyButton = wx.Button(panel1, label=u"修改工作记录")
        modifyButton.Bind(wx.EVT_BUTTON, self.onModify)
        staticButton = wx.Button(panel1, label=u"工作记录统计")
        staticButton.Bind(wx.EVT_BUTTON, self.onStatic)

        hbox = wx.BoxSizer()
        hbox.Add(addButton, proportion=0, flag=wx.LEFT, border=5)
        hbox.Add(deleteButton, proportion=0, flag=wx.LEFT, border=5)
        hbox.Add(modifyButton, proportion=0, flag=wx.LEFT, border=5)
        hbox.Add(staticButton, proportion=0, flag=wx.LEFT, border=5)
        panel1.SetSizer(hbox)

        Info = self.opWorkInfo.wiGetAll()
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
        Info = self.opWorkInfo.wiGetAll()
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

        dlg = wx.SingleChoiceDialog(self.frame, u"请选择删除的工作记录:", u"删除工作记录",
                                    listInfo)
        if dlg.ShowModal() == wx.ID_OK:
            message = dlg.GetStringSelection()  # 获取选择的内容
            dlg_tip = wx.MessageDialog(dlg, u"确认删除："+message+u"？", u"请确认", wx.OK | wx.ICON_INFORMATION | wx.CANCEL)
            if dlg_tip.ShowModal() == wx.ID_OK:
                deleteInfo= message.split(u"，")
                self.Delete(deleteInfo)
            dlg_tip.Destroy()
        dlg.Destroy()
        self.frame.workInfoPanel.Destroy()
        self.frame.workInfoPanel = self.frame.workInfoPanelControl.showWI()
        self.frame.sizer.Add(self.frame.workInfoPanel, 1, wx.EXPAND)
        self.frame.Layout()

    def onModify(self,e):
        emInfo = self.opWorkInfo.wiGetAll()
        listInfo = []
        if emInfo == 0:
            return 1
        for i in emInfo:
            tempOne = []
            for v in i:
                if isinstance(v, (int, float)):
                    v = str(v)
                tempOne.append(v)
            listInfo.append(u"，".join(tempOne))

        self.Modifydlg = wx.SingleChoiceDialog(self.frame, u"请选择修改的工作记录:", u"修改工作记录",
                                    listInfo)

        if self.Modifydlg.ShowModal() == wx.ID_OK:
            message = self.Modifydlg.GetStringSelection()  # 获取选择的内容
            self.wiModify = message.split(u"，")
            self.UI1(self.Modify)
            self.emNameChoice.SetValue(self.wiModify[1])
            self.emIDChoice.SetValue(self.wiModify[0])
            self.wtNameChoice.SetValue(self.wiModify[3])
            self.wtIDChoice.SetValue(self.wiModify[2])
            self.Number.SetValue(self.wiModify[4])
            self.unitPrice.SetValue(self.wiModify[5])
            self.totalPrice.SetValue(self.wiModify[6])
            self.date.SetValue(self.wiModify[7])
            self.dlg.ShowModal()

    def onStatic(self,e):

        emInfo = self.opEmployee.emGetAll()
        if emInfo == 0:
            return 1
        self.dlg = wx.Dialog(self.frame, -1, u'查询工作记录', size=(800, 600))
        emName = ["All"]
        for i in emInfo:
            emName.append(i[1])
        self.emNameChoice = wx.ComboBox(self.dlg, choices=emName)
        self.emNameChoice.Bind(wx.EVT_COMBOBOX, self.OnemChoice)
        self.emIDChoice = wx.ComboBox(self.dlg, choices=[])

        now = datetime.datetime.now()
        dateNow = []
        dateNow.append(now.strftime('%Y-%m-%d'))
        self.dateBegin = wx.ComboBox(self.dlg, choices=dateNow)
        self.dateEnd = wx.ComboBox(self.dlg, choices=dateNow)

        emNametext = wx.StaticText(self.dlg, label=u"员工姓名：")
        emIDtext = wx.StaticText(self.dlg, label=u"员工ID：")
        dateBegintext = wx.StaticText(self.dlg, label=u"起始日期（年-月-日）：")
        dateEndtext = wx.StaticText(self.dlg, label=u"终止日期（年-月-日）：")
        self.allPricetext = wx.StaticText(self.dlg, label=u"总额：",style=wx.ALIGN_CENTER | wx.TE_NOHIDESEL)
        self.allPricetext.SetBackgroundColour("WHITE")
        font = wx.Font(12, wx.DECORATIVE, wx.ITALIC,wx.NORMAL)
        self.allPricetext.SetFont(font)


        WIaddButton = wx.Button(self.dlg, label=u"确定")
        WIaddButton.Bind(wx.EVT_BUTTON, self.Static)
        WIexitButton = wx.Button(self.dlg, label=u"退出")
        WIexitButton.Bind(wx.EVT_BUTTON, self.Exit)

        vbox1 = wx.BoxSizer(wx.VERTICAL)
        vbox2 = wx.BoxSizer(wx.VERTICAL)
        vbox3 = wx.BoxSizer(wx.VERTICAL)
        vbox4 = wx.BoxSizer(wx.VERTICAL)
        vbox5 = wx.BoxSizer(wx.VERTICAL)
        hbox1 = wx.BoxSizer()
        vbox6 = wx.BoxSizer(wx.VERTICAL)


        vbox1.Add(emNametext, proportion=0)
        vbox1.Add((10, 10))
        vbox1.Add(emIDtext, proportion=0)

        vbox2.Add(self.emNameChoice, proportion=1)
        vbox2.Add(self.emIDChoice, proportion=1)

        vbox3.Add(dateBegintext, proportion=0)
        vbox3.Add((10, 10))
        vbox3.Add(dateEndtext, proportion=0)

        vbox4.Add(self.dateBegin, proportion=1)
        vbox4.Add(self.dateEnd, proportion=1)
        vbox4.Add((10,10))
        vbox4.Add(self.allPricetext,proportion=1)

        vbox5.Add(WIaddButton,proportion=1)
        vbox5.Add(WIexitButton, proportion=1)

        hbox1.Add(vbox1, proportion=0)
        hbox1.Add(vbox2, proportion=0)
        hbox1.Add((10, 10))
        hbox1.Add(vbox3, proportion=0)
        hbox1.Add(vbox4, proportion=0)
        hbox1.Add((10, 10))
        hbox1.Add(vbox5, proportion=0)

        Info = self.opWorkInfo.wiGetAll()
        if Info == 0:
            count = 0
        else:
            count = len(Info)
        rowLabels = range(1, count + 1)
        self.staWIGrid = wx.grid.Grid(self.dlg)
        self.STtableBase = gridData.GenericTable(Info, rowLabels, self.colLabels)
        self.staWIGrid.SetTable(self.STtableBase)
        tempAllPrice = 0.0
        for i in Info:
            tempAllPrice = tempAllPrice + float(i[6])
        self.allPricetext.SetLabel(u"总额：%.4f"%tempAllPrice)

        vbox6.Add(hbox1,proportion=0,flag=wx.UP | wx.DOWN | wx.CENTER,border=20)
        vbox6.Add(self.staWIGrid, proportion=1, flag=wx.CENTER)


        self.dlg.SetSizer(vbox6)
        self.dlg.ShowModal()

    def Add(self,e):
        '''
        往后端数据库添加表项，并更新主Panel的显示
        :param e:
        :return:
        '''

        if self.Number.IsEmpty() or self.emNameChoice.IsEmpty() or self.emIDChoice.IsEmpty() or \
                self.wtNameChoice.IsEmpty() or self.wtIDChoice.IsEmpty() or self.unitPrice.IsEmpty() or \
                self.date.IsEmpty():
            wx.MessageBox("添加失败", u"添加失败", wx.OK | wx.ICON_INFORMATION)
        else:
            selectEmName = self.emNameChoice.GetValue()
            selectEmID = self.emIDChoice.GetValue()
            selectWtName = self.wtNameChoice.GetValue()
            selectWtID = self.wtIDChoice.GetValue()
            inputNumber = self.Number.GetValue()
            inputUintPrice = self.unitPrice.GetValue()
            inputDate = self.date.GetValue()
            inputtotalPrice = int(inputNumber) * float(inputUintPrice)
            if 0 == self.opWorkInfo.wiAdd(selectEmID,selectEmName,selectWtID,selectWtName,\
                                          int(inputNumber),float('%.4f'%float(inputUintPrice)),float('%.4f'%inputtotalPrice),inputDate):
                wx.MessageBox("添加失败", u"添加失败", wx.OK | wx.ICON_INFORMATION)

        self.dlg.Destroy()
        self.frame.workInfoPanel.Destroy()
        self.frame.workInfoPanel = self.frame.workInfoPanelControl.showWI()
        self.frame.sizer.Add(self.frame.workInfoPanel, 1, wx.EXPAND)
        self.frame.Layout()

    def Delete(self,deleteInfo):
        if 0 ==self.opWorkInfo.wiDelete(deleteInfo[0],deleteInfo[1],deleteInfo[2],deleteInfo[3],\
            int(deleteInfo[4]),float(deleteInfo[5]),float(deleteInfo[6]),deleteInfo[7]):
            wx.MessageBox("删除失败", u"删除失败", wx.OK | wx.ICON_INFORMATION)


    def Modify(self,e):
        if 0 == self.opWorkInfo.wiModify(self.wiModify[0],self.wiModify[1],self.wiModify[2],self.wiModify[3],int(self.wiModify[4]),\
                                        float(self.wiModify[5]),float(self.wiModify[6]),self.wiModify[7],self.emIDChoice.GetValue(), \
                                        self.emNameChoice.GetValue(), self.wtIDChoice.GetValue(),self.wtNameChoice.GetValue(),\
                                        int(self.Number.GetValue()), float(self.unitPrice.GetValue()), \
                                         int(self.Number.GetValue())*float(self.unitPrice.GetValue()),self.date.GetValue()):
            wx.MessageBox("修改失败", u"修改失败", wx.OK | wx.ICON_INFORMATION)
        self.Modifydlg.Destroy()
        self.dlg.Destroy()
        self.frame.workInfoPanel.Destroy()
        self.frame.workInfoPanel = self.frame.workInfoPanelControl.showWI()
        self.frame.sizer.Add(self.frame.workInfoPanel, 1, wx.EXPAND)
        self.frame.Layout()

    def Static(self,e):
        self.STtableBase.Clear()
        emName = self.emNameChoice.GetValue()
        if emName==u"All":
            beginDate = self.dateBegin.GetValue()
            endDate = self.dateEnd.GetValue()
            data = self.opWorkInfo.wiGetByDateArea(beginDate,endDate)
        else:
            emID = self.emIDChoice.GetValue()
            beginDate = self.dateBegin.GetValue()
            endDate = self.dateEnd.GetValue()
            data = self.opWorkInfo.wiGetByDateAreaAndNameAndId(beginDate,endDate,emName,emID)
        tempAllPrice = 0.0
        if data != 0:
            for i in data:
                tempAllPrice = tempAllPrice + float(i[6])
        self.allPricetext.SetLabel(u"总额：%.4f" % tempAllPrice)
        self.STtableBase.data = data
        self.dlg.Refresh()
    def Exit(self,e):
        self.dlg.Destroy()

    def UI1(self,AddFunction):
        '''
        创建并布局添加对话框
        :param AddFunction:
        :return:
        '''

        self.dlg = wx.Dialog(self.frame, -1, u'添加/修改工作记录', size=(850, 200))
        emInfo = self.opEmployee.emGetAll()
        emName = []
        if emInfo != 0:
            for i in emInfo:
                emName.append(i[1])
        self.emNameChoice = wx.ComboBox(self.dlg, choices=emName)
        self.emNameChoice.Bind(wx.EVT_COMBOBOX, self.OnemChoice)
        self.emIDChoice = wx.ComboBox(self.dlg, choices=[])

        wtInfo = self.opWorkType.wtGetAll()
        wtName = []
        if wtInfo != 0:
            for i in wtInfo:
                wtName.append(i[1])
        self.wtNameChoice = wx.ComboBox(self.dlg, choices=wtName)
        self.wtNameChoice.Bind(wx.EVT_COMBOBOX, self.OnwtChoice)
        self.wtIDChoice = wx.ComboBox(self.dlg, choices=[])
        self.unitPrice = wx.ComboBox(self.dlg, choices=[])

        self.Number = wx.TextCtrl(self.dlg)
        self.totalPrice = wx.TextCtrl(self.dlg)

        now = datetime.datetime.now()
        dateNow=[]
        dateNow.append(now.strftime('%Y-%m-%d'))

        self.date = wx.ComboBox(self.dlg,choices=dateNow)

        emNametext = wx.StaticText(self.dlg, label=u"员工姓名：")
        emIDtext = wx.StaticText(self.dlg, label=u"员工ID：")
        wtNametext = wx.StaticText(self.dlg, label=u"工种名：")
        wtIDtext = wx.StaticText(self.dlg, label=u"工种ID：")
        Numbertext = wx.StaticText(self.dlg, label=u"数量：")
        unitPricetext = wx.StaticText(self.dlg, label=u"单价：")
        totalPricetext = wx.StaticText(self.dlg, label=u"总额(可不填)：")
        datetext = wx.StaticText(self.dlg, label=u"日期（年-月-日）：")

        WIaddButton = wx.Button(self.dlg, label=u"确定")
        WIaddButton.Bind(wx.EVT_BUTTON, AddFunction)
        WIexitButton = wx.Button(self.dlg, label=u"确定")
        WIexitButton.Bind(wx.EVT_BUTTON, self.Exit)

        vbox1 = wx.BoxSizer(wx.VERTICAL)
        vbox2 = wx.BoxSizer(wx.VERTICAL)
        vbox3 = wx.BoxSizer(wx.VERTICAL)
        vbox4 = wx.BoxSizer(wx.VERTICAL)
        vbox5 = wx.BoxSizer(wx.VERTICAL)
        vbox6 = wx.BoxSizer(wx.VERTICAL)
        vbox7 = wx.BoxSizer(wx.VERTICAL)
        vbox8 = wx.BoxSizer(wx.VERTICAL)
        hbox1 = wx.BoxSizer()
        vbox9 = wx.BoxSizer(wx.VERTICAL)
        vbox10 = wx.BoxSizer(wx.VERTICAL)

        vbox1.Add(emNametext, proportion=0)
        vbox1.Add((10, 10))
        vbox1.Add(emIDtext, proportion=0)

        vbox2.Add(self.emNameChoice, proportion=1)
        vbox2.Add(self.emIDChoice, proportion=1)

        vbox3.Add(wtNametext, proportion=0)
        vbox3.Add((10, 10))
        vbox3.Add(wtIDtext, proportion=0)

        vbox4.Add(self.wtNameChoice, proportion=1)
        vbox4.Add(self.wtIDChoice, proportion=1)

        vbox5.Add(Numbertext, proportion=0)
        vbox5.Add((10, 10))
        vbox5.Add(unitPricetext, proportion=0)

        vbox6.Add(self.Number, proportion=1)
        vbox6.Add(self.unitPrice, proportion=1)

        vbox7.Add(totalPricetext, proportion=0)
        vbox7.Add((10, 10))
        vbox7.Add(datetext, proportion=0)

        vbox8.Add(self.totalPrice, proportion=1)
        vbox8.Add(self.date, proportion=1)

        hbox1.Add(vbox1, proportion=0)
        hbox1.Add(vbox2, proportion=0)
        hbox1.Add((10, 10))
        hbox1.Add(vbox3, proportion=0)
        hbox1.Add(vbox4, proportion=0)
        hbox1.Add((10, 10))
        hbox1.Add(vbox5, proportion=0)
        hbox1.Add(vbox6, proportion=0)
        hbox1.Add((10, 10))
        hbox1.Add(vbox7, proportion=0)
        hbox1.Add(vbox8, proportion=0)

        vbox9.Add(WIaddButton, proportion=0)
        vbox9.Add(WIexitButton, proportion=0)
        vbox10.Add(hbox1, proportion=0, flag=wx.RIGHT |wx.UP | wx.LEFT, border=30)
        vbox10.Add(vbox9, proportion=0, flag=wx.LEFT, border=720)

        self.dlg.SetSizer(vbox10)
        # dlg.Show()
    def OnemChoice(self,e):
        selectEmName = self.emNameChoice.GetValue()
        if selectEmName != u"All":
            info = self.opEmployee.emGetByName(selectEmName)
            items = []
            for i in info:
                items.append(i[0])
            self.emIDChoice.SetItems(items)
        else:
            self.emIDChoice.SetItems([u"All"])

    def OnwtChoice(self,e):
        selectWtName = self.wtNameChoice.GetValue()
        info = self.opWorkType.wtGetByName(selectWtName)
        items = []
        uPrice = []
        for i in info:
            items.append(i[0])
            uPrice.append(str(i[2]))
        self.wtIDChoice.SetItems(items)
        self.unitPrice.SetItems(uPrice)


