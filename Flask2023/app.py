from flask import *
import pandas as pd
from pymongo import MongoClient

app = Flask(__name__)
MONGO_URI = 'mongodb://localhost:27017'

@app.route('/')
def display_dataframe():
    data = {'Name': ['John', 'Alice', 'Bob'],
            'Age': [25, 30, 35],
            'City': ['New York', 'London', 'Paris'],
            'Name': ['John1', 'Alice', 'Bob'],
            'Age': [25, 30, 35],
            'City': ['New York', 'London', 'Paris']}
    df = pd.DataFrame(data)

    return render_template('index.html', dataframe=df.to_html())

def display_dataframe2():
    # Connect to MongoDB
    client = MongoClient(MONGO_URI)
    db = client['your_database_name']  # Update with your database name
    collection = db['your_collection_name']  # Update with your collection name

    # Fetch data from MongoDB
    data = list(collection.find())

    # Create a DataFrame from the fetched data
    df = pd.DataFrame(data)

    return render_template('index.html', dataframe=df.to_html())

if __name__ == '__main__':
    app.run(debug=True)
