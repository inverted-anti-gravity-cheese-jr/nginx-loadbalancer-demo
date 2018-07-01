from flask import Flask
from flask import Response
from flask import render_template
import socket
import json

app = Flask(__name__)

@app.route("/")
def main():
	hostname = socket.gethostbyname(socket.gethostname())
	return Response(render_template("main.html", host = hostname), mimetype="text/html")

@app.route("/health")
def health():
	return json.dumps({"health": "ok"})

if __name__ == "__main__":
	app.run(debug=True, host='0.0.0.0')
