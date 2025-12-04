import json
import os
from flask import Flask, jsonify, request, render_template, Response

app = Flask(__name__)

# Example data
data = [
    {"id": 1, "name": "Item A"},
    {"id": 2, "name": "Item B"}
]

@app.route('/', methods=['GET'])
def index():
    return render_template('/index.html')


def read_server_file(file_path):
    try:
        with open(file_path, encoding='utf-8-sig') as f:
            data = json.load(f)
            data = json.dumps(data, indent=4, ensure_ascii=False)
        return data
    except FileNotFoundError:
        return 'File not found.'


# GET all items
@app.route('/api/legal', methods=['GET'])
def get_items():
    data = read_server_file('output_article_only.json')
    return Response(data, mimetype='application/json')


# GET a specific item by ID
@app.route('/api/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    item = next((item for item in data if item['id'] == item_id), None)
    if item:
        return jsonify(item)
    return jsonify({"message": "Item not found"}), 404


# POST (create) a new item
@app.route('/api/items', methods=['POST'])
def create_item():
    new_item = request.json
    if new_item and 'name' in new_item:
        new_item['id'] = len(data) + 1
        data.append(new_item)
        return jsonify(new_item), 201
    return jsonify({"message": "Invalid item data"}), 400


if __name__ == '__main__':
    app.run(debug=False, port=8000)