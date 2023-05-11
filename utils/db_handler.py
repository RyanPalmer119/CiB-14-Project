import sqlite3
import pandas as pd
import datetime
from datetime import timedelta

DB_NAME = "db.sqlite"

## NOTIFICATIONS TABLE CHANGED 'from' TO 'sender' 

schema = [
    """CREATE TABLE IF NOT EXISTS users(
    userID varchar(255) NOT NULL,
    username varchar(255) NOT NULL,
    name varchar(255) NOT NULL,
    hash varchar(255) NOT NULL,
    role varchar(255) NOT NULL,
    PRIMARY KEY(userID)
   );""",
    """ CREATE TABLE IF NOT EXISTS notifications (
        notification_id varchar(255) NOT NULL,
        too varchar(255) NOT NULL,
        sender varchar(255) NOT NULL,
        message varchar(255) NOT NULL,
        read varchar(255) NOT NULL,
        PRIMARY KEY(notification_id)
    );""",
    """ CREATE TABLE IF NOT EXISTS applications (
        app_id varchar(255) NOT NULL,
        app_name varchar(255) NOT NULL,
        primary_location varchar(255) NOT NULL,
        alt_location varchar(255) NOT NULL,
        data_center_id varchar(255) NOT NULL,
        trap_approved varchar(255) NOT NULL,
        trap_id varchar(255) NOT NULL,
        PRIMARY KEY(app_id)
    ); """,
    """ CREATE TABLE IF NOT EXISTS app_staff_link (
        app_id varchar(255) NOT NULL,
        app_staff_1 varchar(255) NOT NULL,
        app_staff_2 varchar(255) NOT NULL,
        op_staff_1 varchar(255) NOT NULL,
        op_staff_2 varchar(255) NOT NULL
    ); """,
    """ CREATE TABLE IF NOT EXISTS app_tests (
        app_test_id varchar(255) NOT NULL,
        app_id varchar(255) NOT NULL,
        test_date varchar(255) NOT NULL,
        scenario varchar(255) NOT NULL,
        duration varchar(255) NOT NULL,
        source_location varchar(255) NOT NULL,
        target_location varchar(255) NOT NULL,
        test_evidence varchar(255),
        test_result varchar(255) NOT NULL,
        PRIMARY KEY(app_Test_ID)
    ); """,
    """ CREATE TABLE IF NOT EXISTS traps (
        trap_id varchar(255) NOT NULL,
        app_id varchar(255) NOT NULL,
        date_created varchar(255) NOT NULL,
        status varchar(255) NOT NULL,
        created_by varchar(255) NOT NULL,
        approved_by varchar(255) NOT NULL,
        location varchar(255) NOT NULL,
        PRIMARY KEY(trap_id)   
    ); """,
    """ CREATE TABLE IF NOT EXISTS data_center (
        data_center_id varchar(255) NOT NULL,
        location varchar(255) NOT NULL,
        contact varchar(255),
        PRIMARY KEY(data_center_id)
    );""",
    """ CREATE TABLE IF NOT EXISTS data_center_tests (
        test_id varchar(255) NOT NULL,
        data_center varchar(255) NOT NULL,
        date varchar(255) NOT NULL,
        complete varchar(255) NOT NULL,
        result varchar(255) NOT NULL,
        evidence varchar(255),
        PRIMARY KEY(test_id)
    );"""
]


default_data = [
    ["static/data/users.csv", "users"],     
    ['static/data/applications.csv', 'applications'], 
    ['static/data/app_staff_link.csv', 'app_staff_link'],   
    ['static/data/application_tests.csv', 'app_tests'], 
    ['static/data/traps.csv', 'traps'], 
    ['static/data/data_center.csv', 'data_center'], 
    ['static/data/data_center_tests.csv', 'data_center_tests'], 
    ["static/data/notifications.csv", "notifications"]
]

def create_schema():
    with sqlite3.connect(DB_NAME) as conn:
        for table in schema:
            conn.execute(table)
        return "200"

def test(table):
    with sqlite3.connect(DB_NAME) as conn:
        try:
            result = conn.execute(f"SELECT * FROM {table};").fetchall()
        except sqlite3.OperationalError:
            result = "404 Table not Found"
        return result

def reset_db(): 
    with sqlite3.connect(DB_NAME) as conn:
        tables = ["users", "notifications", "applications", "app_staff_link", "app_tests", "traps", "data_center", "data_center_tests"]
        for table in tables:
            try:
                conn.execute(f"DROP TABLE {table};")
            except sqlite3.OperationalError:
                pass
        
        create_schema()
        for csv_file in default_data:
          csv_import = pd.read_csv(csv_file[0])
          csv_import.to_sql(csv_file[1], con=conn, index=False, if_exists='append') 
    return "200"


def new_user(user_id, username, name, defined_hash, role):
    """ Creates a New User"""
    with sqlite3.connect(DB_NAME) as conn:
        result = conn.execute("INSERT INTO users(userID, username, name, hash, role) VALUES(?, ?, ?, ?, ?)", (user_id, username, name, defined_hash, role))
        return result.fetchall()


def get_passhash(username):
    with sqlite3.connect(DB_NAME) as conn:
        result = conn.execute("SELECT userID, role, hash FROM users WHERE username = ?;", (username,)).fetchall()
        if len(result) > 0: # If there is a value
            return result[0]
        else:
            return 500, "User doesnt exist"

def verify_user(userID):
    with sqlite3.connect(DB_NAME) as conn:
        result = conn.execute("SELECT username, hash, role FROM users WHERE userID = ?", (userID,)).fetchall()[0]
        if len(result) > 0:
            return (result[0], result[1], result[2])
        else:
            return 404
        

def is_username_taken(username):
    with sqlite3.connect(DB_NAME) as conn:
        result = conn.execute("SELECT userID FROM users WHERE username = ?", (username,)).fetchall()
        return len(result) > 0

def get_testing_entries(app_id, date_from, date_to):
  with sqlite3.connect(DB_NAME) as conn:
    if date_from is None and date_to is None :
        # app_test_id, app_id, test_date, scenario, duration, source_location, target_location, test_evidence, test_result
      result = conn.execute("SELECT * FROM app_tests WHERE app_id = ? ORDER BY test_date desc", (app_id,)).fetchall()
      return result
    else:
      result = conn.execute("SELECT * FROM app_tests WHERE app_ID = ? AND test_date > ? AND test_date < ? ORDER BY test_date desc", (app_id, date_from, date_to)).fetchall()
      return result

def get_tests_for_table(app_id):
  with sqlite3.connect(DB_NAME) as conn:
    pass
    # result = conn.execute("SELECT id test_date scenario result WHERE id = app_name ")

def get_all_app_names():
  with sqlite3.connect(DB_NAME) as conn:
    result = conn.execute("SELECT app_name FROM applications").fetchall()
    return result

# FOR DATES
today = datetime.datetime.now()

def get_upcoming_tests():
  with sqlite3.connect(DB_NAME) as conn:
    result = conn.execute("SELECT app_id, test_date FROM app_tests").fetchall()
    new_results = []
    for test in result:
      if test[1] > today.strftime('%Y-%m-%d'):
        new_results.append([test[0], test[1]])     
#     # # swap app_id for app_name!
    return new_results

def get_app_overview():
    with sqlite3.connect(DB_NAME) as conn:
        result = conn.execute("SELECT app_id, app_name, trap_approved FROM applications").fetchall()
        return result

def get_app(app_id):
    with sqlite3.connect(DB_NAME) as conn:
        # app_id, app_name, primary_location, alt_location, data_center_id, trap_approved, trap_id
        result = conn.execute("SELECT * FROM applications WHERE app_id = ?", (app_id,)).fetchall()
        return result

def is_app_compliant(app_id):
    """ Checks last test, as well as TRAP approval to ensure an app is compliant"""
    app_tests = get_testing_entries(app_id, None, None)
    if len(app_tests) < 1: # If no tests have been done in the time frame
        return False
    else: # If tests have been done
        # CHECK TEST DATES
        latest_test = app_tests[0]
        test_date = latest_test[2]
        years, months, days = test_date.split("-")
        if datetime.datetime(int(years), int(months), int(days)) < datetime.datetime.now() - timedelta(days=365): # If the last test was more than a year ago
            return False
        if latest_test[8] == "0": # If last test was a fail 
            return False
    
        # CHECK TRAP APPROVAL
        with sqlite3.connect(DB_NAME) as conn:
            result = conn.execute("SELECT trap_approved FROM applications WHERE app_id = ?", (app_id,)).fetchall()
            if result[0][0] == "No": # If the trap is not approved
                return False
            else:
                return True

def get_app_assignees(app_id):
    with sqlite3.connect(DB_NAME) as conn:
        result = conn.execute("SELECT app_staff_1, app_staff_2, op_staff_1, op_staff_2 FROM app_staff_link WHERE app_id = ?", (app_id,)).fetchall()[0]
        return result
    
def get_staff_name(user_id):
    with sqlite3.connect(DB_NAME) as conn:
        result = conn.execute("SELECT name FROM users WHERE userID = ?", (user_id,)).fetchall()[0][0]
        return result 

def get_trap(trap_id):
    with sqlite3.connect(DB_NAME) as conn:
        # trap_id, app_id, date_created, status, created_by, approved_by, location
        result = conn.execute("SELECT * FROM traps WHERE trap_id = ?", (trap_id,)).fetchall()[0]
        return result
      
def get_upcoming_traps():
  renew_start = today-timedelta(days=273)
  renew_end = today-timedelta(days=366)
  with sqlite3.connect(DB_NAME) as conn:
    result = conn.execute("SELECT trap_id, app_id, date_created FROM traps").fetchall()
    new_results = []
    for trap in result:
      if trap[2] < renew_start.strftime('%Y-%m-%d') and trap[2] > renew_end.strftime('%Y-%m-%d'):
        new_results.append([trap[0], trap[1], trap[2]])     
    return new_results

def get_dc_tests():
    # test_id, data_center, date, complete, result, evidence
    with sqlite3.connect(DB_NAME) as conn:
        result = conn.execute("SELECT * FROM data_center_tests ORDER BY date desc").fetchall()
        return result

def get_notifs(user_id):
    with sqlite3.connect(DB_NAME) as conn:
        result = conn.execute("SELECT sender, message FROM notifications WHERE too = ?", (user_id,)).fetchall()
        return result