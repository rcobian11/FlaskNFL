import boto3, csv, pytz, scrapper
from datetime import datetime
Gif = ""
Show_Logs = 0
Hide_forms = 0
nfl_abrv = {
"Arizona Cardinals" : "ARI",
"Atlanta Falcons" : "ATL",
"Baltimore Ravens" : "BAL",
"Buffalo Bills" : "BUF",
"Carolina Panthers" : "CAR",
"Chicago Bears" : "CHI",
"Cincinnati Bengals" : "CIN",
"Cleveland Browns" : "CLE",
"Dallas Cowboys" : "DAL",
"Denver Broncos" : "DEN",
"Detroit Lions" : "DET",
"Green Bay Packers" : "GB",
"Houston Texans" : "HOU",
"Indianapolis Colts" : "IND",
"Jacksonville Jaguars" : "JAC",
"Kansas City Chiefs" : "KC",
"Las Vegas Raiders" : "LV",
"Los Angeles Chargers" : "LAC",
"Los Angeles Rams" : "LAR",
"Miami Dolphins" : "MIA",
"Minnesota Vikings" : "MIN",
"New England Patriots" : "NE",
"New Orleans Saints" : "NO",
"New York Giants" : "NYG",
"New York Jets" : "NYJ",
"Philadelphia Eagles" : "PHI",
"Pittsburgh Steelers" : "PIT",
"San Francisco 49ers" : "SF",
"Seattle Seahawks" : "SEA",
"Tampa Bay Buccaneers" : "TB",
"Tennessee Titans" : "TEN",
"Washington Commanders" : "WAS"
}

nfl_logos = {
	"ARI" : "http://loodibee.com/wp-content/uploads/nfl-arizona-cardinals-team-logo-2-300x300.png",
	"ATL" : "http://loodibee.com/wp-content/uploads/nfl-atlanta-falcons-team-logo-2-300x300.png",
	"BAL" : "http://loodibee.com/wp-content/uploads/nfl-baltimore-ravens-team-logo-2-300x300.png",
	"BUF" : "http://loodibee.com/wp-content/uploads/nfl-buffalo-bills-team-logo-2-300x300.png",
	"CAR" : "http://loodibee.com/wp-content/uploads/nfl-carolina-panthers-team-logo-2-300x300.png",
	"CHI" : "http://loodibee.com/wp-content/uploads/nfl-chicago-bears-team-logo-2-300x300.png",
	"CIN" : "http://loodibee.com/wp-content/uploads/nfl-cincinnati-bengals-team-logo-300x300.png",
	"CLE" : "http://loodibee.com/wp-content/uploads/nfl-cleveland-browns-team-logo-2-300x300.png",
	"DAL" : "http://loodibee.com/wp-content/uploads/nfl-dallas-cowboys-team-logo-2-300x300.png",
	"DEN" : "http://loodibee.com/wp-content/uploads/nfl-denver-broncos-team-logo-2-300x300.png",
	"DET" : "http://loodibee.com/wp-content/uploads/nfl-detroit-lions-team-logo-2-300x300.png",
	"GB"  : "http://loodibee.com/wp-content/uploads/nfl-green-bay-packers-team-logo-2-300x300.png",
	"HOU" : "http://loodibee.com/wp-content/uploads/nfl-houston-texans-team-logo-2-300x300.png",
	"IND" : "http://loodibee.com/wp-content/uploads/nfl-indianapolis-colts-team-logo-2-300x300.png",
	"JAC" : "http://loodibee.com/wp-content/uploads/nfl-jacksonville-jaguars-team-logo-2-300x300.png",
	"KC"  : "http://loodibee.com/wp-content/uploads/nfl-kansas-city-chiefs-team-logo-2-300x300.png",
	"LV"  : "http://loodibee.com/wp-content/uploads/nfl-oakland-raiders-team-logo-300x300.png",
	"LAC" : "http://loodibee.com/wp-content/uploads/nfl-los-angeles-chargers-team-logo-2-300x300.png",
	"LAR" : "http://loodibee.com/wp-content/uploads/los-angeles-rams-2020-logo-300x300.png",
	"MIA" : "http://loodibee.com/wp-content/uploads/nfl-miami-dolphins-team-logo-2-300x300.png",
	"MIN" : "http://loodibee.com/wp-content/uploads/nfl-minnesota-vikings-team-logo-2-300x300.png",
	"NE"  : "http://loodibee.com/wp-content/uploads/nfl-new-england-patriots-team-logo-2-300x300.png",
	"NO"  : "http://loodibee.com/wp-content/uploads/nfl-new-orleans-saints-team-logo-2-300x300.png",
	"NYG" : "http://loodibee.com/wp-content/uploads/nfl-new-york-giants-team-logo-2-300x300.png",
	"NYJ" : "http://loodibee.com/wp-content/uploads/nfl-new-york-jets-team-logo-300x300.png",
	"PHI" : "http://loodibee.com/wp-content/uploads/nfl-philadelphia-eagles-team-logo-2-300x300.png",
	"PIT" : "http://loodibee.com/wp-content/uploads/nfl-pittsburgh-steelers-team-logo-2-300x300.png",
	"SF"  : "http://loodibee.com/wp-content/uploads/nfl-san-francisco-49ers-team-logo-2-300x300.png",
	"SEA" : "http://loodibee.com/wp-content/uploads/nfl-seattle-seahawks-team-logo-2-300x300.png",
	"TB"  : "http://loodibee.com/wp-content/uploads/nfl-tampa-bay-buccaneers-team-logo-2-300x300.png",
	"TEN" : "http://loodibee.com/wp-content/uploads/nfl-tennessee-titans-team-logo-2-300x300.png",
	"WAS" : "https://loodibee.com/wp-content/uploads/washington-commanders-logo-300x300.png"
}

def file_len(fname):
	'''
	@param fname: fname = name of file to be opened
	@return int: Length of file as int
	checks length of file and returns value
	'''
	with open(fname) as f:
		for i, l in enumerate(f):
			pass
	f.close()
	return i + 1

def gen_nflpick():
	'''
	Creates and formates both picks.csv and log.txt. files are created and stored in
	same directory that the program is ran in.
	'''
	nflpicks = open("picks.csv", 'w')
	log = open("log.txt", 'w')
	log.write("Log file\n")
	log.close()
	with open('config.csv', newline = '') as csvfile:
		reader = csv.DictReader(csvfile, fieldnames = ['FAV', 'SPREAD', 'UNDER'])#fieldnames are the headers
		pickNum = 1
		nflpicks.write(",")
		for row in reader:
			nflpicks.write('"{}\n{}\n{}",'.format(row['FAV'],
												row['SPREAD'],
												row['UNDER']))
		nflpicks.write('"TIE\n-\nBRK"')
	nflpicks.close()

def get_picks():
	'''
	@return picks: list containing values from config.csv
	iterates through config.csv and stores values in list picks
	'''
	picks = []
	with open('config.csv', newline = '') as csvfile:
		reader = csv.DictReader(csvfile, fieldnames = ['FAV', 'SPREAD', 'UNDER'])#fieldnames are the headers
		for row in reader:
			picks.append((row['FAV'], row['SPREAD'], row['UNDER']))
	return picks

def check_repeat(name):
	with open("picks.csv", "r+") as picks:
		line = picks.readlines()
		picks.seek(0)
		for i in line:
			if name != i.split(',')[0]:
				picks.write(i)
		picks.truncate()

def submit_picks(name, picks, points, dev):
	'''
	@param name: name submitted from form -> str
	@param picks: list of picks subbmited from form -> list
	@param points: number of points submmited from form -> int
	@param dev: set if program ran in development mode -> bool
	gets values submmited from the form and appends them to picks.csv
	adds timestamp to log file when picks are submmited 
	'''
	#write to picks file
	check_repeat(name)
	file = open("picks.csv", 'a')
	file.write("\n")
	file.write(name + ",")
	for pick in picks:
		file.write(pick + ",")
	file.write(points)
	file.close()
	#write to log file
	tz_la = pytz.timezone("America/Los_Angeles")
	date = datetime.now(tz_la)
	log = open("log.txt", 'a')
	log.write(name + ";")
	log.write("{}/{}".format(date.month, date.day))
	log.write("  {:02d}:{:02d}:{:02d}".format(date.hour, date.minute, date.second))
	log.write("\n")
	log.close()
	

def upload_file(file, bucket):
	'''
	@param file: file to be uploaded
	@param bucket: name of S3 bucket
	takes the file and uploads it to specified S3 bucket
	'''
	s3_client = boto3.client('s3')
	s3_client.upload_file(file,bucket,file)

def get_nflpicks():
	'''
	@return nflpicks: list of all picks stored in picks.csv
	@return header:  list of header from picks.csv
	reads contents of picks.csv and stores values in header and picks arrays
	'''
	header = []
	nflpicks = []
	try:
		with open('picks.csv', newline = '') as csvfile:
			reader = csv.DictReader(csvfile)
			ctr = 0
			for row in reader:
				tmp = []
				for k,v in row.items():
					if(not ctr):
						header.append(k.split('\n'))
					tmp.append(v)
				nflpicks.append(tmp)
				ctr = 1
	except FileNotFoundError:
		return nflpicks,header
	return nflpicks,header

def get_log():
	'''
	@return entry: list of entries in log.txt
	reads entries from log.txt and return them in an list
	'''
	entry = []
	try:
		with open('log.txt', 'r') as log:
			for line in log:
				entry.append(line.split(";"))
	except FileNotFoundError:
		return entry

	return entry[1:]

def show_picks():
	'''
	@return boolean: return True if it current time is past 10am pst on gameday
	'''
	tz_la = pytz.timezone("America/Los_Angeles")
	date = datetime.now(tz_la)
	gameDate = scrapper.get_date()
	if(date.day < gameDate or date.hour < 10):
		return False
	else:
		return True

def check_scores() -> list:
	'''
	'''
	scores = scrapper.get_scores()
	winners = []
	with open('config.csv', newline = '') as csvfile:
		reader = csv.DictReader(csvfile, fieldnames = ['FAV', 'SPREAD', 'UNDER'])#fieldnames are the headers
		for row in reader:
			try:
				Fav_team = row['FAV']
				Fav_score = float(scores[row['FAV']])
				spread = float(row['SPREAD'])
				Under_team = row['UNDER']
				Under_score = float(scores[row['UNDER']])
				if Fav_score + spread > Under_score:
					winners.append(Fav_team)
				else:
					winners.append(Under_team)
			except KeyError:
				continue
	return winners
			

if __name__ == '__main__':
	check_scores()