from flask import Flask, request, jsonify
import spire
from typing import List
import requests


app = Flask(__name__)


@app.route('/search_area', methods=['POST'])
def search_area():
    creds = request.form
    query = request.args
    s = spire.Session(creds['user'], creds['password'], creds['spire_id'])
    result = s.search_area(query.get('area'), query.get('room_type'))
    if 'hook' in creds and result:
        return call_hook(result, creds['hook'])
    return jsonify(result)


def call_hook(rooms: List[dict], hook: str):
    formatted = ['%s %s' % (room['building'].capitalize(), room['number']) for room in rooms]
    out = ', '.join(formatted)
    requests.post(hook, data={'text': out})
    return out
