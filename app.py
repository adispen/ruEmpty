from flask import Flask, render_template, redirect, request
from flask_wtf import Form
from wtforms.validators import Required
from wtforms import TextField, TextAreaField, SelectField
import requests

app = Flask(__name__)
app.config.from_pyfile("app.cfg")
buildingsArr = [("Test", 'Test'), ("Test2", 'Test2'), ("Test3", 'Test3')]

class queryForm(Form):
	day = SelectField(u'Day of the Week', coerce=str, choices=[("Monday", 'Monday'), ("Tuesday", 'Tuesday'), ("Wednesday", 'Wednesday'), ("Thursday", 'Thursday'), ("Friday", 'Friday')])
	campus = SelectField(u'Campus', coerce=str, choices=[("Busch", 'Busch'), ("Livingston", 'Livingston'), ("College Ave", 'College Ave'), ("Cook/Douglass", 'Cook/Douglass')])
	building = SelectField(u'Day of the Week', coerce=str, choices=buildingsArr)

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

if __name__ == '__main__':
    app.run(debug=True)
