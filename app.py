from flask import Flask, render_template
import requests

app = Flask(__name__)

@app.route('/')
def hello_world():
	buildings=['one', 'two', 'three', 'examples']
	return render_template('index.html', buildings=buildings)

if __name__ == '__main__':
    app.run(debug=True)
