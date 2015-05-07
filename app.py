from flask import Flask, render_template
import requests

app = Flask(__name__)

@app.route('/')
def main_page():
	buildings=['one', 'two', 'three', 'examples']
	return render_template('index.html', buildings=buildings)

@app.route('/rooms')
def rooms_page():
	return render_template('rooms.html')

if __name__ == '__main__':
    app.run(debug=True)
