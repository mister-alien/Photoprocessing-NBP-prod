from openpyxl import Workbook
from openpyxl import load_workbook

offset = 2
namecol='A'
wb = load_workbook('Line_1234.xlsx')
ws=wb.active
print(ws['A2'])
