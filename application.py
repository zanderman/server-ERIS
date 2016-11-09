
# Modules
from flask 					import Flask, render_template, request
from flask_dynamo 			import Dynamo
from models.nav 			import Nav
from models.incident 		import Incident
from boto.dynamodb2.fields 	import HashKey
from boto.dynamodb2.table 	import Table
import os

# Set environment variables.
os.environ["AWS_ACCESS_KEY_ID"] = ""
os.environ["AWS_SECRET_ACCESS_KEY"] = ""

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

	return render_template('incidents.html', NAV=nav["header"], INCIDENTS=INCIDENTS)


if __name__=='__main__':

	# Turn ON the server.
	app.run(debug=True, host='0.0.0.0')