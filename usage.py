from environment import Simulation
from time import sleep

sim = Simulation("config.txt")
sim.load_matrix_file("matrix.txt")
state = sim.get_state()

done = False
while not done:

    done, state = sim.move(["matrix", "matrix"])
    sleep(1)
#sim.generate_agent_matrix("agent_matrix.txt")
