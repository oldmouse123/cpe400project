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

	def deductEnergy(self):
		self.energy -= 1

	def printInfo(self):
		print("ID: " + self.id)
		print("Links:")
		for link in self.links:
			print("- " + link)

	def printInfoEnergy(self):
		print("ID: " + self.id + " Energy: " + str(self.energy))

class Edge:
	id = ""
	weight = 0

	def __init__(self, node1, node2):
		self.id = node1 + node2
		weight = 0

	#pass node
	def isLink(self, source, destination):
		return (source + destination) == self.id
		#return ((nodeID1 + nodeID2) == self.id) or ((nodeID2 + nodeID1) == self.id)

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


class EdgeContainer:
	edges = []

	def __init__(self, nodelist):
		for node in nodelist.nodes:
			for link in node.links:
				self.edges.append(node.id + link)

	def printInfo(self):
		for edge in self.edges:
			print(edge)


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
if len(sys.argv) > 1:
	if os.path.isfile(sys.argv[1]):
		infile = sys.argv[1]
	else:
		sys.exit("file entered does not exit")

print("All nodes and links: ")
NC = NodeContainer(infile)
NC.printInfo()

print("All edges: ")
EC = EdgeContainer(NC)
EC.printInfo()

print("Node Graph Info:")
NG = NodeGraph(NC)
NG.printInfo()

print("all paths from a to d")
test = NG.findAllPaths('A', 'D')
for path in test:
	print(path)

#routing v.1
count = 0
while not NC.hasDeadNode():
	count += 1
	#get random source and destination
	source = (random.choice(NC.nodes)).id
	destination = (random.choice(NC.nodes)).id

	#source = "A"
	#destination = "D"

	#get all paths from source to destination
	paths = NG.findAllPaths(source, destination)


	#find path with nodes with the most energy
	shortestpath = []
	shortestweight = 999999
	#iterate through all paths
	for path in paths:
		weight = 0

		#for each node, find the total weight of the path
		for nodeid in path:
			node = NC.findNodeByID(nodeid)
			weight += 100 - node.energy

		#found new least weighted path, set it as such
		if weight < shortestweight:
			shortestweight = weight
			shortestpath = path

	print("---")
	print(str(count) + " - Src: " + source + " Dest: " + destination + " Path...")
	print(shortestpath)
	print(shortestweight)
	print("---")

	#deduct all node energys in path
	for nodeid in shortestpath:
		node = NC.findNodeByID(nodeid)
		node.deductEnergy()

NC.printInfoEnergy()




