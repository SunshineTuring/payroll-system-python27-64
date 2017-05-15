import wx

app = wx.App()
win = wx.Frame(None,title="Simple Editor")
# loadButton = wx.Button(win,pos=(225,5),size=(80,25),
#                        label="Open")
# saveButton = wx.Button(win,pos=(315,5),size=(80,25),
#                        label="Save")
# fileName = wx.TextCtrl(win,pos=(5,5),size=(210,25))
# fileName = wx.TextCtrl(win,pos=(5,35),size=(390,260))

def load(event):
    file = open(fileName.GetValue())
    Contents.SetValue(file.read())
    file.close()

def save(event):
    file = open(fileName.GetValue(),'w')
    file.write(Contents.GetValue())
    file.close()

bkg = wx.Panel(win)

loadButton = wx.Button(bkg,label="Open")
loadButton.Bind(wx.EVT_BUTTON,load)

saveButton = wx.Button(bkg,label="Save")
saveButton.Bind(wx.EVT_BUTTON,save)

fileName = wx.TextCtrl(bkg)
Contents = wx.TextCtrl(bkg,style=wx.TE_MULTILINE | wx.HSCROLL)

hbox = wx.BoxSizer()
hbox.Add(loadButton,proportion=0,flag=wx.LEFT,border=5)
hbox.Add(saveButton,proportion=0,flag=wx.LEFT,border=5)
hbox.Add(fileName,proportion=1,flag=wx.EXPAND)

vbox = wx.BoxSizer(wx.VERTICAL)
vbox.Add(hbox,proportion=0,flag=wx.EXPAND | wx.ALL,border=5)
vbox.Add(Contents,proportion=1,flag=wx.EXPAND | wx.LEFT | wx.BOTTOM | wx.RIGHT,border=5)

bkg.SetSizer(vbox)
win.Show()
app.MainLoop()