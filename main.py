import wx

import gui


app = wx.App(False)
notamProcessor = gui.NotamProcessor()
app.MainLoop()
