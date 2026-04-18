from flask import render_template
from flask import Flask

app = Flask(__name__)


@app.route("/hello/")
@app.route("/hello/<name>")
def hello(name=None):
    return render_template("hello.html", person=name)


@app.route("/form")
def form_api():
    return {
        "lo": 0.0,
        "la": 35.7,
    }
