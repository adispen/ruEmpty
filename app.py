from flask import Flask, render_template, redirect, request, jsonify
from flask_wtf import Form
from wtforms.validators import Required
from wtforms import TextField, TextAreaField, SelectField
import requests
import json
import re
from jinja2 import evalcontextfilter, Markup, escape
import logging
import sys

    
app = Flask(__name__)
app.config.from_pyfile("empty.cfg")
app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.DEBUG)

app.logger.debug("Hello World")


_paragraph_re = re.compile(r'(?:\r\n|\r|\n){2,}')
@app.template_filter()
@evalcontextfilter
def linebreaks(eval_ctx, value):
	"""Converts newlines into <p> and <br />s."""
	value = re.sub(r'\r\n|\r|\n', '\n', value) # normalize newlines
	paras = re.split('\n{2,}', value)
	paras = [u'<p>%s</p>' % p.replace('\n', '<br />') for p in paras]
	paras = u'\n\n'.join(paras)
	return Markup(paras)
 
@app.template_filter()
@evalcontextfilter
def linebreaksbr(eval_ctx, value):
	"""Converts newlines into <p> and <br />s."""
	value = re.sub(r'\r\n|\r|\n', '\n', value) # normalize newlines
	paras = re.split('\n{2,}', value)
	paras = [u'%s' % p.replace('\n', '<br />') for p in paras]
	paras = u'\n\n'.join(paras)
	return Markup(paras) 

class roomClass:
	def __init__(self, roomNum, time):
		self.roomNum = roomNum
		self.time = time

def getBuildings():
	campus = request.form.get("campus")
	form = queryForm(request.POST)
	if campus == "Busch":
		form.building.choices = buildingsArr;

class queryForm(Form):
	dayChoices = [("Monday", 'Monday'), ("Tuesday", 'Tuesday'), \
			("Wednesday", 'Wednesday'), ("Thursday", 'Thursday'), \
			("Friday", 'Friday')]
	campusChoices = [("Please choose a campus", 'Please choose a campus'), \
			("Busch", 'Busch'), ("College Avenue", 'College Avenue'), \
			("Cook/Douglass", 'Cook/Douglass'), \
			("Livingston", 'Livingston')]
	defaultBuildings = [("Please choose a campus first", \
			'Please choose a campus first')] 
	day = SelectField(u'Day of the Week', coerce=str, choices=dayChoices)
	campus = SelectField(u'Campus', coerce=str, choices=campusChoices)
	building = SelectField(u'Building', coerce=str, choices=defaultBuildings)

@app.route('/', methods=['GET', 'POST'])
def main_page():
	form = queryForm()
	return render_template('index.html', form=form)

@app.route('/rooms', methods=['GET', 'POST'])
def rooms_page():
	dayOfWeek = request.form.get("day")
	campusName = request.form.get("campus")
	buildingName = request.form.get("building")

	if campusName == "Please choose a campus" \
			or buildingName == "Please choose a campus first":
		return render_template('bug.html')

	rooms = []
	#timesArr = []
	with open('ruemptyJSON.json') as data_file:
		data = json.load(data_file)
		i = 0
		campus = filter(lambda entry: entry["Campus Name"] == campusName, data)
		building = filter(lambda entry: entry["Building Name"] == buildingName\
				, campus[0]["Buildings"])
		for room in building[0]["Rooms"]:
			roomNum = room["Room Number"]
			if dayOfWeek == "Thursday":
				newRoom = roomClass(roomNum, room["TH"])
				rooms.append(newRoom)
				continue
			newRoom = roomClass(roomNum, room[dayOfWeek[:1]])
			rooms.append(newRoom)

	return render_template('rooms.html', dayOfWeek=dayOfWeek, \
			campusName=campusName, buildingName=buildingName, rooms=rooms)

@app.route('/_getBuildings', methods=['GET', 'POST'])
def getBuildings():
	campus = request.args['campus']
	buildingArr = []
	with  open('ruemptyJSON.json') as data_file:
		data = json.load(data_file)
		campusData = filter(lambda entry: entry["Campus Name"] == campus, data)
		for building in campusData[0]["Buildings"]:
			buildingArr.append(building["Building Name"])

	alphaBuildings = sorted(buildingArr)
	return jsonify(buildings=alphaBuildings)


if __name__ == '__main__':
    app.run(debug=True)
