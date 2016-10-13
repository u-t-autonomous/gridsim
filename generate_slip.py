percent_correct = .8
percent_slip = .2 # .1 to slip right and .1 to slip left

f = open("slip.txt", 'w')

for x in range(20):
	for y in range(20):
		for action in ['north', 'east', 'south', 'west']:
			for z in [-1, 0, 1]:
				out = str(x) + " " + str(y) + " " + action + " "
				percent = percent_correct if z == 0 else percent_slip
				if (action == 'north'):
					out += str(x + z) + " " + str(y - 1) + " " + str(percent)
				elif (action == 'south'):
					out += str(x + z) + " " + str(y + 1) + " " + str(percent)
				elif (action == 'east'):
					out += str(x + 1) + " " + str(y + z) + " " + str(percent)
				elif (action == 'west'):
					out += str(x - 1) + " " + str(y + z) + " " + str(percent)
				out += "\n"
				f.write(out)