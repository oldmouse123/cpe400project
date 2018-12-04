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

	#Constructors are defined with __init__
	#All python class functions have self as the first arugment
	#refer to class variables with self.
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
			temp = int((100 - self.energy) / 25) 
			if temp == 0:
				return 1
			else:
				return temp
		else:
			return 100 * (100 - self.energy)

	def deductEnergy(self):
		self.energy -= 1

	def printInfo(self):
		print("ID: " + self.id)
		print("Links:")
		for link in self.links:
			print("- " + link)

	def printInfoEnergy(self):
		print("Node: " + self.id + " Energy: " + str(self.energy))

class NodeContainer:
	nodes = []

	def __init__(self, filename):
		with open(filename, "r") as f:
			data = f.read().splitlines()

			for line in data:
				self.nodes.append(Node(line))

	def findNodeByID(self, id):
		for node in self.nodes:
			if node.id == id:
				return node

	def printInfo(self):
		for node in self.nodes:
			node.printInfo()

	def printInfoEnergy(self):
		for node in self.nodes:
			node.printInfoEnergy()

	def hasDeadNode(self):
		for node in self.nodes:
			if node.energy == 0:
				return True

		return False


class NodeGraph:
	graphdict = {}

	def __init__(self, inNodeContainer):
		for node in inNodeContainer.nodes:
			self.graphdict[node.id] = node.links

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

	def printInfo(self):
		for i in self.graphdict:
			print i, self.graphdict[i]


infile = "in.txt"
#optionable single source or destination, $ is random
singlesource = "$"
singledestination = "$"

if len(sys.argv) == 1:
	sys.exit("How to run: python " + sys.argv[0] + " filein")
if len(sys.argv) > 1:
	if os.path.isfile(sys.argv[1]):
		infile = sys.argv[1]
	else:
		sys.exit("file entered does not exit")
if len(sys.argv) > 2:
	singlesource = sys.argv[2]
if len(sys.argv) > 3:
	singledestination = sys.argv[3]
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

#routing v.1
count = 0
while not NC.hasDeadNode():
	count += 1

	#get random source and destination
	if( singlesource == "$"):
		source = (random.choice(NC.nodes)).id
	else:
		source = singlesource

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

	#find path with nodes with the most energy
	shortestpath = []
	shortestweight = float("inf")
	allweights = []

	#iterate through all paths
	for path in paths:
		weight = 0

		#for each node, add to total weight of the path if not the destination
		for nodeid in path:
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

	print("Iteration: " + str(count) + " Src: " + source + " Dest: " + destination)
	
	print("Path Chosen: " + str(shortestpath))
	print("Weight of Path: " + str(shortestweight))
	print("Path Weights: " + str(allweights))

	print("")

	#deduct all node energys in path
	for nodeid in shortestpath:
		if not nodeid == destination:
			node = NC.findNodeByID(nodeid)
			node.deductEnergy()

print("Final Stats:")
NC.printInfoEnergy()
print("Sources Used:")
print(srcdict)
print("Destinations Used:")
print(destdict)




