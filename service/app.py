from flask import Flask, request
from json import dumps, loads
from src.a_star import A_star

from utils import f

app = Flask(__name__)

fields = {}


@app.route('/maps/', methods=['GET', 'POST'])
def process_fields():
    """
    This page allows to get the list of all the fields or post a new field.

    :return:
    """
    if request.method == 'POST':
        field = loads(request.json)
        field_name = field['name']
        fields[field_name] = field
        return 'OK'
    if request.method == 'GET':
        return dumps(fields)


@app.route('/maps/<field_name>', methods=['GET', 'DELETE'])
def process_field(field_name):
    """
    This page allows to get the solution for the chosen field or delete it.

    :param field_name: field name.
    :return:
    """
    if field_name not in fields:
        return 'Unknown map name'
    if request.method == 'DELETE':
        fields.pop(field_name)
        return 'OK'
    if request.method == 'GET':
        field = fields[field_name]
        return dumps(A_star.call(field['start'], field['finish'], f(field['field'])))
