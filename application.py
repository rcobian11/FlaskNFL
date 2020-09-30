from flask import Flask, redirect, url_for, request, render_template
import argparse, scrapper
import helper
application = Flask(__name__)
DEV = 0

@application.route('/')
def picks():
	PICKS = helper.get_picks()
	config_len = helper.file_len("config.csv")
	return render_template('picks.html', picks=PICKS, ctr=range(1,config_len+1))

@application.route('/submit', methods = ['POST', 'GET'])
def submit():
	config_len = helper.file_len("config.csv")
	picks = []
	if request.method == 'POST':
		name = request.form['name']
		for ctr in range(1,config_len+1):
			pick = request.form['pick' + str(ctr)]
			picks.append(pick)
		points = request.form['points']
		helper.submit_picks(name, picks, points, DEV)
		return render_template("picks_submited.html", gif=helper.Gif)
	return 'done'

@application.route('/gen_config')
def gen_config():
	return render_template("gen_config.html")

@application.route('/gen_submit', methods = ['POST', 'GET'])
def gen_submit():
	if request.method == "POST":
		helper.Gif = request.form['gif']
		url = request.form['url']
		games = int(request.form['games'])
		scrapper.build_config(url, games)
	helper.gen_nflpick()
	return "Success"

@application.route('/logs')
def logs():
	nflpicks,header = helper.get_nflpicks()
	log = helper.get_log()
	return render_template('log.html', nflpicks=nflpicks, header=header, logs=log) 
	
if __name__ == '__main__':
	DEV = 1
	application.run(debug=True)
