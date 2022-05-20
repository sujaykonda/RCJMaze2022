import serial
class Tile:

    def __init__(self):
        self.visited = False  # is the tile visited yet
        self.wall = [False, False, False, False]  # north east south west
        self.source = (-1, -1)  # previous tile

class Maze:

    def __init__(self, nRows, nCols):
        self.rows = nRows
        self.cols = nCols
        self.field = [[Tile() for i in range(self.cols)] for i in range(self.rows)]

class Nav:
   
    def __init__(self):
        self.startPosition = (5, 5)
        self.currentPosition = self.startPosition
        self.targetLocation = None

    def findValidNeighbors(self, maze, current):
        validNeighbors = list()
        adjRow = [1, 0, -1, 0]
        adjCol = [0, 1, 0, -1]
        for k in range(4):
            r = current [0]+ adjRow[k]
            c = current[1] + adjCol[k]
            if r >= 0 and r <= len(maze) and c >= 0 and c  < len(maze[0]) and not maze[current[0]][current[1]].wall[k]:
                validNeighbors.append((r, c))
        return validNeighbors
   
    def findNextBFS(self, maze):
        queue = list()
        maze[self.currentPosition[0]][self.currentPosition[1]].visited = True
        queue.append(self.currentPosition)  # enque start node
        self.targetLocation = None
        while self.targetLocation == None:
            currentLocation = queue.pop(0)
            ns = self.findValidNeighbors(maze, currentLocation)
            for neighbor in ns:
                if not maze[neighbor[0]][neighbor[1]].visited:
                    self.targetLocation = neighbor
                    maze[neighbor[0]][neighbor[1]].source = (currentLocation[0], currentLocation[1])
                    break
                elif maze[neighbor[0]][neighbor[1]].visited and not neighbor in queue:
                    queue.append(neighbor)
                    maze[neighbor[0]][neighbor[1]].source = (currentLocation[0], currentLocation[1])
            #print(queue)
        #print("target")
        #print(self.targetLocation)
        return self.targetLocation

    def generatePath(self, maze):
        path = list()
        target = self.findNextBFS(maze)
        path.append(target)
        position = target
        while position != self.currentPosition:
            path.append(maze[position[0]][position[1]].source)
            position = maze[position[0]][position[1]].source
        path.reverse()
        return path

    def makeDriveCommands(self, maze):  # returns list of directions to travel one tile in, this will get passed to the arduino which will execute it
        path = self.generatePath(maze)
        prevPoint = self.currentPosition
        commands = ""
        for point in path:
            adj = (point[0] - prevPoint[0], point[1] - prevPoint[1])
            #print("adj")
            #print(adj)
            if adj == (1, 0):
                commands += 'N'
            elif adj == (-1,0):
                commands += 'S'
            elif adj == (0, 1):
                commands += 'E'
            elif adj == (0, -1):
                commands += 'W'
            prevPoint = point
        return commands
nav = Nav()
maze = Maze(20, 15)
ser = serial.Serial('/dev/ttyS0', 9600)
ser.reset_input_buffer()
while True:
    while ser.in_waiting == 0:
        pass
    try:
        data = ser.read(6)
        print(data.decode('ascii'))
        rWalls = list(map(lambda x: x == "1", data.decode('ascii')))[:4]
        #print(rWalls)
        maze.field[nav.currentPosition[0]][nav.currentPosition[1]].wall = rWalls
        cmd = nav.makeDriveCommands(maze.field)
        print("writing", cmd)
        ser.write(cmd.encode('ascii'))
        nav.currentPosition = nav.targetLocation
    except Exception as e:
        print(e)
ser.close()