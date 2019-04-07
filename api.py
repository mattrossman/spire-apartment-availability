from flask import Flask, request, jsonify
import spire

app = Flask(__name__)

@app.route('/search_area', methods=['POST'])
def search_area():
    creds = request.form
    query = request.args
    s = spire.Session(creds['user'], creds['password'], creds['spire_id'])
    return jsonify(s.search_area(query.get('area'), query.get('room_type')))
