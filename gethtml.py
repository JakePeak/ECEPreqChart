import requests
from bs4 import BeautifulSoup
import json

#Goes through the web page and writes all of the ECE classes to a json file,
#like a dictionary with the class as the key and the prereqs as a list

#Preqreqs are either 'None' or a list containing a list for each individual
#set of prereqs, where a set of prereqs are the various options.

#Year and season can be inputed as part of a greater function call
def gethtml(year, season, **options):
#Allows to operate as part of a greater function
	if options.get("together") == True:
		func = True
	else:
		func = False

	url = 'https://ece.illinois.edu/academics/courses'
	soup = getpage(url)


	match season:
		case 'Spring':
			month = '1'
		case 'Summer':
			month = '5'
		case 'Fall':
			month = '8'
		case _:
			if year == 'All':
				month = ''
			else:
				print('Error, invalid season')
				return 0

	if year == 'All':
		id = 'tAll'
	else:
		id = "t1" + year + month
	tab = soup.find(id=id)
	titles = tab.find_all('td', 'rubric')

	chart = {}
	for title in titles:
		num = title.string[4:7]
		prereq = title.next_sibling.next_sibling.next_sibling.next_sibling
		prereqlist = prereq.contents
		second = interpret(prereqlist)
		chart[num] = second
	if not func:
		with open('data.json', 'w') as f:
			json.dump(chart, f)

	elif func:
		return chart

#Sorts/parses through the data to leave it in an interpretable state
#Functionally finds what the prerecs/concurrent recs are and labels them
def interpret(prereqlist):
		if prereqlist == []:
			return 'None'
		else:
			output, sublist = [], []
			for x in range(len(prereqlist)):
				match str(prereqlist[x]).strip():
					case 'Credit in':
						sublist.append('credit')
						sublist.append(str(prereqlist[x+1].string.upper()))
					case 'or':
						sublist.append(prereqlist[x+1].string.upper())
					case '':
						output.append(sublist)
						sublist = []
					case 'or Credit or concurrent registration in':
#Removing simplifies work						sublist.append('credit/concurrent')
						sublist.append(prereqlist[x+1].string.upper())
					case 'Credit or concurrent registration in':
						sublist.append('credit/concurrent')
						sublist.append(prereqlist[x+1].string.upper())
					case 'Concurrent registration in':
						sublist.append('concurrent')
						sublist.append(prereqlist[x+1].string.upper())
					case _:
						pass
			return output

def getpage(url):
	r = requests.get(url)
	soup = BeautifulSoup(r.text, 'html.parser')
	return soup


if __name__ == '__main__':
	gethtml('2024', 'Spring')
