import pygame


class Simulation:


    grid = []
    agent_blocks = []
    moving_obstacles = []
    WINDOW_SIZE = [0, 0]
    HEIGTH = 0
    WIDTH = 0
    screen = pygame.display.set_mode((0,0))
    pygame.display.set_caption("Environment")
    
    def __init__(self, configFile, matrixFile):
        configFile = open(configFile, 'r')
        for line in configFile:
            line = line.split(" ")
            if line[0] == "HEIGTH:":
                self. HEIGTH = int(line[1])
            elif line[0] == "WIDTH:":
                self.WIDTH = int(line[1])
                for column in range(self.WIDTH):
                    self.grid.append([])
                    for row in range(self.HEIGTH):
                        self.grid[column].append(empty_block())

            elif line[0] == "MARGIN:":
                self.MARGIN = int(line[1])
            elif line[0] == "WINDOW_SIZE:":
                self.WINDOW_SIZE[0] = int(line[1])
                self.WINDOW_SIZE[1] = int(line[2])
            elif line[0] == "BLOCK:":
                if line[1] == "agent":
                    self.agent_blocks.append(agent_block(int(line[2]),int(line[3])))
                elif line[1] == "fixed_obstacle":
                    self.grid[int(line[2])][int(line[3])] = obstacle_block()
                elif line[1] == "moving_obstacle":
                    self.moving_obstacles.append(moving_obstacle_block(int(line[2]), int(line[3])))
                elif line[1] == "goal":
                    self.grid[int(line[2])][int(line[3])] = goal_block()
                else:
                    self.grid[int(line[2])][int(line[3])] = empty_block()
    

        self.screen = pygame.display.set_mode(self.WINDOW_SIZE)

        pygame.init()


    def clear(self):
        self.screen.fill([0,0,0])

    def move_agent(self, number, action):
        if action == "north":
            self.agent_blocks[number].move_north()
        elif action == "south":
            self.agent_blocks[number].move_south()
        elif action == "west":
            self.agent_blocks[number].move_west()
        elif action == "east":
            self.agent_blocks[number].move_east()
        

    def draw(self):

        for column in range(self.WIDTH):
            for row in range(self.HEIGTH):
                self.grid[column][row].draw(self.screen, column, row, self.MARGIN)


        for agent in self.agent_blocks:
            agent.draw(self.screen, agent.column, agent.row, self.MARGIN)
                                                 
        for obstacle in self.moving_obstacles:
            obstacle.draw(self.screen, obstacle.column, obstacle.row, self.MARGIN)
        
        pygame.display.flip()


def main():

    sim = Simulation("config.txt", "matrix.txt")
    clock = pygame.time.Clock()

    done = False
    while not done:
        #Handle pygame events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        #Clear screen        
        sim.clear()

        #Move agents
        sim.move_agent(0, "east")

        #Update obstacles
        #sim.update()

        #Draw screen
        sim.draw()


        clock.tick(1)

    pygame.quit()


def read_config(fileName):


    configFile = open(fileName, 'r')
    for line in configFile:
        line = line.split(" ")
        if line[0] == "HEIGTH:":
            global HEIGTH
            HEIGTH = int(line[1])
        elif line[0] == "WIDTH:":
            global WIDTH
            WIDTH = int(line[1])
            for column in range(WIDTH):
                grid.append([])
                for row in range(HEIGTH):
                    grid[column].append(empty_block())

        elif line[0] == "MARGIN:":
            global MARGIN
            MARGIN = int(line[1])
        elif line[0] == "WINDOW_SIZE:":
            global WINDOW_SIZE
            WINDOW_SIZE[0] = int(line[1])
            WINDOW_SIZE[1] = int(line[2])
        elif line[0] == "BLOCK:":
            if line[1] == "agent":
                agent_blocks.append(agent_block(int(line[2]),int(line[3])))
            elif line[1] == "fixed_obstacle":
                grid[int(line[2])][int(line[3])] = obstacle_block()
            elif line[1] == "moving_obstacle":
                grid[int(line[2])][int(line[3])] = obstacle_block()
            elif line[1] == "goal":
                grid[int(line[2])][int(line[3])] = goal_block()
            else:
                grid[int(line[2])][int(line[3])] = empty_block()



class block():
    color = (0,0,0)
    block_size = 30

    def draw(self, surface, column, row, MARGIN):
        pygame.draw.rect(surface, self.color, [self.block_size * column + MARGIN, self.block_size * row +  MARGIN, self.block_size-MARGIN, self.block_size-MARGIN])


class obstacle_block(block):
    color = (255,0,0) #red

class moving_obstacle_block(obstacle_block):
    colomn = 0
    row = 0

    def __init__(self, column, row):
        self.column = column
        self.row = row

    def move_north(self):
        self.row += -1
    def move_south(self):
        self.row += 1
    def move_east(self):
        self.column += 1
    def move_west(self):
        self.column += -1

class goal_block(block):
    color = (255,255,0) #yellow

class agent_block(block):
    color = (0,128,0) #green
    colomn = 0
    row = 0

    def __init__(self, column, row):
        self.column = column
        self.row = row

    def move_north(self):
        self.row += -1
    def move_south(self):
        self.row += 1
    def move_east(self):
        self.column += 1
    def move_west(self):
        self.column += -1

class empty_block(block):
    color = (255,255,255)


if __name__ == '__main__':
    main()
