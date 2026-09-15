from flask import Flask, jsonify, redirect, render_template, request, url_for
import argparse, scrapper
import helper
application = app = Flask(__name__)
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
		if helper.Hide_forms:
			return render_template(
				"notice.html",
				title="Picks are closed",
				message="The games have already started, so this week's picks can no longer be submitted.",
			)
		else:
			name = request.form['name'].strip()
			for ctr in range(1,config_len+1):
				pick = request.form['pick' + str(ctr)]
				picks.append(pick)
			points = request.form['points']
			helper.submit_picks(name, picks, points, DEV)
			return render_template("picks_submited.html", gif=helper.Gif)
	return render_template(
		"notice.html",
		title="Nothing to submit",
		message="Open the picks page to submit this week's selections.",
	)

@application.route('/gen_config')
def gen_config():
	return render_template("gen_config.html")

@application.route('/gen_submit', methods = ['POST', 'GET'])
def gen_submit():
	if request.method == "POST":
		helper.Gif = request.form['gif']
		url = "https://api.the-odds-api.com"
		games = int(request.form['games'])
		scrapper.build_config(url, games)
	helper.gen_nflpick()
	return redirect(url_for("index"))

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
			leaderboard = helper.get_leaderboard(nflpicks, scores)
			return render_template('log.html', nflpicks=nflpicks, header=header, winners=scores, leaderboard=leaderboard, logos=helper.nfl_logos)
		else:
			return render_template(
				"notice.html",
				title="Leaderboard coming soon",
				message="Come back once the first game starts on Sunday.",
			)

@application.route('/leaderboard-data')
def leaderboard_data():
	nflpicks, _ = helper.get_nflpicks()
	winners = helper.check_scores()
	return jsonify({
		"leaderboard": helper.get_leaderboard(nflpicks, winners),
		"winners": winners,
	})

@application.route('/admin_logs')
def admin_logs():
	nflpicks,header = helper.get_nflpicks()
	scores = helper.check_scores()
	log = helper.get_log()
	leaderboard = helper.get_leaderboard(nflpicks, scores)
	return render_template('adminLogs.html', nflpicks=nflpicks, header=header, logs=log, winners=scores, 
		leaderboard=leaderboard, log=helper.Show_Logs, forms=helper.Hide_forms)
	
if __name__ == '__main__':
	DEV = 1
	application.run(debug=True)
