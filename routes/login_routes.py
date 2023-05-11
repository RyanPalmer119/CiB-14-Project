from __main__ import app
from utils import hash_utils, db_handler
from flask import request, render_template
import json
from uuid import uuid4
import logging


""" Setup Logging Function """
logs = logging.getLogger("login")
logs.setLevel(logging.DEBUG)
file = logging.FileHandler("logs/login.log")
format = logging.Formatter("%(asctime)s | %(levelname)s | %(name)s - %(message)s")
file.setFormatter(format)
logs.addHandler(file)



@app.route("/login")
def login_page():
    """ Login Page Route """
    src_ip = request.remote_addr
    logs.info(f"{src_ip} - Accessed Login Page")
    return render_template("login.html")

@app.route("/signup")
def signup_page():
    """ Login Page Route """
    src_ip = request.remote_addr
    logs.info(f"{src_ip} - Accessed Signup Page")
    return render_template("signup.html")


# ||== API ROUTES FOR LOGIN ==||

@app.route("/api/login", methods=["POST"])
def api_login_test():
    """ Log In a User """
    body = json.loads(request.data) # Get Login Data
    src_ip = request.remote_addr # Get IP Address

    passhash = db_handler.get_passhash(body["username"]) # Get userID and Passhash from inputted Username
    if passhash[0] == 500:
        logs.warning(f"Login Unsuccessful for { body['username'] } from { src_ip } - Invalid Username")
        return "Username or Password is Incorrect", 400
    userID, role, user_pass_hash = passhash
    inputted_pass_hash = body["passhash"] # Get user inputted passhash
    
    if inputted_pass_hash == user_pass_hash: # If Valid
        logs.info(f"{ src_ip } Login Successful for { body['username'] }")
        return {"id": userID, "role": role}, 200 # Return UserID for UserID Cookie
    else: 
        # Invalid Login
        logs.warning(f"{ src_ip }Login Unsuccessful for { body['username'] } from { src_ip }")
        return "Username or Password is Incorrect", 400

@app.route("/api/new_user", methods=["POST"])
def create_new_user():
    """ Create a New User"""
    # Get all the variables
    body = json.loads(request.data)
    username = body["username"]
    name = body["name"]
    passhash = body["passhash"]
    role = body["role"]
    src_ip = request.remote_addr
    logs.warning(f"{ src_ip } Attempting: Create User {username} as {role}")

    
    try: 
        if db_handler.is_username_taken(username):
            logs.debug(f"{src_ip} used a taken username: {username} ")
            return "Username Taken", 400
        if not hash_utils.verify_is_a_hash(passhash): # If the passhash is in the correct format
            logs.debug(f"{src_ip} used a malformed request || not hashed")
            return "Not Hashed", 400
        new_uuid = str(uuid4())
        db_handler.new_user(new_uuid, username, name, passhash, role) # Create the new user
        logs.info(f"New User from {src_ip}: {new_uuid}, {username}, {role} || Successfully Added")
        return new_uuid, 200
    except Exception as err:
        logs.critical(f"An Error Occured:: {err}")
        print(err)
        return err, 500