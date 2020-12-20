import random
import sys
import math
import operator
import os

class world:
    
    worldsNum = 0
    worlds = {}
    biomes = [".", "8", "#", "v", ".", ".", "."]
    
    
    def __init__(self, consistency):
        
        self.seedMap = {}
        self.worldMap = {}
        
        self.width = 0
        self.height = 0
        self.screenBounds = {"xmin":0, "xmax":0, "ymin":0, "ymax":0}
        self.setBoundsToTerminalSize()
        
        self.biomeConsistency = consistency
        self.generateMap((0,0))
            
        world.worlds[world.worldsNum] = self
        world.worldsNum += 1
    
    def setBoundsToTerminalSize(self):
        
        terminalSize = os.get_terminal_size()
        xsize = int(round(terminalSize.columns / 2)) - 1 #devide by 2 because each character in map is seperated by a space
        ysize = int(round(terminalSize.lines - 4))
        self.width = xsize
        self.height = ysize
        self.screenBounds["xmax"] = terminalSize.columns / 2
        self.screenBounds["ymax"] = terminalSize.lines - 4
        
    def generateMap(self, originCorner):
        
        #generate seeds
        seedChancePerPosition = (1 - self.biomeConsistency)
        
        for y in range(originCorner[1], originCorner[1]+self.height):
            for x in range(originCorner[0], originCorner[0]+self.width):
                if random.random() <= seedChancePerPosition:
                    self.seedMap[(x,y)] = random.choice(self.biomes)
        
        #fill in gaps
        for y in range(originCorner[1], originCorner[1]+self.height):
            for x in range(originCorner[0], originCorner[0]+self.width):
                distances = self.determineDistances((x,y)) #get distance to closest biome of each of the biome
                if distances == None: #if it's a seed do make it the same
                    self.worldMap[(x,y)] = self.seedMap[(x,y)]
                else:
                    
                    sortedDistances = sorted(distances.items(), key=operator.itemgetter(1))
                    greatestDistance = sortedDistances[len(distances)-1][1] 
                    
                    determinedBiome = None
                            
                    for biome in sortedDistances: #start at closest biome (least distance) which has the best chance of satasfying the random number test
                        newNumber =  random.uniform(0, greatestDistance)
                        if biome[1] < newNumber: #if the distance is less than the random number generated than the cell becomes that biome
                            determinedBiome = biome[0]
                            break
                    if determinedBiome == None:
                        determinedBiome = sortedDistances[0][0] #if every biome failed the test then just use the closest one
                    
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
        
    def center(self):
        center = [int(round(self.width/2)), int(round(self.height/2))]
        return center
    
    def getScreenFromPoint(self, point):
        xmin = point[0] - point[0]%self.width
        xmax = xmin + self.width
        ymin = point[1] - point[1]%self.height
        ymax = ymin + self.height
        bounds = {"xmin":int(xmin), "xmax":int(xmax), "ymin":int(ymin), "ymax":int(ymax)}
        return bounds
        
        
class player:
    
    currentPlayer = 1
    playerNum = 0
    playerPositions = {}
    
    def __init__(self, world1):
        
        self.playerPosition = world1.center()
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
        

world1 = world(.99)

def main(win):
    player1 = player(world1)
    bounds=world1.getScreenFromPoint(player1.playerPosition)
    
    win.nodelay(True)
    key=""
    win.clear()                
    win.addstr("Detected key:")
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    
    mapString = str(world1.printMap(bounds))
    mapStringSplit = mapString.split("X")
    win.addstr(mapStringSplit[0])
    win.addstr("X", curses.color_pair(1))
    win.addstr(mapStringSplit[1])
    win.addstr("press q to quit")
    
    while 1:
        try:
            key = win.getkey()
        except:
            continue                     

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
            
        if key == "q":
            win.addstr("terminating\n");
            sys.exit()
            break    
            
        bounds=world1.getScreenFromPoint(player1.playerPosition)
        mapString = str(world1.printMap(bounds))
        mapStringSplit = mapString.split("X")
        win.addstr(mapStringSplit[0])
        win.addstr("X", curses.color_pair(1))
        win.addstr(mapStringSplit[1])
        win.addstr("press q to quit")
                   
        #except Exception as e:
            # No input   
         #   print(e);
                     
#testing()
operatingSystem = sys.platform
if operatingSystem == "linux" or operatingSystem == "darwin":
    import curses
elif operatingSystem == "win32":
    try:
        import curses
    except:
        print("ERROR: The windows-curses library is not installed. Try 'pip install windows-curses'. ")
        sys.exit()

curses.wrapper(main)
        