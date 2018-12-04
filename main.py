#textfile = open("in.txt", "r")
import sys
import os.path
import random

class Node:
	#Identifier for the Node
	id=""
	#Node Neighbors
	links=[]
	#Energy Value at Creation
	energy=99

	def __init__(self, inString):
		#Split id from links (ID;LINK,...,LINK)
		s = inString.split(";")
		#s[0] = ID
		self.id = s[0]
		#s[1] = links, split with ,
		self.links = s[1].split(',')

	#used to increase the weight
	def dangerLevel(self):
		if( self.energy > 10 ):
			#quarter stages for dangerlevel
			temp = int((100 - self.energy) / 25) 
			return temp + 1
		else:
			return 100 * (100 - self.energy)

	def deductEnergy(self):
		self.energy -= 1

	#debugging information, used to print info of nodes
	def printInfo(self):
		print("ID: " + self.id)
		print("Links:")
		for link in self.links:
			print("- " + link)

	def printInfoEnergy(self):
		print("Node: " + self.id + " Energy: " + str(self.energy))

#container for all nodes, used to easily iterate and find specific nodes
class NodeContainer:
	nodes = []

	#create nodes from file
	def __init__(self, filename):
		with open(filename, "r") as f:
			data = f.read().splitlines()

			for line in data:
				self.nodes.append(Node(line))

	#used to get reference to a node with its ID
	def findNodeByID(self, id):
		for node in self.nodes:
			if node.id == id:
				return node

	#debugging information, used to print info of nodes
	def printInfo(self):
		for node in self.nodes:
			node.printInfo()

	def printInfoEnergy(self):
		for node in self.nodes:
			node.printInfoEnergy()

	#used to check if a node in the system has died
	def hasDeadNode(self):
		for node in self.nodes:
			if node.energy == 0:
				return True

		return False

#created a diction with key value pairs
#key = nodeID
#value = [Nodes links]
class NodeGraph:
	graphdict = {}

	def __init__(self, inNodeContainer):
		for node in inNodeContainer.nodes:
			self.graphdict[node.id] = node.links

	#returns a list of all possible paths from start to end
	def findAllPaths(self, start, end, path=[]):
		path = path + [start]
		if start == end:
			return [path]
		if not self.graphdict.has_key(start):
			return []
		paths = []
		for node in self.graphdict[start]:
			if node not in path:
				newpaths = self.findAllPaths(node, end, path)
				for newpath in newpaths:
					paths.append(newpath)
		return paths
	#returns the shortest path from start to end
	def findShortestPath(self, start, end, path=[]):
		path = path + [start]
		if start == end:
			return path
		if not self.graphdict.has_key(start):
			return None
		shortest = None
		for node in graph[start]:
			if node not in path:
				newpath = self.findShortestPath(node, end, path)
				if newpath:
					if not shortest or len(newpath) < len(shortest):
						shortest = newpath

		return shortest

	#print debugging info
	def printInfo(self):
		for i in self.graphdict:
			print i, self.graphdict[i]


#file input string
infile = ""
#optionable single source or destination, $ is random
singlesource = "$"
singledestination = "$"

#take arguments from command line, error out if no arguments provided
if len(sys.argv) == 1:
	sys.exit("How to run: python " + sys.argv[0] + " filein")
#check if provided file is available
if len(sys.argv) > 1:
	if os.path.isfile(sys.argv[1]):
		infile = sys.argv[1]
	else:
		sys.exit("file entered does not exit")

#optional single source
if len(sys.argv) > 2:
	singlesource = sys.argv[2]
#optional single destination
if len(sys.argv) > 3:
	singledestination = sys.argv[3]

#if too many arguments provided, error out with info on how to run
elif len(sys.argv) > 4:
	sys.exit("How to run: python " + sys.argv[0] + " filein")

NC = NodeContainer(infile)
NG = NodeGraph(NC)

#dictionary used to tract what source and destination was chosen
srcdict = {}
destdict = {}
for node in NC.nodes:
	srcdict[node.id] = 0
	destdict[node.id] = 0

#loop until a node is dead
count = 0
while not NC.hasDeadNode():
	count += 1

	#get source
	if( singlesource == "$"):
		source = (random.choice(NC.nodes)).id
	else:
		source = singlesource

	#get destination
	if( singledestination == "$"):
		destination = (random.choice(NC.nodes)).id
		while source == destination:
			destination = (random.choice(NC.nodes)).id
	else:
		destination = singledestination

	#log how many times sources/destinations were chosen
	srcdict[source] += 1
	destdict[destination] += 1

	#get all paths from source to destination
	paths = NG.findAllPaths(source, destination)

	#holders to find shortest path and its weight
	shortestpath = []
	shortestweight = float("inf")
	#debugging info to view all path weights
	allweights = []

	#iterate through all paths
	for path in paths:
		weight = 0

		#for each node, add to total weight of the path if not the destination
		for nodeid in path:
			#destination only receieves, no energy loss
			if not nodeid == destination:
				node = NC.findNodeByID(nodeid)
				tempweight = 100 - node.energy
				weight += tempweight * node.dangerLevel()

		#append each weight gathered for debug purposes
		allweights.append(weight)

		#found new least weighted path, set it as such
		if weight < shortestweight:
			shortestweight = weight
			shortestpath = path

	#show iteration info
	print("Iteration: " + str(count) + " Src: " + source + " Dest: " + destination)
	print("Path Chosen: " + str(shortestpath))
	print("Weight of Path: " + str(shortestweight))
	print("Path Weights: " + str(allweights) + "\n")

	#deduct all node energys in path
	for nodeid in shortestpath:
		if not nodeid == destination:
			node = NC.findNodeByID(nodeid)
			node.deductEnergy()

#print final stats of all nodes when a node is dead
print("Final Stats:")
NC.printInfoEnergy()

#count for each source/destination used
print("Sources Used:")
print(srcdict)
print("Destinations Used:")
print(destdict)




