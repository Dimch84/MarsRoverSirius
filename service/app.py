from flask import Flask, request
from json import dumps, loads
from src.a_star import A_star

app = Flask(__name__)

fields = {}


def f(array: [[int]]):
    string_array = []
    for subarray in array:
        string_array.append(''.join(map(str, subarray)))
    return string_array


@app.route('/maps/', methods=['GET', 'POST'])
def process_maps():
    if request.method == 'POST':
        field = loads(request.json)
        field_name = field['name']
        fields[field_name] = field
        return str(len(fields) - 1)
    if request.method == 'GET':
        return dumps(fields)


@app.route('/maps/<field_name>', methods=['GET'])
def get_solution(field_name):
    if field_name not in fields:
        return 'Unknown map name'
    field = fields[field_name]
    return dumps(A_star.call(field['start'], field['finish'], f(field['field'])))
