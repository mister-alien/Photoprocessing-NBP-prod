from openpyxl import Workbook
from openpyxl import load_workbook
import os, shutil
def renstuff( spreadsheet, directory, namecol, platecol, txcol, prefix, offset ):
   # offset = 2
   # prefix='IMG0000'
   # namecol='A'
   # txcol='D'
   # platecol='E'
   
    Tri=None
   

    wb = load_workbook(spreadsheet)
    ws=wb.active
    #a=ws[platecol +str(offset+ind)]
    n= ws.max_row

    if not os.path.exists('processed'):
        os.makedirs('processed')
    for x in range(1,n-offset):
        name=ws[namecol +str(offset+x)]
        platenum=ws[platecol +str(offset+x)]
        txnum=ws[txcol +str(offset+x)]
        print(name.value)
        if (platenum.value) and (txnum.value):
            shutil.copyfile(directory+'\\raw\\'+prefix[0:(len(prefix)-len(str(platenum.value)))]+str(platenum.value)+'.jpg',directory+'\\processed\\'+name.value+' P.jpg')
#           os.rename('raw\\'+prefix[0:(len(prefix)-len(str(platenum.value)))]+str(platenum.value)+'.jpg',name.value+' P.jpg')
            shutil.copyfile(directory+'\\raw\\'+prefix[0:(len(prefix)-len(str(txnum.value)))]+str(txnum.value)+'.jpg',directory+'\\processed\\'+name.value+' T.jpg')

#            os.rename('raw\\'+prefix[0:(len(prefix)-len(str(txnum.value)))]+str(txnum.value)+'.jpg',name.value+' T.jpg')
        elif (txnum.value) and (platenum.value == None):
            Tri='R'
            shutil.copyfile(directory+'\\raw\\'+prefix[0:(len(prefix)-len(str(txnum.value)))]+str(txnum.value)+'.jpg',directory+'\\processed\\'+name.value+' T.jpg')

#            os.rename('raw\\'+prefix[0:(len(prefix)-len(str(txnum.value)))]+str(txnum.value)+'.jpg',name.value+' T.jpg')
        elif (txnum.value == None) and platenum.value:
            if Tri=='R':
#               os.rename('raw\\'+prefix[0:(len(prefix)-len(str(platenum.value)))]+str(platenum.value)+'.jpg',name.value+'.jpg')
                shutil.copyfile(directory+'\\raw\\'+prefix[0:(len(prefix)-len(str(platenum.value)))]+str(platenum.value)+'.jpg',directory+'\\processed\\'+name.value+'.jpg')
                Tri = 'C'
            elif Tri=='C':
#               os.rename('raw\\'+prefix[0:(len(prefix)-len(str(platenum.value)))]+str(platenum.value)+'.jpg',name.value+'.jpg')
                shutil.copyfile(directory+'\\raw\\'+prefix[0:(len(prefix)-len(str(platenum.value)))]+str(platenum.value)+'.jpg',directory+'\\processed\\'+name.value+'.jpg')

                Tri = 'F'
            elif Tri=='F':
#                os.rename('raw\\'+prefix[0:(len(prefix)-len(str(platenum.value)))]+str(platenum.value)+'.jpg',name.value+'.jpg')
                shutil.copyfile(directory+'\\raw\\'+prefix[0:(len(prefix)-len(str(platenum.value)))]+str(platenum.value)+'.jpg',directory+'\\processed\\'+name.value+'.jpg')

                Tri = None
    return
