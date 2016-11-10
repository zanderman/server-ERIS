
# Modules
from flask 					import Flask, render_template, request, flash
from flask_dynamo 			import Dynamo
from models.nav 			import Nav
from models.incident 		import Incident
from boto.dynamodb2.fields 	import HashKey
from boto.dynamodb2.table 	import Table
from configparser         	import ConfigParser
import os
import sys
import time

# Set environment variables.
config = ConfigParser()
config.read(sys.argv[1])
os.environ["AWS_ACCESS_KEY_ID"] = config.get("dynamodb","aws_access_key_id")
os.environ["AWS_SECRET_ACCESS_KEY"] = config.get("dynamodb","aws_secret_access_key")

# Setup Flask
app = Flask(__name__)
app.secret_key = config.get("flask","flask_secret_key")
app.debug = True
app.config['DYNAMO_TABLES'] = [
    Table(config.get("dynamodb","aws_table_users"), schema=[HashKey(config.get("dynamodb","aws_users_hashkey"))]),
    Table(config.get("dynamodb","aws_table_incidents"), schema=[HashKey(config.get("dynamodb","aws_incidents_hashkey"))]),
]

# Global variables
nav = Nav() 			# Dictionary of navigation bar items.
dynamo = Dynamo(app) 	# Initialize Dynamo
INCIDENTS = []



@app.route('/')
def home():
	"""
	Render the homepage.
	"""
	return render_template('home.html', NAV=nav["header"])



@app.route('/incidents', methods=["GET", "POST"])
def incidents():
	"""
	Render the incident list page.
	"""
	global INCIDENTS

	# Client posting to server.
	if request.method == "POST":

		# Refresh button was pressed.
		if request.form['action'].lower() == "refresh":

			# Get updated incident list.
			updateIncidents()

		# Incident creation button was pressed.
		if request.form['action'].lower() == "create":

			# No scene ID was specified.
			if request.form['data-sceneid'] == "":
				flash('WARNING: No incident ID specified.')

			# All required fields are valid.
			else:
				dynamo.tables[config.get("dynamodb","aws_table_incidents")].put_item(
					data={
					"sceneId" : request.form['data-sceneid'],
					"address" : request.form['data-address'],
					"active" : True,
					"assigned_organizations" : request.form.getlist('check'),
					"description" : request.form['data-description'],
					"latitude" : request.form['data-latitude'],
					"longitude" : request.form['data-longitude'],
					"time" : request.form['data-time'],
					"title" : request.form['data-title'],
					}
					)

				# Small delay to allow the database to be updated.
				time.sleep(0.05)

				# Get updated incident list.
				updateIncidents()

	# Render the incidents HTML page.
	return render_template('incidents.html', NAV=nav["header"], INCIDENTS=INCIDENTS)



def updateIncidents():
	"""
	Scans the entire incident database table for current incidents.
	"""
	global INCIDENTS

	# Clear the list (TODO: don't clear list, instead keep references)
	INCIDENTS = []

	# Obtain boto-style dictionary of incidents.
	incidents = dynamo.tables[config.get("dynamodb","aws_table_incidents")].scan()

	# Iterate over all items in the incident list.
	for item in incidents:

		# Create new incident object.
		incident = Incident(item['sceneId'],item['description'],item['address'],item['latitude'],item['longitude'],item['time'],item['title'],item['assigned_organizations'])

		# Append incident object to the global list of incidents.
		INCIDENTS.append(incident)



if __name__=='__main__':

	# Turn ON the server.
	app.run(debug=True, host='0.0.0.0')