from flask import Flask, redirect, url_for, request, render_template
import argparse
import helper
application = Flask(__name__)

PICKS = helper.gen_nflpick()
config_len = helper.file_len("config.csv")

@application.route('/')
def picks():
	return render_template('ScriptPicks.html', picks=PICKS, ctr=range(1,config_len+1))

@application.route('/submit', methods = ['POST', 'GET'])
def submit():
	picks = []
	if request.method == 'POST':
		name = request.form['name']
		for ctr in range(1,config_len+1):
			pick = request.form['pick' + str(ctr)]
			picks.append(pick)
		points = request.form['points']
		helper.submit_picks(name, picks, points)
		return "<h3 style='color:green'>Your picks have been submited </h>"
	return 'done'
	
if __name__ == '__main__':
	application.run(debug=True)
