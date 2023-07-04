from flask import Flask, jsonify, request
from pymongo import MongoClient
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
client = MongoClient('mongodb://localhost:27017')
db = client['mydatabase']
collection = db['mycollection']

@app.route('/data', methods=['GET'])
def get_data():
    data = []
    cursor = collection.find()
    i = 0
    for document in cursor:
        i += 1
        document['_id'] = str(document['_id'])  # Convert ObjectId to string
        data.append(document)
        
        if i == 100:
            break
    
    symbol = request.args.get("symbol")
    if symbol:
        filtered_data = [item for item in data if item["symbol"] == symbol]
        return jsonify(filtered_data)
    else:
        return jsonify(data)

@app.route('/symbols', methods=['GET'])
def get_symbols():
    symbols = collection.distinct("symbol")
    return jsonify(symbols)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
