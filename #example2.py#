from environment import Simulation
import pygame


def main():

    sim = Simulation("config.txt", "matrix.txt")

    state = sim.get_state()

    done = False
    while not done:

        done, state = sim.move(["matrix", "keyboard"])
        
    #sim.generate_agent_matrix("agent_matrix.txt")


main()
