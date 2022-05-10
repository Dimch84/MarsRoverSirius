from flask import Flask, request
from json import dumps, loads
from src.a_star import A_star

app = Flask(__name__)


@app.route("/", methods=['POST'])
def get_solution():
    form = loads(request.json)
    return dumps(A_star.call(form['start'], form['goal'], form['field']))
