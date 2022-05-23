from flask import Flask, request
from json import dumps, loads
from src.lifelong_a_star import Lifelong_a_star
from src.launch_a_star import get_direction_path

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
        answer = Lifelong_a_star.call(field['start'], field['finish'], f(field['field']))
        answer = (answer[0], get_direction_path(answer[1]))
        return dumps(answer)
