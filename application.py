from flask import Flask, redirect, render_template, request, url_for
import argparse, scrapper
import helper
application = Flask(__name__)
DEV = 0

'''
Gifs to be used 
Boo-ena suerte: https://media.giphy.com/media/9SIY0mFMOho1duVcP6/giphy.gif
simpsons gl: https://media.giphy.com/media/HXF45CT8cvzZC/giphy.gif
'''

@application.route('/', methods = ['POST', 'GET'])
def index():
	if request.method == "POST":
		helper.Hide_forms = int(request.form['Forms'])
		return("Success")
	if request.method == "GET":
		print(helper.Hide_forms)
		if not helper.Hide_forms:
			PICKS = helper.get_picks()
			config_len = helper.file_len("config.csv")
			return render_template('picks.html', picks=PICKS, ctr=range(1,config_len+1), logos=helper.nfl_logos)
		else:
			return redirect(url_for("picks"))

@application.route('/submit', methods = ['POST', 'GET'])
def submit():
	config_len = helper.file_len("config.csv")
	picks = []
	if request.method == 'POST':
		name = request.form['name'].strip()
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
		url = "https://www.oddsshark.com/nfl/odds"
		games = int(request.form['games'])
		scrapper.build_config(url, games)
	helper.gen_nflpick()
	return "Success"

@application.route('/logs',  methods = ['POST', 'GET'])
def picks():
	access = helper.Show_Logs
	if request.method == "POST":
		helper.Show_Logs = int(request.form['logs'])
		return("Success")
	if request.method == "GET":
		if access:
			nflpicks,header = helper.get_nflpicks()
			scores = helper.check_scores()
			log = helper.get_log()
			return render_template('log.html', nflpicks=nflpicks, header=header, winners=scores) 
		else:
			return "<h1>Come back once the first game starts on sunday</h1>"

@application.route('/admin_logs')
def admin_logs():
	nflpicks,header = helper.get_nflpicks()
	scores = helper.check_scores()
	log = helper.get_log()
	return render_template('adminLogs.html', nflpicks=nflpicks, header=header, logs=log, winners=scores, 
		log=helper.Show_Logs, forms=helper.Hide_forms)
	
if __name__ == '__main__':
	DEV = 1
	application.run(debug=True, host="0.0.0.0")
