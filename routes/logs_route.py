from __main__ import app
from flask import send_from_directory

@app.route('/logs/<path:path>')
def send_report(path):
    return send_from_directory('logs', path)
