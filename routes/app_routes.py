from utils.export_utils import export_testing_Report, returnTRAP, exportTRAP
from utils.db_handler import get_testing_entries
from __main__ import app
from flask import request, send_file
import os
# import urllib.request

@app.route("/export_tests_to_excel", methods=['GET', 'POST'])
def export_test_report():
  if request.method == "POST":
    req = request.get_json()
    site_root = '/'.join(os.path.realpath(os.path.dirname(__file__)).split("/")[0:-1]) + "/static/app_documents"
    template_file = os.path.join(site_root, "doc_templates", "blank_testing_report.csv")
    path_4_export = os.path.join(site_root, req['app_name'], "test_report.csv")
    data = get_testing_entries(req['id'], None, None)
    export_testing_Report(data, req['app_name'], template_file, path_4_export)
    return path_4_export
  #   link = "https://replit.com/@theJMC/CiB-14-Project#static/app_documents/DWK-Depository/temp.csv"
  # return urllib.request.urlretrieve(link, "test.csv")
  # return send_file(path_4_export, download_name="download.csv", as_attachment=True)

@app.route('/return_TRAP/<app_name>', methods=['GET'])
def return_trap(app_name):
    if request.method == "GET":
      site_root = '/'.join(os.path.realpath(os.path.dirname(__file__)).split("/")[0:-1]) + "/static/app_documents"
      trapFile = os.path.join(site_root, app_name, "trapExample.xlsx")
      trap_json = returnTRAP(trapFile)
    return trap_json


@app.route("/export_TRAP", methods = ['POST', 'GET'])
def export_trap():
    if request.method == "POST":
        req = request.get_json()
        app_name = req['app_name']
        site_root = '/'.join(os.path.realpath(os.path.dirname(__file__)).split("/")[0:-1]) + "/static/app_documents/" + app_name
        path_4_export = os.path.join(site_root, "-trap.csv")
        exportTRAP(req['data'], path_4_export)
        return send_file(path_4_export, "download.csv", as_attachment=True)

@app.route("/dl_TRAP/<app_name>")
def dl_trap(app_name):
    site_root = '/'.join(os.path.realpath(os.path.dirname(__file__)).split("/")[0:-1]) + "/static/app_documents/" + app_name
    path_4_export = os.path.join(site_root, "-trap.csv")
    return send_file(path_4_export, "download.csv", as_attachment=True)
    
  
  # print(req['url'])
  # print(req['app_name'])