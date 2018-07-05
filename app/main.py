from flask import Flask
from flask import Response
from flask import render_template
from flask import request
import socket
import json
import random
import redis
import os

app = Flask(__name__)
r = redis.StrictRedis(host=os.environ['REDIS_IP'], port=int(os.environ['REDIS_PORT']), db=0)


def authenticate():
	return Response(
		'Could not verify your access level for that URL.\n'
		'You have to login with proper credentials', 401,
		{'WWW-Authenticate': 'Basic realm="Login Required"'})

@app.route("/")
def main():
	r.set("foo", "bar")
	print(r.get("foo"))
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
