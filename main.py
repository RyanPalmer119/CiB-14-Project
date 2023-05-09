""" Main Python File -- RUN THIS TO START APP"""
PROXY = False
# Import Dependencies
from flask import Flask, request, render_template, redirect  # Flask Imports
from utils import db_handler, hash_utils  # Import utility modules
import logging
if PROXY:
    from werkzeug.middleware.proxy_fix import ProxyFix

logs = logging.getLogger("app")
logs.setLevel(logging.DEBUG)
file = logging.FileHandler("logs/app.log")
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
from routes import db_routes, login_routes


def verify_true_user(req):
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


@app.route("/")
def index():
    """ Default Route - Serves Index.html"""
    sender_ip = request.remote_addr
    logs.info(f"{sender_ip} accessed /")
    return render_template("index.html")


@app.route('/app')
def app_route():
    """ Main App Route """
    # Get cookie data
    valid_user = verify_true_user(request)
    if valid_user[1] == 200:
        name, role = valid_user[0]
        return render_template("app.html", username=name, role=role)
    else:
        return redirect("/login")


if PROXY:
    app.wsgi_app = ProxyFix(app.wsgi_app,
                            x_for=1,
                            x_proto=1,
                            x_host=1,
                            x_prefix=1)

app.run(host='0.0.0.0', port=81)
