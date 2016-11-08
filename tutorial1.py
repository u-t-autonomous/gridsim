from environment import Simulation
import pygame


def main():

    sim = Simulation("config.txt")

    #sim.load_matrix_file("matrix.txt") --only include if a matrix file is used

    # sim.load_slip_file("slip.txt") #turns slipping to 'on'

    state = sim.get_state() #grab state

    done = False

    while not done:

        done, state = sim.move(["south"]) #main call

        # print(sim.get_history(2)["agents"]) #get the history from 2 time steps back
        
    #sim.generate_agent_matrix("agent_matrix.txt")


main()
