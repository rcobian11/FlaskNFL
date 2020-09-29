import csv
import boto3, pytz
from datetime import datetime
Gif = ""

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