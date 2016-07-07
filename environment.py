import pygame
import random
import bisect


class Simulation:


    grid = []
    agent_blocks = []
    moving_obstacles = []
    obstacle_percentages = {}
    log = {"agents": [], "moving_obstacles": []} 
    WINDOW_SIZE = [0, 0]
    HEIGHT = 0
    WIDTH = 0
    MARGIN = 2
    time_step = 0
    screen = pygame.display.set_mode((0,0))
    clock = pygame.time.Clock()
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
                        self.grid[column].append(Empty_block())

            #elif line[0] == "MARGIN:":
            #    self.MARGIN = int(line[1])
            elif line[0] == "BLOCK:":
                if line[1] == "agent":
                    self.agent_blocks.append(Agent_block(int(line[2]),int(line[3])))
                elif line[1] == "fixed_obstacle":
                    self.grid[int(line[2])][int(line[3])] = Obstacle_block()
                elif line[1] == "moving_obstacle":
                    self.moving_obstacles.append(Moving_obstacle_block(int(line[2]), int(line[3])))
                elif line[1] == "goal":
                    self.grid[int(line[2])][int(line[3])] = Goal_block()
                else:
                    self.grid[int(line[2])][int(line[3])] = Empty_block()
    
        self.WINDOW_SIZE[0] = int(30*self.WIDTH+2)
        self.WINDOW_SIZE[1] = int(30*self.HEIGHT+2)
        self.screen = pygame.display.set_mode(self.WINDOW_SIZE)

        for i in self.agent_blocks:
            self.log["agents"].append([])
        for i in self.moving_obstacles:
            self.log["moving_obstacles"].append([])

        self.import_matrix(matrixFile)

        pygame.init()

    def clear(self):
        self.screen.fill([0,0,0])

    def move_agent(self, number, action):
        x_pos = self.agent_blocks[number].column
        y_pos = self.agent_blocks[number].row
        self.log["agents"][number].append((self.time_step, (x_pos, y_pos), action))
        if action == "north" and y_pos > 0:
            self.agent_blocks[number].move_north()
        elif action == "south" and y_pos < self.HEIGHT - 1:
            self.agent_blocks[number].move_south()
        elif action == "west" and x_pos > 0:
            self.agent_blocks[number].move_west()
        elif action == "east" and x_pos < self.WIDTH - 1:
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

    def get_state(self):

        agent_list = []
        fixed_obstacle_list = []
        moving_obstacle_list = []

        for agent in self.agent_blocks:
            agent_list.append((agent.column, agent.row))

        for column in range(self.WIDTH):
            for row in range(self.HEIGHT):
                if type(self.grid[column][row]) is Obstacle_block:
                    fixed_obstacle_list.append((column,row))
        
        for obstacle in self.moving_obstacles:
            moving_obstacle_list.append((obstacle.column, obstacle.row))
        
        dict_blocks = {"agents": agent_list, "fixed_obstacles": fixed_obstacle_list, "moving_obstacles": moving_obstacle_list}

        return dict_blocks

    #action = weighted_choice([(1,0), (0,100)])

    def weighted_choice(self, choices):
        values, weights = zip(*choices)
        total = 0
        cum_weights = []
        for w in weights:
            total += w
            cum_weights.append(total)
        x = random.random() * total
        i = bisect.bisect(cum_weights, x)
        return values[i]
        
        
    def move_obstacle(self, number, action):
        x_pos = self.moving_obstacles[number].column
        y_pos = self.moving_obstacles[number].row
        self.log["moving_obstacles"][number].append((self.time_step, (x_pos, y_pos), action))
        if action == "north" and y_pos > 0:
            self.moving_obstacles[number].move_north()
        elif action == "south" and y_pos < self.HEIGHT - 1:
            self.moving_obstacles[number].move_south()
        elif action == "west" and x_pos > 0:
            self.moving_obstacles[number].move_west()
        elif action == "east" and x_pos < self.WIDTH - 1:
            self.moving_obstacles[number].move_east()

    def import_matrix(self, matrixFile):
        matrixFile = file(matrixFile, 'r')
        for line in matrixFile:
            line = line.split(" ")
            self.obstacle_percentages[(int(line[0]), int(line[1]))] = (int(line[2]), int(line[3]), int(line[4]), int(line[5]), int(line[6]))


    def move_obstacles(self):
        index = 0
        for obstacle in self.moving_obstacles:
            obstacle_percentages = self.obstacle_percentages[(obstacle.column, obstacle.row)]
            action = self.weighted_choice((("north", obstacle_percentages[0]), ("east", obstacle_percentages[1]), ("south", obstacle_percentages[2]), ("west", obstacle_percentages[3]), ("stay", obstacle_percentages[4])))
            self.move_obstacle(index, action)
            index += 1

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True

        for agent in self.agent_blocks:
            for obstacle in self.moving_obstacles:
                if agent.column == obstacle.column and agent.row == obstacle.row:
                    print "Moving obstacle hit"
                    return True
            if type(self.grid[agent.column][agent.row]) is Obstacle_block:
                print "Fixed obstacle hit"
                return True
            if type(self.grid[agent.column][agent.row]) is Goal_block:
                print "Goal block hit"
                return True

        return False
                         
    def get_log(self):
        return self.log


    def update(self):
        self.move_obstacles()
        self.draw()
        self.time_step += 1
        self.clock.tick(2)
        return self.handle_events()


class Block():
    color = (0,0,0)
    block_size = 30

    def draw(self, surface, column, row, MARGIN):
        pygame.draw.rect(surface, self.color, [self.block_size * column + MARGIN, self.block_size * row +  MARGIN, self.block_size-MARGIN, self.block_size-MARGIN])


class Obstacle_block(Block):
    color = (255,0,0) #red


class Moving_obstacle_block(Obstacle_block):
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


class Goal_block(Block):
    color = (255,255,0) #yellow


class Agent_block(Block):
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


class Empty_block(Block):
    color = (255,255,255)

