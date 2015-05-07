from flask import Flask, render_template, redirect, request
from flask_wtf import Form
from wtforms.validators import Required
from wtforms import TextField, TextAreaField, SelectField
import requests

app = Flask(__name__)
app.config.from_pyfile("empty.cfg")

def getBuildings():
	campus = request.form.get("campus")
	form = queryForm(request.POST)
	if campus == "Busch":
		form.building.choices = buildingsArr;

class queryForm(Form):
	day = SelectField(u'Day of the Week', coerce=str, choices=[("Monday", 'Monday'), ("Tuesday", 'Tuesday'), ("Wednesday", 'Wednesday'), ("Thursday", 'Thursday'), ("Friday", 'Friday')])
	campus = SelectField(u'Campus', coerce=str, choices=[("Busch", 'Busch'), ("Livingston", 'Livingston'), ("College Ave", 'College Ave'), ("Cook/Douglass", 'Cook/Douglass')])
	building = SelectField(u'Building', coerce=str, choices=[("Please choose a campus first", 'Please choose a campus first'), ("other", 'other')])

@app.route('/', methods=['GET', 'POST'])
def main_page():
	form = queryForm()
	return render_template('index.html', form=form)

@app.route('/rooms', methods=['GET', 'POST'])
def rooms_page():
	dayOfWeek = request.form.get("day")
	campusName = request.form.get("campus")
	buildingName = request.form.get("building")
	return render_template('rooms.html', dayOfWeek=dayOfWeek, campusName=campusName, buildingName=buildingName)

@app.route('/_getBuildings', methods=['GET', 'POST'])
def getBuildings():
	campus = request.args['campus'].upper()
	print campus
	return campus

if __name__ == '__main__':
    app.run(debug=True)
