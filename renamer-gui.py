from __future__ import print_function   # (for when i use py 2 )
import renamethings
import os.path
from renamethings import renstuff
from dupecheck import check_duplicates
from appJar import gui
### tk for python 2.7

from Tkinter import *
import tkFileDialog          
###

## Tk for python 3.xx
#from tkinter import Tk             
#from tkinter.filedialog import askopenfilename
#from tkinter.filedialog import askdirectory
##

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
        filename = tkFileDialog.askopenfilename(filetypes=(("Excel Spreadsheet", "*.xlsx"), \
                                    ("Excel Macro Spreadsheet", "*.xlsm"),("All Files","*.*") )) # show an "Open" dialog box and return the path to the selected file
        app.setEntry("linefile",filename)
        
    elif(btn=="Rename"):
        app.setLabel("status","Renaming... be patient")
        if(os.path.isfile(app.getEntry("linefile"))and os.path.isdir(app.getEntry("workdir"))):
            errs=renstuff(app.getEntry("linefile"),app.getEntry("workdir"),namecol,platecol,txcol,prefix,int(offset))
            
            app.setLabel("status","Idle")
            if not all(l is '' for l in errs):
                errs='\n'.join(errs)
                app.setMessage("dupelist",errs)
                app.showSubWindow("dupew")
            else:
                app.setMessage("dupelist","No Renaming errors.\n")
                app.showSubWindow("dupew")
        elif(os.path.isfile(app.getEntry("linefile"))and not os.path.isdir(app.getEntry("workdir"))):
           app.warningBox("error", "Photo path does not exist")
        elif(not os.path.isfile(app.getEntry("linefile"))and os.path.isdir(app.getEntry("workdir"))):
           app.warningBox("error", "Spreadsheet does not exist")
        elif(not os.path.isfile(app.getEntry("linefile"))and not os.path.isdir(app.getEntry("workdir"))):
           app.warningBox("error", "Spreadsheet and photo path do not exist")

        app.setLabel("status","Idle.")
        
    elif(btn=="work dir"):
        Tk().withdraw()
        direct=tkFileDialog.askdirectory()
        app.setEntry("workdir",direct)
        
    elif(btn=="Check Duplicates"):
        if not app.getEntry("linefile"):
            app.setLabel("status","Pick a spreadsheet first!")
        else:
            app.setLabel("status","Checking for duplicate numbers.")
            if(not os.path.isfile(app.getEntry("linefile"))):
                app.warningBox("error", "Spreadsheet does not exist")
                app.setLabel("status","Error, check spreadsheet path")
            else:
                v=check_duplicates(app.getEntry("linefile"), txcol, platecol, namecol, int(offset))
                app.setLabel("status","Idle")
                if not all(l is '' for l in v):
                    v='\n'.join(v)
                    app.setMessage("dupelist",v)
                    app.showSubWindow("dupew")
                else:
                    app.setMessage("dupelist","No Duplicates Found!\n")
                    app.showSubWindow("dupew")
                
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

#
###################################################

### Loading the configuration on start, OR writing the default configuration if config.txt doesnt exist
if os.path.isfile('config.txt'):
    
    with open('config.txt','r') as cfg:     #if the config file does exist, great! open and parse its values
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
    cfg=open('config.txt','w+')             #If the config doesn't exist, write the default values to it
    offset = 2
    prefix='IMG_0000'
    namecol='A'
    txcol='L'
    platecol='M'
    cfg.write(str(offset)+'\n'+prefix+'\n'+namecol+'\n'+txcol+'\n'+platecol)
    cfg.close()
    
###### END of configuration code

################################
# GUI LAYOUT CODE               #
# Lots of room for improvement  #
# Basically just init code..    #
################################

app=gui(title="Photo-Renamer")

### fillings for MAIN WINDOW

app.addLabel("title","Transformer Survey Photo Renamer",0,0,2)
#row 0, col 0, span of 2   (format of the locating and sizing convention)

## Spreadsheet selection widgets
app.addLabel("linefile","Spreadsheet Path",1,0)
app.addEntry("linefile",1,1)
app.addButton("Browse",press,1,2)

## Source photo selection widgets
app.addLabel("workdir","Raw Photo Directory: ",2,0)
app.addEntry("workdir",2,1)
app.addButton("work dir",press,2,2)

## Buttons.... Yep
app.addButtons(["Rename","Check Duplicates","Cancel"],press,3,0,3)

## Label to put status remarks at later
app.addEmptyLabel("status",5,1)
fileMenus = ["Config", "Info","-", "Close"]
app.addMenuList("File",fileMenus,menuPress)

## Set the cursor to begin at the spreadsheet entry
# (As if anyone is ever going to type in by hand, but it's an option)
app.setEntryFocus("linefile")

### END of fillings for main window

## Config Widgets - Each group of widgets is a single setting
app.startSubWindow("config",modal=True,blocking=True)

# image prefix widgets
app.addLabel("pfix","Raw image prefix: ",1,0)
app.addEntry("pfix",1,1)
app.setEntry("pfix", prefix)

# spreadsheet header row/offset widgets
app.addLabel("ofset","Spreadsheet header row: ",2,0)
app.addEntry("ofset",2,1)
app.setEntry("ofset", str(offset))

# transformer name column widgets
app.addLabel("namcol","Tx name column: ",3,0)
app.addEntry("namcol",3,1)
app.setEntry("namcol", namecol)

# Transformer picture number widgets
app.addLabel("txco","Tx pic column: ",4,0)
app.addEntry("txco",4,1)
app.setEntry("txco", txcol)

# Transformer plate picture number widgets
app.addLabel("plateco","Plate pic column: ",5,0)
app.addEntry("plateco",5,1)
app.setEntry("plateco", platecol)

# Config page buttons
app.addButton("Defaults",press,6,0,1)
app.addButton("OK",press,7,0,1)
app.addButton("Apply",press,7,1,1)
app.addNamedButton("Cancel","cancelconf",press,7,2,1)       # This one is required since there is already a button called cancel.
                                                            # keep this function in mind.

#app.setIcon("config.ico")                                  # Setting the icon of the config window.. uncomment as soon as packaging the icons is figured out.. not major.
app.stopSubWindow()                                         # End of widget declarations for this subwindow.
app.hideSubWindow("config")                                 # Hide the window immediately (I believe it needs to be shown explicitly to display anyways, but just in case.)

app.startSubWindow("info",modal=True,blocking=True)         # Start the info page.. Nothing terribly complex here
app.addMessage("infostuff","(c) Christopher Logan, 2017\n \
             This program is intended only for use in renaming  \
             raw data in the transformer data collection project.\n\n \
             Report any bugs or requests to clogan@nbpower.com.")

#app.setIcon("icon.ico")                                    # Same icon stuff as before.
app.stopSubWindow()                                                 
app.hideSubWindow("info")                                   # End of info window

### Duplicate results window, shows only results of duplicate checking...
app.startSubWindow("dupew",title="Status Window")


#app.setIcon("icon.ico")
app.setGeometry(400, 400)
app.startScrollPane("dupe")                                 # The entire subwindow's widgets are contained within the scrollpane. because it'll have to scroll down hopefully
app.addEmptyMessage("dupelist")                             # Empty message that will hopefully cause it to scroll a lot if necessary
app.stopScrollPane()

app.setResizable(canResize=False)

app.stopSubWindow()                                     
app.hideSubWindow("dupew")                                  

#app.setIcon("icon.ico")                                    # Icon for the main window.. doesn't work when packed yet.
app.go()
