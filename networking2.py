#textfile = open("in.txt", "r")

class Node:
	id=""
	links=[]

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


with open("in.txt", "r") as f:
	data = f.read().splitlines()

for line in data:
	#print(line)
	test = Node(line)
	test.printInfo()

