
# Modules
from flask 			import Flask, render_template, request
from models.nav 	import Nav

# Setup Flask
app = Flask(__name__)
app.debug = True

# Global variables
nav = Nav() 	# Dictionary of navigation bar items.

@app.route('/')
def home():
	"""
	Render the homepage with navigation bar items.
	"""
	return render_template('home.html', NAV=nav["header"])

if __name__=='__main__':

	# Turn ON the server.
	app.run(debug=True, host='0.0.0.0')