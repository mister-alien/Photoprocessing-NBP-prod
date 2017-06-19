import renamethings
import os.path
from renamethings import renstuff
from appJar import gui
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import askdirectory
#from __future__ import print_function    (for when i use py 2 )


###################################################
# Action definitions for the button pressing and the menu buttons
def press(btn):
    global offset
    global prefix
    global namecol
    global txcol
    global platecol
    if(btn=="Cancel"):
        app.stop()
    elif(btn=="Browse"):
        Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
        filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file
        app.setEntry("linefile",filename)
    elif(btn=="Rename"):
#        print(str(offset)+'\n'+prefix+'\n'+namecol+'\n'+txcol+'\n'+platecol)
        renstuff(app.getEntry("linefile"),app.getEntry("workdir"),namecol,platecol,txcol,prefix,offset)
        print("Done")    
    elif(btn=="work dir"):
        Tk().withdraw()
        direct=askdirectory()
        app.setEntry("workdir",direct)
        
    elif(btn=="Defaults"):
        cfg=open('config.txt','w+') #If the config doesn't exist, write the default values to it
        offset = 2
        prefix='IMG_0000'
        namecol='A'
        txcol='L'
        platecol='M'
        cfg.write(str(offset)+'\n'+prefix+'\n'+namecol+'\n'+txcol+'\n'+platecol)
        cfg.close()
        app.setEntry("pfix", prefix)
        app.setEntry("ofset", offset)
        app.setEntry("namcol", namecol)
        app.setEntry("txco", txcol)
        app.setEntry("plateco", platecol)
        
    elif(btn=="OK"):
        prefix = app.getEntry("pfix").rstrip()
        offset = int(app.getEntry("ofset"))
        namecol = app.getEntry("namcol").rstrip()
        txcol = app.getEntry("txco").rstrip()
        platecol = app.getEntry("plateco").rstrip()
        cfg=open('config.txt','w+')
        cfg.write(str(offset)+'\n'+prefix+'\n'+namecol+'\n'+txcol+'\n'+platecol)
        cfg.close()
        app.hideSubWindow("config")
    elif(btn=="Apply"):
        prefix = app.getEntry("pfix")
        offset = app.getEntry("ofset")
        namecol = app.getEntry("namcol")
        txcol = app.getEntry("txco")
        platecol = app.getEntry("plateco")
        cfg=open('config.txt','w+')
        cfg.write(str(offset)+'\n'+prefix+'\n'+namecol+'\n'+txcol+'\n'+platecol)
        cfg.close()
    elif(btn=="cancelconf"):
        app.hideSubWindow("config")
        
def menuPress(menus):
    if(menus=="Config"):
        app.showSubWindow("config")
        
    elif(menus=="Info"):
        app.showSubWindow("info")
    elif(menus=="Close"):
        app.stop()
        #### Default value block
def confpress(btn):
    if(btn=="Cancel"):
        config.stop()
#
###################################################

if os.path.isfile('config.txt'):
    with open('config.txt','r') as cfg: #if the config file does exist, great! open and parse its values
        offset=None
        for line in cfg:
            if offset==None:
                offset = int(line)
                prefix=None
            elif prefix==None:
                prefix = line.rstrip()
                namecol=None
            elif namecol==None:
                namecol = line.rstrip()
                txcol=None
            elif txcol==None:
                txcol = line.rstrip()
                platecol=None
            elif platecol==None:
                platecol = line.rstrip()
            else:
                print('why are there extra lines?')
else:
    cfg=open('config.txt','w+') #If the config doesn't exist, write the default values to it
    offset = 2
    prefix='IMG_0000'
    namecol='A'
    txcol='L'
    platecol='M'
    cfg.write(str(offset)+'\n'+prefix+'\n'+namecol+'\n'+txcol+'\n'+platecol)
    cfg.close()

# print(str(offset)+'\n'+prefix+'\n'+namecol+'\n'+txcol+'\n'+platecol)
app=gui(title="Photo-Renamer")

### fillings

app.addLabel("title","Renamer thing",0,0,2)
#row 0, col 0, span of 2

app.addLabel("linefile","Spreadsheet Path",1,0)
app.addEntry("linefile",1,1)
app.addButton("Browse",press,1,2)

app.addLabel("workdir","Raw Photo Directory: ",2,0)
app.addEntry("workdir",2,1)
app.addButton("work dir",press,2,2)

app.addButtons(["Rename","Cancel"],press,3,0,2)

fileMenus = ["Config", "Info","-", "Close"]
app.addMenuList("File",fileMenus,menuPress)

app.setEntryFocus("linefile")

app.startSubWindow("config",modal=True,blocking=True)
app.addLabel("pfix","Raw image prefix: ",1,0)
app.addEntry("pfix",1,1)
app.setEntry("pfix", prefix)

app.addLabel("ofset","Spreadsheet header row: ",2,0)
app.addEntry("ofset",2,1)
app.setEntry("ofset", str(offset))

app.addLabel("namcol","Tx name column: ",3,0)
app.addEntry("namcol",3,1)
app.setEntry("namcol", namecol)

app.addLabel("txco","Tx pic column: ",4,0)
app.addEntry("txco",4,1)
app.setEntry("txco", txcol)

app.addLabel("plateco","Plate pic column: ",5,0)
app.addEntry("plateco",5,1)
app.setEntry("plateco", platecol)

app.addButton("Defaults",press,6,0,1)
app.addButton("OK",press,7,0,1)
app.addButton("Apply",press,7,1,1)
app.addNamedButton("Cancel","cancelconf",press,7,2,1)
app.setIcon("config.ico")
app.stopSubWindow()
app.hideSubWindow("config")

app.startSubWindow("info",modal=True,blocking=True)
app.addMessage("infostuff","(c) Christopher Logan, 2017\n \
             This program is intended only for use in renaming  \
             raw data in the transformer data collection project.\n\n \
             Report any bugs or requests to clogan@nbpower.com.")
app.setIcon("icon.ico")
app.stopSubWindow()
app.hideSubWindow("info")
app.setIcon("icon.ico")
app.addEmptyLabel("progress")
app.go()
