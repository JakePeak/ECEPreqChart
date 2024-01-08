import json

def sortdata(inputdic={0}, **options):
#Allows to opperate as a function to remove need to read/write files
	if options.get("together") == True:
		func = True
	else:
		func = False

	if func:
		dictionary = inputdic
	else:
		with open('data.json', 'r') as f:
			rawdata = json.load(f)
		dictionary = dict(rawdata)

#Get rid of classes that didn't work, ie. didn't all run this semester
	if options.get('bad') == False:
		pass
	else:
		dictionary = rmbadclasses(dictionary)

#sorter into lists of how many prerequesites there are
#techincally unnecessary aside from getting the baseclasses
	layers = []
	baseclasses, onepreq, twopreq, threepreq = [], [], [], []
	for key in dictionary.keys():
		if dictionary[key] == 'None':
			baseclasses.append(key)
		elif len(dictionary[key]) == 1:
			onepreq.append(key)
		elif len(dictionary[key]) == 2:
			twopreq.append(key)
		elif len(dictionary[key]) == 0:
			dictionary.pop(key)
		else:
			threepreq.append(key)
	layers.append(baseclasses)
	higherclass = onepreq + twopreq + threepreq

#takes single prerequisites and determines what layer beyond base they are
	failurecounter = 0
	while higherclass != []:
		failurecounter += 1
		if failurecounter > 50:
			with open('badclasses.json', 'w') as f:
				json.dump(higherclass, f)
			return 0
		layers.append([])
		oldhigherclass = higherclass
		higherclass = []
		for key in oldhigherclass:
			#preqnumber is the current prereq being tested
			preqnumbers = range(len(dictionary[key]))
			funcreturns, b1, b2 = [], [], []
			for preqnumber in preqnumbers:
				x, preqlist, coreqlist = runallORs(layers, preqnumber, key, dictionary)
				funcreturns.append(x)
				b1 = b1 + preqlist
				b2 = b2 + coreqlist

			if 0 in funcreturns:
				higherclass.append(key)
			elif 3 in funcreturns and 2 in funcreturns:
				layers[len(layers)-2].append(key)
#				b0, b1, b2 = runallORs(layers, preqnumber, key, dictionary)
				addto(layers, b2, 2, key, coreqs=True)
				addto(layers, b1, 3)
			elif 3 in funcreturns:
				layers[len(layers)-2].append(key)
			elif 2 in funcreturns:
				layers[len(layers)-1].append(key)
#				b0, b1, b2 = runallORs(layers, preqnumber, key, dictionary)
				addto(layers, b2, 1, key, coreqs=True)
				addto(layers, b1, 2)
			else:
				layers[len(layers)-1].append(key)

#Formating data to output to file

	if not func:
		with open('sorted.json', 'w') as f:
			json.dump(layers, f)
	else:
		return layers

#Adds a list to the layers list without adding items that are already
#in a layer, z is the offset (1 means current layer, 2 means previous layer)
def addto(layers, lst, z, *key, **coreqs):
	for x in lst:
		if addtosub(layers, lst, x):
			layers[len(layers)-z].append(x)

	if coreqs.get("coreqs") == True:
		key = list(key)[0]
		for coreq in lst:
#			Debugging
#			print(key)
#			print(coreq)
			if coreq in layers[len(layers)-z] and key in layers[len(layers)-z]:
				del layers[len(layers)-z][layers[len(layers)-z].index(coreq)]
				del layers[len(layers)-z][layers[len(layers)-z].index(key)]
				layers[len(layers)-z].append(key)
				layers[len(layers)-z].append(coreq)

#sub function to make addto work
def addtosub(layers, lst, x):
	for y in range(len(layers)):
		if x in layers[y]:
			return False
	return True


#Redefines output after testing all possible paths through which a course's
#prerequisites can be reached, as follows:
#0: add to higher layer (failed)
#1: add to current layer, no external pre/cor reqs
#2: add to current layer, co and pre reqs must be dealth with
#3: add to previous layer
#
#Also returns 2 other lists, one of prereqclasses, and one of corecclasses
def runallORs(layers, preqnumber, key, dictionary):
	outputlist = []
	preqlist = []
	coreqlist = []
	for x in range(len(dictionary[key][preqnumber])-1):
		currentside = x + 1
		y = choosetest(layers, preqnumber, key, dictionary, currentside)
		if y == 0:
			return 0, [], []
		else:
			outputlist.append(y)
			if y == 2:
				dull = (dictionary[key][preqnumber][currentside])
				rmecetag(preqlist, dull)
			elif y == 4:
				dull = (dictionary[key][preqnumber][currentside])
				rmecetag(coreqlist, dull)


	if 3 in outputlist:
		return 3, preqlist, coreqlist
	if 2 in outputlist or 4 in outputlist:
		return 2, preqlist, coreqlist
	else:
		return 1, [], []

#Correctly adds ECE terms to preqlist and coreqlist for RunAllORs
def rmecetag(list, item):
	if item[0:3] == 'ECE':
		list.append(item[4:7])
	else:
		list.append(item)

#Passes correct test output:
#0: add to higher layer (failed)
#1: add to layer
#2: add to layer, add prereq to previous layer
#3: add to previous layer
#4: add to layer, add coreq to same layer
def choosetest(layers, preqnumber, key, dictionary, currentside):
	match dictionary[key][preqnumber][0]:
		case 'credit':
			return credittest(layers, preqnumber, key, dictionary, currentside)
		case 'concurrent':
			return concurrenttest(layers, preqnumber, key, dictionary, currentside)
		case 'credit/concurrent':
			return creorcon(layers, preqnumber, key, dictionary, currentside)


#Returns 1 if the class can be put on that layer, 0 if it must go back
#onto higherclass, 2 if it can go on that layer and its prereq must be
#added to the previous layer
def credittest(layers, preqnumber, key, dictionary, currentside):
	if dictionary[key][preqnumber][currentside][0:3] == 'ECE':
		for x in range(len(layers)-1):
			if dictionary[key][preqnumber][currentside][4:7] in layers[x]:
				return 1
		return 0
	elif dictionary[key][preqnumber][currentside] in layers[len(layers)-1]:
		return 0
	else:
		return 2

#Returns 0 if it must go back onto higherclass, 1 if it can go on that layer,
#3 if it must go onto the previous layer, and 4 if both it and its non-ece
#partner belong on that layer
def concurrenttest(layers, preqnumber, key, dictionary, currentside):
	layer = len(layers)-1
	if dictionary[key][preqnumber][currentside][0:3] == 'ECE':
		if dictionary[key][preqnumber][currentside][4:7] in layers[layer - 1]:
			return 3
		elif dictionary[key][preqnumber][currentside][4:7] in layers[layer]:
			return 4
		else:
			return 0
	else:
		return 4


#Returns 0 if it must go back to higherclass, 1 if it should be put on that
#layer, 3 if it belongs on the previous layer, 4 if its non-ece coreq belongs
#on the same layer
def creorcon(layers, preqnumber, key, dictionary, currentside):
	x = credittest(layers, preqnumber, key, dictionary, currentside)
	match x:
		case 0:
			return concurrenttest(layers, preqnumber, key, dictionary, currentside)
		case 1:
			return 1
		case 2:
			return 4

def rmbadclasses(dictionary):
	with open('badclasses.json', 'r') as f:
		badclasses = json.load(f)
	for bad in list(badclasses):
		dictionary.pop(bad)
	return dictionary

if __name__ == '__main__':
	sortdata()
