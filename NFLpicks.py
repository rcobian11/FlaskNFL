from flask import Flask, redirect, url_for, request, render_template
import argparse
import helper, scrapper
app = Flask(__name__)

PICKS = helper.gen_nflpick()
config_len = helper.file_len("config.csv")

@app.route('/')
def picks():
	return render_template('ScriptPicks.html', picks=PICKS, ctr=range(1,config_len+1))

@app.route('/submit', methods = ['POST', 'GET'])
def submit():
	picks = []
	if request.method == 'POST':
		user = request.form['name']
		for ctr in range(1,config_len+1):
			pick = request.form['pick' + str(ctr)]
			picks.append(pick)
		points = request.form['points']
		print(picks)
		return "done"
	return 'done'
if __name__ == '__main__':
	#TODO get values from form and put them in a csv file
	#incorporate scrapper.py using argparse
	app.run(debug = True)