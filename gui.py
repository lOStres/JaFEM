from jafem import *
from rtree import index

import wx
import psycopg2


APP_EXIT=1

class UI(wx.Frame):

    def __init__(self,*args,**kwargs):
        super(UI, self).__init__(*args, **kwargs)
        self.InitUI()
        self.dirname=''
        self.filename=''


    def InitUI(self):
        global kneighbText, metadataText
        panel=wx.Panel(self)
        panel.SetBackgroundColour('#4f5049')
        vbox=wx.BoxSizer(wx.VERTICAL)
        
        butt1=wx.Button(panel,label='Find k most similar',pos=(10,10))
        butt1.Bind(wx.EVT_BUTTON, self.contentQuery)

        butt4=wx.Button(panel, label='Drop DB', pos=(190,100))
        butt4.Bind(wx.EVT_BUTTON, self.dropDB)

        butt2=wx.Button(panel,label='Initialize DB',pos=(40,100))
        butt2.Bind(wx.EVT_BUTTON, self.initializeDB)

        butt3=wx.Button(panel, label='Search by name', pos=(10,40))
        butt3.Bind(wx.EVT_BUTTON, self.metadataQuery)

        menubar=wx.MenuBar()
        fileMenu=wx.Menu()
        viewMenu=wx.Menu()
        
        kneighbText = wx.TextCtrl(panel, size=(140, -1), pos=(160,10))
        metadataText =  wx.TextCtrl(panel, size=(140, -1), pos=(160,40))
        
        self.Bind(wx.EVT_RIGHT_DOWN, self.OnRightDown)

        
        self.SetSize((320,175))
        self.SetTitle('JaFEM')
        self.Centre()
        self.Show(True)


    def OnQuit(self,e):
        logfile.close()
        self.Close()

    # make content-based query
    def contentQuery(self,e):
        global kneighbText
        kneighbours = kneighbText.GetValue()
        print(kneighbours)
        dlg=wx.FileDialog(self,"Choose a file", self.dirname,"", "*.*", wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            self.filename = dlg.GetFilename()
            self.dirname = dlg.GetDirectory()
            nearest = similarity(self.dirname, self.filename, int(kneighbours))
            print(nearest)
        dlg.Destroy()

    # make metadata based query
    def metadataQuery(self,e):

        global metadataText
        filename = str(metadataText.GetValue())

        con = psycopg2.connect(database='testdb', user='klwnos')
        cur = con.cursor()

        query = """SELECT * FROM metadata
                WHERE id = %s;"""
        data = (filename,)
        cur.execute(query, data)
        records = cur.fetchall()
        print(records)

    # initialize db and spatial index
    def initializeDB(self,e):
        con = None
        try:
            # TODO prepei na allaksei auto gia na mporoume na to xrhsimopoioume kai oi 2
            con = psycopg2.connect(database='testdb', user='klwnos')
            cur = con.cursor()

            cur.execute('''CREATE TABLE metadata
                    (id INT PRIMARY KEY, filesize INT, duration FLOAT,
                    samplerate INT, tags VARCHAR(200) ARRAY, type VARCHAR(7),
                    saliance VARCHAR(5), startime FLOAT, endtime FLOAT,
                    class VARCHAR(20), link VARCHAR(200));''')
            # TODO kai auto pepei na allaksei       
            directory = '/home/klwnos/Documents/children_playing'

            # create or open spatial index
            p = index.Property()
            p.dat_extension = 'data'
            p.idx_extension = 'index'
            p.dimension = 13

            rtree = index.Index('rtreez', properties=p, interleaved=True)
            index_id = 1

            print("scanning directory", directory)
            # scanning directory and inserting values to db
            for filename in os.listdir(directory):
                name , extension = filename.rsplit('.',1);

                if not name:
                    continue;

                # parse meta-data
                if extension == "csv":
                    meta = parseCSV(directory, filename)

                    query = """INSERT INTO metadata
                    (id, startime, endtime, saliance, class)
                    VALUES (%s, %s, %s, %s, %s);"""
                    data = (name, meta[0], meta[1], meta[2], meta[3])
                    cur.execute(query, data)

                elif extension == "json":
                    meta = parseJSON(directory, filename)

                    query = """UPDATE metadata SET filesize = %s,
                        duration = %s, samplerate = %s, tags = %s, type = %s
                        WHERE id = %s;"""
                    data = (meta[0], meta[1], meta[2], meta[3], meta[4], name)
                    cur.execute(query, data)

                else:
                    featureVector = extractFeatures(directory,filename)

                    link = directory + '/' + name + '.' + extension

                    #insert to spatialindex
                    rtree.insert(int(name), (featureVector[0], featureVector[1],
                        featureVector[2], featureVector[3], featureVector[4],
                        featureVector[5], featureVector[6], featureVector[7],
                        featureVector[8], featureVector[9], featureVector[10],
                        featureVector[11], featureVector[12], featureVector[0],
                        featureVector[1], featureVector[2], featureVector[3],
                        featureVector[4], featureVector[5], featureVector[6],
                        featureVector[7], featureVector[8], featureVector[9],
                        featureVector[10], featureVector[11],
                        featureVector[12]))

                    query = """UPDATE metadata SET link = %s
                        WHERE id = %s;"""
                    data = (link, name)
                    cur.execute(query, data)

        except psycopg2.DatabaseError as err:
            print( 'Error %s' % err)
            sys.exit(1)

        finally:

            if con:
                con.commit()
                con.close()

    # dropDB and spatial index
    def dropDB(self,e):
        con = None
        try:
            # TODO kai auto prepei na allaksei
            con = psycopg2.connect(database='testdb', user='klwnos')
            cur = con.cursor()

            cur.execute("DROP TABLE metadata")

        except psycopg2.DatabaseError as err:
            print( 'Error %s' % err)
            sys.exit(1)

        finally:

            if con:
                con.commit()
                con.close()
                os.remove('rtreez.data')
                os.remove('rtreez.index')

        
    def OnRightDown(self,e):
        self.PopupMenu(MyPopupMenu(self), e.GetPosition())



def main():
   
    ex=wx.App()
    UI(None)
    ex.MainLoop()


if __name__== '__main__':
    main()
