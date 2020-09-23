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
		name = request.form['name']
		for ctr in range(1,config_len+1):
			pick = request.form['pick' + str(ctr)]
			picks.append(pick)
		points = request.form['points']
		helper.submit_picks(name, picks, points)
		return "<h3 style='color:green'>Your picks have been submited </h>"
	return 'done'
if __name__ == '__main__':
	parser = argparse.ArgumentParser(description="build website for picks")
	parser.add_argument("-u","--url",help="url of spreads",type=str, required=True)
	parser.add_argument("-g","--games",help="number of games this week",type=int, required=True)
	args = parser.parse_args()
	scrapper.build_config(args.url,args.games)	
	app.run(host='0.0.0.0')