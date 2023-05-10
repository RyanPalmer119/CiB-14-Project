def export_testing_Report(data, file, app_name):
    workbook = load_workbook(filename="static/app_documents/doc_templates/blank_testing_report.xlsx")
    sheet = workbook.active
    start_row = 6
    for row in data:
        sheet["D" + str(start_row)] = app_name
        sheet["E" + str(start_row)] = row[2]
        sheet["F" + str(start_row)] = row[3]
        sheet["G" + str(start_row)] = row[4]
        sheet["H" + str(start_row)] = row[5]
        sheet["I" + str(start_row)] = row[5]
        sheet["J" + str(start_row)] = row[6]
        sheet["K" + str(start_row)] = row[7]
        sheet["L" + str(start_row)] = row[8]
        start_row = start_row + 1
    for column_cells in sheet.columns:
        new_column_length = max(len(as_text(cell.value)) for cell in column_cells)
        new_column_letter = (get_column_letter(column_cells[0].column))
        if new_column_length > 0:
            sheet.column_dimensions[new_column_letter].width = new_column_length + 3
    workbook.save(filename="static/app_documents/" + app_name + "/temp.xlsx")

