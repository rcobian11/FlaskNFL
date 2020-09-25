import csv
import boto3
def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    f.close()
    return i + 1

def gen_nflpick():
	nflpicks = open("picks.csv", 'w')
	with open('config.csv', newline = '') as csvfile:
		reader = csv.DictReader(csvfile, fieldnames = ['FAV', 'SPREAD', 'UNDER'])
		pickNum = 1
		nflpicks.write(",")
		for row in reader:
			nflpicks.write('"{}\n{}\n{}",'.format(row['FAV'],
												row['SPREAD'],
												row['UNDER']))
		nflpicks.write('"TIE\n-\nBRK"')
	nflpicks.close()

def get_picks():
	picks = []
	with open('config.csv', newline = '') as csvfile:
		reader = csv.DictReader(csvfile, fieldnames = ['FAV', 'SPREAD', 'UNDER'])
		for row in reader:
			picks.append((row['FAV'], row['SPREAD'], row['UNDER']))
	return picks

def submit_picks(name, picks, points, dev):
	file = open("picks.csv", 'a')
	file.write("\n")
	file.write(name + ",")
	for pick in picks:
		file.write(pick + ",")
	file.write(points)
	file.close()
	if(not dev):
		upload_file("picks.csv", "elasticbeanstalk-us-west-1-282676831818")

def upload_file(file, bucket):
	s3_client = boto3.client('s3')
	s3_client.upload_file(file,bucket,file)

def get_nflpicks():
	header = []
	nflpicks = []
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
	return nflpicks,header