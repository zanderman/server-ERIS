
# Modules
from flask 					import Flask, render_template, request
from flask_dynamo 			import Dynamo
from models.nav 			import Nav
from models.incident 		import Incident
from boto.dynamodb2.fields 	import HashKey
from boto.dynamodb2.table 	import Table
import os

# Set environment variables.
os.environ["AWS_ACCESS_KEY_ID"] = "AKIAJPSBNOVF7M4MZULA"
os.environ["AWS_SECRET_ACCESS_KEY"] = "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"

# Setup Flask
app = Flask(__name__)
app.debug = True
app.config['DYNAMO_TABLES'] = [
    Table('emergencyresponderin-mobilehub-146580548-User_Data', schema=[HashKey('userId')]),
    Table('emergencyresponderin-mobilehub-146580548-Scenes', schema=[HashKey('sceneId')]),
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
			dynamo.tables['emergencyresponderin-mobilehub-146580548-Scenes'].put_item(
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