#textfile = open("in.txt", "r")
import os.path

class Node:
	#Identifier for the Node
	id=""
	#Node Neighbors
	links=[]
	#Energy Value at Creation
	energy=100

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

	def printInfo(self):
		print("ID: " + self.id)
		print("Links:")
		for link in self.links:
			print("- " + link)

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

	def printInfo(self):
		for node in self.nodes:
			node.printInfo()


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

	def printInfo(self):
		for i in self.graphdict:
			print i, self.graphdict[i]

print("All nodes and links: ")
NC = NodeContainer("in.txt")
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
