from flask import Flask, render_template
import pandas as pd


app = Flask(__name__)

@app.route('/')
def display_dataframe():
    # Create a sample DataFrame
    data = {'Name': ['John', 'Alice', 'Bob'],
            'Age': [25, 30, 35],
            'City': ['New York', 'London', 'Paris']}
    df = pd.DataFrame(data)

    # Render the HTML template and pass the DataFrame as a variable
    return render_template('index.html', dataframe=df.to_html())

