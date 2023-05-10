from export_utils import export_testing_Report
from __main__ import app
from flask import request
import os


@app.route("/export_2_excel")
def export_test_report(app_name):
  if request.method == "GET":
    data = get_all_tests(app_id)
    export_testing_Report(data, app_name)
  return "Excel Report Downloaded"
  
@app.route('/return_TRAP', methods=['GET'])
def return_trap(app_name):
    if request.method == "GET":
        site_root = os.path.realpath(os.path.dirname(__file__))
        trapFile = os.path.join(site_root, app_name, "trapExample.xlsx")
        trap_json = returnTRAP(trapFile)
    return trap_json

