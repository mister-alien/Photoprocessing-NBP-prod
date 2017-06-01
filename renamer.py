from openpyxl import Workbook
from openpyxl import load_workbook

ind=0
offset = 2

namecol='A'
txcol='D'
platecol='E'

wb = load_workbook('Line_1234.xlsx')
ws=wb.active
a=ws[platecol +str(offset+ind)]
print(a.value)
print(a.value ==None)
