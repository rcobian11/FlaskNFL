#test.py
import csv
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
					header.append(k)
				tmp.append(v)
			nflpicks.append(tmp)
			ctr = 1
	return nflpicks,header

picks,header = get_nflpicks()
print(header)
