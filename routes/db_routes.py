""" Database Test Routes 
Holds all of the website endpoints that relate to raw database manipulation, i.e. creating the db schema, inputting test data, retrieving user data, 
"""
from __main__ import app
from flask import request
from utils.db_handler import test, create_schema, reset_db, verify_user, get_passhash
import logging
import json

""" Setup Logging Function"""
logs = logging.getLogger("db")
logs.setLevel(logging.DEBUG)
file = logging.FileHandler("logs/db.log")
format = logging.Formatter("%(asctime)s | %(levelname)s | %(name)s - %(message)s")
file.setFormatter(format)
logs.addHandler(file)

@app.route("/db/test")
def test_db():
    """ Runs the handler test function - Returns all data in the user table """
    src_ip = request.remote_addr
    logs.debug(f"{src_ip} - DB Test")
    result = []
    tables = ["users", "notifications", "applications", "app_staff_link", "app_tests", "traps", "data_center", "data_center_tests"]
    for table in tables: 
        print(table)
        result.append(test(table))
    return result

@app.route("/db/create_schema")
def create_db_schema():
    """ Initiates the Database with the Table Schema"""
    src_ip = request.remote_addr
    logs.critical(f"{src_ip} - Created Schema")
    return create_schema()

@app.route("/db/reset")
def reset_db_route():
    """ Deletes the DB, then re-initiates it with test data as well as the schema"""
    src_ip = request.remote_addr
    logs.critical(f"{src_ip} - Reset the DB")
    return reset_db()

@app.route("/db/verify")
def verify_user_route():
    """ WIP: Tests the Verify_User Function"""
    src_ip = request.remote_addr
    logs.critical(f"{src_ip} - Verify User Route")
    return verify_user("")