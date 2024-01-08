# ECEPreqChart
Personal project to construct a graph of all UIUC ECE classes and their prerequisites.


Instructions
============

To run this program, run getcoursemap.py.  This program uses the libraries
requests, beautifulsoup, bokeh, and one line of pyautogui.  In the final
graph, green means a class is a prerequisite, yellow means a class can be
a prerequisite or corequisite, and red means a class is strictly a corequisite.


Background
===========

As a way to help teach myself python, I decided to try and create a map
of the UIUC ECE courses and their prerequisites.  I was curious what classes
had the largest prerequisite chains, and wanted to use that as an
opportunity to further develop my python skills.

This program was assembled in 3 parts.  The first, gethtml.py, utilized
requests and beautifulsoup to gather information of off a website to produce
a dictionary of courses and prerequisites.  The second, sortdata.py, went
through the dictionary and assembled a superlist containing a list of each
layer of classes for the future chart.  The final, graph.py, utilized bokeh
to create a network graph connecting all ECE classes and their prerequisites.

During construction, json was used to transfer data between the three parts.
In the final getcoursemap.py, most uses of json were removed to reduce the
need to write to files and quicken the program.

I recommend using the ECE website https://ece.illinois.edu/academics/courses
while running this code.  Since I am reading of the the html of this website,
I only have access to the years and months that are shown on the webstie, so
it will tell you what to input into the program.
