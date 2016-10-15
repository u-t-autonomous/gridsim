import pygame
import sys

grid = []
agent_blocks = []
moving_obstacles = []
MARGIN = 2
WINDOW_SIZE = [0, 0]	
WIDTH = 0
HEIGHT = 0	
screen = 0
pygame.display.set_caption("Environment")

def new_config_file():
	global HEIGHT, WIDTH, WINDOW_SIZE, screen

	HEIGHT = int(input("HEIGHT? "))
	WIDTH = int(input("WIDTH? "))
	WINDOW_SIZE[0] = int(30*WIDTH+2)
	WINDOW_SIZE[1] = int(30*HEIGHT+2)

	screen = pygame.display.set_mode(WINDOW_SIZE)



def main():
	global HEIGHT, WIDTH, grid, screen
		

	print("Press key to select block:")
	print("  1 - Empty block (erase) \n  2 - Agent block \n  3 - Fixed obstacle block \n  4 - Moving obstacle block \n  5 - Goal block")
	print("Press the 'ENTER'/'RETURN' key to generate file")

	for column in range(WIDTH):
		grid.append([])
		for row in range(HEIGHT):
			grid[column].append(Empty_block())



	mouse_clicked = False
	block_type = Empty_block()

	pygame.init()
	while True:

		# proceed events
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()

			# mouse_clicked is set to true while the mouse is held down
			elif event.type == pygame.MOUSEBUTTONDOWN:
				mouse_clicked = True
				pos = pygame.mouse.get_pos()
				block_pos = (int(pos[0]/30), int(pos[1]/30))

				try:
					grid[block_pos[0]][block_pos[1]] = block_type
				except IndexError:
					pass

			elif event.type == pygame.MOUSEBUTTONUP:
				mouse_clicked = False

			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_RETURN:
					generate_config_file()
				if event.key == pygame.K_1:
					block_type = Empty_block()
				elif event.key == pygame.K_2:
					block_type = Agent_block(0, 0)
				elif event.key == pygame.K_3:
					block_type = Obstacle_block()
				elif event.key == pygame.K_4:
					block_type = Moving_obstacle_block(0, 0)
				elif event.key == pygame.K_5:
					block_type = Goal_block()


		if mouse_clicked:
			pos = pygame.mouse.get_pos()
			block_pos = (pos[0]/30, pos[1]/30)
			try:
				grid[block_pos[0]][block_pos[1]] = block_type
			except IndexError:
				pass


		draw()




def draw():
	global WIDTH, HEIGHT, grid, screen

	for column in range(WIDTH):
		for row in range(HEIGHT):
			grid[column][row].draw(screen, column, row, MARGIN)
	
	pygame.display.flip()

def generate_config_file():
	global grid, WIDTH, HEIGHT

	configFile = raw_input("Enter file name: ")
	f = open(configFile, 'w+')
	f.write("HEIGHT: " + str(HEIGHT) + "\n")
	f.write("WIDTH: " + str(WIDTH) + "\n")

	for x in range(WIDTH):
		for y in range(HEIGHT):
			block = grid[x][y]
			if isinstance(block, Agent_block):
				f.write("BLOCK: agent " + str(x) + " " + str(y) + "\n")
			elif isinstance(block, Moving_obstacle_block):
				f.write("BLOCK: moving_obstacle " + str(x) + " " + str(y) + "\n")
			elif isinstance(block, Obstacle_block):
				f.write("BLOCK: fixed_obstacle " + str(x) + " " + str(y) + "\n")
			elif isinstance(block, Obstacle_block):
				f.write("BLOCK: goal " + str(x) + " " + str(y) + "\n")

	f.close()
	print("Config file generated")

def load_config_file(configFile):
	global WIDTH, HEIGHT, grid, screen, WINDOW_SIZE

	f = open(configFile, 'r')

	for line in f:
		line = line.split(" ")
		if line[0] == "HEIGHT:":
			HEIGHT = int(line[1])
		elif line[0] == "WIDTH:":
			WIDTH = int(line[1])
			for column in range(WIDTH):
				grid.append([])
				for row in range(HEIGHT):
					grid[column].append(Empty_block())

		#elif line[0] == "MARGIN:":
		#    self.MARGIN = int(line[1])
		elif line[0] == "BLOCK:":
			if line[1] == "agent":
				grid[int(line[2])][int(line[3])] = Agent_block(0,0)
			elif line[1] == "fixed_obstacle":
				grid[int(line[2])][int(line[3])] = Obstacle_block()
			elif line[1] == "moving_obstacle":
				grid[int(line[2])][int(line[3])] = Moving_obstacle_block(0,0)
			elif line[1] == "goal":
				grid[int(line[2])][int(line[3])] = Goal_block()
			else:
				grid[int(line[2])][int(line[3])] = Empty_block()

	WINDOW_SIZE[0] = int(30*WIDTH+2)
	WINDOW_SIZE[1] = int(30*HEIGHT+2)
	screen = pygame.display.set_mode(WINDOW_SIZE)

	f.close()



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



if __name__ == "__main__":
	args = sys.argv
	if len(args) > 2:
		"To many arguments"
	elif len(args) == 2:
		print(args[1])
		load_config_file(args[1])
	else:
		new_config_file()

	main()
