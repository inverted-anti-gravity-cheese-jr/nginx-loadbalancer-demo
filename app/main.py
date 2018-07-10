from flask import Flask
from flask import Response
from flask import render_template
from flask import request
import socket
import json
import random
import redis
import os
import datetime

DATE_FORMAT = "%Y-%m-%d %H:%M:%S.%f"

app = Flask(__name__)
r = redis.StrictRedis(host=os.environ['REDIS_IP'], port=int(os.environ['REDIS_PORT']), db=0)


def authenticate():
	return Response(
		'Could not verify your access level for that URL.\n'
		'You have to login with proper credentials', 401,
		{'WWW-Authenticate': 'Basic realm="Login Required"'})

@app.route("/")
def main():
	hostname = socket.gethostbyname(socket.gethostname())
	sessionValid = False
	setCookie = False
	reauthorize = False
	if "sessionId" in request.cookies:
		try:
			sessId = request.cookies.get("sessionId")
			username = r.get(sessId)
			expiry = datetime.datetime.strptime(r.get(sessId + "-expire"), DATE_FORMAT).date()
			sessionValid = datetime.datetime.now() < expiry
			reauthorize = not sessionValid
		except:
			pass
	if not sessionValid:
		if reauthorize or not request.authorization or not request.authorization.username:
			return authenticate()
		sessId = str(random.randint(100000, 999999))
		date = str(datetime.datetime.now() + datetime.timedelta(seconds = 5))
		username = request.authorization.username
		r.set(sessId, username)
		r.set(sessId + "-expire", date)
		setCookie = True
	resp = Response(render_template("main.html", host = hostname, sessionId = username), mimetype="text/html")
	if setCookie:
		resp.set_cookie("sessionId", sessId)
	return resp

@app.route("/health")
def health():
	return json.dumps({"health": "ok"})

if __name__ == "__main__":
	app.run(debug=True, host='0.0.0.0')
