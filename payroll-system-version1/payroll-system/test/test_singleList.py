#coding=gbk
import wx


class MyFrame(wx.Frame):
    def __init__(self, parent, id):
        wx.Frame.__init__(self, parent, id, u'�������Panel', size=(600, 300))

        # �������
        panel = wx.Panel(self)

        # ��Panel�����Button
        button = wx.Button(panel, label=u'�ر�', pos=(150, 60), size=(100, 60))

        # �󶨵����¼�
        self.Bind(wx.EVT_BUTTON, self.OnCloseMe, button)

    #    #��Ϣ�Ի���
    #    def OnCloseMe(self, event):
    #        dlg = wx.MessageDialog(None, u"��Ϣ�Ի������", u"������Ϣ", wx.YES_NO | wx.ICON_QUESTION)
    #        if dlg.ShowModal() == wx.ID_YES:
    #            self.Close(True)
    #        dlg.Destroy()
    #
    #    #�ı�����Ի���
    #    def OnCloseMe(self, event):
    #        dlg = wx.TextEntryDialog(None, u"���������ı�������������:", u"�ı���������", u"Ĭ������")
    #        if dlg.ShowModal() == wx.ID_OK:
    #            message = dlg.GetValue() #��ȡ�ı����������ֵ
    #            dlg_tip = wx.MessageDialog(None, message, u"������Ϣ", wx.OK | wx.ICON_INFORMATION)
    #            if dlg_tip.ShowModal() == wx.ID_OK:
    #                self.Close(True)
    #            dlg_tip.Destroy()
    #        dlg.Destroy()

    # �б�ѡ��Ի���
    def OnCloseMe(self, event):
        dlg = wx.SingleChoiceDialog(None, u"��ѡ����ϲ����ˮ��:", u"�б�ѡ������",
                                    [u"ƻ��", u"����", u"��ݮ"])
        if dlg.ShowModal() == wx.ID_OK:
            message = dlg.GetStringSelection()  # ��ȡѡ�������
            dlg_tip = wx.MessageDialog(None, message, u"������Ϣ", wx.OK | wx.ICON_INFORMATION)
            if dlg_tip.ShowModal() == wx.ID_OK:
                self.Close(True)
            dlg_tip.Destroy()
        dlg.Destroy()


if __name__ == '__main__':
    app = wx.PySimpleApp()
    frame = MyFrame(parent=None, id=-1)
    frame.Show()
    app.MainLoop()