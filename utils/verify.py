from flask import request
from . import db_handler, hash_utils

def verify_true_user(req, logs):
    """ Checks if a user is valid. In the route pass the `request` variable,  """
    sender_ip = request.remote_addr
    cookie = req.cookies.get("token")
    userID = req.cookies.get("userID")
    if cookie is None or userID is None:  # If cookies are not set
        logs.warning(f"{sender_ip} accessed /app without login")
        return "Cookies Not Set", 400
    else:  # If Cookies are set
        # Verify Cookies are correct
        """ COOKIE FORMAT: 
        userID: The UserID field in the Database
        token: the SHA256 Hash of the Username + Passhash
        """
        name, hash, role = db_handler.verify_user(
            userID)  # Verify is a User, and get User ID and passhash
        if name == "500":  # If user does not exist
            logs.warn(f"{sender_ip} : Invalid Username")
            return "Invalid Username", 400
        valid_token = hash_utils.hash_text(name + hash)
        if cookie != valid_token:  # If the cookies are not valid
            logs.error(f"{sender_ip} : Invalid Cookie using {userID}")
            return "Invalid Cookies", 400
    logs.info(f"{sender_ip} accessed as {userID}")
    return (name, role), 200