from flask import Flask, redirect

app = Flask(__name__, static_folder='', static_url_path='')

@app.route("/", methods=["GET"])
@app.route("/index", methods=["GET"])
def index():
	return  redirect("/index.html")
	
@app.route("/r", methods=["GET"])
def refresh():
	return  "nothing to do"

if __name__ == "__main__":
	app.run(port=80, debug = True)