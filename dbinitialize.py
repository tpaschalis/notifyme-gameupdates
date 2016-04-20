import csv

#initializes a readable dates.csv for steamdb.py
#use it for a first run, in case of corrupt file, or in case someone messes up the csv formatting

inputlinks={}
for key, val in csv.reader(open("inputlinks_experimental.csv")):
	inputlinks[key]=val
	print inputlinks[key]
w = csv.writer(open("dates_experimental.csv", "w"))
for key in inputlinks:
		w.writerow([key, "0"])