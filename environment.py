import pygame
import random
import bisect
# import speech_recognition



class Simulation:


    grid = []
    agent_blocks = []
    moving_obstacles = []
    obstacle_percentages = []
    agent_percentages = []
    # slip_percentages[current_x][current_y][action](x_result, y_result, prob)
    slip_percentages = []
    log = {"agents": [], "moving_obstacles": []} 
    WINDOW_SIZE = [0, 0]
    HEIGHT = 0
    WIDTH = 0
    MARGIN = 2
    time_step = 0
    screen = pygame.display.set_mode((0,0))
    clock = pygame.time.Clock()
    pygame.display.set_caption("Environment")
    # recognizer = speech_recognition.Recognizer()
    matrix_active = False
    slip_active = False
    
    def __init__(self, configFile):

        #import config file
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
            self.agent_percentages.append({})
            self.log["agents"].append([])
        for i in self.moving_obstacles:
            self.obstacle_percentages.append({})
            self.log["moving_obstacles"].append([])


        #setup slip percentages
        for i in range(self.WIDTH):
            self.slip_percentages.append([])
            for k in range(self.HEIGHT):
                self.slip_percentages[i].append([])
                self.slip_percentages[i][k] = {'north': [], 'east': [], 'south': [], 'west': []}


        #self.import_matrix_file(matrixFile)

        pygame.init()

        # self.recognizer.pause_threshold = 0.5

    def clear(self):
        self.screen.fill([0,0,0])

    def out_of_bounds(self, x_pos, y_pos):
        #return true if the position is outside of the playfield
        return not (x_pos >= 0 and x_pos < self.WIDTH and y_pos >= 0 and y_pos < self.HEIGHT)

    def move_agent(self, number, action):
        x_pos = self.agent_blocks[number].column
        y_pos = self.agent_blocks[number].row
        self.log["agents"][number].append((self.time_step, (x_pos, y_pos), action))
        if self.slip_active:
            #then slip
            #only execute of the action would keep the block within the grid
            if action == "north" and y_pos > 0 or action == "south" and y_pos < self.HEIGHT - 1 or action == "west" and x_pos > 0 or action == "east" and x_pos < self.WIDTH - 1:

                percents = []
                percents_temp = self.slip_percentages[x_pos][y_pos][action] #list of tuples in form of ((x_result, y_result), probability of landing there)

                for percent in percents_temp:
                    if not self.out_of_bounds(percent[0][0], percent[0][1]):
                        percents.append(percent)

                result = self.weighted_choice(percents)
                self.agent_blocks[number].move_to(result[0], result[1])

        else:
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

    def load_matrix_file(self, matrixFile):
        matrixFile = file(matrixFile, 'r')
        for line in matrixFile:
            if len(line) == 0:
                continue

            line = line.split(" ")

            if len(line[0]) == 1:
                if line[0] == 'a':
                    for agent_percentage in self.agent_percentages:
                        agent_percentage[(int(line[1]), int(line[2]))] = (int(line[3]), int(line[4]), int(line[5]), int(line[6]), int(line[6]))
                elif line[0] == 'o':
                    for obstacle_percentage in self.obstacle_percentages:
                        obstacle_percentage[(int(line[1]), int(line[2]))] = (int(line[3]), int(line[4]), int(line[5]), int(line[6]), int(line[6]))
                continue

            index = int(line[0][1])
            if line[0][0] == 'a' and index < len(self.agent_percentages):
                self.agent_percentages[index][(int(line[1]), int(line[2]))] = (int(line[3]), int(line[4]), int(line[5]), int(line[6]), int(line[7]))
            elif line[0][0] == 'o' and index < len(self.obstacle_percentages):
                self.obstacle_percentages[index][(int(line[1]), int(line[2]))] = (int(line[3]), int(line[4]), int(line[5]), int(line[6]), int(line[7]))

        self.matrix_active = True
        matrixFile.close()

    def load_slip_file(self, slipFile):
        slipFile = file(slipFile, "r")
        for line in slipFile:
            line = line.split(" ")
            print line
            print line[5]
            # current_x current_y action (x_result, y_result, prob)
            #self.slip_percentages[1][2]['north'].append(1, 1, .5)
            self.slip_percentages[int(line[0])][int(line[1])][line[2]].append(((int(line[3]), int(line[4])), float(line[5])))

        self.slip_active = True
        slipFile.close()

    def move_obstacles(self):
        index = 0
        for obstacle in self.moving_obstacles:
            obstacle_percentages = self.obstacle_percentages[index][(obstacle.column, obstacle.row)]
            action = self.weighted_choice((("north", obstacle_percentages[0]), ("east", obstacle_percentages[1]), ("south", obstacle_percentages[2]), ("west", obstacle_percentages[3]), ("stay", obstacle_percentages[4])))
            self.move_obstacle(index, action)
            index += 1

    def move_agents_matrix(self):
        index = 0
        for agent in self.agent_blocks:
            agent_percentages = self.agent_percentages[index][(agent.column, agent.row)]
            action = self.weighted_choice((("north", agent_percentages[0]), ("east", agent_percentages[1]), ("south", agent_percentages[2]), ("west", agent_percentages[3]), ("stay", agent_percentages[4])))
            self.move_agent(index, action)
            index += 1


    def move_agent_matrix(self, index):
        agent = self.agent_blocks[index]
        agent_percentages = self.agent_percentages[index][(agent.column, agent.row)]
        action = self.weighted_choice((("north", agent_percentages[0]), ("east", agent_percentages[1]), ("south", agent_percentages[2]), ("west", agent_percentages[3]), ("stay", agent_percentages[4])))
        self.move_agent(index, action)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True

        for agent in self.agent_blocks:
            for obstacle in self.moving_obstacles:
                if agent.column == obstacle.column and agent.row == obstacle.row:
                    print "Moving obstacle hit"
                    #return True
            if isinstance(self.grid[agent.column][agent.row], Obstacle_block):
                print "Fixed obstacle hit"
                #return True
            if isinstance(self.grid[agent.column][agent.row], Goal_block):
                print "Goal block hit"
                #return True

        return False
                         
    def get_log(self):
        return self.log

    def get_history(self, steps_back):
        if steps_back > self.time_step:
            steps_back = self.time_step

        out_log = {"agents": [], "moving_obstacles": []} 
        #self.log["agents"][number].append((self.time_step, (x_pos, y_pos), action))
        for number in range(len(self.log["agents"])):
            out_log["agents"].append(self.log["agents"][number][-steps_back:])

        for number in range(len(self.log["moving_obstacles"])):
            out_log["move_obstacles"][number].append(elf.log["moving_obstacles"][number][-steps_back:])

        return out_log


 #    def get_voice(self):
 #        print "Listening..."
 #        with speech_recognition.Microphone() as source:
 #            self.recognizer.non_speaking_duration = 0.3
 #            self.recognizer.pause_threshold = 0.3
 #            self.recognizer.adjust_for_ambient_noise(source)
 #            audio = self.recognizer.listen(source)

	# try:
 #            word = self.recognizer.recognize_sphinx(audio)

	# except speech_recognition.UnknownValueError:
 #            print("Could not understand audio")

	# except speech_recognition.RequestError as e:
 #            print("Recog Error; {0}".format(e))

 #        print "I heard you say: " + word
 #        print "Moving..."
 #        if len(word) == 0:
 #            return "stay"
 #        if word[0] < 'f':
 #            return "east"
 #        elif word[0] < 'l':
 #            return "stay"
 #        elif word[0] < 'q':   # Uniform distribution across alphabet
 #            return "north"    # to generate noise
 #        elif word[0] < 'v':
 #            return "south"
 #        else: 
 #            return "west"
            

    def get_key(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        return "north"
                    elif event.key == pygame.K_RIGHT:
                        return "east"
                    elif event.key == pygame.K_DOWN:
                        return "south"
                    elif event.key == pygame.K_LEFT:
                        return "west"
                    elif event.key == pygame.K_SPACE:
                        return "stay"

    def update(self):
        self.move_obstacles()
        self.draw()
        self.time_step += 1
        #self.clock.tick(2)
        return self.handle_events()

    def step_forward(self):
        self.time_step += 1
        #self.clock.tick(2)
        return self.handle_events()

    def generate_agent_matrix(self, matrixFile):
        log = self.get_log()["agents"]
        f = file(matrixFile, 'w')

        counter = 0
        for agent in log:
            event_count = []
            for column in range(self.WIDTH):
                event_count.append([])
                for row in range(self.HEIGHT):
                    event_count[column].append([0, 0, 0, 0, 0]) #north, east, south, west, stay
            
            for event in agent:
                if event[2] == "north":
                    index = 0
                elif event[2] == "east":
                    index = 1
                elif event[2] == "south":
                    index = 2
                elif event[2] == "west":
                    index = 3
                else:
                    index = 4
                
                event_count[event[1][0]][event[1][1]][index] += 1

            for x in range(len(event_count)):
                for y in range(len(event_count[x])):
                    prob_temp = event_count[x][y]
                    
                    total_count = sum(prob_temp)
                    if total_count == 0:
                        f.write ("a{} {} {} 25 25 25 25 0\n".format(counter, x, y))
                    else:
                        f.write("a{} {} {} {} {} {} {} {}\n".format(counter, x, y, 100*prob_temp[0]/total_count, 100*prob_temp[1]/total_count, 100*prob_temp[2]/total_count, 100*prob_temp[3]/total_count, 100*prob_temp[4]/total_count))
            f.write("\n")
            counter += 1


    

    def move(self, movement):
        self.move_obstacles()
        self.draw()

	if (self.handle_events()): 
            return True, 0

        if movement == "matrix":
            #move according to matrix
            self.move_agents_matrix()
        elif movement == "keyboard":
            #keyboard input
            for agent in range(len(self.agent_blocks)):
                self.move_agent(agent, self.get_key())
        elif movement == "voic":
            for agent in range(len(self.agent_blocks)):
                self.move_agent(agent, self.get_voice())
        elif movement in ['east','west','south','north']:
            for agent in range(len(self.agent_blocks)):
                self.move_agent(agent, movement)

        else:
            #move according to list input
            for agent in range(len(movement)):
                if movement[agent] == "keyboard":
                    self.move_agent(agent, self.get_key())
                elif movement[agent] == "matrix":
                    self.move_agent_matrix(agent)
                elif movement[agent] == "voice":
                    self.move_agent(agent, self.get_voice())
                else:
                    self.move_agent(agent, movement[agent])

        self.draw()

        if (self.step_forward()):
            return True, 0

        return False, self.get_state()


                    
        


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

    def move_to(self, column, row):
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

