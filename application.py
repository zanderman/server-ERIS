
# Modules
from flask import Flask, render_template, request

# Setup Flask
app = Flask(__name__)
app.debug = True

@app.route('/')
def index():
	return "Hello World"

if __name__=='__main__':

	# Turn ON the server.
	app.run(debug=True, host='0.0.0.0')