import csv
import boto3, pytz
from datetime import datetime
Gif = ""
nfl_logos = {
	"ARI" : "https://content.sportslogos.net/logos/7/177/thumbs/kwth8f1cfa2sch5xhjjfaof90.gif",
	"ATL" : "https://content.sportslogos.net/logos/7/173/thumbs/299.gif",
	"BAL" : "https://content.sportslogos.net/logos/7/153/thumbs/318.gif",
	"BUF" : "https://content.sportslogos.net/logos/7/149/thumbs/n0fd1z6xmhigb0eej3323ebwq.gif",
	"CAR" : "https://content.sportslogos.net/logos/7/174/thumbs/f1wggq2k8ql88fe33jzhw641u.gif",
	"CHI" : "https://content.sportslogos.net/logos/7/169/thumbs/364.gif",
	"CIN" : "https://content.sportslogos.net/logos/7/154/thumbs/403.gif",
	"CLE" : "https://content.sportslogos.net/logos/7/155/thumbs/15578552015.gif",
	"DAL" : "https://content.sportslogos.net/logos/7/165/thumbs/406.gif",
	"DEN" : "https://content.sportslogos.net/logos/7/161/thumbs/9ebzja2zfeigaziee8y605aqp.gif",
	"DET" : "https://content.sportslogos.net/logos/7/170/thumbs/17013982017.gif",
	"GB"  : "https://content.sportslogos.net/logos/7/171/thumbs/dcy03myfhffbki5d7il3.gif",
	"HOU" : "https://content.sportslogos.net/logos/7/157/thumbs/570.gif",
	"IND" : "https://content.sportslogos.net/logos/7/158/thumbs/593.gif",
	"JAC" : "https://content.sportslogos.net/logos/7/159/thumbs/15988562013.gif",
	"KC"  : "https://content.sportslogos.net/logos/7/162/thumbs/857.gif",
	"LV"  : "https://content.sportslogos.net/logos/7/6708/thumbs/670885212020.gif",
	"LAC" : "https://content.sportslogos.net/logos/7/6446/thumbs/644616602020.gif",
	"LAR" : "https://content.sportslogos.net/logos/7/5941/thumbs/594183342020.gif",
	"MIA" : "https://content.sportslogos.net/logos/7/150/thumbs/15073062018.gif",
	"MIN" : "https://content.sportslogos.net/logos/7/172/thumbs/17227042013.gif",
	"NE"  : "https://content.sportslogos.net/logos/7/151/thumbs/y71myf8mlwlk8lbgagh3fd5e0.gif",
	"NO"  : "https://content.sportslogos.net/logos/7/175/thumbs/907.gif",
	"NYG" : "https://content.sportslogos.net/logos/7/166/thumbs/919.gif",
	"NYJ" : "https://content.sportslogos.net/logos/7/152/thumbs/15291162019.gif",
	"PHI" : "https://content.sportslogos.net/logos/7/167/thumbs/960.gif",
	"PIT" : "https://content.sportslogos.net/logos/7/156/thumbs/970.gif",
	"SF"  : "https://content.sportslogos.net/logos/7/179/thumbs/17994552009.gif",
	"SEA" : "https://content.sportslogos.net/logos/7/180/thumbs/pfiobtreaq7j0pzvadktsc6jv.gif",
	"TB"  : "https://content.sportslogos.net/logos/7/176/thumbs/17683632020.gif",
	"TEN" : "https://content.sportslogos.net/logos/7/160/thumbs/1053.gif",
	"WAS" : "https://content.sportslogos.net/logos/7/6741/thumbs/674188372020.gif"
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
	@return picks: Array containing values from config.csv
	iterates through config.csv and stores values in array picks
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
	@param picks: array of picks subbmited from form -> array
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
	#if in prod upload to S3 bucket
	if(not dev):
		upload_file("picks.csv", "elasticbeanstalk-us-west-1-282676831818")

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
	@return nflpicks: array of all picks stored in picks.csv
	@return header:  array of header from picks.csv
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
	@return entry: array of entries in log.txt
	reads entries from log.txt and return them in an array
	'''
	entry = []
	try:
		with open('log.txt', 'r') as log:
			for line in log:
				entry.append(line.split(";"))
	except FileNotFoundError:
		return entry

	return entry[1:]