import wx
import pyHook,pythoncom,pygame, datetime, os


APP_EXIT=1

class Example(wx.Frame):

    def __init__(self,*args,**kwargs):
        super(Example, self).__init__(*args, **kwargs)
        self.InitUI()
        self.dirname=''
        self.filename=''
        



    def InitUI(self):
        global editname,metadataText
        panel=wx.Panel(self)
        panel.SetBackgroundColour('#4f5049')
        vbox=wx.BoxSizer(wx.VERTICAL)
        
        butt1=wx.Button(panel,label='Search song',pos=(0,0))
        
        butt1.Bind(wx.EVT_BUTTON, self.OnOpen)
        
        butt3=wx.Button(panel, label='Search by metadata', pos=(0,30))
        butt3.Bind(wx.EVT_BUTTON, self.metadataQuery)

        
        menubar=wx.MenuBar()
        fileMenu=wx.Menu()
        viewMenu=wx.Menu()
        
        kneighbText = wx.TextCtrl(panel, size=(140, -1), pos=(80,0))
        metadataText =  wx.TextCtrl(panel, size=(140, -1), pos=(120,30))
        
        self.Bind(wx.EVT_RIGHT_DOWN, self.OnRightDown)


        
        self.SetSize((300,175))
        self.SetTitle('KeyLogger')
        self.Centre()
        self.Show(True)


    

    def OnQuit(self,e):
        logfile.close()
        self.Close()
        


        
    def OnOpen(self,e):
        global kneighbText
        kneighbours = editname.GetValue()
        print(kneighbours)
        dlg=wx.FileDialog(self,"Choose a file", self.dirname,"", "*.*", wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            self.filename = dlg.GetFilename()
            self.dirname = dlg.GetDirectory()
            print(self.filename)
            print(self.dirname)
        dlg.Destroy()

        
    def metadataQuery(self,e):
        global metadataText
        metadata=metadataText.GetValue()
        print(metadata)


    def OnRightDown(self,e):
        self.PopupMenu(MyPopupMenu(self), e.GetPosition())


        
class MyPopupMenu(wx.Menu):
    def __init__(self,parent):
        super(MyPopupMenu, self).__init__()
        self.parent=parent

        mmi=wx.MenuItem(self, wx.NewId(), 'Minimize')
        self.AppendItem(mmi)
        self.Bind(wx.EVT_MENU, self.OnMinimize, mmi)

        cmi=wx.MenuItem(self, wx.NewId(), 'Close')
        self.AppendItem(cmi)
        self.Bind(wx.EVT_MENU, self.OnClose, cmi)

        
    def OnMinimize(self,e):
        self.parent.Iconize()

    def OnClose(self,e):
        self.parent.Close()
        

        

        
def main():
   
    ex=wx.App()
    Example(None)
    ex.MainLoop()


if __name__== '__main__':
    main()
