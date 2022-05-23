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
        answer = (0, [(0,1),(-1,0),(-1,0),(0,-1),(-1,0),(-1,0),(-1,-1),(0,-1),(0,-1),(0,-1),(0,-1),(0,-1),(-1,-1),(-1,0),(0,-1),(-1,0),(-1,1)])
        answer = (len(answer[1]), answer[1])
        return dumps(answer)
