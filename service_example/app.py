from flask import Flask, request
from json import dumps, loads
from src.a_star import A_star

from utils import f

app = Flask(__name__)


@app.route('/map/', methods=['GET', 'POST'])
def process_field():
    """
    This page allows to get a solution for the posted field.

    :return:
    """
    if request.method == 'POST':
        field = loads(request.json)
        return dumps(A_star.call(field['start'], field['finish'], f(field['field'])))
