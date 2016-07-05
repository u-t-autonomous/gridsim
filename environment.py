import pygame


class Simulation:


    grid = []
    agent_blocks = []
    moving_obstacles = []
    WINDOW_SIZE = [0, 0]
    HEIGHT = 0
    WIDTH = 0
    screen = pygame.display.set_mode((0,0))
    pygame.display.set_caption("Environment")
    
    def __init__(self, configFile, matrixFile):
        configFile = open(configFile, 'r')

        for line in configFile:
            line = line.split(" ")
            if line[0] == "HEIGHT:":
                self.HEIGHT = int(line[1])
            elif line[0] == "WIDTH:":
                self.WIDTH = int(line[1])
                for column in range(self.WIDTH):
                    self.grid.append([])
                    for row in range(self.HEIGHT):
                        self.grid[column].append(empty_block())

            elif line[0] == "MARGIN:":
                self.MARGIN = int(line[1])
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
    
        self.WINDOW_SIZE[0] = int(30.1*self.WIDTH)
        self.WINDOW_SIZE[1] = int(30.1*self.HEIGHT)
        self.screen = pygame.display.set_mode(self.WINDOW_SIZE)

        pygame.init()

    def clear(self):
        self.screen.fill([0,0,0])

    def move_agent(self, number, action):
        blocks = self.export_state()
        y_pos = blocks["agents"][number][0]
        x_pos = blocks["agents"][number][1]
        if action == "north" and y_pos != 0:
            self.agent_blocks[number].move_north()
        elif action == "south" and y_pos != self.HEIGHT - 1:
            self.agent_blocks[number].move_south()
        elif action == "west" and x_pos != 0:
            self.agent_blocks[number].move_west()
        elif action == "east" and y_pos != self.WIDTH - 1:
            self.agent_blocks[number].move_east() 

    def draw(self):

        for column in range(self.WIDTH):
            for row in range(self.HEIGHT):
                self.grid[column][row].draw(self.screen, column, row, self.MARGIN)


        for agent in self.agent_blocks:
            agent.draw(self.screen, agent.column, agent.row, self.MARGIN)
                                                 
        for obstacle in self.moving_obstacles:
            obstacle.draw(self.screen, obstacle.column, obstacle.row, self.MARGIN)
        
        pygame.display.flip()

    def export_state(self):

        agent_list = []
        fixed_obstacle_list = []
        moving_obstacle_list = []

        for agent in self.agent_blocks:
            agent_list.append((agent.column, agent.row))

        for column in range(self.WIDTH):
            for row in range(self.HEIGHT):
                if type(self.grid[column][row]) is obstacle_block:
                    fixed_obstacle_list.append((column,row))
        
        for obstacle in self.moving_obstacles:
            moving_obstacle_list.append((obstacle.column, obstacle.row))
        
        dict_blocks = {"agents": agent_list, "fixed_obstacles": fixed_obstacle_list, "moving_obstacles": moving_obstacle_list}

        return dict_blocks


def main():

    sim = Simulation("config.txt", "matrix.txt")
    clock = pygame.time.Clock()

    done = False
    while not done:
        #Handle pygame events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        #Clear screen (no need for clear)        
        #sim.clear()

        #Move agents
        sim.move_agent(0, "east")

        #Update obstacles
        #sim.update()
        #Replace sim.update() to sim.move_obstacle(obstacle id, action)

        #Draw screen
        sim.draw()
        blocks = sim.export_state()
        print blocks["agents"][0][0]


        clock.tick(1)

    pygame.quit()
    blocks = sim.export_state()

    for agent in blocks["agents"]:
        print agent
    for agent in blocks["moving_obstacles"]:
        print agent
    for agent in blocks["fixed_obstacles"]:
        print agent

    #Export log to text file
    #sim.log()


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
