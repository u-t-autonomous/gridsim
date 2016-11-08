from environment import Simulation
import pygame

# This will be your subscriber node
# You will need to create a callback function
# You will need to move sim.move(command) inside the callback
# command can only be one of the following "south", "north", "west", "east".
# Remember to initiate a ROS node and subscribe to the topic /cmd

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
