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
		""" This class is used to define rooms using their number and the times
		they are available given the date selected by the user.
		"""
		self.roomNum = roomNum
		self.time = time

class queryForm(Form):
	"""Defining form which will be rendered on the main page via WTForms."""
	dayChoices = [("Monday", 'Monday'), ("Tuesday", 'Tuesday'), \
			("Wednesday", 'Wednesday'), ("Thursday", 'Thursday'), \
			("Friday", 'Friday')]

	# Initial choice set to prompt user to change the campus, which fires the
	# GET request which will get all buildings for that campus.
	campusChoices = [("Please choose a campus", 'Please choose a campus'), \
			("Busch", 'Busch'), ("College Avenue", 'College Avenue'), \
			("Cook/Douglass", 'Cook/Douglass'), \
			("Livingston", 'Livingston')]

	# Initially set to a single option because it will be populated by the
	# client based on the chosen campus.
	defaultBuildings = [("Please choose a campus first", \
			'Please choose a campus first')] 
	day = SelectField(u'Day of the Week', coerce=str, choices=dayChoices)
	campus = SelectField(u'Campus', coerce=str, choices=campusChoices)
	building = SelectField(u'Building', coerce=str, choices=defaultBuildings)

@app.route('/', methods=['GET', 'POST'])
def main_page():
	"""Creating a form from the defined class above, rendering it on the page.
	"""
	form = queryForm()
	return render_template('down.html', form=form)

@app.route('/rooms', methods=['GET', 'POST'])
def rooms_page():
	"""Displays the rooms and times they are open for specified day, campus,
	and building.
	"""

	# Grabbing selected options from form on previous page.
	dayOfWeek = request.form.get("day")
	campusName = request.form.get("campus")
	buildingName = request.form.get("building")

	# If somehow they manage to submit with nothing selected catch as bug.
	# TODO: Should really be handled by validators.
	if campusName == "Please choose a campus" \
			or buildingName == "Please choose a campus first":
		return render_template('bug.html')

	# Create an array to store rooms in.
	rooms = []

	# Time to parse the JSON.
	with open('ruemptyJSON.json') as data_file:
		data = json.load(data_file)
		i = 0

		# These two filters make sure that we access the correct building
		# object inside the correct campus object. From there we iterate
		# through the rooms and grab what we need for each.
		campus = filter(lambda entry: entry["Campus Name"] == campusName, data)
		building = filter(lambda entry: entry["Building Name"] == buildingName\
				, campus[0]["Buildings"])
		for room in building[0]["Rooms"]:
			roomNum = room["Room Number"]

			# Catch if the day is Thurday since evaluating the normal way would
			# get us the schedule for Tuesday.
			if dayOfWeek == "Thursday":

				# Create new room objects of the times and number and add them
				# to the array.
				newRoom = roomClass(roomNum, room["TH"])
				rooms.append(newRoom)
				continue

			newRoom = roomClass(roomNum, room[dayOfWeek[:1]])
			rooms.append(newRoom)

	# Returning the necessary data to render the rooms page correctly.
	return render_template('rooms.html', dayOfWeek=dayOfWeek, \
			campusName=campusName, buildingName=buildingName, rooms=rooms)

@app.route('/_getBuildings', methods=['GET', 'POST'])
def getBuildings():
	"""The client will send a GET request to this route when
	selecting a campus, and the server will return an alphabetized list of all
	the available buildings on that campus.  The client uses this to populate
	the selector for buildings.
	"""

	# Grabs the campus from the GET args.
	campus = request.args['campus']

	# Make an array in which top return our buildings.
	buildingArr = []

	# Once again accessing the data file and filtering to our desired campus.
	with  open('ruemptyJSON.json') as data_file:
		data = json.load(data_file)
		campusData = filter(lambda entry: entry["Campus Name"] == campus, data)

		# Populate the array with all buildings in that campus.
		for building in campusData[0]["Buildings"]:
			buildingArr.append(building["Building Name"])

	# Alphabetize the array before returning it as JSON to the client.
	alphaBuildings = sorted(buildingArr)
	return jsonify(buildings=alphaBuildings)


if __name__ == '__main__':
    app.run()
