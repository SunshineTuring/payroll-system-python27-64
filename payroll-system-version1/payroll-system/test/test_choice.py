import wx


class Mywin(wx.Frame):
    def __init__(self, parent, title):
        super(Mywin, self).__init__(parent, title=title, size=(300, 200))

        panel = wx.Panel(self)
        box = wx.BoxSizer(wx.VERTICAL)
        self.label = wx.StaticText(panel, label="Your choice:", style=wx.ALIGN_CENTRE)
        box.Add(self.label, 0, wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 20)
        cblbl = wx.StaticText(panel, label="Combo box", style=wx.ALIGN_CENTRE)

        box.Add(cblbl, 0, wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 5)
        languages = ['C', 'C++', 'Python', 'Java', 'Perl']
        self.combo = wx.ComboBox(panel, choices=languages)

        box.Add(self.combo, 1, wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 5)
        chlbl = wx.StaticText(panel, label="Choice control", style=wx.ALIGN_CENTRE)

        box.Add(chlbl, 0, wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 5)
        self.choice = wx.Choice(panel, choices=languages)
        box.Add(self.choice, 1, wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 5)

        box.AddStretchSpacer()
        self.combo.Bind(wx.EVT_COMBOBOX, self.OnCombo)
        self.choice.Bind(wx.EVT_CHOICE, self.OnChoice)

        panel.SetSizer(box)
        self.Centre()
        self.Show()

    def OnCombo(self, event):
        self.label.SetLabel("You selected" + self.combo.GetValue() + " from Combobox")
        # self.choice.SetItems(["sa"])
        self.choice.SetString(0,"ssa")
        self.choice.SetSelection(0)
        # self.choice.AppendItems("sss")

    def OnChoice(self, event):
        self.label.SetLabel("You selected " + self.choice.GetString
        (self.choice.GetSelection()) + " from Choice")


app = wx.App()
Mywin(None, 'ComboBox & Choice Demo - www.yiibai.com')
app.MainLoop()