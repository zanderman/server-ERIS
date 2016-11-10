
# Modules
from flask 					import Flask, render_template, request
from flask_dynamo 			import Dynamo
from models.nav 			import Nav
from models.incident 		import Incident
from boto.dynamodb2.fields 	import HashKey
from boto.dynamodb2.table 	import Table
from configparser         	import ConfigParser
import os
import sys

# Set environment variables.
config = ConfigParser()
config.read(sys.argv[1])
os.environ["AWS_ACCESS_KEY_ID"] = config.get("dynamodb","aws_access_key_id")
os.environ["AWS_SECRET_ACCESS_KEY"] = config.get("dynamodb","aws_secret_access_key")

# Setup Flask
app = Flask(__name__)
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
	Render the homepage with navigation bar items.
	"""
	return render_template('home.html', NAV=nav["header"])

@app.route('/incidents', methods=["GET", "POST"])
def incidents():
	"""
	Render the incident list page.
	"""
	global INCIDENTS

	if request.method == "POST":

		# Refresh button was pressed.
		if request.form['submit'].lower() == "refresh":
			INCIDENTS.append(Incident("id","hello there","address","latitude","longitude","time","Incident #1",None))
			INCIDENTS.append(Incident("id","oh goodness!","address","latitude","longitude","time","Incident #2",None))
			dynamo.tables[config.get("dynamodb","aws_table_incidents")].put_item(
				data={
				"sceneId" : "1234",
				"address" : "42 Wallaby Way, Sydney",
				"active" : True,
				"assigned_organizations" : ["EMS"],
				"description" : "This is a description",
				"latitude" : "56.3423342",
				"longitude" : "34.342346",
				"time" : "00:00",
				"title" : "Structure Fire",
				}
				)
			# sceneid,address,active,assigned_organization,description,latitude,longitude,time,title

	return render_template('incidents.html', NAV=nav["header"], INCIDENTS=INCIDENTS)


if __name__=='__main__':

	# Turn ON the server.
	app.run(debug=True, host='0.0.0.0')