import csv
def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    f.close()
    return i + 1

def gen_nflpick():
	picks = []
	nflpicks = open("/home/ec2-user/picks.csv", 'w')
	with open('config.csv', newline = '') as csvfile:
		reader = csv.DictReader(csvfile, fieldnames = ['FAV', 'SPREAD', 'UNDER'])
		pickNum = 1
		nflpicks.write(",")
		for row in reader:
			picks.append((row['FAV'], row['SPREAD'], row['UNDER']))
			nflpicks.write('"{}\n{}\n{}",'.format(row['FAV'],
												row['SPREAD'],
												row['UNDER']))
		nflpicks.write('"TIE\n-\nBRK"')
	nflpicks.close()
	return(picks)

def submit_picks(name, picks, points):
	file = open("/home/ec2-user/picks.csv", 'a')
	file.write("\n")
	file.write(name + ",")
	for pick in picks:
		file.write(pick + ",")
	file.write(points)
