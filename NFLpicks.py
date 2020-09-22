from flask import Flask, redirect, url_for, request, render_template
import csv, argparse
app = Flask(__name__)
PICKS = []

@app.route('/')
def picks():
	return render_template('ScriptPicks.html', picks=PICKS)

@app.route('/submit', methods = ['POST', 'GET'])
def submit():
	picks = []
	'''
	if request.method == 'POST':
		user = request.form['name']
		for ctr in range(1,17):
			pick = request.form['pick' + str(ctr)]
			picks.append(pick)
		points = request.form['points']
		print(picks)
		return "done"
	'''
	return 'done'
if __name__ == '__main__':
	#TODO create python script that creates html form
	#TODO create python script that creates js file for validation
	with open('config.csv', newline = "") as csvfile:
		reader = csv.DictReader(csvfile, fieldnames = ['fav', 'spread', 'under'])
		for row in reader:
			PICKS.append((row['fav'], row['spread'], row['under']))
	app.run(debug = True)