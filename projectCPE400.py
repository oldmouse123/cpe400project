import random

#################################################################

# Node class
class Node
	def __init__(self):
		self.energy = 100

	def setFields(id, neighbors):
		self.id = id
		self.neighbors = neighbors

	def reduceEnergy():
		self.energy = self.energy - 1

#################################################################

# Edge class
class Edge
	def setFields(source, dest, cost):
		self.source = source
		self.dest = dest
		self.cost = cost

#################################################################

# Path Function (djikstra's)
def choosePath(nodeList, start, destination):
	# Visited nodes
	nPrime = [start.id]

	# Curent edge cost dictionary (key will be destination node)
	edgeCosts = dict()

	# For all nodes...
	for x in nodeList:

		tempEdge = Edge()

		# If node in nodeList is a neighbor of start node
		if x.id in start.neighbors:
			# Set edge cost using energy value of start
			tempEdge.setFields(start.id, x.id, (100 - start.energy))
		else:
			tempEdge.setFields(-1, -1, float("inf"))

		# add all edge costs to dictionary with key of destination node
		edgeCosts[tempEdge.dest] = tempEdge

	# loop for rest of path
	while len(nPrime) != len(nodeList):
		# set up minimum edge holder
		minEdge = Edge()

		# for all edges...
		for key, value in edgeCosts:
			# if destination node of edge is not in nPrime...
			if key not in nPrime:
				# find minimum edge cost
				minEdge = min(minEdge.cost, value.cost)

		# add minimum cost edge destination node to nPrime
		nPrime.append(minEdge.dest)

		# update edge cost for each neighbor of source edge not in nPrime.
		# for all edges...
		for key, value in edgeCosts:
			# if destination node of edge is not in nPrime...
			if key not in nPrime:
				# and destination node is a neighbor of newly added node to nPrime...
				if key in minEdge.neighbors
					# find the edge from the source to the neighbor
					findEdge(source, neighbor, edgeCosts)
					
					# Update cost of path to destination
					value.cost = min(value.cost, ( + minEdge.cost))

#################################################################

# Recursive function for calculating cost of path
def findEdge(nodeSrc, nodeDest, edgeCosts):
	for key, value in edgeCosts:
		if 

#################################################################

# Create nodes
nodeA = Node()
nodeA.setFields(A, ["B","C"])

nodeB = Node()
nodeB.setFields(B, ["A","C","D"])

nodeC = Node()
nodeC.setFields(C, ["A","B","D"])

nodeD = Node()
nodeD.setFields(D, ["B","C"])

# Add nodes to list
nodeList = [nodeA, nodeB, nodeC, nodeD]

#################################################################

# Loop until node fails
nodeFailure = False

while nodeFailure != True:

	# Pick random start node
	startIndx = random.randint(0, (nodeList.len()+1))
	start = nodeList[startIndx]

	# choose the lowest cost path
	choosePath(nodeList, start, D)