from flask import Flask
from flask import Response
from flask import render_template
from flask import request
import socket
import json
import random

app = Flask(__name__)

@app.route("/")
def main():
	hostname = socket.gethostbyname(socket.gethostname())
	if not "sessionId" in request.cookies:
		sessId = str(random.randint(100000, 999999))
	else:
		sessId = request.cookies["sessionId"]
	resp = Response(render_template("main.html", host = hostname, sessionId = sessId), mimetype="text/html")
	if not "sessionId" in request.cookies:
		resp.set_cookie("sessionId", sessId)
	return resp

@app.route("/health")
def health():
	return json.dumps({"health": "ok"})

if __name__ == "__main__":
	app.run(debug=True, host='0.0.0.0')
