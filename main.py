""" Main Python File -- RUN THIS TO START APP"""
PROXY = False
PROD_MODE = False
# Import Dependencies
from flask import Flask, request, render_template, redirect, jsonify  # Flask Imports
from utils.verify import verify_true_user  # Import utility modules
from utils import export_utils
import json

import logging
if PROXY:
    from werkzeug.middleware.proxy_fix import ProxyFix

logs = logging.getLogger("application")
logs.setLevel(logging.DEBUG)
file = logging.FileHandler("logs/application.log")
format = logging.Formatter(
    "%(asctime)s | %(levelname)s | %(name)s - %(message)s")
file.setFormatter(format)
logs.addHandler(file)


# Initiate Flask App
app = Flask(
    __name__,
    static_folder="static",
)  # Serve the *static* folder as a static source

# Load Additional Routes - Adds these to the current App
from routes import db_routes, login_routes, app_routes, logs_route
from utils.db_handler import get_all_app_names, get_upcoming_tests, get_app_overview, get_testing_entries, get_app, is_app_compliant, get_upcoming_traps, get_app_assignees, get_staff_name, get_trap, get_dc_tests, get_notifs

@app.route("/")
def index():
    """ Main App Route """
    # Get cookie data
    if PROD_MODE:
        valid_user = verify_true_user(request, logs)
        if valid_user[1] == 200:
            name, role = valid_user[0]
            match role:
                case "app":
                    return redirect("/app")
                case "op":
                    return redirect("/op")
                case "res":
                    return redirect("/res")
        else:
            return redirect("/login")
    else:
        valid_user = ("TEST USER", "TEST ROLE"), 200
        name, role = valid_user[0]
        return render_template("app.html", username=name, role=role)


# || == == == == APP STAFF SECTION == == == == ||

@app.route("/app")
def app_dashboard():
    """ Login Page Route """
    if PROD_MODE:
        user = verify_true_user(request, logs)
        print(user)
        if user[1] == 200:
            name, role = user[0]
            match role:
                case "Application":
                    pass
                case "Operate":
                    return redirect("/op")
                case "Resiliency":
                    return redirect("/res")
        else:
            return redirect("/")

    src_ip = request.remote_addr
    logs.info(f"{src_ip} - Accessed App Dash as {name if PROD_MODE else 'PROD'}")
    
    applications = get_all_app_names()
    upcoming_tests = get_upcoming_tests()
    upcoming_traps = get_upcoming_traps()
    return render_template("app_team/dash.html", applications=applications, upcoming_tests=upcoming_tests, upcoming_traps=upcoming_traps)

@app.route("/app/details/<app_id>")
def app_team_details(app_id):
    """ Application Team App Details """
    if PROD_MODE:
        user = verify_true_user(request, logs)
        print(user)
        if user[1] == 200:
            name, role = user[0]
            match role:
                case "Application":
                    pass
                case "Operate":
                    return redirect("/op")
                case "Resiliency":
                    return redirect("/res")
        else:
            return redirect("/")

    src_ip = request.remote_addr
    logs.info(f"{src_ip} - Accessed App Details Page for {app_id} as {name if PROD_MODE else 'PROD'}")
    return render_template("app_team/details.html", app_id=app_id)

# || == == == == RESILIENCY STAFF SECTION == == == == ||

@app.route("/res")
def res_dashboard():
    """ Login Page Route """
    if PROD_MODE:
        user = verify_true_user(request, logs)
        print(user)
        if user[1] == 200:
            name, role = user[0]
            match role:
                case "Application":
                    return redirect("/app")
                case "Operate":
                    return redirect("/op")
                case "Resiliency":
                    pass
        else:
            return redirect("/")
    
    src_ip = request.remote_addr
    logs.info(f"{src_ip} - Accessed Res Page as {name if PROD_MODE else 'PROD'}")
    apps = get_app_overview()
    compliance = []
    for app in apps:
        compliance.append(is_app_compliant(app[0]))
    apps_compliance = zip(apps, compliance)

    dc_tests = []
    all_dc_tests = get_dc_tests()[0:3]
    for test in all_dc_tests:
        # test_id, data_center, date, complete, result, evidence
        test_id, _, date, complete, result, _ = test
        dc_tests.append({
            "id": test_id,
            "date": date,
            "complete": complete == "1",
            "result": result == "1"
        })
    

    return render_template("res_team/dash.html", apps=apps_compliance, dc_tests=dc_tests, compliant=compliance.count(True), noncompliant=compliance.count(False))

@app.route("/res/details/<app_id>")
def res_details(app_id):
    """ Resiliency App Details Route """
    if PROD_MODE:
        user = verify_true_user(request, logs)
        print(user)
        if user[1] == 200:
            name, role = user[0]
            match role:
                case "Application":
                    return redirect("/app")
                case "Operate":
                    return redirect("/op")
                case "Resiliency":
                    pass
        else:
            return redirect("/")
    
    src_ip = request.remote_addr
    logs.info(f"{src_ip} - Accessed Res Details Page for {app_id} as {name if PROD_MODE else 'PROD'}")
    app_raw = get_app(app_id)[0]
    # app_id, app_name, primary_location, alt_location, data_center_id, trap_approved, trap_id
    _, _, trap_date_created, trap_status, _, _, _ = get_trap(app_raw[6])
    allTests = []
    testList = get_testing_entries(app_id, None, None)
    for test in testList:
        app_test_id, _, test_date, scenario, _, _, _, _, test_result = test
        allTests.append({"id": app_test_id, "date": test_date, "scenario": scenario, "result": test_result == "1"})
    
    
    app_1, app_2, op_1, op_2 = get_app_assignees(app_id)
    app = {
        "id": app_raw[0],
        "name": app_raw[1],
        "primary_location": app_raw[2],
        "alt_location": app_raw[3],
        "data_center_id": app_raw[4],
        "trap": {
            "id": app_raw[6],
            "approved_str": app_raw[5],
            "approved_bool": is_app_compliant(app_id),
            "date": trap_date_created
        },
        "app_1": {
            "id": app_1,
            "name": get_staff_name(app_1),
        },
        "app_2": {
            "id": app_2,
            "name": get_staff_name(app_2),
        },
        "op_1": {
            "id": op_1,
            "name": get_staff_name(op_1),
        },
        "op_2": {
            "id": op_2,
            "name": get_staff_name(op_2),
        },
        "tests": allTests
    }
    
    return render_template("res_team/detail.html", app=app)
    
@app.route("/res/tests/<app_id>")
def res_test_route(app_id):
    if PROD_MODE:
        user = verify_true_user(request, logs)
        print(user)
        if user[1] == 200:
            name, role = user[0]
            match role:
                case "Application":
                    return redirect("/app")
                case "Operate":
                    return redirect("/op")
                case "Resiliency":
                    pass
        else:
            return redirect("/")

    app_raw = get_app(app_id)[0]
    app_1, app_2, op_1, op_2 = get_app_assignees(app_id)
    app = {
        "id": app_raw[0],
        "name": app_raw[1],
        "primary_location": app_raw[2],
        "alt_location": app_raw[3],
        "app_1": {
            "id": app_1,
            "name": get_staff_name(app_1),
        },
        "app_2": {
            "id": app_2,
            "name": get_staff_name(app_2),
        },
        "op_1": {
            "id": op_1,
            "name": get_staff_name(op_1),
        },
        "op_2": {
            "id": op_2,
            "name": get_staff_name(op_2),
        },
    }

    src_ip = request.remote_addr
    logs.info(f"{src_ip} - Accessed Res Tests Page for {app_id} as {name if PROD_MODE else 'PROD'}")
    
    return render_template("res_team/tests.html", app=app)
    

# || == == == == RESILIENCY STAFF SECTION == == == == ||

@app.route("/op")
def op_dash():
    if PROD_MODE:
        user = verify_true_user(request, logs)
        print(user)
        if user[1] == 200:
            name, role = user[0]
            match role:
                case "Application":
                    return redirect("/app")
                case "Operate":
                    pass
                case "Resiliency":
                    return redirect("/res")
        else:
            return redirect("/")

    src_ip = request.remote_addr
    logs.info(f"{src_ip} - Accessed Op Dash as {name if PROD_MODE else 'PROD'}")
    return render_template("op_team/dash.html")

@app.route("/op/app/<app_id>")
def op_app(app_id):
    if PROD_MODE:
        user = verify_true_user(request, logs)
        print(user)
        if user[1] == 200:
            name, role = user[0]
            match role:
                case "Application":
                    return redirect("/app")
                case "Operate":
                    pass
                case "Resiliency":
                    return redirect("/res")
        else:
            return redirect("/")


    app_raw = get_app(app_id)[0]
    # app_id, app_name, primary_location, alt_location, data_center_id, trap_approved, trap_id
    _, _, trap_date_created, trap_status, _, _, _ = get_trap(app_raw[6])
    allTests = []
    testList = get_testing_entries(app_id, None, None)
    for test in testList:
        app_test_id, _, test_date, scenario, _, _, _, _, test_result = test
        allTests.append({"id": app_test_id, "date": test_date, "scenario": scenario, "result": test_result == "1"})
    
    
    app_1, app_2, op_1, op_2 = get_app_assignees(app_id)
    
    app = {
        "id": app_raw[0],
        "name": app_raw[1],
        "primary_location": app_raw[2],
        "alt_location": app_raw[3],
        "data_center_id": app_raw[4],
        "trap": {
            "id": app_raw[6],
            "approved_str": app_raw[5],
            "approved_bool": is_app_compliant(app_id),
            "date": trap_date_created
        },
        "app_1": {
            "id": app_1,
            "name": get_staff_name(app_1),
        },
        "app_2": {
            "id": app_2,
            "name": get_staff_name(app_2),
        },
        "op_1": {
            "id": op_1,
            "name": get_staff_name(op_1),
        },
        "op_2": {
            "id": op_2,
            "name": get_staff_name(op_2),
        },
        "tests": allTests
    }

    src_ip = request.remote_addr
    logs.info(f"{src_ip} - Accessed Op Details for {app_id} as {name if PROD_MODE else 'PROD'}")
    return render_template("res_team/detail.html", app=app)



@app.route("/admin")
def admin():
    return render_template("admin.html")

@app.route("/trap_viewer/<app_id>")
def trapview(app_id):
    app_raw = get_app(app_id)[0]
    app = {
        "id": app_raw[0],
        "name": app_raw[1],
    }
    src_ip = request.remote_addr
    logs.info(f"{src_ip} - Accessed TRAP for {app_id}")
    return render_template("trapview.html", app=app)

@app.route("/notifs/<user_id>")
def notifs(user_id):
    user_notifs = get_notifs(user_id)
    all_notifs = []
    for notif in user_notifs:
        all_notifs.append((get_staff_name(notif[0]), notif[0] , notif[1]))
    return json.dumps(all_notifs)

@app.route("/docs")
def docs_page():
    src_ip = request.remote_addr
    logs.info(f"{src_ip} - Accessed Docs")
    return render_template("docs/index.html")


if PROXY:
    app.wsgi_app = ProxyFix(app.wsgi_app,
                            x_for=1,
                            x_proto=1,
                            x_host=1,
                            x_prefix=1)

app.run(host='0.0.0.0', port=81)
