import random
import sys
import math
import operator

class world:
	
	worldsNum = 0
	worlds = {}
	biomes = [".", "8", "#", "v", ".", ".", "."]
	width = 55
	height = 40
	screenBounds = {"xmin":0, "xmax":55, "ymin":0, "ymax":40}
	
	def __init__(self, consistency):
		
		self.seedMap = {}
		self.worldMap = {}
		self.biomeConsistency = consistency
		self.generateMap((0,0))
			
		world.worlds[world.worldsNum] = self
		world.worldsNum += 1
		
	def generateMap(self, originCorner):
		
		#generate seeds
		seedChancePerPosition = (1 - self.biomeConsistency)
		
		for y in range(originCorner[1], originCorner[1]+world.height):
			for x in range(originCorner[0], originCorner[0]+world.width):
				if random.random() <= seedChancePerPosition:
					self.seedMap[(x,y)] = random.choice(world.biomes)
		
		#fill in gaps
		for y in range(originCorner[1], originCorner[1]+world.height):
			for x in range(originCorner[0], originCorner[0]+world.width):
				distances = self.determineDistances((x,y)) #get distance from each biome
				if distances == None: #if it's a seed do make it the same
					self.worldMap[(x,y)] = self.seedMap[(x,y)]
				else:
					
					sortedDistances = sorted(distances.items(), key=operator.itemgetter(1))
					greatestDistance = sortedDistances[len(distances)-1][1] 
					
					determinedBiome = None
							
					for biome in sortedDistances:
						newNumber =  random.uniform(0, greatestDistance)
						if biome[1] < newNumber:
							determinedBiome = biome[0]
							break
					if determinedBiome == None:
						determinedBiome = sortedDistances[0][0]
					
					self.worldMap[(x,y)] = determinedBiome
					
		#world.screenBounds = {"xmin":originCorner[0], "xmax":originCorner[0]+world.width, "ymin":originCorner[1], "ymax":originCorner[1]+world.height}
						
					
	def determineDistances(self, position):
		
		distances = {}
		for biome in world.biomes:
			distances[biome]=None
		
		if position in self.seedMap:
			return None
		else:
			for seed in self.seedMap:
				biome = self.seedMap[seed]
				distance = math.sqrt((position[0] - seed[0])**2 + (position[1] - seed[1])**2)
				prevDistance = distances[biome]
				if prevDistance == None or prevDistance > distance:
					distances[biome] = distance
			return distances
		
	def newMap(self, bounds):
		newOrigin = (bounds["xmin"], bounds["ymin"])	
		self.generateMap(newOrigin)
				
					
	def printMap(self, bounds):
		mapText = ""
		for y in range(bounds["ymin"], bounds["ymax"]):
			for x in range(bounds["xmin"], bounds["xmax"]):
				if not [x,y] in player.playerPositions.values():
					mapText = mapText + " " + self.worldMap[(x, y)]
				else:
					mapText = mapText + " " + "X"
			mapText = mapText + "\n"
		return mapText
		
	@classmethod
	def center(cls):
		center = [cls.width/2, cls.height/2]
		return center
	
	@classmethod
	def getScreenFromPoint(cls, point):
		xmin = point[0] - point[0]%cls.width
		xmax = xmin + cls.width
		ymin = point[1] - point[1]%cls.height
		ymax = ymin + cls.height
		bounds = {"xmin":xmin, "xmax":xmax, "ymin":ymin, "ymax":ymax}
		print(bounds)
		return bounds
		
		
class player:
	
	currentPlayer = 1
	playerNum = 0
	playerPositions = {}
	
	def __init__(self, startingPosition = world.center()):
		
		self.playerPosition = startingPosition
		player.playerNum += 1
		player.playerPositions[player.playerNum] = self.playerPosition
		self.playerNum = player.playerNum
		
	def move(self, direction):
		
		if direction == "e":
			self.playerPosition[0] = self.playerPosition[0] + 1 
		elif direction == "s":
			self.playerPosition[1] = self.playerPosition[1] + 1 
		elif direction == "w":
			self.playerPosition[0] = self.playerPosition[0] - 1 
		elif direction == "n":
			self.playerPosition[1] = self.playerPosition[1] - 1 
			
		player.playerPositions[self.playerNum] = self.playerPosition
		
		if not (self.playerPosition[0], self.playerPosition[1]) in world1.worldMap.keys():
			bounds = world1.getScreenFromPoint(self.playerPosition)
			world1.newMap(bounds)
		
player1 = player()
player2 = player()
world1 = world(.99)
bounds=world1.getScreenFromPoint(player1.playerPosition)
print(world1.printMap(bounds))

def testing():
	while 1:
		key = raw_input(">")
		if key == "d":
			player1.move("e")
		elif key == "s":
			player1.move("s")
		elif key == "a":
			player1.move("w")
		elif key == "w":
			player1.move("n")
		bounds=world1.getScreenFromPoint(player1.playerPosition)
		print(world1.printMap(bounds))
		

def main(win):
	win.nodelay(True)
	key=""
	win.clear()                
	win.addstr("Detected key:")
	while 1:          
		try:                 
			key = win.getkey()         
			win.clear()                
			win.addstr("Detected key:")
			win.addstr(str(key)+"\n") 
			win.addstr(str(len(world1.worldMap)))
			win.addstr(str(player.playerPositions))
			win.addstr("\n")
			if key == "KEY_RIGHT":
				player1.move("e")
			elif key == "KEY_DOWN":
				player1.move("s")
			elif key == "KEY_LEFT":
				player1.move("w")
			elif key == "KEY_UP":
				player1.move("n")
				
			bounds=world1.getScreenFromPoint(player1.playerPosition)
			win.addstr(world1.printMap(bounds))
			
			if key == os.linesep:
				break           
		except Exception as e:
			# No input   
			pass         

#testing()
import curses
curses.wrapper(main)
		