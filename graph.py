import json
from bokeh.plotting import figure, show
from bokeh.models import (GraphRenderer, Text, StaticLayoutProvider, MultiLine,
				HoverTool, TapTool, NodesAndLinkedEdges,
				EdgesAndLinkedNodes, NodesAndAdjacentNodes)
from sortdata import rmbadclasses
from pyautogui import size

def graph(inputdic={0}, inputdata=[0], **options):
#If called as a function to eliminated json use
	if options.get("together") == True:
		func = True
	else:
		func = False

#Open files
	if not func:
		dictionary = dict(openfile('data.json'))
		data = list(openfile('sorted.json'))
	else:
		dictionary = inputdic
		data = inputdata


#Prune dictionary of datapoints that didn't work
	if not func:
		dictionary = rmbadclasses(dictionary)

#Data manipulation
	nodenumber, compounddatalist = 0, []
	for i in range(len(data)):
		#Calculates the number of nodes for the node indices
		nodenumber += len(data[i])
		#Puts all the classes into a single list in order for
		#the node indices
		compounddatalist = compounddatalist + data[i]

	node_indices = list(range(nodenumber))

#Centering points
	centerpoint = []
	for i in compounddatalist:
		centerpoint.append(-4*len(i))

#Setting up the plot
	screenx, screeny = size()

	plot = figure(title="ECE Classes Prerequisite Map",
		x_range=(-1,.5*(len(data[0])+1)),
		y_range=(0,(len(data)+1)),
		width=(screenx-800),
		height=(screeny-600),
		x_axis_location=None,
		y_axis_location=None)
	plot.add_tools(HoverTool(tooltips=None), TapTool())

	graph = GraphRenderer()

	graph.node_renderer.glyph = Text(text_font_size='16px', text='classes',
         text_color="orange", border_line_color = "blue",
	 background_fill_color = 'white', x_offset = 'centered',
	 y_offset = 6)

	graph.node_renderer.data_source.data = dict(
		index=node_indices, classes=compounddatalist, centered=centerpoint)

	graph.edge_renderer.glyph = MultiLine(line_color="Black",
		line_width=1, line_alpha=.3)


#Building nodes during selection
	graph.node_renderer.nonselection_glyph = Text(text_font_size='16px', text='classes',
	 text_color="orange", border_line_color = "blue",
	 background_fill_color = 'white', x_offset = 'centered',
	 y_offset = 6, border_line_alpha=.2, text_alpha=.2)

	graph.node_renderer.hover_glyph = Text(text_font_size='16px', text='classes',
         text_color="orange", border_line_color = "blue",
	 background_fill_color = 'white', x_offset = 'centered',
	 y_offset = 6, border_line_width=2)

#Creating connections/edges
	startlist, endlist = BuildConnectionsLists(dictionary, compounddatalist)
	graph.edge_renderer.data_source.data = dict(
		start=startlist,
		end=endlist)

#Recoloring edges during selection
	colorslist = []
	for x in range(len(endlist)):
		point = compounddatalist[endlist[x]]
		for y in range(len(dictionary[point])):
			breakvar = True
			point2 = compounddatalist[startlist[x]]
			if len(point2) == 3:
				adjusted = "ECE " + point2
			else:
				adjusted = point2
			for zz in range(len(dictionary[point][y])-1):
				z = zz+1
				if dictionary[point][y][z].startswith(adjusted):
					match dictionary[point][y][0]:
						case 'credit':
							colorslist.append('Green')
						case 'concurrent':
							colorslist.append('Red')
						case 'credit/concurrent':
							colorslist.append('Yellow')
					breakvar = False
					break
			if breakvar == False:
				break


	graph.edge_renderer.selection_glyph = MultiLine(line_color="colors",
		line_width=1, line_alpha=1)

	graph.edge_renderer.data_source.data['colors'] = colorslist

#Finalizing edges during selection
	graph.edge_renderer.hover_glyph = MultiLine(line_color='colors',
		line_width=1, line_alpha=.75)

	graph.edge_renderer.nonselection_glyph = MultiLine(
		line_color='Black', line_width=1, line_alpha=.1)

#Defining Selection
	graph.selection_policy = NodesAndAdjacentNodes()
	graph.inspection_policy = NodesAndLinkedEdges()

#Creates Coordinates
	x, y = CoordBuilder(data)
	graph_layout = dict(zip(node_indices, zip(x, y)))


#Final graphing steps
	graph.layout_provider = StaticLayoutProvider(graph_layout=graph_layout)
	plot.renderers.append(graph)
	show(plot)



#Builds Centered Coordinates
def CoordBuilder(data):
	size = [len(x) for x in data]
	x, y = [], []
	for row in range(len(data)):
		for i in range(size[row]):
			x.append((size[0]-size[row])/4+.5*i)
			y.append(len(data)-row)
	return x, y

#Creates a parallel start and end list for every connection
def BuildConnectionsLists(dictionary, compounddatalist):
	startlist, endlist = [], []
	for key in dictionary.keys():
		if dictionary[key] == 'None':
			continue
		else:
			for preq in dictionary[key]:
				for name in preq:
					if preq[0] == name:
						 continue
					else:
						if name[0:3].upper() == 'ECE':
							startlist.append(compounddatalist.index(name[4:7]))
						else:
							startlist.append(compounddatalist.index(name))
						endlist.append(compounddatalist.index(key))

	return startlist, endlist

#Read json function
def openfile(name):
	with open(name, 'r') as f:
		output = json.load(f)
	return output

if __name__ == '__main__':
	graph()
