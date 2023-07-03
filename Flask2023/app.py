from flask import *
import pandas as pd

app = Flask(__name__)

@app.route('/')
def display_dataframe():
    data = {'Name': ['John', 'Alice', 'Bob'],
            'Age': [25, 30, 35],
            'City': ['New York', 'London', 'Paris']}
    df = pd.DataFrame(data)

    return render_template('index.html', dataframe=df.to_html())

if __name__ == '__main__':
    app.run(debug=True)
