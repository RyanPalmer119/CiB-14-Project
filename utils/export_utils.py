from openpyxl import load_workbook
from openpyxl.utils import get_column_letter
import os

def as_text(value):
    if value is None:
        return ""
    return str(value)

def export_testing_Report(headers, data, app_name):
  workbook = load_workbook(filename="static/app_documents/doc_templates/blank_testing_report.xlsx")
  sheet = workbook.active
  start_row = 6
  sheet["E5"] = headers[0]
  sheet["F5"] = headers[1]
  sheet["G5"] = headers[2]
  sheet["H5"] = headers[3]
  sheet["I5"] = headers[4]
  sheet["J5"] = headers[5]
  sheet["K5"] = headers[6]
  sheet["L5"] = headers[7]
  for row in data:
      sheet["D" + str(start_row)] = app_name
      sheet["E" + str(start_row)] = row[0]
      sheet["F" + str(start_row)] = row[1]
      sheet["G" + str(start_row)] = row[2]
      sheet["H" + str(start_row)] = row[3]
      sheet["I" + str(start_row)] = row[4]
      sheet["J" + str(start_row)] = row[5]
      sheet["K" + str(start_row)] = row[6]
      sheet["L" + str(start_row)] = row[7]
      start_row = start_row + 1
  for column_cells in sheet.columns:
      new_column_length = max(len(as_text(cell.value)) for cell in column_cells)
      new_column_letter = (get_column_letter(column_cells[0].column))
      if new_column_length > 0:
          sheet.column_dimensions[new_column_letter].width = new_column_length + 3
  path = 'static/app_documents/' + app_name
  if(os.path.exists(path)):
    workbook.save(filename =  path + "/temp.xlsx")
  else:
    new_folder = os.path.join(path, app_name)
    os.mkdir(new_folder)
    workbook.save(filename = new_folder + "/temp.xlsx")


def export_updated_TRAP(data, appname):
  pass