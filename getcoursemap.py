from gethtml import gethtml
from sortdata import sortdata
from graph import graph
import json


def main():
	year = str(input("Enter the year of classes you wish to view: "))
	season = str(input("Enter the season in which they ran (ie. Fall): "))
	getcoursemap(year, season)

def getcoursemap(year, season):

	try:
		dictionary = gethtml(year, season, together=True)
	except AttributeError:
		print("Error, year no longer on website")
		return 0

#If the request failed
	if dictionary == 0:
		return 1

#Clear out the badclasses json file to prevent errors
	clearbadclasses()

#Run sortdata twice to filter out the bad classes
	if 0 == sortdata(dictionary, together=True):
		data = sortdata(dictionary, together=True)
	else:
		data = sortdata(dictionary, together=True, bad=False)

#Output graph
	graph(dictionary, data, together=True)

def clearbadclasses():
	with open('badclasses.json', 'w') as f:
		json.dump({}, f)

if __name__ == '__main__':
	main()
