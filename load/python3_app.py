#!/usr/bin/python
from flask import Flask, render_template, request
import time
import urllib.parse
app = Flask(__name__)


@app.route("/target_endpoint")
def target():
	# You could do any information passing here if you want (i.e Post or Get request)
	some_data = "Here's some example data"
	some_data = urllib.parse.quote(some_data) # urllib2 is used if you have fancy characters in your data like "+"," ", or "="
	# This is where the loading screen will be.
	# ( You don't have to pass data if you want, but if you do, make sure you have a matching variable in the html i.e {{my_data}} )
	return render_template('loading.html', my_data = some_data)

@app.route("/processing")
def processing():
	# This is where the time-consuming process can be.
	data = "No data was passed"
	# In this case, the data was passed as a get request as you can see at the bottom of the loading.html file
	if request.args.to_dict(flat=False)['data'][0]:
		data = str(request.args.to_dict(flat=False)['data'][0])
	# This is where your time-consuming stuff can take place (sql queries, checking other apis, etc)
	time.sleep(10) # To simulate something time-consuming, I've tested up to 100 seconds
	# You can return a success/fail page here or whatever logic you want
	return render_template('success.html', passed_data = data)

if __name__ == '__main__':
	app.run(host = '0.0.0.0')
