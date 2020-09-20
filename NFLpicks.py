from flask import Flask, redirect, url_for, request, render_template
app = Flask(__name__)

@app.route('/')
def picks():
	return render_template('picks.html')

@app.route('/submit', methods = ['POST', 'GET'])
def login():
	picks = []
	if request.method == 'POST':
		user = request.form['name']
		for ctr in range(1,17):
			pick = request.form['pick' + str(ctr)]
			picks.append(pick)
		points = request.form['points']
		print(picks)
		return "done"

if __name__ == '__main__':
	app.run(debug = True)