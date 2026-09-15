import hashlib
import os
from flask import Flask, jsonify, redirect, render_template, request, session, url_for
import argparse, scrapper
import helper
import accounts
application = app = Flask(__name__)
application.config["SECRET_KEY"] = os.environ.get("FLASK_SECRET_KEY", "local-development-key")
DEV = 0

'''
Gifs to be used 
Boo-ena suerte: https://media.giphy.com/media/9SIY0mFMOho1duVcP6/giphy.gif
simpsons gl: https://media.giphy.com/media/HXF45CT8cvzZC/giphy.gif
'''

def current_user():
	return accounts.get_user(session["user_id"]) if session.get("user_id") else None

def config_key():
	with open(os.path.join(os.path.dirname(__file__), "config.csv"), "rb") as config:
		return hashlib.sha256(config.read()).hexdigest()

@application.route('/', methods = ['POST', 'GET'])
def index():
	if request.method == "POST":
		helper.Hide_forms = int(request.form['Forms'])
		return("Success")
	if request.method == "GET":
		if not helper.picks_closed():
			user = current_user()
			if not user:
				return redirect(url_for("login", next=url_for("index")))
			PICKS = helper.get_picks()
			config_len = helper.file_len("config.csv")
			saved = accounts.get_picks(user["id"], config_key()) if user else None
			return render_template('picks.html', picks=PICKS, ctr=range(1,config_len+1),
				logos=helper.nfl_logos, user=user, saved=saved,
				started_games=helper.started_game_indices())
		else:
			return redirect(url_for("picks"))

@application.route('/submit', methods = ['POST', 'GET'])
def submit():
	config_len = helper.file_len("config.csv")
	picks = []
	if request.method == 'POST':
		user = current_user()
		if not user:
			return redirect(url_for("login", next=url_for("index")))
		if helper.picks_are_locked():
			return render_template(
				"notice.html",
				title="Picks are closed",
				message="The games have already started, so this week's picks can no longer be submitted.",
			)
		else:
			name = user["name"]
			saved = accounts.get_picks(user["id"], config_key())
			started_games = helper.started_game_indices()
			if started_games and not saved:
				return render_template(
					"notice.html",
					title="Started games are locked",
					message="Submit your picks before games begin.",
				)
			for ctr in range(1,config_len+1):
				index = ctr - 1
				pick = request.form.get("pick" + str(ctr))
				if index in started_games:
					pick = saved["picks"][index]
				if not pick:
					return render_template(
						"notice.html",
						title="Picks are incomplete",
						message="Choose a team for every game before submitting.",
					)
				picks.append(pick)
			if saved and any(
				index >= len(saved["picks"]) or picks[index] != saved["picks"][index]
				for index in started_games
			):
				return render_template(
					"notice.html",
					title="Started games are locked",
					message="Your picks for games that have started cannot be changed.",
				)
			points = request.form['points']
			helper.submit_picks(name, picks, points, DEV)
			accounts.save_picks(user["id"], config_key(), picks, int(points))
			return render_template("picks_submited.html", gif=helper.Gif)
	return render_template(
		"notice.html",
		title="Nothing to submit",
		message="Open the picks page to submit this week's selections.",
	)

@application.route('/register', methods=['GET', 'POST'])
def register():
	if current_user():
		return redirect(url_for("index"))
	if request.method == "POST":
		name = request.form.get("name", "").strip()
		email = request.form.get("email", "").strip()
		password = request.form.get("password", "")
		if not name:
			return render_template("auth.html", title="Create account", register=True,
				error="Name is required.", name=name, email=email)
		if len(password) < 8:
			return render_template("auth.html", title="Create account", register=True,
				error="Password must be at least 8 characters.", name=name, email=email)
		user_id = accounts.create_user(name, email, password)
		if user_id is None:
			return render_template("auth.html", title="Create account", register=True,
				error="An account with that email already exists.", name=name, email=email)
		session["user_id"] = user_id
		return redirect(url_for("index"))
	return render_template("auth.html", title="Create account", register=True)

@application.route('/login', methods=['GET', 'POST'])
def login():
	if current_user():
		return redirect(url_for("index"))
	if request.method == "POST":
		email = request.form.get("email", "").strip()
		user = accounts.authenticate(email, request.form.get("password", ""))
		if not user:
			return render_template("auth.html", title="Log in", register=False,
				error="Email or password is incorrect.", email=email)
		session["user_id"] = user["id"]
		return redirect(url_for("index"))
	return render_template("auth.html", title="Log in", register=False)

@application.route('/logout')
def logout():
	session.clear()
	return redirect(url_for("index"))

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
