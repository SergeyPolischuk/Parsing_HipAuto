from openpyxl import load_workbook

wb = load_workbook('C:/Users/Sergey/Desktop/Book1.xlsx')
sheet = wb['Sheet1']

val = sheet['A1'].value

print(val)

# print(str(wb.get_sheet_names))