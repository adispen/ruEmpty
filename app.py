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

class timeSlot:
	def __init__(self, time):
		self.time = time

class roomClass:
	def __init__(self, roomNum, slot):
		self.roomNum = roomNum
		self.slot = slot

def getBuildings():
	campus = request.form.get("campus")
	form = queryForm(request.POST)
	if campus == "Busch":
		form.building.choices = buildingsArr;

class queryForm(Form):
	day = SelectField(u'Day of the Week', coerce=str, choices=[("Monday", 'Monday'), ("Tuesday", 'Tuesday'), ("Wednesday", 'Wednesday'), ("Thursday", 'Thursday'), ("Friday", 'Friday')])
	campus = SelectField(u'Campus', coerce=str, choices=[("Please choose a campus", 'Please choose a campus'), ("Busch", 'Busch'), ("Livingston", 'Livingston'), ("College Avenue", 'College Avenue'), ("Cook/Douglass", 'Cook/Douglass')])
	building = SelectField(u'Building', coerce=str, choices=[("Please choose a campus first", 'Please choose a campus first')])

@app.route('/', methods=['GET', 'POST'])
def main_page():
	form = queryForm()
	return render_template('index.html', form=form)

@app.route('/rooms', methods=['GET', 'POST'])
def rooms_page():
	dayOfWeek = request.form.get("day")
	campusName = request.form.get("campus")
	buildingName = request.form.get("building")
	rooms = []
	timesArr = []
	with open('ruemptyJSON.json') as data_file:
		data = json.load(data_file)
		for entry in data:
			if entry["Campus Name"] == campusName:
				for building in entry["Buildings"]:
					if building["Building Name"] == buildingName:
						for room in building["Rooms"]:
							roomNum = room["Room Number"]
							print "********* START" + roomNum + "*********** \n"
							for day, times in room.iteritems():
								if day == "Room Number":
									continue
								if day == dayOfWeek[:1]:
									print dayOfWeek[:1]
									print times
									newTimeSlot = timeSlot(times)
									timesArr.append(newTimeSlot)

							print len(timesArr)
							newRoom = roomClass(roomNum, timesArr)
							timesArr=[]

							rooms.append(newRoom)
							print  "******** END" + roomNum + " **********  \n"

	return render_template('rooms.html', dayOfWeek=dayOfWeek, campusName=campusName, buildingName=buildingName, rooms=rooms)

@app.route('/_getBuildings', methods=['GET', 'POST'])
def getBuildings():
	campus = request.args['campus']
	buildingArr = []
	with  open('ruemptyJSON.json') as data_file:
		data = json.load(data_file)
		for entry in data:
			if entry["Campus Name"] == campus:
				for buildingEntry in entry["Buildings"]:
					buildingArr.append(buildingEntry["Building Name"])

	print buildingArr
	return jsonify(buildings=buildingArr)


if __name__ == '__main__':
    app.run(debug=True)
